from discord.ext import commands


class Core(commands.Cog):
	@commands.command()
	async def logout(self, ctx):
		await ctx.bot.pool.close()
		await ctx.bot.close()

	@commands.command()
	async def ping(self, ctx):
		await ctx.send("Pong!")

	@commands.command()
	async def reload(self, ctx, extention):
		await ctx.bot.unload_extention(f"extensions.{extention}")
		
		try:
			await ctx.bot.load(f"extensions.{extention}")
		except:
			await ctx.send("Error loading extension.")


def setup(bot):
	bot.add_cog(Core())