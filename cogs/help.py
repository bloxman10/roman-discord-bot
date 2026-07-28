import discord

from discord.ext import commands
from discord import app_commands


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="help",
        description="Show all bot commands"
    )
    async def help(
        self,
        interaction: discord.Interaction
    ):

        embed = discord.Embed(
            title="🏛️ Empire of the Romans Bot Help",
            description=(
                "Welcome to the Roman Bot command guide.\n\n"
                "Use `/command` to run commands."
            ),
            color=discord.Color.gold()
        )


        # General
        embed.add_field(
            name="🏛️ General",
            value=(
                "`/help`\n"
                "→ Shows this help menu"
            ),
            inline=False
        )


        # Recruitment
        embed.add_field(
            name="📝 Recruitment",
            value=(
                "`/setup_apply`\n"
                "→ Creates the application panel (Admin)\n\n"

                "`/interview_start`\n"
                "→ Starts an application interview\n\n"

                "`/interview_stop`\n"
                "→ Stops the current interview"
            ),
            inline=False
        )


        # Foreign Affairs
        embed.add_field(
            name="🤝 Foreign Affairs",
            value=(
                "`/setup_embassy`\n"
                "→ Creates the embassy panel (Admin)"
            ),
            inline=False
        )


        # Reaction Roles
        embed.add_field(
            name="🎭 Reaction Roles",
            value=(
                "`/reactionrole_create`\n"
                "→ Creates a reaction role message\n\n"

                "`/reactionrole_add`\n"
                "→ Adds an emoji role\n\n"

                "`/reactionrole_remove`\n"
                "→ Removes a reaction role message\n\n"

                "`/reactionrole_list`\n"
                "→ Lists reaction role messages"
            ),
            inline=False
        )


        # Giveaways
        embed.add_field(
            name="🎉 Giveaways",
            value=(
                "`/giveaway create`\n"
                "→ Creates a giveaway\n\n"

                "`/giveaway list`\n"
                "→ Shows active giveaways\n\n"

                "`/giveaway remove`\n"
                "→ Removes a giveaway (Admin)"
            ),
            inline=False
        )


        # Colosseum
        embed.add_field(
            name="⚔️ Colosseum",
            value=(
                "`/colosseum_fight`\n"
                "→ Challenge another member to a gladiator duel\n\n"
                "Both gladiators start with 100 HP.\n"
                "Attacks and damage are randomly selected."
            ),
            inline=False
        )


        # Reminders
        embed.add_field(
            name="⏰ Reminders",
            value=(
                "`/reminder_create`\n"
                "→ Create a reminder\n\n"

                "`/reminder_list`\n"
                "→ View reminders\n\n"

                "`/reminder_remove`\n"
                "→ Remove a reminder"
            ),
            inline=False
        )


        # Setup/Admin
        embed.add_field(
            name="⚙️ Administration",
            value=(
                "`/setup_mainwelcome`\n"
                "→ Set the main server welcome channel\n\n"

                "`/setup_fawelcome`\n"
                "→ Set the FA server welcome channel\n\n"

                "`/setup_apply`\n"
                "→ Create application panel\n\n"

                "`/setup_embassy`\n"
                "→ Create embassy panel"
            ),
            inline=False
        )


        embed.set_footer(
            text="Empire of the Romans • Roma Invicta!"
        )


        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )



async def setup(bot):

    await bot.add_cog(
        Help(bot)
    )

    print(
        "✅ Help loaded"
    )