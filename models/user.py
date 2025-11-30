from db.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String,Integer,DateTime
from datetime import date,datetime

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(String(50))
    password:Mapped[str] = mapped_column(String(100))
    created_at: Mapped[date] = mapped_column(DateTime, default=datetime.now)