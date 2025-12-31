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

	async def send_or_edit_door_message(self, embed):
		door_message_id = await self.redis.get("door_message:id")
		if door_message_id is None:
			door_message = await self.bot.get_channel(DOOR_STATUS_CHANNEL).send(content="Door status: ", embed=embed)
			await self.redis.set("door_message:id", door_message.id)
		else:
			door_message = await self.bot.get_channel(DOOR_STATUS_CHANNEL).fetch_message(door_message_id)
			await door_message.edit(content="Door status: ", embed=embed)

	async def open_door(self, display_name):
		await self.redis.set("door:status", "OPEN")
		await self.redis.publish("door:updates", "OPEN")
		open_embed = discord.Embed(
			title="Door Open!",
			description="The door is open!",
			colour=discord.Colour.green(),
			timestamp=datetime.now(tz=timezone(timedelta(hours=8))),
		)
		open_embed.set_footer(text=f"Last opened by {display_name}")
		open_embed.set_image(url="https://unigames.asn.au/static/images/misc/unigames_open.png")
		await self.send_or_edit_door_message(embed=open_embed)

	async def close_door(self, display_name):
		await self.redis.set("door:status", "CLOSED")
		await self.redis.publish("door:updates", "CLOSED")
		closed_embed = discord.Embed(
			title="Door Closed!",
			description="The door is closed!",
			colour=discord.Colour.red(),
			timestamp=datetime.now(tz=timezone(timedelta(hours=8))),
		)
		closed_embed.set_footer(text=f"Last closed by {display_name}")
		closed_embed.set_thumbnail(url="https://unigames.asn.au/static/images/misc/unigames_closed.png")
		await self.send_or_edit_door_message(embed=closed_embed)

	@app_commands.default_permissions()
	@app_commands.command(description="Open the clubroom")
	async def open(self, interaction: discord.Interaction):
		await self.open_door(display_name=interaction.user.display_name)
		await interaction.response.send_message("Door opened.", ephemeral=True)

	@app_commands.default_permissions()
	@app_commands.command(description="Close the clubroom")
	async def close(self, interaction: discord.Interaction):
		await self.close_door(display_name=interaction.user.display_name)
		await interaction.response.send_message("Door closed.", ephemeral=True)
	
	@tasks.loop()
	async def door_watcher(self):
		async with self.redis.pubsub() as pubsub:
			await pubsub.subscribe("door:updates")
			while True:
				message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=None)

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
