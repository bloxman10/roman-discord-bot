import discord
from discord.ext import commands
import asyncio

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


COGS = [
    "cogs.main_welcome",
    "cogs.fa_welcome",
    "cogs.apply_system",
    "cogs.embassy_system",
    "cogs.reaction_roles",
    "cogs.giveaway",
    "cogs.reminders",
    "cogs.colosseum",
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


async def main():

    async with bot:

        await bot.start(
            TOKEN
        )


asyncio.run(main())