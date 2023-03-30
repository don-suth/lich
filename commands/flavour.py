import asyncio
from aiohttp import ClientSession
import re
import discord


def format_flavour_text(raw_flavour):
	# Add asterisks to the start and end of the text.
	formatted_flavour = '*' + raw_flavour + '*'
	# Replace pairs of asterisks with only whitespace between them.
	pattern = re.compile(r'\*\s*\*')
	formatted_flavour = pattern.sub('', formatted_flavour)
	# If an asterisk appears after whitespace, also put one after it.
	pattern = re.compile(r'\s\*')
	formatted_flavour = pattern.sub('* ', formatted_flavour)
	return formatted_flavour


async def get_random_flavour():
	url = 'https://api.scryfall.com/cards/random?q=ft%3A%2F%5E.%2B%2F'
	json = {}
	async with ClientSession() as session:
		try:
			response = await session.request(method="GET", url=url, timeout=20.0)
			json = await response.json()
		except asyncio.exceptions.TimeoutError:
			print("Timed out.")
	flavour_text = json.get("flavor_text", None)
	if flavour_text:
		return format_flavour_text(flavour_text)
	else:
		return None


class FlavourGetter:
	def __init__(self):
		self.random_card_queue = asyncio.Queue(maxsize=10)
		self.random_card_task = None

	async def fill_random_card_cache(self):
		while True:
			while not self.random_card_queue.full():
				flavour_text = await get_random_flavour()
				if flavour_text is not None:
					await self.random_card_queue.put(flavour_text)
					print("Put flavour text in queue:", flavour_text, f"[{self.random_card_queue.qsize()}]")
					await asyncio.sleep(0.1)
			await asyncio.sleep(10)

	async def pull_random_flavour(self):
		flavour_text = await self.random_card_queue.get()
		return flavour_text




async def setup(bot):
	flavour_getter = FlavourGetter()

	@discord.app_commands.command(name="flavour", description="Returns a random flavour text from Magic the Gathering. See if you can guess the card!")
	async def return_flavour(interaction: discord.Interaction):
		flavour_text = await flavour_getter.pull_random_flavour()
		await interaction.response.send_message(flavour_text)

	if flavour_getter.random_card_task is None:
		print('Populating flavour text cache:')
		flavour_getter.random_card_task = asyncio.create_task(flavour_getter.fill_random_card_cache())
	bot.tree.add_command(return_flavour)
