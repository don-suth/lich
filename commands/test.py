from aiohttp import ClientSession
import discord


def item_embed_from_json(json) -> discord.Embed:
	item_embed = discord.Embed(title=json['name'], description=json['description'][:200])
	item_embed.set_thumbnail(url=json['image'])
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

	@discord.app_commands.command(description="test API access")
	async def random_item(self, interaction: discord.Interaction):
		async with ClientSession() as session:
			response = await session.request(method="GET", url="http://phylactery-dev/api/library/items/random/item", timeout=20.0)
			json = await response.json()
			embed = item_embed_from_json(json)
			await interaction.response.send_message(embed=embed)


async def setup(bot):
	bot.tree.add_command(TestGroup(name="test"))
