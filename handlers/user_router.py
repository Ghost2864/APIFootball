from typing import Annotated
from schema.user import UserSchema,UserResponse
from dal.userDAL import UserDAL,get_user_dal
from fastapi import Depends,APIRouter
from dal.userDAL import UserDAL
from core.jwt import oauth2_scheme

user_router = APIRouter()

@user_router.post('/register')
async def register_user(user_data:UserSchema, user_dal:UserDAL = Depends(get_user_dal)):
    await user_dal.register_user(user_data)
    return {"message":"Вы успешно зарегестрировались"}


@user_router.post('/login')
async def login_user(user_data:UserSchema, user_dal:UserDAL = Depends(get_user_dal)):
    token = await user_dal.login(user_data)
    return token


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_dal: Annotated[UserDAL, Depends(get_user_dal)],
):
    return await user_dal.get_current_user(token)

