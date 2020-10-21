import discord
import logging
import sys
import os
from discord.ext import commands
from twilio.rest import Client as TwilioClient
import http.client
import time

root = logging.getLogger()
root.setLevel(logging.DEBUG)
stdouthandler = logging.StreamHandler(sys.stdout)
stdouthandler.setLevel(logging.DEBUG)
root.addHandler(stdouthandler)

logger = logging.getLogger('bot')

class Renetti(commands.Bot):
    def __init__(self,
                 description="Pineapple is at it again.",
                 **options):
        super().__init__(description=description, **options)
        self.smsclient = None
        # writing this for one guild currently, not sure how to write it for more yet
        assert len(self.guilds) <= 1
        logger.debug("initializing bot")
        self.httpconn = http.client

    def init_twilio(self, accsid, accauth):
        if not self.smsclient:
            self.smsclient = TwilioClient(accsid, accauth)

    async def on_ready(self):
        logger.debug(f"{self.user} connected to guilds {self.guilds}")
        # for debug dm's
        self.admin = self.get_user(os.getenv('ADMIN'))
        self.admindm = None
        self.guild = self.guilds[0]
        self.channels = self.guild.channels

        self._all_pins = []
        self._pins = {}

        # logger.debug(self.channels)
        # logger.debug(len(self.channels))
        # for chan in self.channels:
        #     chanpins = await chan.pins()
        #     self._pins[chan.name] = chanpins
        #     self._all_pins.extend(self._pins[chan.name])
        #     time.sleep(1)

    async def full_help(self, msg):
        print(msg)
        await msg.channel.send("Testing the help command")
        # cmds = [c for c in await ]
        # res = self.description + '\n' + cmds
        # msg.channel.send(res)

    async def on_member_join(self, member):
        print(f"{member.name} has joined")
        if not self.admindm:
            self.admindm = await self.admin.create_dm()
        await self.admindm.send(f"{member.name} joined the server.\nID:{member.id}")
        await super().on_member_join(member)

    async def on_message(self, message):
        if message.author == self.user:
            return

        # if message.content == "!help":
        #     await self.full_help(message)

        print(message.author)
        if not self.admindm:
            self.admindm = await self.admin.create_dm()
        await self.admindm.send(f"A crow from {message.author} ID:{message.author.id} of the north milord. It reads:\n {message.content}")

        if "pineapple" == message.content and not isinstance(message.channel, discord.DMChannel):
            await message.channel.send("The safeword has been uttered. Winter is coming, and there be dragons.")
        await self.process_commands(message)
        # await super().on_message(message)

    @commands.command()
    async def test(self, ctx, msg):
        print(f"context: {ctx}, msg: {msg}")
