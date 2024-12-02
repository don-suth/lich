import random
import discord

prefixes = ['Sedge', 'Spider', 'Beech', 'Mottle', 'Wigeon', 'Shrew', 'Swan', 'Daisy', 'Duck', 'Poppy', 'Soot', 'Stoat', 'Dunlin', 'Minnow', 'Mist', 'Tip', 'Crow', 'Leopard', 'Marigold', 'Beetle', 'Skipper', 'Barley', 'Swift', 'Russet', 'Gannet', 'Grouse', 'Heather', 'Thyme', 'Brambling', 'Quail', 'Chanterelle', 'Lizard', 'Dove', 'Nettle', 'Leech', 'Willow', 'Ant', 'Burdock', 'Vole', 'Fox', 'Swallow', 'Blue', 'Frost', 'Hemlock', 'Juniper', 'Fennel', 'Fir', 'Bittern', 'Wasp', 'Sloe', 'Asphodel', 'Nightingale', 'Pipit', 'Dawn', 'Speckle', 'Fallow', 'Bee', 'Rat', 'Oat', 'Eagle', 'Eel', 'Dapple', 'Light', 'Carp', 'Rye', 'Comfrey', 'Tiger', 'Thistle', 'Briar', 'Campion', 'Elder', 'Comma', 'Elm', 'Hornet', 'Brown', 'Wren', 'Fleck', 'Alder', 'Yew', 'Tawny', 'Rowan', 'Whimbrel', 'Pigeon', 'Muntjac', 'Vervain', 'Badger', 'Sparrow', 'Tern', 'Mistletoe', 'Burnet', 'Lily', 'Sheep', 'Hazel', 'Bramble', 'Mud', 'Harrier', 'Rush', 'Linnet', 'Toad', 'Nerite', 'Marten', 'Gudgeon', 'Martin', 'Lion', 'Plum', 'Black', 'Night', 'Orchid', 'Goose', 'Pike', 'Smoke', 'Cormorant', 'Bright', 'Holly', 'Mallow', 'Teasel', 'Laburnum', 'Dark', 'Reed', 'Gorse', 'Grey', 'Pale', 'Privet', 'Pebble', 'Rudd', 'Blizzard', 'Cinder', 'Shadow', 'Silver', 'White', 'Fog', 'Rabbit', 'Cedar', 'Whinchat', 'Fawn', 'Argus', 'Lamprey', 'Adder', 'Boulder', 'Slug', 'Morning', 'Magpie', 'Kite', 'Dust', 'Otter', 'Wisteria', 'Lavender', 'Mink', 'Yarrow', 'Hare', 'Aster', 'Chervil', 'Stone', 'Mint', 'Cloud', 'Pheasant', 'Garlic', 'Trout', 'Lark', 'Sand', 'Pear', 'Godwit', 'Curlew', 'Gull', 'Gadwall', 'Dandelion', 'Roach', 'Cypress', 'Twite', 'Falcon', 'Bream', 'Avocet', 'Partridge', 'Heron', 'Egret', 'Pochard', 'Moth', 'Red', 'Loach', 'Sorrel', 'Limpet', 'Hail', 'Knot', 'Bat', 'Patch', 'Shell', 'Dace', 'Wax', 'Spotted', 'Dunnock', 'Dipper', 'Oak', 'Fritillary', 'Golden', 'Raven', 'Snake', 'Mouse', 'Murk', 'Aspen', 'Brindle', 'Squirrel', 'Lichen', 'Evening', 'Sage', 'Loon', 'Kestrel', 'Starling', 'Robin', 'Cuckoo', 'Weevil', 'Dusk', 'Small', 'Clover', 'Rain', 'Apple', 'Valerian', 'Rook', 'Honey', 'Ginger', 'Daffodil', 'Snail', 'Little ', 'Mosquito', 'Yellow', 'Sycamore', 'Acorn', 'Tiny ', 'Frog', 'Crane', 'Fumitory', 'Sleet', 'Thrush', 'Weasel', 'Thrift', 'Copper', 'Ember', 'Storm', 'Cherry', 'Pansy', 'Tansy', 'Snow ', 'Fly', 'Laurel', 'Shrike', 'Deer', 'Larch', 'Rail', 'Bleak', 'Ivy', 'Owl', 'Diver', 'Birch', 'Maple', 'Newt', 'Ash', 'Salmon', 'Jay', 'Chub', 'Poplar', 'Buzzard', 'Mole', 'Shade', 'Fire', 'Rose', 'Ice ', 'Rock', 'Pine', 'Plover', 'Coot', 'Lightning']
suffixes = ['Claw', 'Cloud', 'Ear', 'Eye', 'Face', 'Fang', 'Flower', 'Foot', 'Fur', 'Heart', 'Jaw', 'Leaf', 'Nose', 'Pelt', 'Step', 'Storm', 'Stream', 'Stripe', 'Tail', 'Whisker']


async def get_warriorcat_name():
	pre = random.choice(prefixes)
	suf = random.choice(suffixes)
	warriorcat_name = f'{pre}{suf}'.title()
	return warriorcat_name


@discord.app_commands.command(description="Generate a random Warrior Cat name. Results may vary.")
async def warriorcat(interation: discord.Interaction):
	warriorcat_name = await get_warriorcat_name()
	await interation.response.send_message(f'Your Warrior Cat name is: {warriorcat_name}')


async def setup(bot):
	bot.tree.add_command(warriorcat)
