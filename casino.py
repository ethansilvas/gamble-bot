import random
from discord.ext import commands

import constants

class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print(reaction, user)

    @commands.command()
    async def roll(self, ctx, *args):
        """Roll dice either between 0 and 100 or 0 and a specified range

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
                    await ctx.send(f'{commandAuthor.mention} {constants.ROLL_VALUE_ERROR}')
            else:
                await ctx.send(f'{commandAuthor.mention} {constants.ROLL_ARGUMENT_ERROR}')
        else: 
            print('no args')
            await ctx.send(f'{commandAuthor.mention} rolled: {random.randint(0, 100)}')

    @commands.command()
    async def bet(self, ctx, *, args):
        """Make bets with other users using the same concept of /roll"""
        commandAuthor = ctx.message.author
        argsSplit = args.split()

        if (len(argsSplit) <= 1):
            await ctx.send(constants.MISSING_REQUIRED_ARGUMENT_ERROR)
        else:
            try: 
                maxRoll = int(argsSplit[0])
                argsSplit.pop(0)
                print(argsSplit)

                betParticipants = ' '.join(argsSplit)

                await ctx.send(f'{commandAuthor.mention} wants to bet ${maxRoll} against {betParticipants}')
            except ValueError:
                await ctx.send(f'{commandAuthor.mention} {constants.BET_VALUE_ERROR}')


