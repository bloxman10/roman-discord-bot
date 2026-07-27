import asyncio
import discord

from discord.ext import commands
from discord import app_commands


QUESTIONS = [
    "1. Are you new to PnW? If no, what was your previous alliance?",
    "2. Please use /register command to register with Locutus. Also, please send your nation link.",
    "3. Do you owe money/resources to your previous alliance or any banks?",
    "4. Have you ever been kicked or asked to leave an alliance before?",
    "5. What's your timezone and first language?",
    "6. We as an alliance have high standards for activity. How often will you be able to log in?",
    "7. Please fill out these forms, then type **Done** when you finish:\n\nhttps://docs.google.com/forms/d/e/1FAIpQLSfmTKtYhWjd0BIg8Pf9ouENcs8taGPHqsDTl5wPrw5R-11mgA/viewform\n\nhttps://docs.google.com/forms/d/e/1FAIpQLSee3vRjlen2YS0aGnnOjxSH0cuyzFTp1lFaeJtYK0PDc5sScA/viewform",
    "8. What made you want to join Rome?",
    "9. What about Rome interests you?",
    "10. How did you find out about Rome?",
    "11. What skills, knowledge and values can you bring to the alliance?",
    "12. Do you have any questions or anything else you want to tell us?"
]


active_interviews = {}


class Interview(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="interview_start",
        description="Start an application interview"
    )
    async def interview_start(
        self,
        interaction: discord.Interaction
    ):

        channel = interaction.channel
        user = interaction.user

        if channel.id in active_interviews:

            await interaction.response.send_message(
                "❌ An interview is already running in this channel.",
                ephemeral=True
            )
            return


        active_interviews[channel.id] = True

        await interaction.response.send_message(
            "✅ Interview started."
        )


        try:

            for question in QUESTIONS:

                if channel.id not in active_interviews:
                    return

                await channel.send(question)

                def check(message):

                    return (
                        message.channel.id == channel.id
                        and message.author.id == user.id
                    )

                await self.bot.wait_for(
                    "message",
                    check=check
                )

                await asyncio.sleep(0.5)


            if channel.id in active_interviews:
                del active_interviews[channel.id]

            await channel.send(
                "✅ **Interview completed!**\n\nA recruiter will review your answers shortly."
            )

        except Exception:

            active_interviews.pop(channel.id, None)


    @app_commands.command(
        name="interview_stop",
        description="Stop the current interview"
    )
    async def interview_stop(
        self,
        interaction: discord.Interaction
    ):

        if interaction.channel.id not in active_interviews:

            await interaction.response.send_message(
                "❌ No interview is running.",
                ephemeral=True
            )
            return


        del active_interviews[interaction.channel.id]

        await interaction.response.send_message(
            "🛑 Interview stopped."
        )


async def setup(bot):
    await bot.add_cog(Interview(bot))
    print("✅ Interview loaded")