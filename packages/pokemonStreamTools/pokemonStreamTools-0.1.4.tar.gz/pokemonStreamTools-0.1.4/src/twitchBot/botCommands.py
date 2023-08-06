from twitchio.ext import commands, routines
from shinyOdds import probShiny, findProb
import re


class Bot(commands.Bot):
    """
    The twitch bot
    """

    def __init__(self, *args, **kwargs):
        """
        The constructor for the bot
        :param args: args to be passed to the super bot class
        :param kwargs: kwargs to be passed to the super bot class
        """

        # I think this is the only way to get the channel name being used
        self.channel = kwargs["initial_channels"][0]
        super().__init__(*args, **kwargs)

        # I'm guessing this isn't the best place to start this routine
        self.repos.start()

    async def event_ready(self):
        """
        Print to screen the the bot is ready
        :return:
        """
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def hello(self, ctx: commands.Context):
        """
        Send a hello to a user
        :param ctx: The context of the message that triggered this command
        :return:
        """
        await ctx.send(f'Hello {ctx.author.name.strip()}!')

    @commands.command()
    async def shinyCalc(self, ctx: commands.Context):
        """
        Calculate the probability of finding a shiny
        :param ctx: The context of the message that triggered this command
        :return:
        """
        pattern = re.compile("!shinyCalc [0-9]+/([+-]?(?=\\.\\d|\\d)(?:\\d+)?(?:\\.?\\d*))(?:[eE]([+-]?\\d+))? [0-9]+")
        msg = ctx.message.content
        if pattern.fullmatch(msg) is None:
            await ctx.send(f'{ctx.author.name.strip()}, Error invalid usage. The command should be something like '
                           f'\"!shinyCalc 1/4096 725\"')
        else:
            msg = msg.split(' ')
            nEncounters = int(msg[2])
            odds = msg[1]
            odds = odds.split('/')
            odds = float(odds[0]) / float(odds[1])
            await ctx.send(f'{ctx.author.name.strip()}, your probability to have found a shiny by {nEncounters} '
                           f'encounters is {100 * probShiny(nEncounters, odds, 1):.2f}%.')

    @commands.command()
    async def findEncounters(self, ctx: commands.Context):
        """
        Calculate the number of encounters needed for a certain probability
        :param ctx: The context of the message that triggered this command
        :return:
        """
        pattern = re.compile(
            "!findEncounters [0-9]+/([+-]?(?=\\.\\d|\\d)(?:\\d+)?(?:\\.?\\d*))(?:[eE]([+-]?\\d+))? [0-9]*\\.[0-9]+[%]?")
        msg = ctx.message.content
        if pattern.fullmatch(msg) is None:
            await ctx.send(f'{ctx.author.name.strip()}, Error invalid usage. The command should be something like '
                           f'\"!shinyCalc 1/4096 725\"')
        else:
            msg = msg.split(' ')
            wantedOdds = float(msg[2].replace("%", "")) / 100
            odds = msg[1]
            odds = odds.split('/')
            odds = float(odds[0]) / float(odds[1])
            nenc, prob = findProb(wantedOdds, odds, 1)
            await ctx.send(
                f'{ctx.author.name.strip()}, You\'ll need {nenc} encounters to reach {100 * wantedOdds:.2f}%')

    @commands.command()
    async def help(self, ctx: commands.Context):
        """
        Send a help message
        :param ctx: The context of the message that triggered this command
        :return:
        """
        await ctx.send(f'{ctx.author.name.strip()}, please go to https://bit.ly/3DyFkYh for a list of commands.')

    @routines.routine(hours=3)
    async def repos(self):
        """
        Send a message every 3 hours to the repo for this and the auto controller
        :return:
        """
        msg = "Want to use the programs I'm using? Overlay items/bots: " \
              "https://github.com/drkspace/Pokemon-Stream-Tools. The reset bot: " \
              "https://github.com/brianuuu/AutoController_swsh. "
        await self.wait_for_ready()
        channel = self.get_channel(self.channel)

        await channel.send(msg)
