from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).resolve().parent / ".env"
POSITION_FIELDS = { "Attacker":
                   {
                    "team": ["name", "logo"],
                    "league" : ["name", "logo"],
                    "goals": ["total", "assists"],
                    "games" : ["lineups", "minutes", "rating"],
                    "dribbles" : ["attempts", "success"],
                    "passes" : ["total", "key"]
                    },
                    "Midfielder":
                    {
                        "team": ["name", "logo"],
                        "league" : ["name", "logo"],
                        "goals": ["total", "assists"],
                        "games" : ["lineups", "minutes", "rating"],
                    },
                    "Defender":
                    {
                        "team": ["name", "logo"],
                        "league" : ["name", "logo"],
                        "goals": ["total", "assists"],
                        "games" : ["lineups", "minutes", "rating"],
                        "duels" : ["total", "won"], "cards" : ["yellow", "red"]
                    }, 
                    "Goalkeeper" : {
                        "team": ["name", "logo"],
                        "league" : ["name", "logo"],
                        "games" : ["lineups", "minutes", "rating"], "goals" : ["saves","conceded"], "penalty": ["saved"]
                    } }

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_API_KEY: str
    base_api_url: str = "v3.football.api-sports.io"

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        extra="ignore"
    )

    @staticmethod
    def extract_position_stats(player, stats):
        pos = stats["games"]["position"]
        groups = POSITION_FIELDS.get(pos, {})
        result = {}
        for group, fields in groups.items():
            for field in fields: result[f"{group}.{field}"] = stats.get(group, {}).get(field)
        return result
    
    @property
    def headers(self) -> dict: return {"x-apisports-key": self.SECRET_API_KEY}


class RedisConfig(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    MAIN_TTL:int = 3600
    STATE_TTL:int = 86400
    
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        extra="ignore"
    )


settings = Settings()

redis_config = RedisConfig()