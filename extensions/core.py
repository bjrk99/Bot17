from discord.ext import commands


class Core(commands.Cog):
	@commands.command()
	async def ping(self, ctx):
		await ctx.send("Pong!")

def setup(bot):
	bot.add_cog(Core())