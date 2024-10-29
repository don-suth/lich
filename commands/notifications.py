import discord
from discord import app_commands
from discord.ext import commands, tasks
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

	@tasks.loop()
	async def redis_pubsub_reader(self):
		async with self.redis.pubsub() as pubsub:
			await pubsub.subscribe("discord:notifications:ping")
			while True:
				message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=None)
				if message is not None:
					print(message)

	async def cog_load(self):
		self.redis = await redis.Redis(host="localhost", port=6379, decode_responses=True)
		print(f"\t - {self.__class__.__name__} loaded")
		self.redis_pubsub_reader.start()
		print(f"\t\t - Task 'redis_pubsub_reader' started")

	async def cog_unload(self):
		self.redis_pubsub_reader.stop()
		await self.redis.close()
		print(f"\t - {self.__class__.__name__} unloaded")


async def setup(bot: commands.Bot):
	await bot.add_cog(NotificationsCog(bot=bot))
