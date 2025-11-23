from fastapi import FastAPI, Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from handlers.league_router import league_router
from handlers.player_router import player_router
from handlers.squad_router import squad_router
from handlers.team_router import team_router


app = FastAPI()
app.include_router(league_router)
app.include_router(player_router)
app.include_router(squad_router)
app.include_router(team_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_main_page():
    return FileResponse("static/index.html")



@app.get("/league")
def serve_league_page():
    return FileResponse("static/leagues.html")


@app.get("/teams")
def serve_teams_page():
    return FileResponse("static/teams.html")


@app.get("/squad")
def serve_squad_page():
    return FileResponse("static/squad.html")

@app.get("/profile")
def serve_profile_page():
    return FileResponse("static/profile.html")








if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
