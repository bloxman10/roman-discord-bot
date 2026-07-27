import discord
from discord.ext import commands
from discord import app_commands

from utils.config_manager import load_config, save_config


class FAWelcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="setup_fawelcome",
        description="Set the FA server welcome channel"
    )
    @app_commands.describe(
        channel="Channel where FA welcome messages will be sent"
    )
    async def setup_fawelcome(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel
    ):

        config = load_config()

        config["fa_welcome_channel"] = channel.id

        save_config(config)

        await interaction.response.send_message(
            f"✅ FA welcome messages will now be sent in {channel.mention}",
            ephemeral=True
        )


    @commands.Cog.listener()
    async def on_member_join(
        self,
        member: discord.Member
    ):

        config = load_config()

        channel_id = config.get(
            "fa_welcome_channel"
        )

        if channel_id is None:
            return


        channel = self.bot.get_channel(
            channel_id
        )

        if channel is None:
            return


        embed = discord.Embed(
            title="🤝 Welcome to the Empire of the Romans Embassy",
            description=(
                f"Welcome, {member.mention}!\n\n"
                "This server is the official Foreign Affairs "
                "hub of the **Empire of the Romans**.\n\n"
                "We use this server for diplomatic communication, "
                "treaty discussions, and alliance relations."
            ),
            color=discord.Color.blue()
        )


        embed.add_field(
            name="🏛️ Embassy Guidelines",
            value=(
                "• Please identify yourself\n"
                "• State your alliance and position\n"
                "• Contact Foreign Affairs staff if needed"
            ),
            inline=False
        )


        embed.add_field(
            name="📜 Diplomacy",
            value=(
                "We welcome all diplomatic visitors "
                "and look forward to productive relations."
            ),
            inline=False
        )


        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        embed.set_footer(
            text="Empire of the Romans • Foreign Affairs"
        )


        await channel.send(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(FAWelcome(bot))