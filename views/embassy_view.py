import discord

from config import (
    EMBASSY_CATEGORY_ID,
    EMBASSY_STAFF_ROLE_ID
)


class EmbassyButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(
        label="Open Embassy",
        emoji="🤝",
        style=discord.ButtonStyle.blurple,
        custom_id="embassy_button"
    )
    async def embassy(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        guild = interaction.guild
        member = interaction.user


        if guild is None:

            await interaction.response.send_message(
                "❌ This button can only be used in a server.",
                ephemeral=True
            )

            return



        channel_name = (
            f"embassy-{member.name}"
            .lower()
            .replace(" ", "-")
        )


        existing = discord.utils.get(
            guild.channels,
            name=channel_name
        )


        if existing:

            await interaction.response.send_message(
                f"❌ You already have an embassy room: {existing.mention}",
                ephemeral=True
            )

            return



        category = guild.get_channel(
            EMBASSY_CATEGORY_ID
        )

        staff_role = guild.get_role(
            EMBASSY_STAFF_ROLE_ID
        )


        if category is None:

            await interaction.response.send_message(
                "❌ Embassy category is not configured correctly.",
                ephemeral=True
            )

            return


        if staff_role is None:

            await interaction.response.send_message(
                "❌ Embassy staff role is not configured correctly.",
                ephemeral=True
            )

            return



        overwrites = {

            guild.default_role:
                discord.PermissionOverwrite(
                    view_channel=False
                ),


            member:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                ),


            staff_role:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                )
        }



        try:

            channel = await guild.create_text_channel(
                name=channel_name,
                category=category,
                overwrites=overwrites
            )


        except discord.Forbidden:

            await interaction.response.send_message(
                "❌ I don't have permission to create channels.",
                ephemeral=True
            )

            return



        await interaction.response.send_message(
            f"✅ Your embassy room has been created: {channel.mention}",
            ephemeral=True
        )



        embed = discord.Embed(
            title="🤝 Embassy Opened",
            description=(
                f"Welcome {member.mention}.\n\n"
                "Please provide the following information:"
            ),
            color=discord.Color.blue()
        )


        embed.add_field(
            name="Required Information",
            value=(
                "• Alliance name\n"
                "• Your position\n"
                "• Reason for contacting us\n"
                "• Any additional details"
            ),
            inline=False
        )


        embed.set_footer(
            text="Empire of the Romans • Foreign Affairs"
        )


        await channel.send(
            content=(
                f"{member.mention} "
                f"<@&{EMBASSY_STAFF_ROLE_ID}>"
            ),
            embed=embed
        )