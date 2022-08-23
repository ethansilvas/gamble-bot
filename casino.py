import random

from discord.ext import commands

import constants

class Gambling(commands.Cog):
    def __init__(self, bot, bank):
        self.bot = bot
        self.bank = bank

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Monitors reactions to see if a bet or other commands have the correct amount and people reacting to initiate it

        TODO:  most likely want to move the /bet logic out of here and at least make it it's own method
            could possibly use json to hold ongoing bets and check on_reaction_add to see if the message is from @GambleBot and if it is a bet...
        """
        if reaction.message.author == self.bot.user:
            users = await reaction.users().flatten()
            mentions = reaction.message.mentions

            print(reaction.message.content)

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
                    
                    # print out all of the bet participant's rolls and print out the winner
                    for user in unique_users:
                        get_roll = self.__get_roll(user)

                        if (highest_roll is None) or (highest_roll is not None and get_roll[0] > highest_roll):
                            highest_roll = get_roll[0]
                            winner = user

                        await reaction.message.channel.send(get_roll[1])
                    
                    await reaction.message.channel.send(f'{winner.mention} wins with a roll of {highest_roll}!')

                    # adjust the money values of all the bet participants
                    for user in unique_users:
                        guild = str(reaction.message.guild.id)

                        bet_value = int(reaction.message.content.split('$')[1].split()[0])

                        if user == winner: 
                            self.bank.add_money(guild, str(user.id), bet_value)
                        else: 
                            self.bank.add_money(guild, str(user.id), -bet_value)

                    # update records.json with updated records object
                    self.bank.update_records()

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
                max_roll = int(args_split.pop(0))
                
                if command_author.mention in args_split:
                    await ctx.send(f'{command_author.mention} bet participants cannot contain your own username')
                else: 
                    bet_participants = ' '.join(args_split)
                    await ctx.send(f'{command_author.mention} wants to bet ${max_roll} against {bet_participants}')
            except ValueError:
                await ctx.send(f'{command_author.mention} {constants.BET_VALUE_ERROR}')
