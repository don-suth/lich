import discord
from discord import app_commands
from discord.ext import commands, tasks
import redis.asyncio as redis
import os


NOTIFICATION_TYPES = [
	"minutes",
	"news",
	"operations",
	"door",
]


class ChannelInputModal(discord.ui.Modal, title="Enter Channel ID:"):
	channel_id = discord.ui.TextInput(label="Enter Channel ID:")

	def __init__(self, *args, redis_client, notification_type, remove=False, **kwargs):
		super().__init__(*args, **kwargs)
		self.redis_client = redis_client
		self.notification_type = notification_type
		self.title = f"({self.notification_type.title()}) Enter Channel ID:"
		self.remove = remove

	async def on_submit(self, interaction: discord.Interaction) -> None:
		try:
			subscribed_channel_id = int(f"{self.channel_id}")
			text_channel = interaction.client.get_channel(subscribed_channel_id)
			channel_name = text_channel.name
			channel_guild_name = text_channel.guild.name
		except ValueError:
			await interaction.response.send_message("An error occurred.", ephemeral=True)
			return
		if self.remove:
			await self.redis_client.srem(f"discord:{self.notification_type}:channels", subscribed_channel_id)
			await interaction.response.send_message(
				f"`Removed {channel_name} (in Guild {channel_guild_name}) from receiving {self.notification_type} notifications.`",
				ephemeral=False
			)
		else:
			await self.redis_client.sadd(f"discord:{self.notification_type}:channels", subscribed_channel_id)
			await interaction.response.send_message(
				f"`Set up {channel_name} (in Guild {channel_guild_name}) to receive {self.notification_type} notifications.`",
				ephemeral=False
			)


@app_commands.guild_only()
class NotificationsCog(commands.GroupCog, group_name="notifications"):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.redis = None

	@app_commands.command(description="Setup a channel for minutes notifications")
	async def setup_minutes(self, interaction: discord.Interaction):
		await interaction.response.send_modal(ChannelInputModal(redis_client=self.redis, notification_type="minutes"))

	@app_commands.command(description="Setup a channel for news notifications")
	async def setup_news(self, interaction: discord.Interaction):
		await interaction.response.send_modal(ChannelInputModal(redis_client=self.redis, notification_type="news"))

	@app_commands.command(description="Setup a channel for operational notifications")
	async def setup_operations(self, interaction: discord.Interaction):
		await interaction.response.send_modal(ChannelInputModal(redis_client=self.redis, notification_type="operations"))

	@app_commands.command(description="Setup a channel for door notifications")
	async def setup_door(self, interaction: discord.Interaction):
		await interaction.response.send_modal(ChannelInputModal(redis_client=self.redis, notification_type="door"))

	@app_commands.command(description="Setup a channel for minutes notifications")
	async def remove_minutes(self, interaction: discord.Interaction):
		await interaction.response.send_modal(ChannelInputModal(remove=True, redis_client=self.redis, notification_type="minutes"))

	@app_commands.command(description="Setup a channel for news notifications")
	async def remove_news(self, interaction: discord.Interaction):
		await interaction.response.send_modal(ChannelInputModal(remove=True, redis_client=self.redis, notification_type="news"))

	@app_commands.command(description="Setup a channel for operational notifications")
	async def remove_operations(self, interaction: discord.Interaction):
		await interaction.response.send_modal(ChannelInputModal(remove=True, redis_client=self.redis, notification_type="operations"))

	@app_commands.command(description="Setup a channel for door notifications")
	async def remove_door(self, interaction: discord.Interaction):
		await interaction.response.send_modal(ChannelInputModal(remove=True, redis_client=self.redis, notification_type="door"))

	@app_commands.command(description="Remove this channel from the list of channels to be pinged")
	async def remove_all(self, interaction: discord.Interaction):
		for notification_type in NOTIFICATION_TYPES:
			await self.redis.delete(f"discord:{notification_type}:channels")
		await interaction.response.send_message(
			"Removed all channels from receiving notifications.",
			ephemeral=False
		)

	@tasks.loop()
	async def redis_pubsub_reader(self):
		async with self.redis.pubsub() as pubsub:
			await pubsub.subscribe(*[f"discord:{notification_type}:ping" for notification_type in NOTIFICATION_TYPES])
			while True:
				message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=None)
				if message is not None:
					async for channel_id in self.redis.sscan_iter(f"discord:{message['channel'][8:-5]}:channels"):
						allowed_mentions = discord.AllowedMentions.all()
						await self.bot.get_channel(int(channel_id)).send(
							content=message.get("data"),
							allowed_mentions=allowed_mentions
						)

	async def cog_load(self):
		redis_host = os.environ.get("REDIS_HOST", "localhost")
		self.redis = await redis.Redis(host=redis_host, port=6379, decode_responses=True)
		print(f"\t - {self.__class__.__name__} loaded")
		self.redis_pubsub_reader.start()
		print(f"\t\t - Task 'redis_pubsub_reader' started")

	async def cog_unload(self):
		self.redis_pubsub_reader.stop()
		await self.redis.aclose()
		print(f"\t - {self.__class__.__name__} unloaded")


async def setup(bot: commands.Bot):
	await bot.add_cog(NotificationsCog(bot=bot))
