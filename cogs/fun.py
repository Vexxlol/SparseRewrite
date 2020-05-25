from discord.ext import commands
import discord
import random as r

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="8ball")
    async def _8ball(self, ctx):
        """
        Rnadom 8ball Command, Replys with the following below to your question(s)
        """
        random_response = ["My soruces are telling me no", "No", "Try again later", "Negative", "Im sorry, but i dont understand", "Please repeat", "The answer shall remain unknown", "Yes", "Postitive", "My sources are telling me yes."]
        await ctx.send(r.choice(random_response))
    
    @commands.command(name="calculator")
    async def _calculator(self, ctx, arg1, arg2)
    """
    Very Very basic command just for fun + to test webhook
    """
       results = float(arg1) * float(arg2)
        await ctx.send(f"your results were {results}")
        
        
def setup(bot):
    bot.add_cog(Fun(bot))
