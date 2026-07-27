import discord
from discord.ext import commands, tasks
import asyncio
import random

from views.apply_view import ApplyButton
from views.embassy_view import EmbassyButton

from config import TOKEN


intents = discord.Intents.default()

intents.message_content = True
intents.members = True
intents.reactions = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


ROMAN_STATUS = [
    "Guarding the citizens of Rome",
    "Watching over the Eternal City",
    "Protecting Rome from its enemies",
    "Guiding the Empire towards glory",
    "My shield guards the Roman people",
    "Standing beside the Roman legions",
    "Watching over Roman lands",
    "Bringing honour to the Empire",
    "Defending the glory of Rome",
    "Blessing the citizens of the Empire",
    "I stand eternal as Rome's guardian"
]


@tasks.loop(minutes=5)
async def roman_presence():

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(
            random.choice(ROMAN_STATUS)
        )
    )



COGS = [
    "cogs.main_welcome",
    "cogs.fa_welcome",
    "cogs.apply_system",
    "cogs.embassy_system",
    "cogs.reaction_roles",
    "cogs.giveaway",
    "cogs.reminders",
    "cogs.colosseum",
    "cogs.interview",
]



async def load_cogs():

    for cog in COGS:

        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded {cog}")

        except Exception as e:
            print(f"❌ Failed {cog}: {e}")



@bot.event
async def setup_hook():

    await load_cogs()

    bot.add_view(
        ApplyButton()
    )

    bot.add_view(
        EmbassyButton()
    )


    synced = await bot.tree.sync()

    print(
        f"Synced {len(synced)} commands"
    )



@bot.event
async def on_ready():

    print(
        f"Logged in as {bot.user}"
    )


    if not roman_presence.is_running():

        roman_presence.start()



async def main():

    async with bot:

        await bot.start(
            TOKEN
        )


asyncio.run(main())