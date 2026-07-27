import discord
import time
import re

from discord.ext import commands
from discord import app_commands

from views.giveaway_view import GiveawayView

from utils.giveaway_manager import (
    add_giveaway,
    get_giveaway,
    remove_giveaway
)


def parse_time(duration: str):

    match = re.match(r"(\d+)([mhd])", duration.lower())

    if not match:
        return None

    amount = int(match.group(1))
    unit = match.group(2)

    if unit == "m":
        return amount * 60

    if unit == "h":
        return amount * 60 * 60

    if unit == "d":
        return amount * 60 * 60 * 24



class Giveaway(commands.GroupCog, name="giveaway"):

    def __init__(self, bot):
        self.bot = bot



    @app_commands.command(
        name="create",
        description="Create a giveaway"
    )
    @app_commands.describe(
        prize="What is the prize?",
        duration="Example: 30m, 2h, 3d",
        winners="Number of winners",
        channel="Where to post the giveaway"
    )
    async def create(
        self,
        interaction: discord.Interaction,
        prize: str,
        duration: str,
        winners: int,
        channel: discord.TextChannel
    ):

        seconds = parse_time(duration)


        if not seconds:

            await interaction.response.send_message(
                "❌ Invalid time format. Use 30m, 2h, 3d",
                ephemeral=True
            )

            return



        end_time = int(time.time()) + seconds


        embed = discord.Embed(
            title="🎉 GIVEAWAY 🎉",
            color=discord.Color.gold()
        )


        embed.add_field(
            name="Prize",
            value=prize,
            inline=False
        )


        embed.add_field(
            name="Hosted by",
            value=interaction.user.mention,
            inline=True
        )


        embed.add_field(
            name="Ends",
            value=f"<t:{end_time}:R>",
            inline=True
        )


        embed.add_field(
            name="Winners",
            value=str(winners),
            inline=True
        )


        embed.add_field(
            name="Entries",
            value="0",
            inline=True
        )


        embed.set_footer(
            text="React using the button below to enter!"
        )


        message = await channel.send(
            embed=embed
        )


        giveaway_data = {

            "message_id": message.id,
            "channel_id": channel.id,
            "guild_id": interaction.guild.id,
            "prize": prize,
            "host_id": interaction.user.id,
            "end_time": end_time,
            "winners": winners,
            "entries": [],
            "ended": False

        }


        add_giveaway(
            giveaway_data
        )


        await message.edit(
            view=GiveawayView(
                message.id
            )
        )


        await interaction.response.send_message(
            "✅ Giveaway created!",
            ephemeral=True
        )



    @app_commands.command(
        name="remove",
        description="Remove a giveaway"
    )
    @app_commands.describe(
        message_id="Giveaway message ID"
    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def remove(
        self,
        interaction: discord.Interaction,
        message_id: str
    ):


        giveaway = get_giveaway(
            int(message_id)
        )


        if not giveaway:

            await interaction.response.send_message(
                "❌ Giveaway not found.",
                ephemeral=True
            )

            return



        try:

            channel = self.bot.get_channel(
                giveaway["channel_id"]
            )

            message = await channel.fetch_message(
                giveaway["message_id"]
            )

            await message.delete()


        except Exception:

            pass



        remove_giveaway(
            int(message_id)
        )


        await interaction.response.send_message(
            "✅ Giveaway removed.",
            ephemeral=True
        )



async def setup(bot):

    await bot.add_cog(
        Giveaway(bot)
    )