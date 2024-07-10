import uuid

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    pass


class UserTestSchema(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserSchema(UserBaseSchema):
    id: uuid.UUID
