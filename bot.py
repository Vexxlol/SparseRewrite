import sys, os
from misc.injectENV import bang
from SparseClient import client as c

def run():
    bang()
    client = c.SparseClient(prefix="-", token=os.getenv("token"), commandDirs="cogs")
    client.loadCog("misc")
    client.loadCog("fun")
    # TODO: WORK ON MODERATION COG
    #client.loadCog("moderation")
    client.connect()

run()

