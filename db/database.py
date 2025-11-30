from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,           
    pool_pre_ping=True    
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


Base = declarative_base()

async def get_db():
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
