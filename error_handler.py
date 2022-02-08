from discord.ext import commands

import constants

class ErrorHandler(commands.Cog):
    """Global error handling"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(constants.MISSING_REQUIRED_ARGUMENT_ERROR)
        else: 
            print(ctx, error)