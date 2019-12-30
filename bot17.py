from datetime import datetime

from discord.ext import commands
import discord

import secrets


extensions = ("core", "music")


class Bot17(commands.AutoShardedBot):
	def __init__(self, pool=None, *args, **kwargs):
		super().__init__(self.callable_prefix, *args, **kwargs)

		self.epoch = datetime.now()
		self.pool = pool
		self.prefixes = {}

		for extension in extensions:
			self.load_extension(f"extensions.{extension}")

	def callable_prefix(self, bot, msg):
		return self.prefixes.get(msg.guild.id, secrets.default_prefix)