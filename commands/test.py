from aiohttp import ClientSession
import discord


class TestGroup(discord.app_commands.Group):
	@discord.app_commands.command(description="test interconnectivity")
	async def get_webpage(self, interaction: discord.Interaction):
		async with ClientSession() as session:
			response = await session.request(method="GET", url="http://phylactery-dev", timeout=20.0)
			message = f"Status: {response.status}\n" \
				f"Content-type: {response.headers['content-type']}\n"
			html = await response.text()
			message += f"Body: {html[:15]}..."
			interaction.response.send_message(message)


async def setup(bot):
	bot.tree.add_command(TestGroup(name="test"))