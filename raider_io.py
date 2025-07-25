import aiohttp

async def get_weekly_affixes(region-"us", locale-"en"):
     url = f"https://raider.io/api/v1/mythic-plus/affixes?region={region}&locale={locale-}"
     async with aiohttp.ClientSession() as session:
         async with session.get(url) as resp:
             if resp.status == 200:
                 return await resp.json()
             else:
                 raise Exception(f"Failed to get affix(s): {resp.status}")