import discord


class EmbedPaginatorButton(discord.ui.Button):
	def __init__(self, label, embed, starting=False):
		super().__init__(label=label)
		self.embed = embed
		if starting is True:
			self.style = discord.ButtonStyle.primary
		else:
			self.style = discord.ButtonStyle.secondary

	async def callback(self, interaction: discord.Interaction):
		for child in self.view.children:
			child.style = discord.ButtonStyle.secondary
		self.style = discord.ButtonStyle.primary
		await interaction.response.edit_message(embed=self.embed, view=self.view)
