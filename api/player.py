import httpx
from config import settings





    
async def get_profile_by_player_id(player_id: int):
    async with httpx.AsyncClient(base_url=f"https://{settings.base_api_url}") as client:
        response = await client.get(
            f"/players?id={player_id}&season=2023",
            headers=settings.headers
        )
        
        response.raise_for_status()
        data_obj = response.json()
        data = data_obj["response"]

        player = data[0]["player"]
        statistics = data[0]["statistics"]  

        all_stats = []
        for st in statistics:
            rating_raw = st["games"].get("rating")
            st["games"]["rating"] = round(float(rating_raw), 2) if rating_raw else None

            extracted = settings.extract_position_stats(player, st)
            all_stats.append(player)
            all_stats.append({
                "league": st["league"]["name"],
                "team": st["team"]["name"],
                "stats": extracted
            })
        return all_stats

        






        
        
