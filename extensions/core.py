import io
from contextlib import redirect_stdout
import textwrap
import time
import traceback

from discord.ext import commands
import discord

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
		"""Logout Bot17"""
		await ctx.send("Logging out...")
		await ctx.bot.stop()

	@commands.command(name="reload")
	async def cmd_reload(self, ctx, extention):
		"""Reload a specific extension"""
		await ctx.bot.unload_extention(f"extensions.{extention}")
		
		try:
			await ctx.bot.load_extention(f"extensions.{extention}")
		except:
			await ctx.send("Error loading extension.")

	@commands.command(hidden=True)
	async def sql(self, ctx, *, query: str):
		"""Run some SQL

		Credit to https://github.com/rapptz"""
		query = self.cleanup_code(query)

		is_multistatement = query.count(';') > 1
		strategy = ctx.bot.pool.execute if is_multistatement else ctx.bot.pool.fetch

		try:
			start = time.perf_counter()
			results = await strategy(query)
			dt = (time.perf_counter() - start) * 1000.0
		except Exception:
			return await ctx.send(f'```py\n{traceback.format_exc()}\n```')

		rows = len(results)
		if is_multistatement or rows == 0:
			return await ctx.send(f'`{dt:.2f}ms: {results}`')

		headers = list(results[0].keys())
		table = TabularData()
		table.set_columns(headers)
		table.add_rows(list(r.values()) for r in results)
		render = table.render()

		fmt = f'```\n{render}\n```\n*Returned {plural(rows):row} in {dt:.2f}ms*'
		if len(fmt) > 2000:
			fp = io.BytesIO(fmt.encode('utf-8'))
			await ctx.send('Too many results...', file=discord.File(fp, 'results.txt'))
		else:
			await ctx.send(fmt)


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
		"""Add prefixes to the server config"""
		config = ctx.bot.guild_configs.get(ctx.guild.id)

		if not config:
			config = ctx.bot.gen_config(ctx.guild.id)
		
		current_prefixes = config["prefixes"]
		current_prefixes.extend(prefixes)

		await ctx.send(f"New prefixes added.")
		config["updated"] = True

	@cmd_prefixes.command(name="remove")
	async def cmd_prefixes_remove(self, ctx, *prefixes):
		"""Remove prefixes from the server config"""
		config = ctx.bot.guild_configs.get(ctx.guild.id)

		if not config:
			config = ctx.bot.gen_config(ctx.guild.id)
		
		for p in prefixes:
			config["prefixes"].remove(p)

		await ctx.send("Prefixes removed.")
		config["updated"] = True


class plural:
	"""Support for SQL command

	Credit to https://github.com/rapptz"""
	def __init__(self, value):
		self.value = value
	def __format__(self, format_spec):
		v = self.value
		singular, sep, plural = format_spec.partition('|')
		plural = plural or f'{singular}s'
		if abs(v) != 1:
			return f'{v} {plural}'
		return f'{v} {singular}'


class TabularData:
	"""Support for SQL command

	Credit to https://github.com/rapptz"""
	def __init__(self):
		self._widths = []
		self._columns = []
		self._rows = []

	def set_columns(self, columns):
		self._columns = columns
		self._widths = [len(c) + 2 for c in columns]

	def add_row(self, row):
		rows = [str(r) for r in row]
		self._rows.append(rows)
		for index, element in enumerate(rows):
			width = len(element) + 2
			if width > self._widths[index]:
				self._widths[index] = width

	def add_rows(self, rows):
		for row in rows:
			self.add_row(row)

	def render(self):
		"""Renders a table in rST format.
		Example:
		+-------+-----+
		| Name  | Age |
		+-------+-----+
		| Alice | 24  |
		|  Bob  | 19  |
		+-------+-----+
		"""

		sep = '+'.join('-' * w for w in self._widths)
		sep = f'+{sep}+'

		to_draw = [sep]

		def get_entry(d):
			elem = '|'.join(f'{e:^{self._widths[i]}}' for i, e in enumerate(d))
			return f'|{elem}|'

		to_draw.append(get_entry(self._columns))
		to_draw.append(sep)

		for row in self._rows:
			to_draw.append(get_entry(row))

		to_draw.append(sep)
		return '\n'.join(to_draw)


def setup(bot):
	bot.add_cog(Admin())
	bot.add_cog(Core())