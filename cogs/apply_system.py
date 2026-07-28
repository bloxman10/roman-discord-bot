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
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def setup_apply(
        self,
        interaction: discord.Interaction
    ):

        embed = discord.Embed(
            title="🏛️ Join Empire of the Romans",
            description=(
                "Click the button below to apply to join the "
                "**Empire of the Romans**.\n\n"
            ),
            color=discord.Color.gold()
        )


        embed.set_footer(
            text="Empire of the Romans Recruitment"
        )


        await interaction.channel.send(
            embed=embed,
            view=ApplyButton()
        )


        await interaction.response.send_message(
            "✅ Application message created.",
            ephemeral=True
        )



async def setup(bot):

    await bot.add_cog(
        ApplySystem(bot)
    )

    print(
        "✅ Apply System loaded"
    )