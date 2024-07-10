import uuid

from pydantic import BaseModel


class ToppingBaseSchema(BaseModel):
    name: str
    price: float
    description: str

    class Config:
        orm_mode = True


class ToppingCreateSchema(ToppingBaseSchema):
    stock: int


class ToppingTestSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ToppingSchema(ToppingCreateSchema):
    id: uuid.UUID


class ToppingListItemSchema(BaseModel):
    id: uuid.UUID
    name: str
    price: float
    description: str

    class Config:
        orm_mode = True
