import os
import discord
from discord import app_commands
from discord.ext import commands
import redis.asyncio as redis
from datetime import datetime, timezone, timedelta

# Channel where Gatekeepers post updates about the door
DOOR_UPDATES_CHANNEL = 1284487409987223613

# Channel where the bot posts updates about the door
DOOR_STATUS_CHANNEL = 1313015976551383103


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

	async def cog_load(self):
		redis_host = os.environ.get("REDIS_HOST", "localhost")
		self.redis = await redis.Redis(host=redis_host, port=6379, decode_responses=True)
		print(f"\t - {self.__class__.__name__} loaded")

	async def cog_unload(self):
		print(f"\t - {self.__class__.__name__} unloaded")
		await self.redis.aclose()


async def setup(bot: commands.Bot):
	await bot.add_cog(DoorCog(bot=bot))
