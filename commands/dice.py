import discord
import d20


async def roll_dice(expression):
	error = False
	try:
		dice_result = str(d20.roll(expression))
	except d20.errors.RollSyntaxError as e:
		dice_result = \
			f"There was an error in rolling your dice: \n" \
			f"```Unexpected input on line {e.line}, col {e.col}\n" \
			f"{expression}\n" \
			f"{' '*(e.col-1)}^\n" \
			f"Expected {e.expected}, got {e.got}.```"
		error = True
	except d20.errors.TooManyRolls:
		dice_result = \
			f"There was an error in rolling your dice: \n" \
			f"```Too many dice were rolled. Please choose an expression that will roll less dice.```"
		error = True
	except d20.errors.RollError:
		dice_result = \
			f"There was an unknown error in rolling your dice. Please alter your expression and try again."
		error = True
	return dice_result, error


async def get_help():
	help_text = \
		"Basic Syntax:\n" \
		"`[X]d[Y]` rolls X Y-sided dice.\n" \
		"Supports basic arithmatic. e.g. `1d20+4`\n" \
		"Modifiers can be appended to alter dice-rolling behaviour.\n\n" \
		"Examples:\n" \
		"`1d20 + 4` : Rolls a d20 and adds 4.\n" \
		"`8d6` : Rolls 4d6 and sums them.\n" \
		"`4d6dl1` : Rolls 4d6 and [d]rops the [l]owest [1] dice.\n" \
		"`4d6kh3` : Rolls 4d6 and [k]eeps the [h]ighest [3] dice. \n" \
		"`3d10e10` : Rolls 3d10 and [e]xplodes any 10s rolled.\n\n" \
		"For full syntax, see https://d20.readthedocs.io/en/latest/start.html#dice-syntax"
	return help_text


@discord.app_commands.command(description="Roll some dice! See syntax by using 'help' as your expression.")
async def roll(interaction: discord.Interaction, expression: str):
	if expression.lower() == 'help':
		dice_result = await get_help()
		error = True
	else:
		dice_result, error = await roll_dice(expression)
	await interaction.response.send_message(dice_result, ephemeral=error)


async def setup(bot):
	bot.tree.add_command(roll)
