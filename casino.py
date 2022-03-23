import random
import json

from discord.ext import commands

import constants

class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.records = self.__load_records()
    
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
    
    @commands.command()
    async def initServerBank(self, ctx):
        """Initializes the server bank by adding a constant-defined amount to each non-bot member of the guild"""
        if ctx.message.author.name != 'eLou':
            print(ctx.message.author.name)
            print('not eLou')
        else:
            if len(self.records) == 0:
                guild = str(ctx.message.guild.id)
                self.records[guild] = {}

                for member in ctx.message.guild.members:
                    if not member.bot:
                        # records will eventually be converted to a JSON which only allows string key/values
                        member_id = str(member.id)

                        self.records[guild][member_id] = {}
                        self.records[guild][member_id]['name'] = member.name
                        self.records[guild][member_id]['money'] = constants.INIT_MONEY_AMOUNT

                with open('records.json', 'w') as outfile:
                    json.dump(self.records, outfile)

    @commands.command()
    async def money(self, ctx):
        await self.get_money(ctx)
    
    async def get_money(self, ctx):
        if len(self.records) != 0:
            guild = str(ctx.message.guild.id)
            messageAuthor = ctx.message.author
            await ctx.send(f"{messageAuthor.mention}, you have ${self.records[guild][str(messageAuthor.id)]['money']}")
        else: 
            await ctx.send(constants.SERVER_BANK_NOT_INIT)
    
    @commands.command()
    async def leaderboard(self, ctx): 
        if len(self.records) != 0:
            guild = str(ctx.message.guild.id)
            
            for member in self.records[guild]: 
                await ctx.send(f"{self.records[guild][member]['name']} has: ${self.records[guild][member]['money']}")
        else: 
            await ctx.send(constants.SERVER_BANK_NOT_INIT)

class Gambling(commands.Cog):
    def __init__(self, bot, bank):
        self.bot = bot
        self.bank = bank

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.author == self.bot.user:
            users = await reaction.users().flatten()
            mentions = reaction.message.mentions

            """TODO: need to add a check so that someone can't bet against only themselves"""

            if len(users) == len(mentions):
                # users and mentions can list the users in different orders, so use a set to determine if the lists are identical
                unique_users = set()

                for i in range(len(users)):
                    unique_users.add(users[i])
                    unique_users.add(mentions[i])

                if len(unique_users) == len(users):
                    highest_roll = None
                    winner = None
                    
                    for user in unique_users:
                        get_roll = self.__get_roll(user)

                        if (highest_roll is None) or (highest_roll is not None and get_roll[0] > highest_roll):
                            highest_roll = get_roll[0]
                            winner = user

                        await reaction.message.channel.send(get_roll[1])
                    
                    await reaction.message.channel.send(f'{winner.mention} wins with a roll of {highest_roll}!')

                    for user in unique_users:
                        print(user)
                        print(user == winner)

    @commands.command()
    async def roll(self, ctx, *args):
        get_roll = self.__get_roll(ctx.message.author, args)
        await ctx.send(get_roll[1])

    def __get_roll(self, command_author, args=None):
        """Roll dice either between 0 and 100 or 0 and a specified range

        TODO: for now this is coded to be open for more than just 0-100 and 0-n rolling but maybe more functionalities aren't needed
        """
        roll = None
        message = ""

        if args:
            if len(args) == 1:
                try: 
                    max_roll = int(args[0])
                    roll = random.randint(0, max_roll)
                    message = f'{command_author.mention} rolled: {roll}'
                except ValueError:
                    message = f'{command_author.mention} {constants.ROLL_VALUE_ERROR}'
            else:
                message = f'{command_author.mention} {constants.ROLL_ARGUMENT_ERROR}'
        else: 
            roll = random.randint(0, 100)
            message = f'{command_author.mention} rolled: {roll}'
        
        return [roll, message]

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
                bet_participants = ' '.join(args_split)

                await ctx.send(f'{command_author.mention} wants to bet ${max_roll} against {bet_participants}')
            except ValueError:
                await ctx.send(f'{command_author.mention} {constants.BET_VALUE_ERROR}')


