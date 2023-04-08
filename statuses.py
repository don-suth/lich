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


STATUS_CHOICES = [
	('playing',         'with my new dice'),
	('playing',         'a Paranoia one-shot'),
	('playing',         'a 5-player EDH game'),
	('playing', 		'a 13th Age campaign'),
	('playing', 		'a Smithy; +3 cards'),
	('playing', 		'a Counterspell.'),
	('playing',			'three Wild Magics!!!'),
	('playing',			'not Dungeons & Dragons'),
	('playing',			random_boardgame),
	('playing',			random_cardgame),
	('watching',        'the webcams 👁️'),
	('watching',        'my minis dry'),
	('watching',        'board game reviews'),
	('watching',        'the OGM liveblog'),
	('watching', 		'for the Imposter'),
	('listening to',    'Vengabus.'),
	('listening to',    'the Tav noise'),
	('listening to',	'a Committee meeting'),
]


async def change_status(discord_client):
	while True:
		activity = await get_random_status_choice()
		await discord_client.change_presence(activity=activity)
		if LICH_DEBUG == 'FALSE':
			await asyncio.sleep(60*20)
		else:
			await asyncio.sleep(10)


async def get_random_status_choice():
	choice = random.choice(STATUS_CHOICES)
	if callable(choice[1]):
		activity_name = await choice[1]()
	else:
		activity_name = choice[1]
	activity = None
	if choice[0] == 'playing':
		activity = discord.Game(activity_name)
	if choice[0] == 'watching':
		activity = discord.Activity(type=discord.ActivityType.watching, name=activity_name)
	if choice[0] == 'listening to':
		activity = discord.Activity(type=discord.ActivityType.listening, name=activity_name)
	if choice[0] == 'streaming':
		activity = discord.Streaming(name=activity_name, url='twitch.tv/uwaunigames')
	return activity

