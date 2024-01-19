import discord
from discord import ui, Interaction
from aiohttp import ClientSession
from io import BytesIO


DONALD_ID = 243405584651517954


def check_if_its_me(interaction: discord.Interaction):
	return interaction.user.id == DONALD_ID


async def get_image(image_url, session, filename):
	image_bytes = BytesIO()
	async with session.get(image_url) as response:
		image_bytes.write(await response.read())
	discord_file = discord.File(image_bytes, filename=filename)
	return discord_file


class InputBox(ui.Modal, title="Enter Webcam Password:"):
	password = ui.TextInput(label="Webcam Password", style=discord.TextStyle.short)

	async def on_submit(self, interaction: Interaction) -> None:
		if str(self.password) != "supersecret":
			await interaction.response.send_message("Sorry, the password you entered was incorrect.", ephemeral=True)
		else:
			await interaction.response.defer(ephemeral=False, thinking=True)
			async with ClientSession() as session:
				test_image = await get_image(image_url="https://preview.redd.it/5l9c34dl57q21.png", session=session, filename="voja.png")
			embed = discord.Embed(title="Voja")
			embed.set_image(url="attachment://voja.png")
			await interaction.followup.send(embed=embed, files=[test_image])


@discord.app_commands.command(description="Testing the new webcam commands.")
@discord.app_commands.guild_only()
@discord.app_commands.check(check_if_its_me)
async def test_new_webcams(interaction: discord.Interaction):
	await interaction.response.send_modal(InputBox())


async def setup(bot):
	bot.tree.add_command(test_new_webcams)
