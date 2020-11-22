from discord.ext import commands
import discord


class Music(commands.Cog):
	@commands.command(name='connect', aliases=('c',))
	async def cmd_connect(self, ctx):
		await ctx.author.voice.channel.connect()

	@commands.command(name='disconnect', aliases=('dc',))
	async def cmd_disconnect(self, ctx):
		await ctx.voice_client.disconnect()

def setup(bot):
	bot.add_cog(Music())