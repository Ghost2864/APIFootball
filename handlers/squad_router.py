
from fastapi import APIRouter
from api.squad import get_squad_by_team_id
from services.redis_service import get_data_with_cache

squad_router = APIRouter(
    tags=["leagues"],
    responses={404:{"message": "Not found"}}
)






@squad_router.get("/api/squad/{team_id}")
async def api_squad_by_team_id(team_id:int):
    data = await get_data_with_cache(get_squad_by_team_id, team_id)
    return data