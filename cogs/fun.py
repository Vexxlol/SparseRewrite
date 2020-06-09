from discord.ext import commands
import discord
import random as r

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
   
   
        
def setup(bot):
    bot.add_cog(Fun(bot))
