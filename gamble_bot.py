import os
from dotenv import load_dotenv

from discord.ext import commands

import casino

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
print('Discord token: ' + token)

bot = commands.Bot(command_prefix='/')

bot.add_cog(casino.Gambling(bot))

bot.run(token)
