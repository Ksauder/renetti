import os
import json
import random
import time
import requests
from dotenv import find_dotenv, load_dotenv
import logging

logger = logging.getLogger(__name__)

from discord.ext import commands

class QuotesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # load_dotenv(find_dotenv())
        self.movie_headers = {
            'x-rapidapi-host': "juanroldan1989-moviequotes-v1.p.rapidapi.com",
            'x-rapidapi-key': f"{os.getenv('MOVIEQUOTES_AUTH')}"
        }
        self.famousq_headers = {
            'x-rapidapi-host': "andruxnet-random-famous-quotes.p.rapidapi.com",
            'x-rapidapi-key': f"{os.getenv('ANDRUX_AUTH')}",
            'content-type': "application/x-www-form-urlencoded"
        }
        self.quote_fmtstr = "{0} -{1}"
        self._pins = {}
        self._all_pins = []

    @commands.Cog.listener()
    async def on_ready(self):
        logger.debug('Hit on_ready in quotecog')
        logger.debug(self.bot.channels)
        logger.debug(len(self.bot.channels))
        try:
            for chan in self.bot.channels:
                if not getattr(chan, 'pins', None):
                    continue
                chanpins = await chan.pins()
                self._pins[chan.name] = chanpins
                self._all_pins.extend(self._pins[chan.name])
                time.sleep(.1)
        except Exception as e:
            logger.warning(repr(e))

    @commands.command(aliases=['movieq'])
    async def moviequote(self, ctx, *args):
        """Pulls a random movie quote from andruxnet-random-famous-quotes.p.rapidapi.com
        In the future, you'll be able to specify the movie"""
        # conn = self.bot.httpconn.HTTPSConnection("juanroldan1989-moviequotes-v1.p.rapidapi.com")
        # conn.request("GET", "/api/v1/quotes?actor=Al%20Pacino", headers=self.movie_headers)
        # res = conn.getresponse()
        # data = res.read().decode("utf-8")
        conn = self.bot.httpconn.HTTPSConnection("andruxnet-random-famous-quotes.p.rapidapi.com")
        payload = ""
        conn.request("POST", "/?count=1&cat=movies", payload, self.famousq_headers)
        res = conn.getresponse()
        data = json.load(res)
        print(data[0])
        movieq_str = "{0} -{1}"
        await ctx.channel.send(self.quote_fmtstr.format(data[0]['quote'], data[0]['author']))

    @commands.command()
    async def famousquote(self, ctx, *args):
        """Pulls a random famous quote from andruxnet-random-famous-quotes.p.rapidapi.com
        In the future, you may be able to specify the author"""
        conn = self.bot.httpconn.HTTPSConnection("andruxnet-random-famous-quotes.p.rapidapi.com")
        payload = ""
        conn.request("POST", "/?count=1&cat=famous", payload, self.famousq_headers)
        res = conn.getresponse()
        data = json.load(res)
        print(data[0])
        await ctx.channel.send(self.quote_fmtstr.format(data[0]['quote'], data[0]['author']))

    @commands.command()
    async def pinquote(self, ctx, *args):
        """Pulls a quote from the pins on the server"""
        logger.info('Hit the pin quote')
        logger.debug(ctx)
        logger.debug(self._all_pins)
        q = random.choice(self._all_pins)
        logger.debug(f"q = {q}")
        await ctx.channel.send(self.quote_fmtstr.format(q.content, q.author.display_name))


def setup(bot: commands.Bot):
    """Load the quote cog."""
    bot.add_cog(QuotesCog(bot))
