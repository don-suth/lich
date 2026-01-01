import os
import discord
from discord import app_commands
from discord.ext import commands, tasks
import redis.asyncio as redis
from datetime import datetime, timezone, timedelta

# Channel where Gatekeepers post updates about the door
DOOR_UPDATES_CHANNEL = 1284487409987223613

# Channel where the bot posts updates about the door
DOOR_STATUS_CHANNEL = 1284487409987223613


class DoorCog(commands.GroupCog, group_name="door"):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.redis = None

	async def send_door_opened_notification(self, display_name):
		open_embed = discord.Embed(
			title="Door Open!",
			description="The door is open!",
			colour=discord.Colour.green(),
			timestamp=datetime.now(tz=timezone(timedelta(hours=8))),
		)
		open_embed.set_footer(text=f"Opened by {display_name}")
		open_embed.set_image(url="https://unigames.asn.au/static/images/misc/unigames_open.png")
		await self.bot.get_channel(DOOR_STATUS_CHANNEL).send(content="Door status: ", embed=open_embed)
	
	async def send_door_closed_notification(self, display_name):
		closed_embed = discord.Embed(
			title="Door Closed!",
			description="The door is closed!",
			colour=discord.Colour.red(),
			timestamp=datetime.now(tz=timezone(timedelta(hours=8))),
		)
		closed_embed.set_footer(text=f"Closed by {display_name}")
		closed_embed.set_thumbnail(url="https://unigames.asn.au/static/images/misc/unigames_closed.png")
		await self.bot.get_channel(DOOR_STATUS_CHANNEL).send(content="Door status: ", embed=closed_embed)
	
	async def redis_open_door(self, discord_id, discord_display_name):
		"""
		Updates Redis to open the Door.
		This involves:
			1) Changing the status of the "door:status" key.
			2) Publishing the status on the Pubsub channel "door:updates".
			3) Adding an entry to the Redis stream with:
				- timestamp
				- new status
				- member id
				- member name
				- source (phylactery/lich)
		"""
		pipe = self.redis.pipeline()
		pipe.set("door:status", "OPEN")
		pipe.xadd(
			"door:stream", {
				"timestamp": datetime.now(timezone.utc).timestamp(),
				"new_status": "OPEN",
				"id_type": "discord",
				"discord_id": discord_id,
				"display_name": discord_display_name,
				"source": "lich"
			}
		)
		pipe.publish("door:updates", "OPEN")
		await pipe.execute()
	
	async def redis_close_door(self, discord_id, discord_display_name):
		"""
		Updates Redis to open the Door.
		This involves:
			1) Changing the status of the "door:status" key.
			2) Publishing the status on the Pubsub channel "door:updates".
			3) Adding an entry to the Redis stream with:
				- timestamp
				- new status
				- member id
				- member name
				- source (phylactery/lich)
		"""
		pipe = self.redis.pipeline()
		pipe.set("door:status", "CLOSED")
		pipe.xadd(
			"door:stream", {
				"timestamp": datetime.now(timezone.utc).timestamp(),
				"new_status": "CLOSED",
				"id_type": "discord",
				"discord_id": discord_id,
				"display_name": discord_display_name,
				"source": "lich"
			}
		)
		pipe.publish("door:updates", "CLOSED")
		await pipe.execute()
	
	@app_commands.default_permissions()
	@app_commands.command(description="Open the clubroom")
	async def open(self, interaction: discord.Interaction):
		await self.redis_open_door(discord_id=interaction.user.id, discord_display_name=interaction.user.display_name)
		await interaction.response.send_message("Door opened.", ephemeral=True)

	@app_commands.default_permissions()
	@app_commands.command(description="Close the clubroom")
	async def close(self, interaction: discord.Interaction):
		await self.redis_close_door(discord_id=interaction.user.id, discord_display_name=interaction.user.display_name)
		await interaction.response.send_message("Door closed.", ephemeral=True)
	
	@tasks.loop()
	async def door_watcher(self):
		"""
		Watch for door updates made by other services and post about them.
		"""
		while True:
			# Wait until the door status gets updated
			message_info = (await self.redis.xread({"door:stream": "$"}, count=1, block=0))[0][1][0][1]
			if message_info["source"] != "lich":
				# Only post something if lich didn't update it
				if message_info["new_status"] == "OPEN":
					await self.send_door_opened_notification(display_name=message_info["display_name"])
				elif message_info["new_status"] == "CLOSED":
					await self.send_door_closed_notification(display_name=message_info["display_name"])
			

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		"""
			Listens to messages in the Door Updates Channel, and updates the door status
			if it finds the words "open" or "closed" in the message.
		"""
		# If the message is from a particular channel...
		if message.channel.id == 1284487409987223613:
			# ...And the message didn't come from the bot...
			if message.author.id != self.bot.user.id:
				if message.content == "":
					print("Empty message")
				contains_open = "open" in message.content.lower()
				contains_closed = "close" in message.content.lower()

				if contains_open and not contains_closed:
					# Opem the door, and react to the post to confirm
					await self.open_door(display_name=message.author.display_name)
					await message.add_reaction("<a:room:1341342965859356682>")
					await message.add_reaction("<a:is:1341343001351421992>")
					await message.add_reaction("<a:open:1341343021601394770>")

				elif contains_closed and not contains_open:
					# Close the door, and react to the post to confirm
					await self.close_door(display_name=message.author.display_name)
					await message.add_reaction("<a:room:1341342965859356682>")
					await message.add_reaction("<a:is:1341343001351421992>")
					await message.add_reaction("<a:shut:1341343034918572123>")

				elif contains_open and contains_closed:
					# Ambiguous - do nothing and let the user know.
					await message.author.send(
						'Your door status update contained both "open" and "close". \n'
						'Please send a new update with exactly one of those keywords. \n'
						'Thank you, citizen! Remember, compliance is mandatory!'
					)
					await message.add_reaction("❌")
				elif not contains_open and not contains_closed:
					# No detected updates - do nothing and let the user know.
					await message.author.send(
						'Your door status update didn\'t contain either "open" or "close". \n'
						'Please send a new update with exactly one of those keywords. \n'
						'Thank you, citizen! Remember, compliance is mandatory!'
					)
					await message.add_reaction("❌")

	async def cog_load(self):
		redis_host = os.environ.get("REDIS_HOST", "localhost")
		self.redis = await redis.Redis(host=redis_host, port=6379, decode_responses=True)
		print(f"\t - {self.__class__.__name__} loaded")
		self.door_watcher.start()
		print(f"\t\t - Task 'door_watcher' started")

	async def cog_unload(self):
		print(f"\t - {self.__class__.__name__} unloaded")
		self.door_watcher.stop()
		print(f"\t\t - Task 'door_watcher' stopped")
		await self.redis.aclose()


async def setup(bot: commands.Bot):
	await bot.add_cog(DoorCog(bot=bot))
