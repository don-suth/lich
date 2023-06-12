import random
import discord

fields = {
	'{activities}' : [
		'bought something from the Unigames clubroom',
		'been sick',
		'watered a plant',
		'left the state',
		'entered the state',
		'had a haircut',
		'been swimming',
		'finished a shift at work',
		'watched a full movie',
		'woken up',
		'ate something',
		'had a drink of water',
		'listened to music',
	],
	'{colours}' : [
		'white', 'blue', 'black', 'red', 'green', 'purple', 'grey', 'yellow', 'orange', 'pink', 'brown'
	],
	'{objects}' : [
		'a Magic: the Gathering card',
		'a non-Magic: the Gathering trading card',
		'a fruit',
		'a vegetable',
		'some dice',
		'a pencil',
		'a stapler',
		'a calculator',
		'a USB drive',
		'some kind of hot beverage',
		'a miniature',
		'some kind of hot food',
	],
	'{directions}' : [
		'north', 'south', 'east', 'west',
		'northeast', 'northwest', 'southeast', 'southwest'
	],
	'{dice}' : [
		'a d20', 'a d100', '4d6 and drops the lowest',
		'a d6', 'a d12', 'a d8', 'a d10',
	],
}

rules = [
	'The player with the longest hair',
	'The player with the shortest hair',
	'The player with the most elvish looking ears',
	'The player with the biggest hands',
	'The player with the smallest hands',
	'The oldest player',
	'The youngest player',
	'The player with the age closest to the average',
	'The player that looks the oldest (decide as a group)',
	'The player that looks the youngest (decide as a group)',
	'The player that is wearing the most {colour}',
	'The player that has most recently held {object}',
	'The player that has most recently bought {object}',
	'The player that has most recently {activity}',
	'Each player rolls {dice}. The highest total',
	'Each player rolls {dice}. The lowest total',
	'The player immediately to the left of {user}',
	'The player immediately to the right of {user}',
	'The player furthest to the {direction}',
]


class RerollStartingRuleView(discord.ui.View):
	@discord.ui.button(label='That rule is lame. Give me another one!', style=discord.ButtonStyle.blurple)
	async def reroll(self, interaction: discord.Interaction, button: discord.ui.Button):
		new_rule = get_random_starting_rule(interaction.user.display_name)
		await interaction.response.edit_message(content=new_rule)


def get_random_starting_rule(user):
	rule = random.choice(rules)
	rule += ' goes first!'

	if '{direction}' in rule:
		rule += "\n*(If you're in Unigames, then the wall with the windows is north)*"

	if '{user}' in rule:
		rule = rule.replace('{user}', user)

	for field, options in fields:
		if field in rule:
			option = random.choice(options)
			rule = rule.replace(field, option)

	return rule


@discord.app_commands.command(description="Get a random rule for seeing who goes first in your game!")
async def starting_rule(interaction: discord.Interaction):
	rule = get_random_starting_rule(interaction.user.display_name)
	await interaction.response.send_message(f'Starting rule: {rule}', view=RerollStartingRuleView())


async def setup(bot):
	bot.tree.add_command(starting_rule)
