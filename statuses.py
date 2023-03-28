import random
import discord
import asyncio


STATUS_CHOICES = [
	('playing',         'with my new dice'),
	('playing',         'a Paranoia one-shot'),
	('playing',         'a 5-player EDH game'),
	('playing', 		'a 13th Age campaign'),
	('playing', 		'a Smithy; +3 cards'),
	('playing', 		'a Counterspell.'),
	('playing',			'three Wild Magics!!!'),
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
		activity = get_random_status_choice()
		await discord_client.change_presence(activity=activity)
		await asyncio.sleep(60*10)


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

