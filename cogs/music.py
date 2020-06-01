from discord.ext import commands
import lavalink
from discord import utils
from discord import Embed
from os import getenv as ge
import discord
import re
from discord.utils import get

#from misc import jsonHandler as jh

#data = jh.read_json('mode.json')


url_rx = re.compile(r'https?://(?:www\.)?.+')


class Music(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    if not hasattr(bot, 'music'):  # This ensures the client isn't overwritten during cog reloads.
        self.bot.music = lavalink.Client(self.bot.user.id)
        self.bot.music.add_node(ge("lavalinkus"), 80, ge("password"), 'asia', 'au-music-node')
        self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
        
    self.bot.music.add_event_hook(self.track_hook)


  async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            print(error)
            await ctx.send(error.original)

  async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        # Create returns a player if one exists, otherwise creates.
        # This line is important because it ensures that a player always exists for a guild.

        # Most people might consider this a waste of resources for guilds that aren't playing, but this is
        # the easiest and simplest way of ensuring players are created.

        # These are commands that require the bot to join a voicechannel (i.e. initiating playback).
        # Commands such as volume/skip etc don't require the bot to be in a voicechannel so don't need listing here.
        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            # Our cog_command_error handler catches this and sends it to the voicechannel.
            # Exceptions allow us to "short-circuit" command invocation via checks so the
            # execution state of the command goes no further.
            raise commands.CommandInvokeError('Join a voicechannel first.')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voicechannel.')

  async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None
        #  This is essentially the same as `@commands.guild_only()`
        #  except it saves us repeating ourselves (and also a few lines).

        if guild_check:
            await self.ensure_voice(ctx)
            #  Ensure that the bot and command author share a mutual voicechannel.

  @commands.command(name='play', aliases=["p"])
  async def play(self, ctx, *, query):
    """
        Play a tune in discord!
    """
    try:
      # Get the player for this guild from cache.
        player = self.bot.music.player_manager.get(ctx.guild.id)
        # Remove leading and trailing <>. <> may be used to suppress embedding links in Discord.
        query = query.strip('<>')

        # Check if the user input might be a URL. If it isn't, we can Lavalink do a YouTube search for it instead.
        # SoundCloud searching is possible by prefixing "scsearch:" instead.
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        # Get the results for the query from Lavalink.
        results = await player.node.get_tracks(query)

        # Results could be None if Lavalink returns an invalid response (non-JSON/non-200 (OK)).
        # ALternatively, resullts['tracks'] could be an empty array if the query yielded no tracks.
        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = Embed(color=discord.Color.blurple())

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        if results['loadType'] == 'LOAD_FAILED':
            return await ctx.send(f"An error has occured whilst loading this song!")
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                # Add all of the tracks from the playlist to the queue.
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed.title = 'Track Enqueued'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'

            # You can attach additional information to audiotracks through kwargs, however this involves
            # constructing the AudioTrack class yourself.
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

        # We don't want to call .play() if the player is playing as that will effectively skip
        # the current track.
        if not player.is_playing:
            await player.play()


    except Exception as error:
      print(error)
          

  @commands.command(name='volume', aliases=['v', 'vol'])
  async def _volume(self, ctx, num: int):
    """
        Set the player volume
    """
    player = self.bot.music.player_manager.get(ctx.guild.id)


    embed = Embed(color=discord.Color.blurple())
    embed.description = f":white_check_mark: Setting volume to:  **{num}**"
    await player.set_volume(num)
    await ctx.send(embed=embed)

  @commands.command(name="now", aliases=["nowplaying", "np"])
  async def _nowplaying(self, ctx):
      """
        Sends info about the current song playing.
      """
      player = self.bot.music.player_manager.get(ctx.guild.id)
      #manager = self.bot.music.players.get_player(ctx.guild.id)

      embed = Embed(color=discord.Color.blurple())
      embed.add_field(name=f"🎵 Song Name", value=f"```{player.current.title}```", inline=False)
      embed.add_field(name="🎤 Author", value=f"{player.current.author}", inline=True)
      embed.add_field(name="🕒 Duration", value=f"{lavalink.format_time(player.current.duration)}", inline=True)
      embed.add_field(name="🔗 Song Link", value=f"[Link]({player.current.uri})", inline=True)
      embed.add_field(name="👂 Requester", value=f"{self.bot.get_user(player.current.requester)}", inline=True)
      if 'youtube' == None in track.uri:
          return await ctx.send(embed=embed)
        
      embed.set_thumbnail(url=f"https://img.youtube.com/vi/{player.current.identifier}/default.jpg")

      #print(data['length'])
      await ctx.send(embed=embed)
      
  @commands.command(name="queue", aliases=['q'])
  async def _queue(self, ctx):
      """
        returns the player queue
      """
      i = 0
      tracks = ""
      embed = Embed(color=discord.Color.blurple())
      length = 0
      for track in self.bot.music.player_manager.get(ctx.guild.id).queue:
        i += 1
        if i == 15:
            tracks += f"{i}. {track.title}\n"
            length = len(self.bot.music.player_manager.get(ctx.guild.id).queue)
            embed.description = f"{tracks}"
            embed.title = f"Queue for {ctx.guild.name}"
            embed.set_footer(text=f"Queue Length: {length}, Visual Limit {i}")
            return await ctx.send(embed=embed)
        
        tracks += f"{i}. {track.title}\n"


      if len(self.bot.music.player_manager.get(ctx.guild.id).queue) == 0:
          await ctx.send(':no_entry: The queue is empty, why not add some songs!')
      else:
        embed.description = f"{tracks}"
        embed.title = f"Queue for {ctx.guild.name}"
        embed.set_footer(text=f"Queue Length: {len(self.bot.music.player_manager.get(ctx.guild.id).queue)}")
        await ctx.send(embed=embed)
      
  @commands.command(name="skip", aliases=["next"])
  async def _skip(self, ctx):
      """
        skips the current song
      """
      player = self.bot.music.player_manager.get(ctx.guild.id)
      await player.skip()
      embed = Embed(color=discord.Colour.blurple())
      embed.title = f":white_check_mark: Skipping Song"
      if player.current is None:       
        return await ctx.send(":white_check_mark: Queue Finished!")
      embed.description = f":white_check_mark: Now playing {player.current.title}"
      embed.set_footer(text=f":hammer_pick: Skipped by {ctx.author.name}")
      await ctx.send(embed=embed)
  @commands.command(name="bassboost", aliases=["bass"])
  async def _bassboost(self, ctx, strength: str):
      player = self.bot.music.player_manager.get(ctx.guild.id)

      if strength.lower() == "2" or strength.lower() == "deep":
          freq = 0.1
      elif strength.lower() == "1" or strength.lower() == "low":
          freq = 0.2
      elif strength.lower() == "3" or strength.lower() == "med":
          freq = 0.4
      elif strength.lower() == "4" or strength.lower() == "high":
          freq = 0.7
      elif strength.lower() == "5" or strength.lower() == "death":
          freq = 1.0
      elif strength.lower() == "negative" or strength.lower() == "neg":
          freq = -0.25
      elif strength.lower() == "0":
          freq = 0.0
      else: 
          embed = Embed(color=discord.Colour.blurple())
          embed.title("Not a valid option! Please choose from `0`, `negative`, `1`, `2`, `3`, `4`, `5`")
          return await ctx.send(embed=embed)

      await player.set_gain(1, freq)
      await player.set_gain(7, freq)
      await player.set_gain(14, freq)
      embed = Embed(color=discord.Color.blurple())
      embed.description = f":white_check_mark: Setting bass to:  **{strength.lower()}**"
      await ctx.send(embed=embed)

  @commands.command(name="bands")
  async def _bands(self, ctx, band: int, freq: float):
      
      player = self.bot.music.player_manager.get(ctx.guild.id)
      await player.set_gain(band, freq)
      await ctx.send(f"Updating equaliser")
      
  @commands.command(name="playerstats", aliases=["ps"])
  async def _playerstats(self, ctx):
      player = self.bot.music.player_manager.get(ctx.guild.id)
      embed = Embed(color=discord.Colour.blurple())
      days, hours, minutes, seconds = lavalink.utils.parse_time(player.node.stats.uptime)
      embed.title = f"Playerstats for {player.node.name.split('.')[0]}"
      embed.add_field(name="Uptime", value=f"{round(days)} Days, {round(hours)} Hours, and {round(minutes)} Minutes")
      #embed.add_field(name="Uptime", value=f"{round(player.node.stats.uptime / 8.64e+7)} Days, {round(player.node.stats.uptime / 3.6e+6)} Hours, and {round(player.node.stats.uptime / 60000)} Minutes", inline=True)
      embed.add_field(name="Players", value=f"{player.node.stats.players}", inline=True)
      embed.add_field(name="Active players", value=f"{player.node.stats.playing_players}", inline=True)
      embed.add_field(name="Free Memory", value=f"{round(player.node.stats.memory_free / 8e+6)}gb", inline=True)
      embed.add_field(name="Used Memory", value=f"{round(player.node.stats.memory_used / 8e+6)}gb", inline=True)
      embed.add_field(name="Allocated Memory", value=f"{round(player.node.stats.memory_allocated / 8e+6)}gb", inline=True)
      embed.add_field(name="CPU Cores", value=f"{player.node.stats.cpu_cores}", inline=True)
      embed.add_field(name="Frames Sent", value=f"{player.node.stats.frames_sent}", inline=True)
      embed.add_field(name="Decited Frames", value=f"{player.node.stats.frames_deficit}", inline=True)
      embed.add_field(name="Null Frames", value=f"{player.node.stats.frames_nulled}", inline=True)
      #embed.add_field(name="Penalty Total", value=f"{player.node.penalty.total}", inline=True)
      await ctx.send(embed=embed)    
  @commands.command(name='id')
  async def _id(self, ctx):
      await ctx.send(self.bot.music.player_manager.get(ctx.guild.id).current)
  async def track_hook(self, event):
    if isinstance(event, lavalink.events.TrackStartEvent):
        print('New Song')
    if isinstance(event, lavalink.events.QueueEndEvent):
      guild_id = int(event.player.guild_id)
      await self.connect_to(guild_id, None)
      
  async def connect_to(self, guild_id: int, channel_id: str):
    ws = self.bot._connection._get_websocket(guild_id)
    await ws.voice_state(str(guild_id), channel_id)

def setup(bot):
  bot.add_cog(Music(bot))