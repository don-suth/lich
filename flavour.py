import asyncio
from aiohttp import ClientSession
import re

random_cards_queue = asyncio.Queue(maxsize=10)


async def fill_random_card_cache():
    while True:
        while not random_cards_queue.full():
            flavour_text = await get_random_flavour()
            if flavour_text is not None:
                await random_cards_queue.put(flavour_text)
                print("Put flavour text in queue:", flavour_text, f"[{random_cards_queue.qsize()}]")
                await asyncio.sleep(0.1)
        await asyncio.sleep(10)


def format_flavour_text(flavour):
    # Add asterisks to the start and end of the text.
    flavour = '*' + flavour + '*'
    # Replace pairs of asterisks with only whitespace between them.
    pattern = re.compile(r'\*\s*\*')
    flavour = pattern.sub('', flavour)
    # If an asterisk appears after whitespace, also put one after it.
    pattern = re.compile(r'\s\*')
    flavour = pattern.sub('* ', flavour)
    return flavour


async def get_random_flavour():
    url = 'https://api.scryfall.com/cards/random?q=ft%3A%2F%5E.%2B%2F'
    json = {}
    async with ClientSession() as session:
        try:
            response = await session.request(method="GET", url=url, timeout=20.0)
            json = await response.json()
        except asyncio.exceptions.TimeoutError:
            print("Timed out.")
    flavour_text = json.get("flavor_text", None)
    if flavour_text:
        return format_flavour_text(flavour_text)
    else:
        return None


async def pull_random_flavour():
    flavour_text = await random_cards_queue.get()
    return flavour_text
