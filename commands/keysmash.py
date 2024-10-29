import discord
from discord import app_commands
from discord.ext import commands
from password_calculator import password_calculator
import string


async def is_valid_keysmash(keysmash):
	# We don't want to get too bogged down - max length is 200 - restricted to standard keyboard symbols only.
	if len(keysmash) > 200:
		return False
	if len(keysmash) == 0:
		return False
	for char in keysmash:
		if char not in string.printable:
			return False
	return True


class KeysmashCog(commands.Cog):
	@app_commands.context_menu(name="Evaluate Keysmash")
	async def evaluate_keysmash(self, interaction: discord.Interaction, message: discord.Message):
		# Evaluates a string and estimates how long it would take to crack it if you used it as your password.
		# This uses a long JS function converted into python. See password_calculator.py for more info.
		keysmash = message.content
		valid = await is_valid_keysmash(keysmash)
		if valid:
			keysmash_data = password_calculator.zxcvbn(keysmash)
			time_to_crack = password_calculator.toWords(keysmash_data['crack_time'])
			time_to_crack = time_to_crack.replace('  ', ' ')
			bonus = ""
			if keysmash_data['crack_time'] > 32000000000:
				bonus = f"\n*(Nice keysmash {message.author.display_name})*"
			await interaction.response.send_message(
				f'It would take `{time_to_crack}` to crack `{keysmash}` if you used it as your password.{bonus}'
			)
		else:
			await interaction.response.send_message(
				"I can't evaluate that message, as it is either too long, too short, or contains non-standard symbols.",
				ephemeral=True
			)

	async def cog_load(self):
		print(f"\t - {self.__class__.__name__} loaded")

	async def cog_unload(self):
		print(f"\t - {self.__class__.__name__} unloaded")


async def setup(bot: commands.Bot):
	await bot.add_cog(KeysmashCog(bot=bot))
