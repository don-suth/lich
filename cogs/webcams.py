import discord
from discord import app_commands
from discord.ext import commands


@app_commands.guild_only()
class WebcamsCog(commands.Cog):

	@app_commands.command(description="Deprecated")
	async def webcams(self, interaction: discord.Interaction):
		await interaction.response.send_message(
			"The Webcams are no longer viewable due to UWA Student Guild regulations. "
			"If you have further questions, please contact Committee.",
			ephemeral=True
		)

	async def cog_load(self):
		print(f"\t - {self.__class__.__name__} loaded")

	async def cog_unload(self):
		print(f"\t - {self.__class__.__name__} unloaded")


async def setup(bot: commands.Bot):
	await bot.add_cog(WebcamsCog(bot=bot))
