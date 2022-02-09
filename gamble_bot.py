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

"""
TODO: could maybe put json file here and call the bank cog with it f

try: 
    records_file = open('records.json')
    records = json.load(records_file)
    print(records)
except IOError:
    print('Could not find Records file.')
    bot.add_cog(casino.Bank(bot))
except json.JSONDecodeError:
    print('Empty records file')
"""
bot.add_cog(casino.Bank(bot))


bot.run(token)
