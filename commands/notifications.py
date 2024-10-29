import discord
from discord import app_commands
from discord.ext import commands
import redis.asyncio as redis


@app_commands.guild_only()
class NotificationsCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.redis = None

	@app_commands.default_permissions()
	@app_commands.command(description="Add this channel to the list of channels to be pinged")
	async def setup_notifications(self, interaction: discord.Interaction):
		await self.redis.sadd("discord:notifications:channels", interaction.channel_id)
		await interaction.response.send_message(
			"This channel has been setup to receive notifications.",
			ephemeral=True
		)

	@app_commands.default_permissions()
	@app_commands.command(description="Remove this channel from the list of channels to be pinged")
	async def remove_notifications(self, interaction: discord.Interaction):
		await self.redis.srem("discord:notifications:channels", interaction.channel_id)
		await interaction.response.send_message(
			"This channel won't receive notifications.",
			ephemeral=True
		)

	@app_commands.default_permissions()
	@app_commands.command(description="Send a message to all notification channels")
	async def send_notification(self, interaction: discord.Interaction):
		async for channel_id in self.redis.sscan_iter("discord:notifications:channels"):
			await self.bot.get_channel(int(channel_id)).send("Hello!")
		await interaction.response.send_message(
			"Sent.",
			ephemeral=True
		)

	async def cog_load(self):
		self.redis = await redis.Redis(host="localhost", port=6379, protocol=3, decode_responses=True)
		print(f"\t - {self.__class__.__name__} loaded")

	async def cog_unload(self):
		await self.redis.close()
		print(f"\t - {self.__class__.__name__} unloaded")


async def setup(bot: commands.Bot):
	await bot.add_cog(NotificationsCog(bot=bot))
