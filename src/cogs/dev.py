import logging
import time
import os
from pprint import pprint

from discord.ext import commands

from db.mongomodels import User, FeatureRequest, MultipleObjectsReturned, DoesNotExist

log = logging.getLogger('devcog')

class DevCog(commands.Cog, name="Dev"):
    def __init__(self, bot):
        self.bot = bot
        print('devcog starting')
        self._timeout_cache = {} # {'user': {'funcname': timelastused, }, 'user2': {{},}, }
        self._cmd_timeout = {'txtdev': 300,
                             'ftrequest_cmd': 60}

    @commands.command(name='ftrequest', aliases=('ftreq',))
    async def ftrequest_cmd(self, ctx, *args):
        """This command can be used to save a feature idea or request to the server for pineapple to review.
        Usage: !ftrequest/!ftreq "You should add a random quote of the day feature" """
        pprint(f"context: {ctx.__dict__}")
        msg = ' '.join(args)
        timeout, left = self._check_timeout(ctx.author.id, "ftrequest_cmd")
        if not timeout:
            # save request in db
            try:
                user = User.objects(discord_id__exact=ctx.author.id).get()
            except MultipleObjectsReturned as mr:
                print("we have duplicate users")
                raise mr
            except DoesNotExist:
                user = User(name=ctx.author.name,
                            discord_id=ctx.author.id,
                            discriminator=ctx.author.discriminator)
                user.save()

            ftreq = FeatureRequest(author=user, status='new', body=msg)
            ftreq.save()
            # response
            await ctx.channel.send("Feature request received! Estimated time till implementation: Hodor. "
                                   "(hint: donations of coffee will help)",
                                   delete_after=10)
        else:
            await ctx.channel.send(f"Yeah, how about we wait for a while.. maybe {format(left, '.2f')} seconds?",
                                   delete_after=10)

    # @commands.command(aliases=('annoypineapple',))
    # async def txtdev(self, ctx, *args):
    #     txt = ' '.join(args)
    #     timeout, left = self._check_timeout(ctx.author.id, 'txtdev')
    #     if timeout:
    #         ctx.channel.send(f"You just sent a text, chill! Wait {format(left, '.2f')} more seconds",
    #                          delete_after=10)
    #     else:
    #         self.bot.smsclient.messages.create(
    #             body=txt,
    #             to=f"{os.getenv('ADMINPHONE')}",
    #             from="+777777"
    #         )

    def _check_timeout(self, user, function):
        userdict = self._timeout_cache.get(user, None)
        if userdict:
            functime = userdict.get(function, 0)
        else:
            self._timeout_cache[user] = {}
            functime = None

        if functime:
            dif = time.time() - functime
            if dif > self._cmd_timeout[function]:
                return False, 0
            else:
                return True, (self._cmd_timeout[function] - dif)
        else:
            self._timeout_cache[user][function] = time.time()
            return False, 0


def setup(bot: commands.Bot):
    """Load the dev cog."""
    bot.add_cog(DevCog(bot))
