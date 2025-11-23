import httpx
from config import settings

async def get_teams_by_league_id(league_id:int):
    async with httpx.AsyncClient(base_url=f"https://{settings.base_api_url}") as client:
        response = await client.get(
            f"/teams?league={league_id}&season=2023",
            headers=settings.headers
        )
        response.raise_for_status()
        data = response.json()
        teams = data["response"]
        res = []
        for team in teams:
            res.append({
                "id": team['team']['id'],
                "name": team['team']['name'],
                "logo": team['team']['logo'],
            })
        return res