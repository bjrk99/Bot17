import io
from contextlib import redirect_stdout
import textwrap
import traceback

from discord.ext import commands


class Core(commands.Cog):
	def cleanup_code(self, code):
		if code.startswith("```") and code.endswith("```"):
			return "\n".join(code.split("\n")[1:-1])

		return code.strip("` \n")

	@commands.command(name="eval")
	async def cmd_eval(self, ctx, *, code):
		"""Evaluate some code in Bot17's environment
		
		Credit to https://github.com/rapptz
		"""
		env = {
			"ctx": ctx
		}
		env.update(globals())

		code = self.cleanup_code(code)
		stdout = io.StringIO()

		to_compile = f"async def func():\n{textwrap.indent(code, '  ')}"

		try:
			exec(to_compile, env)
		except Exception as e:
			return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")

		func = env["func"]
		try:
			with redirect_stdout(stdout):
				ret = await func()
		except Exception as e:
			value = stdout.getvalue()
			await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
		else:
			value = stdout.getvalue()

			if ret is None:
				if value:
					await ctx.send(f"```py\n{value}\n```")
			else:
				await ctx.send(f"```py\n{value}{ret}\n```")

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