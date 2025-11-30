from fastapi import Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from schema.user import UserSchema
from models.user import User
from sqlalchemy import select
from core.jwt import get_password_hash,verify_password

class UserDAL():
    def __init__(self, db_session:AsyncSession):
        self.db = db_session
        
    async def register_user(self, user_data: UserSchema):
        async with self.db.begin():
            login = await self.db.execute(select(User).where(User.login == user_data.login))
            if login.scalar_one_or_none():
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user with this username already exists")
            
            if len(user_data.password) < 8:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password must be longer than 8 characters.")
            
            user = User(
                login=user_data.login,
                password=get_password_hash(user_data.password)
            )
            self.db.add(user)
        await self.db.refresh(user)
        return user


    async def login(self, user_data:UserSchema):
        stmt = await self.db.execute(select(User).where(User.login == user_data.login))
        res = stmt.scalar_one_or_none()
        if res and verify_password(user_data.password,res.password):
            return res
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect login or password")

async def get_user_dal(db_session: AsyncSession = Depends(get_db)) -> UserDAL:
    return UserDAL(db_session)