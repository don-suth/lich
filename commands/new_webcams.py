import discord
from discord import ui, Interaction


DONALD_ID = 243405584651517954


def check_if_its_me(interaction: discord.Interaction):
	return interaction.user.id == DONALD_ID


class InputBox(ui.Modal, title="Enter Webcam Password:"):
	password = ui.TextInput(label="Webcam Password", style=discord.TextStyle.short)

	async def on_submit(self, interaction: Interaction) -> None:
		await interaction.response.send_message(f"The password you entered was {self.password}", ephemeral=True)

@discord.app_commands.command(description="Testing the new webcam commands.")
@discord.app_commands.guild_only()
@discord.app_commands.check(check_if_its_me)
async def test_new_webcams(interaction: discord.Interaction):
	await interaction.response.send_modal(InputBox())


async def setup(bot):
	bot.tree.add_command(test_new_webcams)
