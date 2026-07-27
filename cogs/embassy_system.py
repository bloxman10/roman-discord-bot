import discord
from discord.ext import commands
from discord import app_commands

from views.embassy_view import EmbassyButton


class EmbassySystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="setup_embassy",
        description="Create the embassy button message"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_embassy(
        self,
        interaction: discord.Interaction
    ):

        embed = discord.Embed(
            title="🤝 Empire of the Romans Embassy",
            description=(
                "Click the button below to open an embassy room "
                "with our Foreign Affairs team."
            ),
            color=discord.Color.blue()
        )


        embed.set_footer(
            text="Empire of the Romans • Foreign Affairs"
        )


        # Public embassy message
        await interaction.channel.send(
            embed=embed,
            view=EmbassyButton()
        )


        # Only the admin sees this
        await interaction.response.send_message(
            "✅ Embassy message created.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(
        EmbassySystem(bot)
    )