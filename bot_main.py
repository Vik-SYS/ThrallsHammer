import discord
import time
from discord.ext import commands
from discord import app_commands
import asyncio
from blizzard_api import get_guild_roster
from raider_io import get_weekly_affixes
from raider_io import get_mythic_plus_profile

GUILD_REALM = "guild realm here"
GUILD_NAME = "guild name here"

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

@bot.tree.command(name="affixes", description="Get this week's Mythic+ dungeon affixes")
async def affixes(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

    try:
        data = await get_weekly_affixes()
        affix_list = data["affix_details"]

        embed = discord.Embed(
            title="This week's Mythic+ affixes",
            color=discord.Color.teal()
        )

        for affix in affix_list:
            embed.add_field(name-affix["name"], value=affix["description"],inline=False)

        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"Failed to get affixes:\n```\n{e}\n```")


@bot.tree.command(name="mythicplus", description="Check a player's Raider.IO score and best runs")
@app_commands.describe(name="Character name", realm="Realm")
async def mythicplus(interaction: discord.Interaction, name: str, realm: str):
    await interaction.response.defer(thinking=True)

    try:
        profile = await get_mythic_plus_profile(name,realm)

        embed = discord.Embed(
            title=f"{profile['name']} - {profile['active_spec_name']} {profile['class']}",
            description=f"Raider.IO score: **{profile}['mythic_plus_scores]['all']}**",
            color=discord.Color.blurple()

        )
        embed.set_thumbnail(url=profile.get("thumbnail_url", ""))

        for run in profile.get("mythic_plus)best_runs", [])[:3]:
            embed.add_field(
                name=f"{run['dungeon']} +{run['mythic_level']}",
                value=f"Time: {run['clear_time_ms'] // 60000}min\nAffixes: {', '.join(run['affixes'])}",
                inline=False
            )

        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"Could not get profile:\n```\n{e}\n```")

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    bot.loop.create_task(check_for_new_runs())

async def check_for_new_runs():
    await bot.wait_until_ready()
    channel = discord.utils.get(bot.get_all_channels(), name="mythic-plus")
    if not channel:
        print("'mythic-plus' channel not found!")
        return

    print("Starting M+ run monitor...")
    while not bot.is_closed():
        try:
            roster_data = await get_guild_roster(GUILD_REALM, GUILD_NAME)
            members = roster_data.get("members", [])
            for member in members:
                char = member["character"]
                name = char["name"]
                realm = char["realm"]["slug"]

                try:
                    profile = await get_mythic_plus_profile(name, realm)
                    best_runs = profile.get("mythic_plus_best_runs", [])

                    for run in best_runs:
                        run_id = (name, run["dungeon"], run["completed_at"])
                        if run_id not in posted_runs:
                            posted_runs.add(run_id)

                            embed = discord.Embed(
                                title=f"{name} completed {run['dungeon']} +{run['mythic_level']}",
                                description=f"🎉 {profile['active_spec_name']} {profile['class']} from {realm.capitalize()}",
                                color=discord.Color.green()
                            )
                            embed.add_field(name="Score", value=profile['mythic_plus_scores']['all'],inline=True)
                            embed.add_field(name="Time", value=run['completed_at'].split("T")[0], inline=True)
                            embed.add_field(name="Affixes", value=", ".join(a["name"] for a in run["affixes"]),inline=False)
                            embed.set_thumbnail(url=profile.get("thumbnail_url", ""))
                            await channel.send(embed=embed)

                            await asyncio.sleep(1)

                except Exception as e:
                    print(f"Failed to fetch M+ for {name}: {e}")

            await asyncio.sleep(300)  # Wait 5 minutes between scans

                except Exception as err:
                print(f"Error in background task: {err}")
                await asyncio.sleep(60)

        bot.run("YOUR DISCORD TOKEN HERE")
