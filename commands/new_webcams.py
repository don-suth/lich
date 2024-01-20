import asyncio

import discord
from discord import ui, Interaction
from aiohttp import ClientSession
from io import BytesIO
import datetime
import base64


DONALD_ID = 243405584651517954
UNIGAMES_CAMERAS = ['ipcamera6', 'ipcamera9', 'ipcamera10']
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


async def get_image(image_url, session, filename, headers):
	image_bytes = BytesIO()
	async with session.get(image_url, headers=headers) as response:
		if response.status != 200:
			raise PermissionError
		response_bytes = await response.read()
	image_bytes.write(response_bytes)
	image_bytes.seek(0)
	discord_file = discord.File(image_bytes, filename=filename)
	return discord_file


def tob64(code):
	code_bytes = code.encode("ascii")
	b64_bytes = base64.b64encode(code_bytes)
	return b64_bytes.decode("ascii")


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
		time_now = datetime.datetime.now(PERTH_TIME)
		time_string = time_now.strftime("Unigames @ %d/%m/%Y %H:%M")
		time_code = time_now.strftime("%Y%m%d-%H%M")

		code = tob64(f"ucc:{self.password}")

		try:
			async with ClientSession() as session:
				async with asyncio.TaskGroup() as tg:
					discord_files_tasks = []
					for camera in UNIGAMES_CAMERAS:
						webcam_url = f"https://webcam.ucc.asn.au/archive.php?camera={camera}&timestamp={time_code}"
						headers = {"Authorization": f"Basic {code}"}
						discord_files_tasks.append(tg.create_task(get_image(image_url=webcam_url, session=session, filename=f"{camera}.jpeg", headers=headers)))
			resulting_files = tuple(map(lambda t: t.result(), discord_files_tasks))
		except PermissionError:
			await interaction.response.send_message(content="Sorry, the password you entered didn't seem to work.", ephemeral=True)
		else:
			await interaction.response.defer(thinking=False, ephemeral=True)
			await self.followup.send(content=time_string, files=resulting_files, ephemeral=False)


@discord.app_commands.command(description="Testing the new webcam commands.")
@discord.app_commands.guild_only()
@discord.app_commands.check(check_if_its_me)
async def test_new_webcams(interaction: discord.Interaction):
	await interaction.response.send_modal(PasswordInputModal(followup=interaction.followup))


async def setup(bot):
	bot.tree.add_command(test_new_webcams)
