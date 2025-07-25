import discord
from discord.ext import commands
from discord import app_commands
import asyncio

from blizzard_api import get_guild_roster #<--- This is the API function

  # your guild and realm info will go here
GUILD_REALM = "greymane"
GUILD_NAME = "South of Heaven"

intents = discord.Intents.default()
bot  = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is running. Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync command(s): {e}")

@bot.tree.command(name="guildroster", description="Show Guild Roster")
async def guildroster(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

    try:
        data = await get_guild_roster(GUILD_REALM, GUILD_NAME)
        members = data["Members"]

        embed = discord.Embed(
            title=f"Guild Roster: {GUILD_NAME.replace('-', '  ').title()}",
            description=f"Total Members: {len(members)}",
            color=discord.Color.purple()
        )

        for member in members[:10]:
            char = member["character"]
            name = char["name"]
            level = char["level"]
            char_class = char["playable_class"]["name"]
            embed.add_field(name=name, value=f"Level {level} {char_class}", inline=True)

        if len(members) > 10:
            embed.set_footer(text=f"Only showing first 10 of {len(members)} members.")

        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"Failed to grab Guild Roster.\n```\n{e}\n```")

        bot.run("YOUR DISCORD TOKEN HERE")
