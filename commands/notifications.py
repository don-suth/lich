import discord
from discord import app_commands
from discord.ext import commands
import redis


@app_commands.guild_only()
class NotificationsCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.redis = redis.Redis(host="localhost", port=6379, protocol=3, decode_responses=True)

	@app_commands.default_permissions()
	@app_commands.command(description="Add this channel to the list of channels to be pinged")
	async def setup_notifications(self, interaction: discord.Interaction):
		self.redis.sadd("discord:notifications:channels", interaction.channel_id)
		await interaction.response.send_message(
			"This channel has been setup to receive notifications.",
			ephemeral=True
		)

	@app_commands.default_permissions()
	@app_commands.command(description="Send a message to all notification channels")
	async def send_notification(self, interaction: discord.Interaction):
		for channel_id in self.redis.sscan_iter("discord:notifications:channels"):
			print(type(channel_id), channel_id)
			await self.bot.get_channel(int(channel_id)).send("Hello!")
		await interaction.response.send_message(
			"Sent.",
			ephemeral=True
		)

	async def cog_load(self):
		print(f"\t - {self.__class__.__name__} loaded")

	async def cog_unload(self):
		print(f"\t - {self.__class__.__name__} unloaded")


async def setup(bot: commands.Bot):
	await bot.add_cog(NotificationsCog(bot=bot))
