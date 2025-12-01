from pydantic import BaseModel


class UserSchema(BaseModel):
    login:str
    password:str




class UserResponse(BaseModel):
    login:str | None

    class Config:
        from_attributes = True