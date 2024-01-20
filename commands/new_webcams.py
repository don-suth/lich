import asyncio

import discord
from discord import ui, Interaction
from aiohttp import ClientSession
from io import BytesIO
import UIComponents
import datetime


DONALD_ID = 243405584651517954
PERTH_TIME = datetime.timezone(datetime.timedelta(hours=8))
WEBCAM_CONFIRM_MESSAGE = """The Webcams now require a password to view.
Eventually, you will be able to link your Discord account to your Unigames account to bypass this check.
However, until then, you will need to enter the *shared* password for the webcams.

**Please do not enter your Discord password or your UCC account password.**"""

TEST_IMAGES = (
	"https://cards.scryfall.io/normal/front/0/6/06d4fbe1-8a2f-4958-bb85-1a1e5f1e8d87.jpg?1562202321",
	"https://cards.scryfall.io/normal/front/c/7/c7167648-7ef3-4e2e-ad32-72e8bcfa4b9f.jpg?1640736597",
	"https://cards.scryfall.io/normal/front/5/9/59faa45d-868b-4bc7-934c-0e077642e129.jpg?1674420209",
)


def check_if_its_me(interaction: discord.Interaction):
	return interaction.user.id == DONALD_ID


async def get_image(image_url, session, filename):
	image_bytes = BytesIO()
	async with session.get(image_url) as response:
		response_bytes = await response.read()
	image_bytes.write(response_bytes)
	image_bytes.seek(0)
	discord_file = discord.File(image_bytes, filename=filename)
	return discord_file


class WebcamConfirmView(discord.ui.View):
	def __init__(self, *args, followup, **kwargs):
		super().__init__(*args, **kwargs)
		self.followup = followup

	@discord.ui.button(label="Enter Shared Password", style=discord.ButtonStyle.green)
	async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.send_modal(PasswordInputModal(followup=self.followup))
		self.stop()


class PasswordInputModal(ui.Modal, title="Please enter the Shared Webcam Password:"):
	password = ui.TextInput(label="Shared Webcam Password:", style=discord.TextStyle.short, placeholder="DO NOT ENTER YOUR PERSONAL PASSWORDS", required=True)

	def __init__(self, *args, followup, **kwargs):
		super().__init__(*args, **kwargs)
		self.followup = followup

	async def on_submit(self, interaction: Interaction) -> None:
		if str(self.password) != "supersecret":
			await asyncio.sleep(4)
			await self.followup.send("Sorry, the password you entered was incorrect.", ephemeral=True)
		else:
			async with ClientSession() as session:
				async with asyncio.TaskGroup() as tg:
					discord_files_tasks = []
					for i in range(len(TEST_IMAGES)):
						discord_files_tasks.append(tg.create_task(get_image(image_url=TEST_IMAGES[i], session=session, filename=f"{i}.png")))
			resulting_files = tuple(map(lambda t: t.result(), discord_files_tasks))

			await interaction.response.defer(thinking=False, ephemeral=True)
			await self.followup.send(content="Testing", files=resulting_files, ephemeral=False)


#			switcher_view = WebcamSwitcherView(files=resulting_files)
#			card_embed = switcher_view.get_current_embed()
#			await interaction.followup.send(embed=card_embed, files=resulting_files, view=switcher_view)


@discord.app_commands.command(description="Testing the new webcam commands.")
@discord.app_commands.guild_only()
@discord.app_commands.check(check_if_its_me)
async def test_new_webcams(interaction: discord.Interaction):
	await interaction.response.send_modal(PasswordInputModal(followup=interaction.followup))



async def setup(bot):
	bot.tree.add_command(test_new_webcams)
