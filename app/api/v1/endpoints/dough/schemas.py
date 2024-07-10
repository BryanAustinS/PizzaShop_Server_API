import uuid

from pydantic import BaseModel


class DoughBaseSchema(BaseModel):
    name: str
    price: float
    description: str

    class Config:
        orm_mode = True


class DoughCreateSchema(DoughBaseSchema):
    stock: int


class DoughSchema(DoughCreateSchema):
    id: uuid.UUID


class DoughListItemSchema(BaseModel):
    id: uuid.UUID
    name: str
    price: float
    description: str

    class Config:
        orm_mode = True
