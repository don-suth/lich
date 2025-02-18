import discord
from discord.ext import commands
from get_docker_secret import get_docker_secret
import os
import logging


LICH_DEBUG = os.environ.get("LICH_DEBUG", "FALSE")


logger = logging.getLogger("discord")
logger.setLevel(logging.NOTSET)
logger.addHandler(logging.StreamHandler())


guilds = []

try:
	secret_guilds = get_docker_secret('discord_bot_guilds', safe=False).split('\n')
	for line in secret_guilds:
		guilds.append(discord.Object(id=line.rstrip('\n')))
except (TypeError, ValueError):
	with open('guilds') as guild_file:
		for line in guild_file.readlines():
			guilds.append(discord.Object(id=line.rstrip('\n')))

controller_guild = discord.Object(id="842784899916365854")


class LichClient(commands.Bot):
	def __init__(self):
		starting_intents = discord.Intents.default()
		starting_intents.typing = False
		starting_intents.message_content = True
		allowed_mentions = discord.AllowedMentions.none()
		super().__init__(command_prefix="this_will_never_trigger", intents=starting_intents, allowed_mentions=allowed_mentions)
		self.default_extensions = [
			"cogs.startingrules", "cogs.dice", "cogs.warriorcat",
			"cogs.flavour", "cogs.gavin", "cogs.library_items",
			"cogs.keysmash", "cogs.webcams", "cogs.door",
			"cogs.statuses"
		]
		self.controller_extensions = [
			"cogs.relay", "cogs.notifications"
		]
		if LICH_DEBUG == "TRUE":
			self.default_extensions.append('cogs.test')

		self.random_card_task = None
		self.random_status_task = None

	async def setup_hook(self):
		if LICH_DEBUG == "TRUE":
			print('Lich is operating in DEBUG mode')
		for extension in self.default_extensions:
			await self.load_extension(extension)
		for guild in guilds:
			try:
				self.tree.copy_global_to(guild=guild)
				await self.tree.sync(guild=guild)
			except discord.errors.Forbidden:
				print("Forbidden Error whilst copying default extensions")
		
		for controller_extension in self.controller_extensions:
			await self.load_extension(controller_extension)
		try:
			self.tree.copy_global_to(guild=controller_guild)
			await self.tree.sync(guild=controller_guild)
		except discord.errors.Forbidden:
			print("Forbidden Error whilst copying controller extensions")
		print("Done Setup")

	async def on_ready(self):
		print(f'Logged in as {client.user} (ID: {client.user.id})')
		print('------')


client = LichClient()


if __name__ == "__main__":
	try:
		secret = get_docker_secret('discord_bot_token', safe=False)
	except (TypeError, ValueError):
		with open('secret', 'r') as f:
			secret = f.read()
	client.run(secret, log_handler=None)
