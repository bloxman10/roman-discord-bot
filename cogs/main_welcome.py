import discord
from discord.ext import commands
from discord import app_commands

from utils.config_manager import load_config, save_config


class MainWelcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="setup_mainwelcome",
        description="Set the channel for welcome messages"
    )
    @app_commands.describe(
        channel="Channel where welcome messages will be sent"
    )
    async def setup_mainwelcome(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel
    ):

        config = load_config()

        config["main_welcome_channel"] = channel.id

        save_config(config)


        await interaction.response.send_message(
            f"✅ Welcome messages will now be sent in {channel.mention}",
            ephemeral=True
        )


    @commands.Cog.listener()
    async def on_member_join(
        self,
        member: discord.Member
    ):

        config = load_config()

        channel_id = config.get(
            "main_welcome_channel"
        )


        if channel_id is None:
            return


        channel = self.bot.get_channel(
            channel_id
        )


        if channel is None:
            return


        embed = discord.Embed(
            title="🏛️ Welcome to the Empire of the Romans!",
            description=(
                f"Ave, {member.mention}!\n\n"
                "Welcome to **Empire of the Romans**.\n\n"
                "Please read the rules and complete the required steps."
            ),
            color=discord.Color.gold()
        )


        embed.add_field(
            name="📜 Getting Started",
            value=(
                "• Read the rules\n"
                "• Introduce yourself\n"
                "• Contact government if you need help"
            ),
            inline=False
        )


        embed.add_field(
            name="⚔️ Glory to Rome",
            value="SPQR",
            inline=False
        )


        embed.set_thumbnail(
            url=member.display_avatar.url
        )


        embed.set_footer(
            text="Empire of the Romans"
        )


        await channel.send(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(MainWelcome(bot))