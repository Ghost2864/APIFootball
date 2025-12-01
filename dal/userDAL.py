from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException,status
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from schema.jwt import Token, TokenData
from schema.user import UserSchema
from core.jwt import create_access_token, oauth2_scheme
from models.user import User
from sqlalchemy import select
from config import settings
from core.jwt import get_password_hash,verify_password

class UserDAL():
    def __init__(self, db_session:AsyncSession):
        self.db = db_session
        
    async def register_user(self, user_data: UserSchema):
        async with self.db.begin():
            login = await self.get_user_by_login(user_data.login)
            if login:
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

    async def get_user_by_login(self,login:str):
        stmt = await self.db.execute(select(User).where(User.login == login))
        user = stmt.scalar_one_or_none()
        if user:
            return user
        else: return None

    async def login(self, user_data:UserSchema) -> Token:
        user = await self.get_user_by_login(user_data.login)
        if not user and verify_password(user_data.password,user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.login}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            login = payload.get("sub")
            if login is None:
                raise credentials_exception
            token_data = TokenData(login=login)
        except jwt.InvalidTokenError:
            raise credentials_exception
        user = await self.get_user_by_login(login)
        if user is None:
            raise credentials_exception
        return user

async def get_user_dal(db_session: AsyncSession = Depends(get_db)) -> UserDAL:
    return UserDAL(db_session)



