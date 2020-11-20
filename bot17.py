import asyncio
from datetime import datetime

from discord.ext import commands
import discord

import secrets


extensions = ("core", "music")


class Bot17(commands.AutoShardedBot):
	def __init__(self, pool=None, guild_configs={}, *args, **kwargs):
		super().__init__(self.callable_prefix, *args, **kwargs)

		self.epoch = datetime.now()
		self.pool = pool
		self.guild_configs = guild_configs

		self.loop.create_task(self.sync_db_loop())

		for extension in extensions:
			self.load_extension(f"extensions.{extension}")

	def callable_prefix(self, bot, msg):
		config = self.guild_configs.get(msg.guild.id)
		return config["prefixes"] if config else secrets.default_prefixes

	def gen_config(self, guild_id):
		self.guild_configs[guild_id] = {"guild_id": guild_id, "prefixes": ['?', '!']}
		return self.guild_configs[guild_id]

	async def sync_db(self):
		insert = 'INSERT INTO guilds VALUES ($1, $2);'
		update = 'UPDATE guilds SET prefixes = $1 WHERE guild_id = $2'

		for config in self.guild_configs.values():
			if config.get("updated"):
				if not config.get("exists"):
					await self.pool.execute(insert, config["guild_id"], config["prefixes"])
					config["exists"] = True
				else:
					await self.pool.execute(update, config["prefixes"], config["guild_id"])

				config['updated'] = False

	async def sync_db_loop(self):
		while not self.is_closed():
			await asyncio.sleep(30)
			await self.sync_db()

