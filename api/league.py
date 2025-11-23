import httpx
from config import settings
import json


async def get_leagues_by_country_code(country_code:str):
    async with httpx.AsyncClient(base_url=f"https://{settings.base_api_url}") as client:
            response = await client.get(
                f"/leagues",
                headers=settings.headers
            )
            response.raise_for_status()
            data = response.json()
            teams = data["response"]
            res = []
            for team in teams:
                if team['country']['code'] == country_code and team['league']['type'] == "League":
                    res.append({
                        "id" : f"{team['league']['id']}",
                        "name" : f"{team['league']['name']}",
                        "logo" : f"{team['league']['logo']}"

                    })
        

    return res



