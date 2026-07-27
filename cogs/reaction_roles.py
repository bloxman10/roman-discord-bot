import discord

from discord.ext import commands
from discord import app_commands

from utils.config_manager import load_config, save_config


class ReactionRoles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="reactionrole_create",
        description="Create a reaction role message"
    )
    @app_commands.describe(
        channel="Channel to send the message",
        title="Embed title",
        description="Embed description"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def create(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        title: str,
        description: str
    ):

        await interaction.response.defer(
            ephemeral=True
        )

        try:

            embed = discord.Embed(
                title=title,
                description=description,
                color=discord.Color.gold()
            )


            message = await channel.send(
                embed=embed
            )


            config = load_config()


            if "reaction_roles" not in config:
                config["reaction_roles"] = {}


            config["reaction_roles"][str(message.id)] = {
                "channel_id": channel.id,
                "roles": {}
            }


            save_config(config)


            await interaction.followup.send(
                f"✅ Reaction role created!\n\n"
                f"Message ID: `{message.id}`\n"
                f"{message.jump_url}",
                ephemeral=True
            )


        except Exception as e:

            print(
                "Reaction role create error:",
                e
            )

            await interaction.followup.send(
                f"❌ Error: {e}",
                ephemeral=True
            )



    @app_commands.command(
        name="reactionrole_add",
        description="Add emoji role to a reaction role message"
    )
    @app_commands.describe(
        message_id="Reaction role message ID",
        emoji="Emoji",
        role="Role to give"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def add(
        self,
        interaction: discord.Interaction,
        message_id: str,
        emoji: str,
        role: discord.Role
    ):

        config = load_config()


        data = config.get(
            "reaction_roles",
            {}
        ).get(
            message_id
        )


        if not data:

            await interaction.response.send_message(
                "❌ Reaction role message not found.",
                ephemeral=True
            )

            return


        data["roles"][emoji] = role.id


        save_config(config)


        try:

            channel = self.bot.get_channel(
                data["channel_id"]
            )

            message = await channel.fetch_message(
                int(message_id)
            )

            await message.add_reaction(
                emoji
            )


        except Exception as e:

            print(
                "Add reaction error:",
                e
            )


        await interaction.response.send_message(
            f"✅ Added {emoji} → {role.mention}",
            ephemeral=True
        )



    @app_commands.command(
        name="reactionrole_remove",
        description="Remove reaction role message"
    )
    @app_commands.describe(
        message_id="Message ID"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def remove(
        self,
        interaction: discord.Interaction,
        message_id: str
    ):

        config = load_config()


        data = config.get(
            "reaction_roles",
            {}
        ).get(
            message_id
        )


        if not data:

            await interaction.response.send_message(
                "❌ Reaction role message not found.",
                ephemeral=True
            )

            return


        # Delete Discord message
        try:

            channel = self.bot.get_channel(
                data["channel_id"]
            )


            if channel:

                message = await channel.fetch_message(
                    int(message_id)
                )

                await message.delete()


        except Exception as e:

            print(
                "Delete message error:",
                e
            )


        # Remove from config
        del config["reaction_roles"][message_id]


        save_config(config)


        await interaction.response.send_message(
            "✅ Reaction role removed and message deleted.",
            ephemeral=True
        )



    @app_commands.command(
        name="reactionrole_list",
        description="List reaction role messages"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def list_roles(
        self,
        interaction: discord.Interaction
    ):

        config = load_config()


        roles = config.get(
            "reaction_roles",
            {}
        )


        if not roles:

            await interaction.response.send_message(
                "❌ No reaction roles found.",
                ephemeral=True
            )

            return


        embed = discord.Embed(
            title="🎭 Reaction Roles",
            color=discord.Color.gold()
        )


        for message_id, data in roles.items():

            role_text = ""


            for emoji, role_id in data["roles"].items():

                role_text += (
                    f"{emoji} → <@&{role_id}>\n"
                )


            if not role_text:

                role_text = "No roles added"


            embed.add_field(
                name=f"Message ID: {message_id}",
                value=role_text,
                inline=False
            )


        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )



    @commands.Cog.listener()
    async def on_raw_reaction_add(
        self,
        payload
    ):

        if payload.guild_id is None:
            return


        config = load_config()


        data = config.get(
            "reaction_roles",
            {}
        ).get(
            str(payload.message_id)
        )


        if not data:
            return


        emoji = str(payload.emoji)


        role_id = data["roles"].get(
            emoji
        )


        if not role_id:
            return


        guild = self.bot.get_guild(
            payload.guild_id
        )


        if not guild:
            return


        member = guild.get_member(
            payload.user_id
        )


        if not member:

            try:

                member = await guild.fetch_member(
                    payload.user_id
                )

            except:

                return


        if member.bot:
            return


        role = guild.get_role(
            role_id
        )


        if role:

            await member.add_roles(
                role
            )



    @commands.Cog.listener()
    async def on_raw_reaction_remove(
        self,
        payload
    ):

        if payload.guild_id is None:
            return


        config = load_config()


        data = config.get(
            "reaction_roles",
            {}
        ).get(
            str(payload.message_id)
        )


        if not data:
            return


        emoji = str(payload.emoji)


        role_id = data["roles"].get(
            emoji
        )


        if not role_id:
            return


        guild = self.bot.get_guild(
            payload.guild_id
        )


        if not guild:
            return


        member = guild.get_member(
            payload.user_id
        )


        if not member:

            try:

                member = await guild.fetch_member(
                    payload.user_id
                )

            except:

                return


        role = guild.get_role(
            role_id
        )


        if role:

            await member.remove_roles(
                role
            )



async def setup(bot):

    await bot.add_cog(
        ReactionRoles(bot)
    )

    print("✅ Reaction Roles loaded")