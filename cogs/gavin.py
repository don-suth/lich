import discord
from discord import app_commands
from discord.ext import commands


class ClubroomCog(commands.GroupCog, group_name="clubroom"):
	@app_commands.command(description="Let us guide you to Unigames from the Tav!")
	async def tav(self, interaction: discord.Interaction):
		await interaction.response.send_message(
			"Follow us from the Tav!\nhttps://www.youtube.com/watch?v=ufswr_-B3tA"
		)

	@app_commands.command(description="Let us guide you to Unigames from the Guild Village!")
	async def guild_village(self, interaction: discord.Interaction):
		await interaction.response.send_message(
			"Follow us from the Guild Village!\nhttps://www.youtube.com/watch?v=O0SrGr8TwBU"
		)

	async def cog_load(self):
		print(f"\t - {self.__class__.__name__} loaded")

	async def cog_unload(self):
		print(f"\t - {self.__class__.__name__} unloaded")


class OldGavinCog(commands.GroupCog, group_name="old_gavin"):
	@app_commands.command(
		description="(Outdated) Let Gavin guide you to Unigames from the Tav!"
	)
	async def tav(self, interaction: discord.Interaction):
		await interaction.response.send_message(
			"Follow Gavin from the Tav!\nhttps://www.youtube.com/watch?v=sg4XJG8HGTw"
		)

	@app_commands.command(
		description="(Outdated) Let Gavin guide you to Unigames from the middle of Guild Village!"
	)
	async def guild_village(self, interaction: discord.Interaction):
		await interaction.response.send_message(
			"Follow Gavin from Guild Village!\nhttps://www.youtube.com/watch?v=Jaw6zF5cB7Q"
		)

	async def cog_load(self):
		print(f"\t - {self.__class__.__name__} loaded")

	async def cog_unload(self):
		print(f"\t - {self.__class__.__name__} unloaded")


async def setup(bot: commands.Bot):
	await bot.add_cog(ClubroomCog(bot=bot))
	await bot.add_cog(OldGavinCog(bot=bot))
