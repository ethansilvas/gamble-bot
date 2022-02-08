import random
from discord.ext import tasks, commands

class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def roll(self, ctx, *args):
        """roll dice either between 0 and 100 or 0 and a specified range

        TODO: for now this is coded to be open for more than just 0-100 and 0-n rolling but maybe more functionalities aren't needed
        """
        print(ctx.message.content)
        commandAuthor = ctx.message.author

        if (args):
            if (len(args) == 1):
                try: 
                    maxRoll = int(args[0])
                    await ctx.send(f'{commandAuthor.mention} rolled: {random.randint(0, maxRoll)}')
                except ValueError:
                    print('value error')
            else:
                await ctx.send(f'{commandAuthor.mention} /roll command either accepts no arguments or only the max, inclusive, range to roll. Ex: "/roll" or "/roll 1000"')
        else: 
            print('no args')
            await ctx.send(f'{commandAuthor.mention} rolled: {random.randint(0, 100)}')

    @commands.command()
    async def bet(self, ctx, *args):
        """make bets with other users using the same concept of /roll"""
        print(ctx.message.content)
        print(args)