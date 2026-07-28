import discord
import random
import asyncio

from discord.ext import commands
from discord import app_commands

from utils.config_manager import load_config, save_config



ATTACKS = [

    {
        "name": "Punch",
        "rarity": "Common",
        "chance": 50,
        "damage": (5, 10)
    },

    {
        "name": "Sword Slash",
        "rarity": "Uncommon",
        "chance": 25,
        "damage": (10, 18)
    },

    {
        "name": "Spear Thrust",
        "rarity": "Rare",
        "chance": 12,
        "damage": (18, 28)
    },

    {
        "name": "Gladiator Strike",
        "rarity": "Epic",
        "chance": 8,
        "damage": (28, 40)
    },

    {
        "name": "Godly Execution",
        "rarity": "Legendary",
        "chance": 3,
        "damage": (40, 60)
    },

    {
        "name": "Critical Fury",
        "rarity": "Mythic",
        "chance": 2,
        "damage": (60, 80)
    }

]



active_fights = set()



def get_attack():

    attacks = []

    for attack in ATTACKS:

        attacks.extend(
            [attack] * attack["chance"]
        )

    return random.choice(
        attacks
    )



class Colosseum(commands.Cog):

    def __init__(
        self,
        bot
    ):

        self.bot = bot



    @app_commands.command(
        name="colosseum_fight",
        description="Challenge someone to a colosseum duel"
    )
    async def fight(
        self,
        interaction: discord.Interaction,
        opponent: discord.Member
    ):


        if opponent.bot:

            await interaction.response.send_message(
                "❌ You cannot fight bots.",
                ephemeral=True
            )

            return


        if opponent.id == interaction.user.id:

            await interaction.response.send_message(
                "❌ You cannot fight yourself.",
                ephemeral=True
            )

            return



        fight_id = tuple(
            sorted(
                [
                    interaction.user.id,
                    opponent.id
                ]
            )
        )


        if fight_id in active_fights:

            await interaction.response.send_message(
                "❌ This fight is already happening.",
                ephemeral=True
            )

            return



        active_fights.add(
            fight_id
        )


        await interaction.response.send_message(
            f"🏟️ **The Colosseum opens!**\n\n"
            f"⚔️ {interaction.user.mention} vs {opponent.mention}\n\n"
            f"Both gladiators enter with **100 HP**!"
        )



        hp = {

            interaction.user.id: 100,

            opponent.id: 100

        }



        players = [

            interaction.user,

            opponent

        ]



        attacker_index = random.randint(
            0,
            1
        )



        await asyncio.sleep(3)



        while True:


            attacker = players[
                attacker_index
            ]


            defender = players[
                1 - attacker_index
            ]



            attack = get_attack()


            damage = random.randint(
                attack["damage"][0],
                attack["damage"][1]
            )


            hp[defender.id] -= damage


            if hp[defender.id] < 0:

                hp[defender.id] = 0



            embed = discord.Embed(
                title="⚔️ Colosseum Battle",
                color=discord.Color.red()
            )


            embed.add_field(
                name="Attacker",
                value=attacker.mention,
                inline=True
            )


            embed.add_field(
                name="Attack",
                value=(
                    f"{attack['name']}\n"
                    f"⭐ {attack['rarity']}"
                ),
                inline=True
            )


            embed.add_field(
                name="Damage",
                value=f"💥 {damage}",
                inline=True
            )


            embed.add_field(
                name=f"{defender.display_name}'s HP",
                value=f"❤️ {hp[defender.id]}/100",
                inline=False
            )



            await interaction.channel.send(
                embed=embed
            )



            if hp[defender.id] <= 0:


                await asyncio.sleep(2)


                await interaction.channel.send(
                    f"🏆 **{attacker.mention} wins the Colosseum duel!**\n\n"
                    f"☠️ {defender.mention} has fallen!"
                )


                break



            attacker_index = 1 - attacker_index


            await asyncio.sleep(3)



        active_fights.remove(
            fight_id
        )



async def setup(bot):

    await bot.add_cog(
        Colosseum(bot)
    )

    print(
        "✅ Colosseum loaded"
    )