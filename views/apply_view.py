import discord

from config import (
    APPLICATION_CATEGORY_ID,
    APPLICATION_STAFF_ROLE_ID
)

from utils.config_manager import load_config



class ApplyButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)



    @discord.ui.button(
        label="Apply to Join",
        emoji="🏛️",
        style=discord.ButtonStyle.green,
        custom_id="apply_button"
    )
    async def apply(
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
            f"application-{member.name}"
            .lower()
            .replace(" ", "-")
        )


        existing = discord.utils.get(
            guild.channels,
            name=channel_name
        )


        if existing:

            await interaction.response.send_message(
                f"❌ You already have an application open: {existing.mention}",
                ephemeral=True
            )
            return



        category = guild.get_channel(
            APPLICATION_CATEGORY_ID
        )


        staff_role = guild.get_role(
            APPLICATION_STAFF_ROLE_ID
        )


        if category is None:

            await interaction.response.send_message(
                "❌ Application category is not configured correctly.",
                ephemeral=True
            )
            return


        if staff_role is None:

            await interaction.response.send_message(
                "❌ Application staff role is not configured correctly.",
                ephemeral=True
            )
            return



        # Load extra ticket access roles
        config = load_config()

        ticket_roles = config.get(
            "ticket_roles",
            []
        )



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


            # Main ping staff role also gets access
            staff_role:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                )
        }



        # Add extra roles from JSON
        for role_id in ticket_roles:

            role = guild.get_role(role_id)

            if role:

                overwrites[role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                )



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
            f"✅ Your application has been created: {channel.mention}",
            ephemeral=True
        )



        embed = discord.Embed(
            title="🏛️ Empire of the Romans Application",
            description=(
                "**Welcome!**\n\n"
                "Glad to see that you are interested in applying to "
                "**Empire of the Romans**.\n\n"
                "When you have about **5 to 10 minutes** of free time, "
                "kindly use the **/interview_start** command to begin a short interview."
            ),
            color=discord.Color.gold()
        )


        embed.add_field(
            name="Interview Process",
            value=(
                "You will be asked a few questions about your nation, "
                "experience, and interest in joining Rome.\n\n"
                "Please answer honestly and provide as much detail as possible."
            ),
            inline=False
        )


        embed.set_footer(
            text="Empire of the Romans Recruitment"
        )



        # Only APPLICATION_STAFF_ROLE_ID is pinged
        await channel.send(
            content=(
                f"{member.mention} "
                f"<@&{APPLICATION_STAFF_ROLE_ID}>"
            ),
            embed=embed
        )