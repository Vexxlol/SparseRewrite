from discord.ext import commands
import discord
import sys, os

client = commands.Bot(command_prefix="-")
class SparseClient():
    def __init__(self, prefix: str, token: str, commandDirs: str):
        self.token = token
        self.prefix = prefix
        self.cogsDir = commandDirs

    def connect(self):
        print(f"[Client] Connected to discord gateway")
        client.run(self.token)
        

    def loadCog(self, name: str):
        client.load_extension(f"{self.cogsDir}.{name}")

    def logout():
        client.logout()
        print("Client logged out!")

    def unloadCog(self, name: str):
        client.unload_extension(f"{self.cogsDir}.{name}")
    