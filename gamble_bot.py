import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

import casino, error_handler

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
print('Discord token: ' + token)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

bank = casino.Bank(bot)

bot.add_cog(error_handler.ErrorHandler(bot))
bot.add_cog(bank)
bot.add_cog(casino.Gambling(bot, bank))

bot.run(token)
