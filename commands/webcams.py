import discord

@discord.app_commands.command(description="Deprecated")
@discord.app_commands.guild_only()
async def webcams(interaction: discord.Interaction):
	await interaction.response.send_message("The Webcams are no longer viewable due to UWA Student Guild regulations. If you have further questions, please contact Committee.", ephemeral=True)

async def setup(bot):
	bot.tree.add_command(webcams)
