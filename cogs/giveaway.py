import discord
import time
import re
import random

from discord.ext import commands, tasks
from discord import app_commands

from views.giveaway_view import GiveawayView

from utils.giveaway_manager import (
    add_giveaway,
    get_giveaway,
    remove_giveaway,
    get_active_giveaways,
    update_giveaway
)



def parse_time(duration: str):

    match = re.match(
        r"(\d+)([mhd])",
        duration.lower()
    )

    if not match:
        return None


    amount = int(match.group(1))
    unit = match.group(2)


    if unit == "m":
        return amount * 60

    if unit == "h":
        return amount * 3600

    if unit == "d":
        return amount * 86400



class Giveaway(commands.GroupCog, name="giveaway"):

    def __init__(self, bot):

        self.bot = bot
        self.check_giveaways.start()



    @app_commands.command(
        name="create",
        description="Create a giveaway"
    )
    @app_commands.describe(
        prize="Giveaway prize",
        duration="Example: 30m, 2h, 3d",
        winners="Number of winners",
        channel="Channel to send giveaway"
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
                "❌ Invalid duration.",
                ephemeral=True
            )

            return



        end_time = int(time.time()) + seconds



        embed = discord.Embed(
            title="🎉 GIVEAWAY 🎉",
            color=discord.Color.gold()
        )


        embed.add_field(
            name="🎁 Prize",
            value=prize,
            inline=False
        )


        embed.add_field(
            name="👑 Host",
            value=interaction.user.mention
        )


        embed.add_field(
            name="⏰ Ends",
            value=f"<t:{end_time}:R>"
        )


        embed.add_field(
            name="🏆 Winners",
            value=str(winners)
        )


        embed.add_field(
            name="👥 Entries",
            value="0"
        )


        embed.set_footer(
            text="Press the button below to enter!"
        )



        message = await channel.send(
            embed=embed
        )



        data = {

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



        add_giveaway(data)



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
        name="list",
        description="List active giveaways"
    )
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def list(
        self,
        interaction: discord.Interaction
    ):


        giveaways = get_active_giveaways()



        if not giveaways:

            await interaction.response.send_message(
                "❌ No active giveaways.",
                ephemeral=True
            )

            return



        embed = discord.Embed(
            title="🎉 Active Giveaways",
            color=discord.Color.gold()
        )


        for giveaway in giveaways:


            embed.add_field(

                name=f"{giveaway['prize']}",

                value=(

                    f"ID: `{giveaway['message_id']}`\n"
                    f"Ends: <t:{giveaway['end_time']}:R>\n"
                    f"Entries: {len(giveaway['entries'])}"

                ),

                inline=False
            )



        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )





    @app_commands.command(
        name="remove",
        description="Remove a giveaway"
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


        except:

            pass



        remove_giveaway(
            int(message_id)
        )



        await interaction.response.send_message(
            "✅ Giveaway removed.",
            ephemeral=True
        )





    @tasks.loop(seconds=15)
    async def check_giveaways(self):


        giveaways = get_active_giveaways()


        now = int(time.time())


        for giveaway in giveaways:


            if giveaway["end_time"] > now:
                continue



            guild = self.bot.get_guild(
                giveaway["guild_id"]
            )


            if not guild:
                continue



            channel = guild.get_channel(
                giveaway["channel_id"]
            )


            if not channel:
                continue



            winners = giveaway["winners"]

            entries = giveaway["entries"]



            if not entries:


                await channel.send(

                    f"🎉 Giveaway ended!\n\n"
                    f"Prize: **{giveaway['prize']}**\n\n"
                    "❌ Nobody entered the giveaway."

                )


            else:


                selected = random.sample(

                    entries,

                    min(
                        winners,
                        len(entries)
                    )

                )


                mentions = " ".join(

                    f"<@{x}>"

                    for x in selected

                )


                await channel.send(

                    f"🎉 Giveaway ended!\n\n"
                    f"🏆 Prize: **{giveaway['prize']}**\n"
                    f"Congratulations {mentions}!"

                )



            try:

                message = await channel.fetch_message(
                    giveaway["message_id"]
                )


                await message.edit(
                    view=None
                )


            except:

                pass



            giveaway["ended"] = True

            update_giveaway(
                giveaway
            )



    def cog_unload(self):

        self.check_giveaways.cancel()





async def setup(bot):

    await bot.add_cog(
        Giveaway(bot)
    )

    print(
        "✅ Giveaway loaded"
    )