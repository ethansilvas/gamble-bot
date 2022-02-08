from discord.ext import commands

class ErrorHandler(commands.Cog):
    """Global error handling"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'You are missing a required argument in your command.')
        else: 
            print(ctx, error)