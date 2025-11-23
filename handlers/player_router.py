from fastapi import APIRouter
from services.redis_service import get_data_with_cache
from api.player import get_profile_by_player_id


player_router = APIRouter(
    tags=["leagues"],
    responses={404:{"message": "Not found"}}
)


@player_router.get("/api/profile/{player_id}")
async def api_profile_by_player_id(player_id:int):
    data = await get_data_with_cache(get_profile_by_player_id, player_id)
    return data