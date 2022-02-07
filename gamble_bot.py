import os
from dotenv import load_dotenv

from discord.ext import commands
import random

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
print('Discord token: ' + token)

bot = commands.Bot(command_prefix='/')

@bot.command()
async def roll(ctx, *args):
    print(ctx.message.content)
    commandAuthor = ctx.message.author

    if (args):
        if (len(args) == 1):
            await ctx.send(f'{commandAuthor.mention} rolled: {random.randint(0, int(args[0]))}')
        else:
            await ctx.send(f'{commandAuthor.mention} /roll command either accepts no arguments or only the max, inclusive, range to roll. Ex: "/roll" or "/roll 1000"')
    else: 
        print('no args')
        await ctx.send(f'{commandAuthor.mention} rolled: {random.randint(0, 100)}')

bot.run(token)


"""
Possibly outdated client method (as opposed to bot method)

client = discord.Client()
@client.event
async def on_ready():
    print('We are logged in as: {0.user}'.format(client))

@client.event
async def on_message(message):
    print(message.content)
    if (message.channel.name == 'gambling'):
        if (message.content == '/roll'):
            await message.channel.send(f'{message.author.mention} rolled: {random.randint(0, 100)}')

#client.run(token)
"""


