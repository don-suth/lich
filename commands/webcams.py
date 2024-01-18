import discord
import datetime
import UIComponents

UNIGAMES_CAMERAS = ['ipcamera6', 'ipcamera9', 'ipcamera10']
PERTH_TIME = datetime.timezone(datetime.timedelta(hours=8))

DONALD_ID = 243405584651517954


def check_if_it_is_me(interaction: discord.Interaction):
	return interaction.user.id == DONALD_ID


class WebcamSwitcherView(discord.ui.View):
	children: [UIComponents.EmbedPaginatorButton]

	def __init__(self):
		super().__init__()
		time_now = datetime.datetime.now(PERTH_TIME)
		time_string = time_now.strftime("Unigames @ %d/%m/%Y %H:%M")
		time_code = time_now.strftime("%Y%m%d-%H%M")
		for i in range(len(UNIGAMES_CAMERAS)):
			camera = UNIGAMES_CAMERAS[i]
			camera_embed = discord.Embed(title=time_string)
			camera_embed.set_image(url=f"https://webcam.ucc.asn.au/archive.php?camera={camera}&timestamp={time_code}")
			self.add_item(UIComponents.EmbedPaginatorButton(label=str(i + 1), embed=camera_embed, starting=(i == 0)))
		self.current_camera = 0

	def get_current_embed(self):
		return self.children[self.current_camera].embed


class JokeWebcamView(discord.ui.View):
	children: [UIComponents.EmbedPaginatorButton]

	def __init__(self):
		super().__init__()


@discord.app_commands.command(description="Take a look at what's happening in the clubroom right now!")
@discord.app_commands.guild_only()
async def webcams(interaction: discord.Interaction):
	switcher_view = WebcamSwitcherView()
	camera_embed = switcher_view.get_current_embed()
	await interaction.response.send_message(embed=camera_embed, view=switcher_view)





async def setup(bot):
	bot.tree.add_command(webcams)