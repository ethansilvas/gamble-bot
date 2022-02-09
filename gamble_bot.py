import os
import json
from dotenv import load_dotenv

from discord.ext import commands

import casino, error_handler

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
print('Discord token: ' + token)

bot = commands.Bot(command_prefix='/')

bot.add_cog(error_handler.ErrorHandler(bot))
bot.add_cog(casino.Gambling(bot))
bot.add_cog(casino.Bank(bot))


bot.run(token)
