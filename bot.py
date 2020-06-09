import sys, os
from misc.injectENV import bang#This may error, ignore it, it isnt harmful      
from SparseClient import client as c # Imports SparseClient.py

def run():
    bang()
    client = c.SparseClient(prefix="!", token=os.getenv("token"), commandDirs="cogs")#this checks woth sparseclient.py if you want to update the token and lavalink servers do it in the .env file
    client.loadCog("misc")# Loads the cogs      
    client.loadCog("fun")# Loads the cogs
    # TODO: Work on sql querys for premium commands. Premium commands include emoji picker etc.
    client.connect()#connects to discord 

run()

