import os
import discord
from datetime import datetime, timezone
from discord.ext import commands
import redis.asyncio as redis


class LetMeInCog(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.redis = None

	async def publish_letmein_request(self, name, entrance):
		timestamp = datetime.now(timezone.utc).timestamp()
		stream_id = await self.redis.xadd("letmein:stream", {
			"timestamp": timestamp,
			"name": name,
			"entrance": entrance,
			"source": "lich"
		})
		await self.redis.publish("letmein:updates", str(stream_id))

	async def cog_load(self):
		redis_host = os.environ.get("REDIS_HOST", "localhost")
		self.redis = await redis.Redis(host=redis_host, port=6379, decode_responses=True)
		print(f"\t - {self.__class__.__name__} loaded")

	async def cog_unload(self):
		await self.redis.aclose()
		print(f"\t - {self.__class__.__name__} unloaded")

