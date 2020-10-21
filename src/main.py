import os
import discord
import renetti

discordauth = os.getenv('DISCORDAUTH')

bot = renetti.Renetti(command_prefix='!',
                      activity=discord.Game(name='Commands: !help'),
                      case_insensitive=True)

bot.init_twilio(os.getenv('TWILIOSID'), os.getenv('TWILIOAUTH'))

# init localdb - mongo db currently
bot.load_extension("cogs.localdatabase")

bot.load_extension("cogs.dev")
bot.load_extension("cogs.quote")

bot.run(discordauth)
print(os.environ)