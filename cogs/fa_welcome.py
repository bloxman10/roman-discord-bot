import discord

from discord.ext import commands
from discord import app_commands

from utils.config_manager import load_config, save_config


class FAWelcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="setup_fawelcome",
        description="Set the Foreign Affairs welcome channel"
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
        config["fa_server_id"] = interaction.guild.id

        save_config(config)

        await interaction.response.send_message(
            f"✅ Foreign Affairs welcome channel set to {channel.mention}",
            ephemeral=True
        )


    @commands.Cog.listener()
    async def on_member_join(
        self,
        member: discord.Member
    ):

        config = load_config()

        # Only allow FA server to trigger this welcome
        if member.guild.id != config.get("fa_server_id"):
            return


        channel_id = config.get(
            "fa_welcome_channel"
        )

        if not channel_id:
            return


        channel = self.bot.get_channel(
            channel_id
        )

        if channel is None:
            return


        # Separate FA verify channel
        fa_verify_channel = config.get(
            "fa_verify_channel"
        )

        # Open ticket channel
        open_ticket_channel = config.get(
            "open_ticket_channel"
        )

        # Bloxman
        fa_contact = config.get(
            "fa_contact"
        )

        if not fa_verify_channel or not open_ticket_channel:
            print(
                "❌ FA welcome is missing fa_verify_channel "
                "or open_ticket_channel in config.json"
            )
            return


        embed = discord.Embed(
            description=(
                "**Welcome!**\n\n"

                "Welcome to the **Roman FA server!** "
                f"First please go to <#{fa_verify_channel}> "
                f"and register with <@{config['locutus_user']}>.\n\n"

                "After doing that, please open a ticket in "
                f"<#{open_ticket_channel}>, "
                f"or DM <@{fa_contact}>.\n\n"

                "You will be added to your embassy shortly after that.\n\n"

                "Thanks!"
            ),
            color=discord.Color.blue()
        )


        embed.set_author(
            name=member.display_name,
            icon_url=member.display_avatar.url
        )


        embed.set_thumbnail(
            url=config.get("welcome_logo")
        )


        embed.set_image(
            url=config.get("welcome_banner")
        )


        embed.set_footer(
            text="Empire of the Romans • Foreign Affairs"
        )


        await channel.send(
            content=member.mention,
            embed=embed
        )


async def setup(bot):

    await bot.add_cog(
        FAWelcome(bot)
    )

    print(
        "✅ FA Welcome loaded"
    )