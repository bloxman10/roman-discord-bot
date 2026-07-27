import discord

from utils.giveaway_manager import (
    get_giveaway,
    update_giveaway
)


class GiveawayView(discord.ui.View):

    def __init__(self, message_id: int):
        super().__init__(timeout=None)
        self.message_id = message_id


    @discord.ui.button(
        label="🎉 Enter Giveaway",
        style=discord.ButtonStyle.green,
        custom_id="giveaway_enter"
    )
    async def enter(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        giveaway = get_giveaway(
            self.message_id
        )

        if not giveaway:

            await interaction.response.send_message(
                "❌ This giveaway no longer exists.",
                ephemeral=True
            )

            return


        user_id = interaction.user.id


        # Toggle entry

        if user_id in giveaway["entries"]:

            giveaway["entries"].remove(
                user_id
            )

            message = (
                "❌ You left the giveaway."
            )


        else:

            giveaway["entries"].append(
                user_id
            )

            message = (
                "✅ You entered the giveaway!"
            )


        update_giveaway(
            giveaway
        )


        await interaction.response.send_message(
            message,
            ephemeral=True
        )


        # Update message count

        try:

            channel = interaction.guild.get_channel(
                giveaway["channel_id"]
            )

            msg = await channel.fetch_message(
                self.message_id
            )


            embed = msg.embeds[0]


            for field in embed.fields:

                if field.name == "Entries":

                    embed.set_field_at(
                        embed.fields.index(field),
                        name="Entries",
                        value=str(
                            len(giveaway["entries"])
                        ),
                        inline=True
                    )


            await msg.edit(
                embed=embed
            )


        except Exception:

            pass