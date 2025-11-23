
from fastapi import APIRouter
from api.team import get_teams_by_league_id
from services.redis_service import get_data_with_cache

team_router = APIRouter(
    tags=["leagues"],
    responses={404:{"message": "Not found"}}
)



@team_router.get("/api/teams/{league_id}")
async def api_teams_by_league_id(league_id:int):
    data = await get_data_with_cache(get_teams_by_league_id, league_id)
    return data

