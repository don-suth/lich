import discord
from discord import app_commands
from discord.ext import commands


class DoorCog(commands.GroupCog, group_name="door"):
	@app_commands.default_permissions()
	@app_commands.command(description="Open the clubroom")
	async def open(self, interaction: discord.Interaction):
		await interaction.response.send_message("OPEN!", ephemeral=True)

	@app_commands.default_permissions()
	@app_commands.command(description="Close the clubroom")
	async def close(self, interaction: discord.Interaction):
		await interaction.response.send_message("CLOSE!", ephemeral=True)

	async def cog_load(self):
		print(f"\t - {self.__class__.__name__} loaded")

	async def cog_unload(self):
		print(f"\t - {self.__class__.__name__} unloaded")


async def setup(bot: commands.Bot):
	await bot.add_cog(DoorCog(bot=bot))
