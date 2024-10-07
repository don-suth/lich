import discord
from discord import ui, Interaction


class ChannelInputModal(ui.Modal, title="Enter channel ID:"):
	channel_id = ui.TextInput(label="Enter Channel ID:")

	def __init__(self, *args, relay_message, **kwargs):
		super().__init__(*args, **kwargs)
		self.relay_message = relay_message

	async def on_submit(self, interaction: Interaction) -> None:
		try:
			relay_channel_id = int(f"{self.channel_id}")
		except ValueError:
			return
		channel = interaction.client.get_channel(relay_channel_id)
		await channel.send(self.relay_message)
		await interaction.response.send_message("Sent message", ephemeral=True)


@discord.app_commands.context_menu(name="Relay Message")
@discord.app_commands.guild_only()
async def relay(interaction: discord.Interaction, message: discord.Message):
	relay_message = message.content
	await interaction.response.send_modal(ChannelInputModal(relay_message=relay_message))


async def setup(bot):
	bot.tree.add_command(relay)
