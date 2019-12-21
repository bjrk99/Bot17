from discord.ext import commands
import discord


class Music(commands.Cog):
	@commands.command()
	async def connect(self, ctx):
		await ctx.author.voice.channel.connect()

	@commands.command()
	async def disconnect(self, ctx):
		await ctx.voice_client.disconnect()

def setup(bot):
	bot.add_cog(Music())