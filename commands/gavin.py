import discord


class GavinGroup(discord.app_commands.Group):
	@discord.app_commands.command(description="Let Gavin guide you to Unigames from the Tav!")
	async def tav(self, interaction: discord.Interaction):
		await interaction.response.send_message("Follow Gavin from the Tav!\nhttps://www.youtube.com/watch?v=sg4XJG8HGTw")

	@discord.app_commands.command(description="Let Gavin guide you to Unigames from the middle of Guild Village!")
	async def guild_village(self, interaction: discord.Interaction):
		await interaction.response.send_message("Follow Gavin from Guild Village!\nhttps://www.youtube.com/watch?v=Jaw6zF5cB7Q")


async def setup(bot):
	bot.tree.add_command(GavinGroup(name="gavin", description="Let Gavin guide you to Unigames..."))
