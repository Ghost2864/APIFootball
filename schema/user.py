from pydantic import BaseModel


class UserSchema(BaseModel):
    login:str
    password:str