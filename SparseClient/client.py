from discord.ext import commands
import discord
import sys, os

class SparseClient():
    def __init__(self, prefix: str, token: str, commandDirs: str):
        self.token = token
        self.prefix = prefix
        self.cogsDir = commandDirs
        self.client = commands.Bot(command_prefix="-", description="Sparse is a multi utility bot written in python, with discord.py By Vex#3899, and Laudre#0001")

    def connect(self):
        print(f"[Client] Connected to discord gateway")
        self.client.run(self.token)
        

    def loadCog(self, name: str):
        print(f"Loaded {self.cogsDir}.{name}")
        self.client.load_extension(f"{self.cogsDir}.{name}")

    def logout():
        self.client.logout()
        print("Client logged out!")

    def unloadCog(self, name: str):
        print(f"Unloaded {self.cogsDir}.{name}")
        self.client.unload_extension(f"{self.cogsDir}.{name}")
    