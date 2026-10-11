import discord
from discord import app_commands
from discord.ext import commands

class ZapCog(commands.Cog):
    """
    The vision:
        1) Unigames member says something worthy of being shot at by a laz-gun.
        2) Right click on message -> Zap
        3) Enter reason
        4) Sent to me for approval + bot reacts with an Eye emoji.
        5) If approved:
            Bot will increment counter based on user ID
            Bot will post a message: "<user> has been executed/zapped/terminated for <reason>. Clones remaining: <number."
            Optional promotion of reporter?
        6) If declined, user is instead zapped (or demoted?).
    - Charity donations for extra clones
    - If member hits 0 clones and is zapped again, idk.
    """
    pass
