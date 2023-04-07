from aiohttp import ClientSession
import discord


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
		url=json['url'],
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


class TestGroup(discord.app_commands.Group):
	@discord.app_commands.command(description="test interconnectivity")
	async def get_webpage(self, interaction: discord.Interaction):
		async with ClientSession() as session:
			response = await session.request(method="GET", url="http://phylactery-dev", timeout=20.0)
			message = f"Status: {response.status}\n" \
				f"Content-type: {response.headers['content-type']}\n"
			html = await response.text()
			message += f"Body: {html[:15]}..."
			await interaction.response.send_message(message)

	@discord.app_commands.command(description="test JSON")
	async def raw_json(self, interaction: discord.Interaction):
		async with ClientSession() as session:
			response = await session.request(method="GET", url="http://dev.unigames.asn.au/api/items/random/any",
											 timeout=20.0)
			json = await response.json()
			message = f'JSON:\n```{json}```'
			await interaction.response.send_message(message)

	@discord.app_commands.command(description="test API access")
	async def random_item(self, interaction: discord.Interaction):
		async with ClientSession() as session:
			response = await session.request(method="GET", url="http://dev.unigames.asn.au/api/items/random/any", timeout=20.0)
			json = await response.json()
			embed = item_embed_from_json(json)
			await interaction.response.send_message(embed=embed)


async def setup(bot):
	bot.tree.add_command(TestGroup(name="test"))
