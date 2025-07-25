import aiohttp
import asyncio
import base64
import os
from dotenv import load_dotenv

load_dotenv()

BNET_CLIENT_ID = os.getenv("BNET_CLIENT_ID")
BNET_CLIENT_SECRET = os.getenv("BNET_CLIENT_SECRET")
BNET_REGION = "us"

TOKEN_URL = f"https://{BNET_REGION}/oauth/token"

async def get_bnet_token():
    credentials = f"{BNET_CLIENT_ID}:{BNET_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",

    }

    data = "grant_type=client_credentials"

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(TOKEN_URL, headers=headers, data=data) as resp:
            response = await resp.json()
            return response["access_token"]

async def get_guild_roster(realm_slug, guild_name):
    token = await get_bnet_token()
    namespace = f"https://{BNET_REGION}.api.blizzard.com/data/wow/guild/{realm_slug}/{guild_name}/roster"

    params = {
        "namespace":namespace,
        "locale":LOCALE,
        "access_token":token,

    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                error = await resp.text()
                raise Exception(f"Failed to get roster: {resp.status}\n{error}")

async def get_guild_achievements(realm_slug, guild_name):
    token = await get_bnet_token()
    namespace = f"profile--{BNET_REGION}"
    url = f"https://{BNET_REGION}.api.blizzard.com/data/wow/guild/{realm_slug}/achievements"

    params - {
        "namespace": namespace,
        "locale": LOCALE,
        "access_token": token
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                return await resp.json()
        else:
            error = await resp.text()
            raise Exception(f"Failed to get achievements: {resp.status}\n{error}")
