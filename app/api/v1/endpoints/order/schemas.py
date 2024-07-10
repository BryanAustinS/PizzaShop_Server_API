import datetime
import uuid
from enum import Enum

from pydantic import BaseModel

from app.api.v1.endpoints.beverage.schemas import BeverageBaseSchema
from app.api.v1.endpoints.order.address.schemas import AddressCreateSchema, AddressSchema
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeBaseSchema


class OrderStatus(str, Enum):
    TRANSMITTED = 'TRANSMITTED'
    PREPARING = 'PREPARING'
    IN_DELIVERY = 'IN_DELIVERY'
    COMPLETED = 'COMPLETED'


class OrderBaseSchema(BaseModel):
    class Config:
        orm_mode = True


class OrderCreateSchema(OrderBaseSchema):
    address: AddressCreateSchema
    user_id: uuid.UUID


class OrderSchema(OrderCreateSchema):
    order_status: OrderStatus
    id: uuid.UUID
    order_datetime: datetime.datetime
    address: AddressSchema


class OrderPriceSchema(OrderBaseSchema):
    price: float


class PizzaBaseSchema(BaseModel):
    class Config:
        orm_mode = True


class PizzaCreateSchema(PizzaBaseSchema):
    pizza_type_id: uuid.UUID


class PizzaSchema(PizzaCreateSchema):
    id: uuid.UUID


class PizzaWithoutPizzaTypeSchema(PizzaBaseSchema):
    id: uuid.UUID


class JoinedPizzaPizzaTypeSchema(PizzaWithoutPizzaTypeSchema, PizzaTypeBaseSchema):
    pass


class JoinedPizzaSpecialWishPizzaSchema(PizzaWithoutPizzaTypeSchema):
    pass


class OrderBeverageQuantityBaseSchema(BaseModel):
    quantity: int

    class Config:
        orm_mode = True


class OrderBeverageQuantityCreateSchema(OrderBeverageQuantityBaseSchema):
    beverage_id: uuid.UUID


class JoinedOrderBeverageQuantitySchema(OrderBaseSchema, BeverageBaseSchema):
    pass


class OrderUpdateOrderStatusSchema(OrderBaseSchema):
    id: uuid.UUID
    order_status: OrderStatus
