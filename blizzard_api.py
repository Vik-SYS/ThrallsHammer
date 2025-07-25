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