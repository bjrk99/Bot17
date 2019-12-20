class Core:
	@commands.command()
	async def ping(ctx):
		await ctx.send("Pong!")