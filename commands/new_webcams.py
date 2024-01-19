import discord
from discord import ui, Interaction
import asyncio


DONALD_ID = 243405584651517954


def check_if_its_me(interaction: discord.Interaction):
	return interaction.user.id == DONALD_ID


class InputBox(ui.Modal, title="Enter Webcam Password:"):
	password = ui.TextInput(label="Webcam Password", style=discord.TextStyle.short)

	async def on_submit(self, interaction: Interaction) -> None:
		await interaction.response.defer(ephemeral=False, thinking=True)
		await asyncio.sleep(5)
		await interaction.followup.send(f"Success! The password was {self.password}")


@discord.app_commands.command(description="Testing the new webcam commands.")
@discord.app_commands.guild_only()
@discord.app_commands.check(check_if_its_me)
async def test_new_webcams(interaction: discord.Interaction):
	await interaction.response.send_modal(InputBox())


async def setup(bot):
	bot.tree.add_command(test_new_webcams)
