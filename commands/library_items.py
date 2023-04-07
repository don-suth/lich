from aiohttp import ClientSession
import discord
import os


API_ACCESS = os.environ.get('API_ACCESS', 'http://127.0.0.1:8000/api')
SITE_PREFIX = os.environ.get('SITE_PREFIX', 'http://127.0.0.1:8000')


item_code = {
	'BG': 'Board Game',
	'BK': 'Book',
	'CG': 'Card Game',
	'??': '',
}


def trim_description(description):
	if len(description) < 200:
		trimmed = description[:200]+'...'
	else:
		trimmed = description
	return trimmed


def item_embed_from_json(json) -> discord.Embed:
	item_embed = discord.Embed(
		title=json['name'],
		description=trim_description(json['description']),
		colour=discord.Colour.from_str('#622c29'),
		url=SITE_PREFIX+json['url'],
	)
	item_embed.set_thumbnail(
		url=json['image'],
	)
	item_embed.set_author(
		name=item_code[json['type']],
	)
	item_embed.add_field(
		name="In the clubroom?",
		value=json['availability']['in_clubroom'],
		inline=True,
	)
	if json['is_borrowable'] is True:
		item_embed.add_field(
			name="Available to borrow?",
			value=json['availability']['is_available'],
			inline=True,
		)
	else:
		item_embed.add_field(
			name="Borrowable?",
			value=json['availability']['is_available'],
			inline=True,
		)
	if json['availability']['expected_availability_date'] is not None:
		item_embed.add_field(
			name="Expected availability date:",
			value=json['availability']['expected_availability_date'],
			inline=False,
		)
	return item_embed


class RandomGroup(discord.app_commands.Group):
	@discord.app_commands.command(name="item", description="Get a random item from the Unigames library!")
	async def random_item(self, interaction: discord.Interaction):
		async with ClientSession() as session:
			response = await session.request(
				method="GET",
				url=API_ACCESS+"/items/random/any",
				timeout=20.0
			)
			json = await response.json()
			embed = item_embed_from_json(json)
			await interaction.response.send_message(embed=embed)

	@discord.app_commands.command(name="book", description="Get a random Book from the Unigames library!!")
	async def random_book(self, interaction: discord.Interaction):
		async with ClientSession() as session:
			response = await session.request(
				method="GET",
				url=API_ACCESS+"/items/random/book",
				timeout=20.0
			)
			json = await response.json()
			embed = item_embed_from_json(json)
			await interaction.response.send_message(embed=embed)

	@discord.app_commands.command(name="boardgame", description="Get a random Book from the Unigames library!!")
	async def random_boardgame(self, interaction: discord.Interaction):
		async with ClientSession() as session:
			response = await session.request(
				method="GET",
				url=API_ACCESS + "/items/random/boardgame",
				timeout=20.0
			)
			json = await response.json()
			embed = item_embed_from_json(json)
			await interaction.response.send_message(embed=embed)

	@discord.app_commands.command(name="cardgame", description="Get a random Book from the Unigames library!!")
	async def random_cardgame(self, interaction: discord.Interaction):
		async with ClientSession() as session:
			response = await session.request(
				method="GET",
				url=API_ACCESS + "/items/random/cardgame",
				timeout=20.0
			)
			json = await response.json()
			embed = item_embed_from_json(json)
			await interaction.response.send_message(embed=embed)


async def setup(bot):
	bot.tree.add_command(RandomGroup(name="random"))
