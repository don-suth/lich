from aiohttp import ClientSession
import discord


class TestGroup(discord.app_commands.Group):
	@discord.app_commands.command(description="test interconnectivity")
	async def get_webpage(self, interaction: discord.Interaction):
		async with ClientSession() as session:
			response = await session.request(method="GET", url="http://phylactery-dev", timeout=20.0)
			print("Status:", response.status)
			print("Content-type:", response.headers['content-type'])

			html = await response.text()
			print("Body:", html[:15], "...")



async def setup(bot):
	bot.tree.add_command(TestGroup(name="test"))