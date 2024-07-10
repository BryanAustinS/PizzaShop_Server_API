import logging
import uuid
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.v1.endpoints.order.address.crud import create_address
from app.api.v1.endpoints.order.schemas import \
    JoinedPizzaPizzaTypeSchema, OrderBeverageQuantityCreateSchema, OrderCreateSchema
from app.database.models import Order, Pizza, PizzaType, OrderBeverageQuantity, Beverage, OrderStatus


def create_order(schema: OrderCreateSchema, db: Session):
    address = create_address(schema.address, db)
    order = Order(user_id=schema.user_id)
    order.address = address
    order.order_status = OrderStatus.TRANSMITTED
    db.add(order)
    db.commit()
    logging.info('Order created with id, status, address id : {}, status: {}, address id: {}'
                 .format(order.id, order.order_status.name, order.address_id))
    return order


def get_order_by_id(order_id: uuid.UUID, db: Session):
    entity = db.query(Order).filter(Order.id == order_id).first()
    logging.info('Get beverage by id successful with id {}'.format(order_id))
    return entity


def get_all_order_by_status(order_status: OrderStatus, db: Session):
    entities = db.query(Order).filter(Order.order_status == order_status)
    return_list = []

    for order in entities.all():
        return_list.append(order)

    logging.info('Get all order by status: {}'.format(order_status))
    return return_list


def get_all_orders(db: Session):
    entities = db.query(Order).all()
    logging.info('Get all beverages done')
    return entities


def delete_order_by_id(order_id: uuid.UUID, db: Session):
    entity = get_order_by_id(order_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Delete beverage by id successful with id{}'.format(order_id))


def update_order_status(order: Order, changed_order: OrderStatus, db: Session):
    setattr(order, 'order_status', changed_order)
    db.commit()
    db.refresh(order)
    logging.info('Update order status from: {} to {}'.format(order.order_status, changed_order))
    return order


def create_pizza(pizza_type: PizzaType,
                 db: Session):
    entity = Pizza()
    if pizza_type:
        entity.pizza_type_id = pizza_type.id
    db.add(entity)
    db.commit()
    logging.info(
        f'Pizza created with id: {entity.id}, pizza type name: {pizza_type.name}, dough id: {pizza_type.dough.id}')
    return entity


def add_pizza_to_order(order: Order, pizza_type: PizzaType,
                       db: Session):
    pizza = create_pizza(pizza_type, db)
    order.pizzas.append(pizza)
    db.commit()
    db.refresh(order)
    logging.info('Pizza with id: {} added to order with id: {}'.format(pizza.id, order.id))
    return pizza


def get_pizza_by_id(pizza_id: uuid.UUID, db):
    entity = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    logging.info('Get beverage by id with id {}'.format(pizza_id))
    return entity


def get_all_pizzas_of_order(order: Order, db: Session):
    pizza_types = db.query(Pizza.id, PizzaType.name, PizzaType.price, PizzaType.description, PizzaType.dough_id) \
        .join(Pizza.pizza_type) \
        .filter(Pizza.order_id == order.id)

    returnlist: List[JoinedPizzaPizzaTypeSchema] = []
    for pizza_type in pizza_types.all():
        returnlist.append(pizza_type)
    logging.info('Get all pizzas done')
    return returnlist


def delete_pizza_from_order(order: Order, pizza_id: uuid.UUID, db: Session):
    entity = db.query(Pizza).filter(Pizza.order_id == order.id, Pizza.id == pizza_id).first()
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Pizza with id: {} deleted from order with id: {}'.format(pizza_id, order.id))
        return True
    else:
        return False


def create_beverage_quantity(
        order: Order,
        schema: OrderBeverageQuantityCreateSchema,
        db: Session,
):
    entity = OrderBeverageQuantity(**schema.dict())
    order.beverages.append(entity)
    db.commit()
    db.refresh(order)
    logging.info('Create Beverage quantity with id: {}, added to order with id: {}'
                 .format(entity.beverage_id, order.id))
    return entity


def get_beverage_quantity_by_id(
        order_id: uuid.UUID,
        beverage_id: uuid.UUID,
        db: Session,
):
    entity = db.query(OrderBeverageQuantity) \
        .filter(OrderBeverageQuantity.beverage_id == beverage_id,
                OrderBeverageQuantity.order_id == order_id) \
        .first()
    logging.info('Get Beverage Quantity with id: {}, found for order with id: {}'
                 .format(beverage_id, order_id))
    return entity


def get_joined_beverage_quantities_by_order(
        order_id: uuid.UUID,
        db: Session,
):
    entities = db.query(OrderBeverageQuantity) \
        .filter(OrderBeverageQuantity.order_id == order_id)
    return entities.all()


def update_beverage_quantity_of_order(order_id: uuid.UUID, beverage_id: uuid.UUID, new_quantity: int, db: Session):
    order_beverage = db.query(OrderBeverageQuantity).filter(order_id == OrderBeverageQuantity.order_id,
                                                            beverage_id == OrderBeverageQuantity.beverage_id).first()
    if order_beverage:
        setattr(order_beverage, 'quantity', new_quantity)
        db.commit()
        db.refresh(order_beverage)
        logging.info('Update Quantity of beverage with id: {} from order with id: {}, from quantity: {}, to quantity: '
                     '{} '.format(beverage_id, order_id, order_beverage.quantity, new_quantity))
    return order_beverage


def delete_beverage_from_order(order_id: uuid.UUID, beverage_id: uuid.UUID, db: Session):
    entity = db.query(OrderBeverageQuantity).filter(order_id == OrderBeverageQuantity.order_id,
                                                    beverage_id == OrderBeverageQuantity.beverage_id).first()
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Beverage with id: {} deleted from order with id: {}'.format(beverage_id, order_id))
        return True
    else:
        return False


def get_price_of_order(
        order_id: uuid.UUID,
        db: Session,
):
    price_beverage: float = 0
    for row in db.query(Beverage.price, OrderBeverageQuantity.quantity) \
            .join(OrderBeverageQuantity) \
            .join(Order) \
            .filter(Order.id == order_id):
        price_beverage += (row.price * row.quantity)

    price_pizza = db.query(func.sum(PizzaType.price)) \
        .join(Pizza) \
        .join(Order) \
        .filter(Order.id == order_id).first()[0]

    # If order has no pizzas, only beverage
    if price_pizza is None:
        return price_beverage

    # if order has pizza and beverage, return the price of pizza + beverage
    if price_pizza is not None:
        return price_pizza + price_beverage
