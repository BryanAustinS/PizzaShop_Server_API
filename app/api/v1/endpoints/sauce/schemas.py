import uuid

from pydantic import BaseModel


class SauceBaseSchema(BaseModel):
    name: str
    price: float
    description: str

    class Config:
        orm_mode = True


class SauceCreateSchema(SauceBaseSchema):
    stock: int


class SauceTestSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class SauceSchema(SauceCreateSchema):
    id: uuid.UUID


class SauceListItemSchema(BaseModel):
    id: uuid.UUID
    name: str
    price: float
    description: str

    class Config:
        orm_mode = True
