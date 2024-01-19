import asyncio

import discord
from discord import ui, Interaction
from aiohttp import ClientSession
from io import BytesIO
import UIComponents
import datetime


DONALD_ID = 243405584651517954
PERTH_TIME = datetime.timezone(datetime.timedelta(hours=8))
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


class WebcamSwitcherView(discord.ui.View):
	children: [UIComponents.EmbedPaginatorButton]

	def __init__(self, *args, files, **kwargs):
		super().__init__(*args, **kwargs)
		time_now = datetime.datetime.now(PERTH_TIME)
		time_string = time_now.strftime("Unigames @ %d/%m/%Y %H:%M")
		for i in range(len(files)):
			card = files[i]
			card_embed = discord.Embed(title=time_string)
			card_embed.set_image(url=f"attachment://{card.filename}")
			self.add_item(UIComponents.EmbedPaginatorButton(label=str(i + 1), embed=card_embed, starting=(i == 0)))
		self.current_camera = 0

	def get_current_embed(self):
		return self.children[self.current_camera].embed


class InputModal(ui.Modal, title="Enter Webcam Password:"):
	password = ui.TextInput(label="Webcam Password", style=discord.TextStyle.short)

	async def on_submit(self, interaction: Interaction) -> None:
		if str(self.password) != "supersecret":
			await interaction.response.send_message("Sorry, the password you entered was incorrect.", ephemeral=True)
		else:
			await interaction.response.defer(ephemeral=False, thinking=True)
			async with ClientSession() as session:
				async with asyncio.TaskGroup() as tg:
					discord_files_tasks = []
					for i in range(len(TEST_IMAGES)):
						discord_files_tasks.append(tg.create_task(get_image(image_url=TEST_IMAGES[i], session=session, filename=f"{i}.png")))
			resulting_files = tuple(map(lambda t: t.result(), discord_files_tasks))

			switcher_view = WebcamSwitcherView(files=resulting_files)
			card_embed = switcher_view.get_current_embed()
			await interaction.followup.send(embed=card_embed, files=resulting_files, view=switcher_view)


@discord.app_commands.command(description="Testing the new webcam commands.")
@discord.app_commands.guild_only()
@discord.app_commands.check(check_if_its_me)
async def test_new_webcams(interaction: discord.Interaction):
	await interaction.response.send_modal(InputModal())


async def setup(bot):
	bot.tree.add_command(test_new_webcams)
