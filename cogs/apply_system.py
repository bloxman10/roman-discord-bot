import discord
from discord.ext import commands
from discord import app_commands

from views.apply_view import ApplyButton


class ApplySystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="setup_apply",
        description="Create the application message"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_apply(
        self,
        interaction: discord.Interaction
    ):

        embed = discord.Embed(
            title="🏛️ Join Empire of the Romans",
            description=(
                "Interested in joining our alliance?\n\n"
                "Click the button below to start your application."
            ),
            color=discord.Color.gold()
        )

        embed.add_field(
            name="Application Requirements",
            value=(
                "• Nation link\n"
                "• Activity level\n"
                "• Previous alliances\n"
                "• Reason for joining"
            ),
            inline=False
        )

        embed.set_footer(
            text="Empire of the Romans"
        )


        # Public message
        await interaction.channel.send(
            embed=embed,
            view=ApplyButton()
        )


        # Private confirmation
        await interaction.response.send_message(
            "✅ Application message created.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(ApplySystem(bot))