import discord
from discord.ext import commands
from statuses import change_status
import asyncio
from get_docker_secret import get_docker_secret
import os


LICH_DEBUG = os.environ.get("LICH_DEBUG", False)


guilds = []

try:
	secret_guilds = get_docker_secret('discord_bot_guilds', safe=False).split('\n')
	for line in secret_guilds:
		guilds.append(discord.Object(id=line.rstrip('\n')))
except (TypeError, ValueError):
	with open('guilds') as guild_file:
		for line in guild_file.readlines():
			guilds.append(discord.Object(id=line.rstrip('\n')))


class LichClient(commands.Bot):
	def __init__(self):
		starting_intents = discord.Intents.default()
		starting_intents.typing = False
		super().__init__(command_prefix="this_will_never_trigger", intents=starting_intents)
		self.default_extensions = \
			['commands.startingrules', 'commands.dice', 'commands.warriorcat', 'commands.flavour',
				'commands.webcams', 'commands.gavin', 'commands.library_items']
		if LICH_DEBUG:
			self.default_extensions.append('commands.test')

		self.random_card_task = None
		self.random_status_task = None

	async def setup_hook(self):
		for extension in self.default_extensions:
			await self.load_extension(extension)
		for guild in guilds:
			try:
				self.tree.copy_global_to(guild=guild)
				await self.tree.sync(guild=guild)
			except discord.errors.Forbidden:
				pass

	async def on_ready(self):
		print(f'Logged in as {client.user} (ID: {client.user.id})')
		print('------')
		if self.random_status_task is None:
			self.random_status_task = asyncio.create_task(change_status(self))


client = LichClient()


if __name__ == "__main__":
	try:
		secret = get_docker_secret('discord_bot_secret', safe=False)
	except (TypeError, ValueError):
		with open('secret', 'r') as f:
			secret = f.read()
	client.run(secret)
