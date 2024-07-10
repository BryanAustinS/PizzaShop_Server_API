import uuid

from pydantic import BaseModel


class BeverageBaseSchema(BaseModel):
    name: str
    price: float
    description: str

    class Config:
        orm_mode = True


class BeverageCreateSchema(BeverageBaseSchema):
    stock: int


class BeverageTestSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class BeverageSchema(BeverageCreateSchema):
    id: uuid.UUID


class BeverageListItemSchema(BaseModel):
    id: uuid.UUID
    name: str
    price: float
    description: str

    class Config:
        orm_mode = True
