import random

activities = [
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
]

colours = [
	'white', 'blue', 'black', 'red', 'green', 'purple', 'grey', 'yellow', 'orange', 'pink', 'brown'
]

objects = [
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
]

directions = [
	'north', 'south', 'east', 'west',
	'northeast', 'northwest', 'southeast', 'southwest'
]

dice = [
	'a d20', 'a d100', '4d6 and drops the lowest',
	'a d6', 'a d12', 'a d8', 'a d10',
]

rules = [
	'The player with the longest hair',
	'The player with the shortest hair',
	'The player with the most elvish looking ears',
	'The player with the biggest hands',
	'The player with the smallest hands',
	'The oldest player',
	'The youngest player',
	'The player with the age closest to the average'
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
	'The player furthest to the {direction}'
]

def get_random_starting_rule(user):
	base_rule = random.choice(rules)
	base_rule += ' goes first!'
	final_rule = None
	if '{colour}' in base_rule:
		random_colour = random.choice(colours)
		final_rule = base_rule.replace('{colour}', random_colour)
	elif '{object}' in base_rule:
		random_object = random.choice(objects)
		final_rule = base_rule.replace('{object}', random_object)
	elif '{activity}' in base_rule:
		random_activity = random.choice(activities)
		final_rule = base_rule.replace('{activity}', random_activity)
	elif '{dice}' in base_rule:
		random_dice = random.choice(dice)
		final_rule = base_rule.replace('{dice}', random_dice)
	elif '{direction}' in base_rule:
		random_direction = random.choice(directions)
		final_rule = base_rule.replace('{direction}', random_direction)
		final_rule += "\n*(If you're in Unigames, then the wall with the windows is north)*"
	elif '{user}' in base_rule:
		final_rule = base_rule.replace('{user}', user)
	else:
		final_rule = base_rule

	return final_rule
