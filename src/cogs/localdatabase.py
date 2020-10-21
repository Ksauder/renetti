from discord.ext import commands
from mongoengine import register_connection, connect
from db import mongo

# init the cog and check for updates to the pins
# save any new pins to the db
# one method will handle new pins on all channels

class LocalDataBase(commands.Cog):
    """Attempt to create a local db for the server to take care of pins, messages, or other items
    that shouldn't need to be queried every time used, and to have a backup."""
    def __init__(self, bot):
        self.bot = bot

        # not instituting authentication yet
        self.db_alias = 'renettidb'
        register_connection(alias=self.db_alias,
                                      name='renetti',
                                      host='mongo',
                                      port=27017,
                                      )
        self.db = connect(self.db_alias)
        self.initialize_db() # initialize db to catch up to any changes that have happened

    def initialize_db(self):
        """Initialize the db based on time stamps on messages and changes. Perhaps this could be done
        by analyzing the server logs, or simply per job. I.e. find all messages/pins/users since
        last entry in db."""
        print('Initializing DB')
        pass

def setup(bot: commands.Bot):
    """Load the localdb cog."""
    bot.add_cog(LocalDataBase(bot))
