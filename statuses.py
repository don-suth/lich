import random
import discord
import asyncio


STATUS_CHOICES = [
	('playing',         'with my new dice'),
	('playing',         'a TTRPG'),
	('playing',         'a 5-player EDH game'),
	('watching',        'the webcams 👁️'),
	('watching',        'my minis dry'),
	('watching',        'board game reviews'),
	('watching',        'the OGM liveblog'),
	('listening to',    'Vengabus.'),
	('listening to',    'the Tav noise'),
]


async def change_status(discord_client):
	while True:
		activity = get_random_status_choice()
		await discord_client.change_presence(activity=activity)
		await asyncio.sleep(5)


def get_random_status_choice():
	choice = random.choice(STATUS_CHOICES)
	activity = None
	if choice[0] == 'playing':
		activity = discord.Game(choice[1])
	if choice[0] == 'watching':
		activity = discord.Activity(type=discord.ActivityType.watching, name=choice[1])
	if choice[0] == 'listening to':
		activity = discord.Activity(type=discord.ActivityType.listening, name=choice[1])
	if choice[0] == 'streaming':
		activity = discord.Streaming(name=choice[0], url='twitch.tv/uwaunigames')
	return activity

