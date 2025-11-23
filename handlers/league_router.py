from fastapi import APIRouter
from api.league import get_leagues_by_country_code
from services.redis_service import get_data_with_cache

league_router = APIRouter(
    tags=["leagues"],
    responses={404:{"message": "Not found"}}
)

@league_router.get("/api/leagues/{country_code}")
async def api_all_league(country_code:str):
    data = await get_data_with_cache(get_leagues_by_country_code, country_code)
    return data