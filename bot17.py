from datetime import datetime

from discord.ext import commands
import discord


extensions = ("core",)


class Bot17(commands.AutoShardedBot):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.epoch = datetime.now()

		for extension in extensions:
			self.load_extension(f"extensions.{extension}")