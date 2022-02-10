from email import message
import random
import json
from discord.ext import commands

import constants

class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.records = self.__load_records()
        print(f'records: {self.records}')
        print(f'guilds: {bot.guilds}')

    @commands.command()
    async def money(self, ctx):
        guild = str(ctx.message.guild.id)
        messageAuthor = ctx.message.author
        await ctx.send(f'{messageAuthor.mention}, you have ${self.records[guild][messageAuthor.name]}')

    @commands.command()
    async def initServerBank(self, ctx):
        """Initializes the server bank by adding a constant-defined amount to each non-bot member of the guild"""
        if ctx.message.author.name != 'eLou':
            print(ctx.message.author.name)
            print('not eLou')
        else:
            if len(self.records) == 0:
                guild = ctx.message.guild.id
                self.records[guild] = {}

                for member in ctx.message.guild.members:
                    if not member.bot:
                        self.records[guild][member.name] = constants.INIT_MONEY_AMOUNT

                with open('records.json', 'w') as outfile:
                    json.dump(self.records, outfile)
    
    def __load_records(self): 
        try: 
            records_file = open('records.json')
            records = json.load(records_file)
            return records
        except IOError:
            print(constants.NO_RECORDS_FOUND)
            open('records.json', 'w')
            return {}
        except json.JSONDecodeError:
            print(constants.CREATED_EMPTY_RECORDS)
            return {}


class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print(reaction, user)
        print(reaction.message.content)

        if reaction.message.author == self.bot.user:
            print('wow this worked')
            print(reaction.message.reactions)

    @commands.command()
    async def roll(self, ctx, *args):
        """Roll dice either between 0 and 100 or 0 and a specified range

        TODO: for now this is coded to be open for more than just 0-100 and 0-n rolling but maybe more functionalities aren't needed
        """
        command_author = ctx.message.author

        if args:
            if len(args) == 1:
                try: 
                    max_roll = int(args[0])
                    await ctx.send(f'{command_author.mention} rolled: {random.randint(0, max_roll)}')
                except ValueError:
                    await ctx.send(f'{command_author.mention} {constants.ROLL_VALUE_ERROR}')
            else:
                await ctx.send(f'{command_author.mention} {constants.ROLL_ARGUMENT_ERROR}')
        else: 
            print('no args')
            await ctx.send(f'{command_author.mention} rolled: {random.randint(0, 100)}')

    @commands.command()
    async def bet(self, ctx, *, args):
        """Make bets with other users using the same concept of /roll"""
        command_author = ctx.message.author
        args_split = args.split()

        if len(args_split) <= 1:
            await ctx.send(constants.MISSING_REQUIRED_ARGUMENT_ERROR)
        else:
            try: 
                max_roll = int(args_split[0])
                args_split.pop(0)
                print(args_split)

                bet_participants = ' '.join(args_split)

                await ctx.send(f'{command_author.mention} wants to bet ${max_roll} against {bet_participants}')
            except ValueError:
                await ctx.send(f'{command_author.mention} {constants.BET_VALUE_ERROR}')


