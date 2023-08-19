import random
import discord
import asyncio
from aiohttp import ClientSession
import os

API_ACCESS = os.environ.get('API_ACCESS', 'http://127.0.0.1:8000/api')
LICH_DEBUG = os.environ.get('LICH_DEBUG', 'FALSE')


async def random_boardgame():
	async with ClientSession() as session:
		response = await session.request(
			method="GET",
			url=API_ACCESS + "/items/random/boardgame",
			timeout=20.0
		)
		json = await response.json()
	return json['name']


async def random_cardgame():
	async with ClientSession() as session:
		response = await session.request(
			method="GET",
			url=API_ACCESS + "/items/random/cardgame",
			timeout=20.0
		)
		json = await response.json()
	return json['name']


async def evaluate_callable(potential_callable):
	# Helper function - if the argument is a callable it calls it and returns the result
	# Otherwise it just returns the argument again
	if callable(potential_callable):
		return await potential_callable()
	return potential_callable

# Character limit  is about this V much:
# Playing not Dungeons & Dragons |
# Running in DEBUG mode

STATUS_CHOICES = [
	('playing',         'with my new dice'),
	('playing',         'a Paranoia one-shot'),
	('playing',         'a 5-player EDH game'),
	('playing', 		'a 13th Age campaign'),
	('playing', 		'a Smithy; +3 cards'),
	('playing', 		'a Counterspell.'),
	('playing',			'three Wild Magics!!!'),
	('playing',			'not Dungeons & Dragons'),
	('playing',			'[REDACTED]'),
	('playing',			random_boardgame),
	('playing',			random_cardgame),
	('watching',        'the webcams 👁️'),
	('watching',        'my minis dry'),
	('watching',        'board game reviews'),
	('watching',        'the OGM liveblog'),
	('watching', 		'for the Imposter'),
	('watching',		'for Trouble'),
	('watching',		'for Communists'),
	('watching',		'for Mutants'),
	('watching',		'for Secret Societies'),
	('watching',		'the Committee closely'),
	('listening to',    'Vengabus.'),
	('listening to',    'the Tav noise'),
	('listening to',	'a Committee meeting'),
	('listening to',	'the Ultra Violets'),
	('custom',			'Removing seconds'),
	('custom',			'Amending the constitution'),
	('custom',			'Not touching the money box'),
	('custom',			'Trying to pick a game to play'),
	('custom',			'Seconding'),
	('custom',			'Probably running an event'),
	('custom',			'Embarrassed with Babish'),  # Emoji ID: 1008040626723491871
	('custom',			'Battling with Scryfall'),
	('custom',			'Keen for Roleplay4Life'),
	('custom',			'Drafting'),
	('custom',			'Making up starting rules'),
	('custom',			'Vaporising traitors'),
	('custom',			'Sipping on Vonk'),
	('custom',			'Morbing'),
	('custom',			'Trans rights!!'),
]


async def change_status(discord_client):
	while True:
		activity = await get_random_status_choice(discord_client)
		await discord_client.change_presence(activity=activity)
		if LICH_DEBUG == 'FALSE':
			await asyncio.sleep(60*20)
		else:
			await asyncio.sleep(10)


def check_for_special_status():
	# This function will check for certain conditions,
	# and guarantee a certain status if those conditions are met.
	special_status = None
	if LICH_DEBUG == 'TRUE':
		# Custom status for debug mode
		special_status = ('custom', 'Running in DEBUG mode')
	return special_status


async def get_random_status_choice(discord_client):
	status = check_for_special_status()
	if status is None:
		status = random.choice(STATUS_CHOICES)
	activity = None
	match status:
		case ('playing', activity_name):
			activity = discord.Game(await evaluate_callable(activity_name))
		case ('watching', activity_name):
			activity = discord.Activity(type=discord.ActivityType.watching, name=await evaluate_callable(activity_name))
		case ('listening to', activity_name):
			activity = discord.Activity(type=discord.ActivityType.listening, name=await evaluate_callable(activity_name))
		case ('streaming', activity_name):
			activity = discord.Streaming(name=await evaluate_callable(activity_name), url='twitch.tv/uwaunigames')
		case ('custom', custom_status, emoji):
			activity_name = await evaluate_callable(custom_status)
			emoji = discord_client.get_emoji(emoji)
			activity = discord.CustomActivity(name=activity_name, state=activity_name, emoji=emoji)
		case ('custom', custom_status):
			activity_name = await evaluate_callable(custom_status)
			activity = discord.CustomActivity(name=activity_name, state=activity_name)

	return activity
