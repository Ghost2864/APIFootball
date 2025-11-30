from schema.user import UserSchema
from dal.userDAL import UserDAL,get_user_dal
from fastapi import Depends,APIRouter



user_router = APIRouter()

@user_router.post('/register')
async def register_user(user_data:UserSchema, user_dal:UserDAL = Depends(get_user_dal)):
    await user_dal.register_user(user_data)
    return {"message":"Вы успешно зарегестрировались"}


@user_router.post('/login')
async def login_user(user_data:UserSchema, user_dal:UserDAL = Depends(get_user_dal)):
    await user_dal.login(user_data)
    return {"message":"Вы успешно авторизировались"}