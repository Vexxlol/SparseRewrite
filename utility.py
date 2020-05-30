from discord.ext import commands
import discord
import bitly_api

class utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.apikey = "KEY"

    @commands.command(name="shorten")
    async def _shorten(self, ctx, *, args = None):
        """
        shorten command
        """
        API_USER = "username" #Api User goes here from https://dev.bitly.com/
        API_KEY = "KEY" #Your api key! 
        b = bitly_api.Connection(API_USER, API_KEY) 
        
        urls = args
        url = b.shorten(uri = urls)
        await ctx.send(f"Here is your new link: **{url}**")
        
def setup(bot):
    bot.add_cog(utility(bot))
