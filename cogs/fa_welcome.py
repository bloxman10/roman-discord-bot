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



        embed = discord.Embed(
            description=(
                "**Welcome!**\n\n"
                "Welcome to the **Empire of the Romans Foreign Affairs** server.\n\n"

                "If you are here for diplomacy, treaty discussions, embassies, "
                "or other diplomatic matters, our Foreign Affairs team will assist you shortly.\n\n"

                "To contact us, please create an embassy using the embassy button "
                "or wait for a member of the FA team.\n\n"

                "Ave Roma!"
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