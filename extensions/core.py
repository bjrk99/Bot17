import io
from contextlib import redirect_stdout
import textwrap
import traceback

from discord.ext import commands


class Admin(commands.Cog):
	def cleanup_code(self, code):
		if code.startswith("```") and code.endswith("```"):
			return "\n".join(code.split("\n")[1:-1])

		return code.strip("` \n")

	@commands.command(name="eval")
	async def cmd_eval(self, ctx, *, code):
		"""Evaluate some code in Bot17's environment

		Credit to https://github.com/rapptz"""
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

	@commands.command(name="logout")
	async def cmd_logout(self, ctx):
		await ctx.bot.pool.close()
		await ctx.bot.close()

	@commands.command(name="reload")
	async def cmd_reload(self, ctx, extention):
		await ctx.bot.unload_extention(f"extensions.{extention}")
		
		try:
			await ctx.bot.load_extention(f"extensions.{extention}")
		except:
			await ctx.send("Error loading extension.")


class Core(commands.Cog):
	@commands.command(name="ping")
	async def cmd_ping(self, ctx):
		"""Ping Bot17"""
		await ctx.send("Pong!")

	@commands.group(name="prefixes", invoke_without_command=True)
	async def cmd_prefixes(self, ctx):
		"""Server specific prefix control"""
		prefixes = ctx.bot.callable_prefix(ctx.bot, ctx.message)
		await ctx.send("Prefixes for this Server:\n" + "\n".join(prefixes))

	@cmd_prefixes.command(name="add")
	async def cmd_prefixes_add(self, ctx, *prefixes):
		config = ctx.bot.guild_configs.get(ctx.guild.id)

		if not config:
			config = ctx.bot.gen_config(ctx.guild.id)
		
		current_prefixes = config["prefixes"]
		current_prefixes.extend(prefixes)

		await ctx.send(f"New prefixes added.")
		config["updated"] = True

	@cmd_prefixes.command(name="remove")
	async def cmd_prefixes_remove(self, ctx, *prefixes):
		config = ctx.bot.guild_configs.get(ctx.guild.id)

		if not config:
			config = ctx.bot.gen_config(ctx.guild.id)
		
		for p in prefixes:
			config["prefixes"].remove(p)

		await ctx.send("Prefixes removed.")
		config["updated"] = True


def setup(bot):
	bot.add_cog(Admin())
	bot.add_cog(Core())