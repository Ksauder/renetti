from pathlib import Path
import discord

import theboysclient

secfile = Path("secret.txt")
secret = secfile.read_text()

client = theboysclient.TheBoysClient()

client.run(secret)
