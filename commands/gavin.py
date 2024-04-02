import discord


class ClubroomGroup(discord.app_commands.Group):
	@discord.app_commands.command(description="Let us guide you to Unigames from the Tav!")
	async def tav(self, interaction: discord.Interaction):
		await interaction.response.send_message("Follow us from the Tav!\nhttps://www.youtube.com/watch?v=ufswr_-B3tA")

	@discord.app_commands.command(description="Let us guide you to Unigames from the Guild Village!")
	async def guild_village(self, interaction: discord.Interaction):
		await interaction.response.send_message("Follow us from the Guild Village!\nhttps://www.youtube.com/watch?v=O0SrGr8TwBU")


class OldGavinGroup(discord.app_commands.Group):
	@discord.app_commands.command(description="(Outdated) Let Gavin guide you to Unigames from the Tav!")
	async def tav(self, interaction: discord.Interaction):
		await interaction.response.send_message(
			"Follow Gavin from the Tav!\nhttps://www.youtube.com/watch?v=sg4XJG8HGTw")

	@discord.app_commands.command(description="(Outdated) Let Gavin guide you to Unigames from the middle of Guild Village!")
	async def guild_village(self, interaction: discord.Interaction):
		await interaction.response.send_message(
			"Follow Gavin from Guild Village!\nhttps://www.youtube.com/watch?v=Jaw6zF5cB7Q")


async def setup(bot):
	bot.tree.add_command(OldGavinGroup(name="old_gavin", description="(Outdated) Let Gavin guide you to Unigames..."))
	bot.tree.add_command(ClubroomGroup(name="clubroom", description="Let us guide you to the Unigames clubroom..."))
