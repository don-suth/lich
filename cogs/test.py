from typing import Any

from aiohttp import ClientSession
import discord
from discord import Interaction
from discord._types import ClientT
from discord.ext import commands


item_code = {
	'BG': 'Board Game',
	'BK': 'Book',
	'CG': 'Card Game',
	'??': '',
}


class LetMeInView(discord.ui.LayoutView):
	class MyButton(discord.ui.Button):
		async def callback(self, interaction: Interaction[ClientT]) -> Any:
			await interaction.response.send_message('Hi!', ephemeral=True)
	
	container = discord.ui.Container(
		discord.ui.TextDisplay("# Let Me In!"),
		discord.ui.Separator(),
		discord.ui.TextDisplay(
			"If you are locked out of Cameron Hall, you can send a message to "
			"the people inside the Unigames clubroom so they can let you in."
		),
		discord.ui.TextDisplay(
			"Conditions:\n"
			"- The clubroom must be open.\n"
			"- You must be an active Unigames member.\n"
			"- You must have linked your Unigames account with your Discord account.\n"
			"- Don't use this unless you are physically at Cameron Hall waiting to get in."
		),
		discord.ui.ActionRow(
			MyButton(label="I Understand - Let Me In!", style=discord.ButtonStyle.success)
		)
	)


@discord.app_commands.guild_only()
class TestCog(commands.GroupCog, group_name="test"):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@discord.app_commands.command(description="Test a modal")
	async def test_modal(self, interaction: discord.Interaction):
		await interaction.response.send_message(ephemeral=True, view=LetMeInView())
	
	@discord.app_commands.command(description="Reload test commands")
	async def test_reload(self, interaction: discord.Interaction):
		await interaction.response.defer(ephemeral=True, thinking=True)
		await self.bot.reload_extension("cogs.test")
		await interaction.followup.send("Reloaded!")


	async def cog_load(self):
		print(f"\t - {self.__class__.__name__} loaded")
	
	async def cog_unload(self):
		print(f"\t - {self.__class__.__name__} unloaded")


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


async def setup(bot: commands.Bot):
	await bot.add_cog(TestCog(bot=bot))
