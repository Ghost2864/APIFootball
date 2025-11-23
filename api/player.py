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
        data = data_obj["response"][0]

        player = data["player"]
        stats = data["statistics"][0]

        # Добавляем обработку рейтинга
        rating_raw = stats["games"].get("rating")
        stats["games"]["rating"] = round(float(rating_raw), 2) if rating_raw else None

        res = []
        res.append(player)
        res.append(settings.extract_position_stats(player, stats))
        return res

        






        
        
