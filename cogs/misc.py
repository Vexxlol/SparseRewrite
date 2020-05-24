from discord.ext import commands
import discord

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="ping")
    async def _ping(self, ctx):
        """
        sends the bot latency
        """
        await ctx.send(f"{round(self.bot.latency * 1000)}ms")
        
def setup(bot):
    bot.add_cog(Misc(bot))
    print(f"Loaded cog Misc")