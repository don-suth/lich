import discord
from discord.ext import commands
from statuses import change_status
import asyncio
from get_docker_secret import get_docker_secret
import datetime

UNIGAMES_CAMERAS = ['ipcamera6', 'ipcamera9', 'ipcamera10']

guilds = []

try:
	secret_guilds = get_docker_secret('discord_bot_guilds', safe=False).split('\n')
	for line in secret_guilds:
		guilds.append(discord.Object(id=line.rstrip('\n')))
except (TypeError, ValueError):
	with open('guilds') as guild_file:
		for line in guild_file.readlines():
			guilds.append(discord.Object(id=line.rstrip('\n')))


class LichClient(commands.Bot):
	def __init__(self):
		starting_intents = discord.Intents.default()
		starting_intents.typing = False
		super().__init__(command_prefix="this_will_never_trigger", intents=starting_intents)
		self.default_extensions = ['commands.startingrules', 'commands.dice', 'commands.warriorcat', 'commands.flavour']
		self.random_card_task = None
		self.random_status_task = None

	async def setup_hook(self):
		for extension in self.default_extensions:
			await self.load_extension(extension)
		for guild in guilds:
			self.tree.copy_global_to(guild=guild)
			await self.tree.sync(guild=guild)

	async def on_ready(self):
		print(f'Logged in as {client.user} (ID: {client.user.id})')
		print('------')
		if self.random_status_task is None:
			self.random_status_task = asyncio.create_task(change_status(self))


# class RerollStartingRuleView(discord.ui.View):
# 	@discord.ui.button(label='That rule is lame. Give me another one!', style=discord.ButtonStyle.blurple)
# 	async def reroll(self, interaction: discord.Interaction, button: discord.ui.Button):
# 		new_rule = get_random_starting_rule(interaction.user.display_name)
# 		await interaction.response.edit_message(content=new_rule)


class EmbedPaginatorButton(discord.ui.Button):
	def __init__(self, label, embed, starting=False):
		super().__init__(label=label)
		self.embed = embed
		if starting is True:
			self.style = discord.ButtonStyle.primary
		else:
			self.style = discord.ButtonStyle.secondary

	async def callback(self, interaction: discord.Interaction):
		for child in self.view.children:
			child.style = discord.ButtonStyle.secondary
		self.style = discord.ButtonStyle.primary
		await interaction.response.edit_message(embed=self.embed, view=self.view)


# class WebcamSwitcherButton(discord.ui.Button):
# 	def __init__(self, label, camera, time, start):
# 		super().__init__(label=label)
# 		self.image_url = f"https://webcam.ucc.asn.au/archive.php?camera={camera}&timestamp={time}"
# 		self.webcam_embed = discord.Embed(title="Unigames @ ")
# 		self.webcam_embed.set_image(url=self.image_url)
# 		if start is True:
# 			self.style = discord.ButtonStyle.primary
# 			self.disabled = True
# 		else:
# 			self.style = discord.ButtonStyle.secondary
# 			self.disabled = False
#
# 	async def callback(self, interaction: discord.Interaction):
# 		for child in self.view.children:
# 			child.disabled = False
# 			child.style = discord.ButtonStyle.secondary
# 		self.disabled = True
# 		self.style = discord.ButtonStyle.primary
# 		await interaction.response.edit_message(embed=self.webcam_embed, view=self.view)


class WebcamSwitcherView(discord.ui.View):
	children: [EmbedPaginatorButton]
	def __init__(self):
		super().__init__()
		time_now = datetime.datetime.now()
		time_string = time_now.strftime("Unigames @ %d/%m/%Y %H:%M")
		time_code = time_now.strftime("%Y%m%d-%H%M")
		for i in range(len(UNIGAMES_CAMERAS)):
			camera = UNIGAMES_CAMERAS[i]
			camera_embed = discord.Embed(title=time_string)
			camera_embed.set_image(url=f"https://webcam.ucc.asn.au/archive.php?camera={camera}&timestamp={time_code}")
			self.add_item(EmbedPaginatorButton(label=str(i+1), embed=camera_embed, starting=(i == 0)))
		self.current_camera = 0

	def get_current_embed(self):
		return self.children[self.current_camera].embed


class JokeWebcamView(discord.ui.View):
	children: [EmbedPaginatorButton]

	def __init__(self):
		super().__init__()


client = LichClient()







# @client.tree.command(description="Get a random rule for seeing who goes first in your game!")
# async def starting_rule(interaction: discord.Interaction):
# 	rule = get_random_starting_rule(interaction.user.display_name)
# 	await interaction.response.send_message(f'Starting rule: {rule}', view=RerollStartingRuleView())


@client.tree.command(description="Show how to get to the Unigames clubroom!")
async def gavin(interaction: discord.Interaction):
	await interaction.response.send_message('Delegated. (coming soon)')

@client.tree.command(description="Take a look at what's happening in the clubroom right now!")
async def webcams(interaction: discord.Interaction):
	switcher_view = WebcamSwitcherView()
	camera_embed = switcher_view.get_current_embed()
	await interaction.response.send_message(embed=camera_embed, view=switcher_view)


# @client.tree.command(description="Set the status of the bot.")
# async def status(interaction: discord.Interaction, status_text: str):
# 	game = discord.Game(name=status_text)
# 	await client.change_presence(status=discord.Status.online, activity=game)
# 	await interaction.response.send_message('Status changed.', ephemeral=True, delete_after=10)

if __name__ == "__main__":
	try:
		secret = get_docker_secret('discord_bot_secret', safe=False)
	except (TypeError, ValueError):
		with open('secret', 'r') as f:
			secret = f.read()
	client.run(secret)
