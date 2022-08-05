import json

from discord.ext import commands

import constants

class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.records = self.__load_records()
    
    """TODO: need to close files"""

    def __load_records(self):
        """Initializes the local records.json file"""
        try: 
            with open('records.json') as records_file:
                return json.load(records_file)
        except IOError:
            print(constants.NO_RECORDS_FOUND)
            with open('records.json', 'w') as f:
                return {}
        except json.JSONDecodeError:
            print(constants.CREATED_EMPTY_RECORDS)
            return {}

    def update_records(self):
        """Updates the local records.json file with whatever the current records object value is"""
        try:
            with open('records.json', 'r+') as records_file:
                records_file.write(json.dumps(self.records))
                records_file.close()
        except: 
            print('Unable to update records.json')
    
    @commands.command(name='InitServerBank')
    async def init_server_bank(self, ctx):
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
        """Prints out the current money of all members in the guild"""
        if len(self.records) != 0:
            guild = str(ctx.message.guild.id)
            
            for member in self.records[guild]: 
                await ctx.send(f"{self.records[guild][member]['name']} has: ${self.records[guild][member]['money']}")
        else: 
            await ctx.send(constants.SERVER_BANK_NOT_INIT)