import discord
import time
import re

from discord.ext import commands, tasks
from discord import app_commands

from utils.config_manager import load_config, save_config



def parse_time(value):

    match = re.match(
        r"^(\d+)(m|h|d)$",
        value.lower()
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



class Reminders(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.check_reminders.start()



    @app_commands.command(
        name="reminder_set",
        description="Create a reminder for yourself, a user, or a role"
    )
    @app_commands.describe(
        duration="Example: 10m, 2h, 3d",
        message="Reminder message",
        user="User to remind",
        role="Role to remind"
    )
    async def reminder_set(
        self,
        interaction: discord.Interaction,
        duration: str,
        message: str,
        user: discord.Member = None,
        role: discord.Role = None
    ):

        seconds = parse_time(duration)


        if not seconds:

            await interaction.response.send_message(
                "❌ Invalid format. Use 10m, 2h, 3d",
                ephemeral=True
            )

            return



        config = load_config()


        if "reminders" not in config:

            config["reminders"] = []



        if user:

            target_user_id = user.id
            target_role_id = None
            target = user.mention


        elif role:

            target_user_id = None
            target_role_id = role.id
            target = role.mention


        else:

            target_user_id = interaction.user.id
            target_role_id = None
            target = interaction.user.mention



        reminder = {

            "id": int(time.time()),

            "guild_id": interaction.guild.id,

            "channel_id": interaction.channel.id,

            "creator_id": interaction.user.id,

            "target_user_id": target_user_id,

            "target_role_id": target_role_id,

            "message": message,

            "time": int(time.time()) + seconds

        }



        config["reminders"].append(
            reminder
        )


        save_config(
            config
        )


        await interaction.response.send_message(
            f"✅ Reminder created for {target}\n"
            f"⏰ <t:{reminder['time']}:R>",
            ephemeral=True
        )



    @app_commands.command(
        name="reminder_list",
        description="Show your reminders"
    )
    async def reminder_list(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.defer(
            ephemeral=True
        )


        config = load_config()


        reminders = [
            r for r in config.get("reminders", [])
            if r.get("creator_id") == interaction.user.id
        ]



        if not reminders:

            await interaction.followup.send(
                "❌ You have no reminders.",
                ephemeral=True
            )

            return



        embed = discord.Embed(
            title="⏰ Your Reminders",
            color=discord.Color.gold()
        )


        for r in reminders:


            if r.get("target_user_id"):

                target = f"<@{r['target_user_id']}>"


            elif r.get("target_role_id"):

                target = f"<@&{r['target_role_id']}>"


            else:

                target = "Yourself"



            embed.add_field(
                name=f"ID: {r['id']}",
                value=(
                    f"Target: {target}\n"
                    f"Message: {r['message']}\n"
                    f"Time: <t:{r['time']}:R>"
                ),
                inline=False
            )



        await interaction.followup.send(
            embed=embed,
            ephemeral=True
        )



    @app_commands.command(
        name="reminder_remove",
        description="Remove your reminders"
    )
    async def reminder_remove(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.defer(
            ephemeral=True
        )


        config = load_config()


        reminders = config.get(
            "reminders",
            []
        )


        before = len(reminders)


        reminders = [
            r for r in reminders
            if r.get("creator_id") != interaction.user.id
        ]


        config["reminders"] = reminders


        save_config(
            config
        )


        removed = before - len(reminders)


        if removed:

            await interaction.followup.send(
                f"✅ Removed {removed} reminder(s).",
                ephemeral=True
            )

        else:

            await interaction.followup.send(
                "❌ You have no reminders.",
                ephemeral=True
            )



    @tasks.loop(seconds=10)
    async def check_reminders(self):

        config = load_config()


        reminders = config.get(
            "reminders",
            []
        )


        now = int(
            time.time()
        )


        remaining = []



        for r in reminders:


            if r["time"] <= now:


                guild = self.bot.get_guild(
                    r["guild_id"]
                )


                if guild:

                    channel = guild.get_channel(
                        r["channel_id"]
                    )


                    if channel:


                        if r.get("target_role_id"):

                            mention = (
                                f"<@&{r['target_role_id']}>"
                            )


                        elif r.get("target_user_id"):

                            mention = (
                                f"<@{r['target_user_id']}>"
                            )


                        else:

                            mention = ""



                        await channel.send(
                            f"⏰ Reminder {mention}\n\n"
                            f"{r['message']}"
                        )


            else:

                remaining.append(r)



        config["reminders"] = remaining


        save_config(
            config
        )



    def cog_unload(self):

        self.check_reminders.cancel()



async def setup(bot):

    await bot.add_cog(
        Reminders(bot)
    )

    print("✅ Reminders loaded")