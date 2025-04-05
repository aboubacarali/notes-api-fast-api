from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    id: int = Field(default=None)
    email: str = Field(default=None)
    password: str = Field(default=None)

class UserRequest(BaseModel):
    email: str = Field(default=None)
    password: str = Field(default=None)

class UserMeta(BaseModel):
    status: int
    success: bool
    message: str

class ReturnUser(UserSchema):
    id: int
    email: str
    token: str

class UserResponse(BaseModel):
    meta: UserMeta
    user: ReturnUser

    class Config:
        form_attributes = True