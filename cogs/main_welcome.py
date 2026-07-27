import discord

from discord.ext import commands
from discord import app_commands

from utils.config_manager import load_config, save_config


class MainWelcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="setup_mainwelcome",
        description="Set the welcome channel"
    )
    @app_commands.describe(
        channel="Channel where welcome messages will be sent"
    )
    async def setup_mainwelcome(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel
    ):

        try:

            config = load_config()

            config["main_welcome_channel"] = channel.id
            config["main_server_id"] = interaction.guild.id

            save_config(config)


            await interaction.response.send_message(
                f"✅ Welcome channel set to {channel.mention}",
                ephemeral=True
            )


        except Exception as e:

            print(f"Welcome setup error: {e}")

            if interaction.response.is_done():

                await interaction.followup.send(
                    f"❌ Error: {e}",
                    ephemeral=True
                )

            else:

                await interaction.response.send_message(
                    f"❌ Error: {e}",
                    ephemeral=True
                )



    @commands.Cog.listener()
    async def on_member_join(
        self,
        member: discord.Member
    ):

        config = load_config()


        # Prevent FA server from triggering main welcome
        if member.guild.id != config.get("main_server_id"):
            return



        channel_id = config.get(
            "main_welcome_channel"
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
                "Greetings! Welcome to the **Empire of the Romans**, "
                "also known as **Imperium Romanum**.\n\n"

                f"Please visit <#{config['verify_channel']}> and register with "
                f"<@{config['locutus_user']}>.\n\n"

                f"After verifying, please check out "
                f"<#{config['info_channel']}> for more information about Rome.\n\n"

                f"Join our Foreign Affairs server or contact "
                f"<@{config['fa_contact']}> for all FA inquiries.\n\n"

                f"To join Rome please go to "
                f"<#{config['apply_channel']}> and press the application button.\n\n"

                "Thanks!"
            ),
            color=discord.Color.gold()
        )


        embed.set_author(
            name=member.display_name,
            icon_url=member.display_avatar.url
        )


        embed.set_thumbnail(
            url=config["welcome_logo"]
        )


        embed.set_image(
            url=config["welcome_banner"]
        )


        embed.set_footer(
            text="Roma Invicta!"
        )


        await channel.send(
            content=member.mention,
            embed=embed
        )



async def setup(bot):

    await bot.add_cog(
        MainWelcome(bot)
    )

    print("✅ Main Welcome loaded")