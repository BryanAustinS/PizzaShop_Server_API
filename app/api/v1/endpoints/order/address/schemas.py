import uuid

from pydantic import BaseModel


class AddressBaseSchema(BaseModel):
    street: str
    post_code: str
    house_number: int
    country: str
    town: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class AddressCreateSchema(AddressBaseSchema):
    pass


class AddressSchema(AddressCreateSchema):
    id: uuid.UUID
