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

		for extension in extensions:
			self.load_extension(f"extensions.{extension}")

	def callable_prefix(self, bot, msg):
		config = self.guild_configs.get(msg.guild.id)
		return config["prefixes"] if config else secrets.default_prefixes

	def gen_config(self, guild_id):
		self.guild_configs[guild_id] = {"prefixes": {'?', '!'}}