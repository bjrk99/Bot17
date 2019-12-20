from discord.ext import commands


class Core:
	@commands.command()
	async def ping(ctx):
		await ctx.send("Pong!")