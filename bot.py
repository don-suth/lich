import discord
from discord import app_commands
from flavour import pull_random_flavour, fill_random_card_cache
from warriorcat import get_warriorcat_name
from dice import roll_dice, get_help
import asyncio

guilds = []
with open('guilds') as guild_file:
    for line in guild_file.readlines():
        guilds.append(discord.Object(id=line.rstrip('\n')))


class LichClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.random_card_task = None
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        for guild in guilds:
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

    async def on_ready(self):
        print(f'Logged in as {client.user} (ID: {client.user.id})')
        print('------')
        print('Populating flavour text cache')
        if self.random_card_task is None:
            self.random_card_task = asyncio.create_task(fill_random_card_cache())


client = LichClient()


@client.tree.command(description="Returns a random flavour text from Magic the Gathering. See if you can guess the card!")
async def flavour(interaction: discord.Interaction):
    flavour_text = await pull_random_flavour()
    await interaction.response.send_message(flavour_text)


@client.tree.command(description="Generate a random Warrior Cat name. Results may vary.")
async def warriorcat(interation: discord.Interaction):
    warriorcat_name = await get_warriorcat_name()
    await interation.response.send_message(f'Your Warrior Cat name is: {warriorcat_name}')


@client.tree.command(description="Roll some dice! See syntax by using 'help' as your expression.")
async def roll(interaction: discord.Interaction, expression: str):
    if expression.lower() == 'help':
        dice_result = await get_help()
        error = True
    else:
        dice_result, error = await roll_dice(expression)
    await interaction.response.send_message(dice_result, ephemeral=error)

if __name__ == "__main__":
    with open('secret', 'r') as f:
        secret = f.read()
    client.run(secret)
