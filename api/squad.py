import httpx
from config import settings



async def get_squad_by_team_id(team_id:int):
    async with httpx.AsyncClient(base_url=f"https://{settings.base_api_url}") as client:
        response = await client.get(
            f"/players/squads?team={team_id}",
            headers=settings.headers
        )
        response.raise_for_status()
        data = response.json()
        teams = data["response"]
        res = []
        for team in teams:
            for player in team["players"]:
                res.append({
                    "id": player["id"],
                    "name": player["name"],
                    "age": player["age"],
                    "photo": player["photo"]
                })
        return res