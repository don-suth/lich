import os
import discord
from discord import app_commands
from discord.ext import commands
import redis.asyncio as redis


class DoorCog(commands.GroupCog, group_name="door"):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.redis = None

	@app_commands.default_permissions()
	@app_commands.command(description="Open the clubroom")
	async def open(self, interaction: discord.Interaction):
		await self.redis.set("door:status", "OPEN")
		await self.redis.publish("door:updates", "OPEN")
		await interaction.response.send_message("OPEN!", ephemeral=True)

	@app_commands.default_permissions()
	@app_commands.command(description="Close the clubroom")
	async def close(self, interaction: discord.Interaction):
		await self.redis.set("door:status", "CLOSED")
		await self.redis.publish("door:updates", "CLOSED")
		await interaction.response.send_message("CLOSE!", ephemeral=True)

	async def cog_load(self):
		redis_host = os.environ.get("REDIS_HOST", "localhost")
		self.redis = await redis.Redis(host=redis_host, port=6379, decode_responses=True)
		print(f"\t - {self.__class__.__name__} loaded")

	async def cog_unload(self):
		print(f"\t - {self.__class__.__name__} unloaded")
		await self.redis.aclose()


async def setup(bot: commands.Bot):
	await bot.add_cog(DoorCog(bot=bot))
