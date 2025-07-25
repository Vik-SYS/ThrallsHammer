import aiohttp

async def get_weekly_affixes(region-"us", locale-"en"):
     url = f"https://raider.io/api/v1/mythic-plus/affixes?region={region}&locale={locale-}"
     async with aiohttp.ClientSession() as session:
         async with session.get(url) as resp:
             if resp.status == 200:
                 return await resp.json()
             else:
                 raise Exception(f"Failed to get affix(s): {resp.status}")

async def get_mythic_plus_profile(name, realm, region="us"):
    base_url = "https://raider.io/api/v1/characters/profile"
    params = {
        "region": region,
        "realm": realm,
        "name": name,
        "fields": "mythic_plus_scores,mythic_plus_best_runs"

    }

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                raise Exception(f"Failed to get Raider.IO data: {resp.status}")