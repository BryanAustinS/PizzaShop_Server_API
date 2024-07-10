import uuid
import logging

from sqlalchemy.orm import Session

from app.api.v1.endpoints.pizza_type.schemas import \
    PizzaTypeCreateSchema, \
    PizzaTypeToppingQuantityCreateSchema, PizzaTypeSauceQuantityCreateSchema
from app.database.models import PizzaType, PizzaTypeToppingQuantity, PizzaTypeSauceQuantity


def create_pizza_type(schema: PizzaTypeCreateSchema, db: Session):
    entity = PizzaType(**schema.dict())
    db.add(entity)
    db.commit()
    logging.info(
        'pizza type created with id {} called {} and created with {}'.format(entity.id, entity.name, entity.dough),
    )
    return entity


def get_pizza_type_by_id(pizza_type_id: uuid.UUID, db: Session):
    entity = db.query(PizzaType).filter(PizzaType.id == pizza_type_id).first()
    logging.info(
        f'Get Pizza type by id successful with id {pizza_type_id}, {PizzaType.name}, {PizzaType.dough}',
    )
    return entity


def get_pizza_type_by_name(pizza_type_name: str, db: Session):
    entity = db.query(PizzaType).filter(PizzaType.name == pizza_type_name).first()
    logging.info(
        f'Get Pizza type by name successful with name {pizza_type_name}, {PizzaType.name}, {PizzaType.dough}',
    )
    return entity


def get_all_pizza_types(db: Session):
    entities = db.query(PizzaType).all()
    logging.info('Get all pizza type done')
    return entities


def update_pizza_type(pizza_type: PizzaType, changed_pizza_type: PizzaTypeCreateSchema, db: Session):
    for key, value in changed_pizza_type.dict().items():
        setattr(pizza_type, key, value)

    db.commit()
    db.refresh(pizza_type)
    logging.info(
        f'Pizza type updated with id {PizzaType.id} called {PizzaType.name} and created with {PizzaType.dough}')
    return pizza_type


def delete_pizza_type_by_id(pizza_type_id: uuid.UUID, db: Session):
    entity = get_pizza_type_by_id(pizza_type_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info(
            f'Pizza type deleted with id {PizzaType.id} called {PizzaType.name} and created with {PizzaType.dough}')


def create_topping_quantity(
        pizza_type: PizzaType,
        schema: PizzaTypeToppingQuantityCreateSchema,
        db: Session,
):
    entity = PizzaTypeToppingQuantity(**schema.dict())
    pizza_type.toppings.append(entity)
    db.commit()
    db.refresh(pizza_type)
    logging.info(
        f'Topping quantity created with topping id {entity.topping_id} pizza_type id {PizzaType.id}, {PizzaType.name},'
        f' {PizzaType.dough}')
    return entity


def get_topping_quantity_by_id(
        pizza_type_id: uuid.UUID,
        topping_id: uuid.UUID,
        db: Session,
):
    entity = db.query(PizzaTypeToppingQuantity) \
        .filter(PizzaTypeToppingQuantity.topping_id == topping_id,
                PizzaTypeToppingQuantity.pizza_type_id == pizza_type_id) \
        .first()
    return entity


def get_joined_topping_quantities_by_pizza_type(
        pizza_type_id: uuid.UUID,
        db: Session,
):
    entities = db.query(PizzaTypeToppingQuantity) \
        .filter(PizzaTypeToppingQuantity.pizza_type_id == pizza_type_id)
    return entities.all()


def create_sauce_quantity(
        pizza_type: PizzaType,
        schema: PizzaTypeSauceQuantityCreateSchema,
        db: Session,
):
    entity = PizzaTypeSauceQuantity(**schema.dict())
    pizza_type.sauces.append(entity)
    db.commit()
    db.refresh(pizza_type)
    logging.info(
        f'Sauce quantity created with sauce id {entity.sauce_id} pizza_type id {PizzaType.id}, {PizzaType.name},'
        f' {PizzaType.dough}')
    return entity


def get_sauce_quantity_by_id(
        pizza_type_id: uuid.UUID,
        sauce_id: uuid.UUID,
        db: Session,
):
    entity = db.query(PizzaTypeSauceQuantity) \
        .filter(PizzaTypeSauceQuantity.sauce_id == sauce_id,
                PizzaTypeSauceQuantity.pizza_type_id == pizza_type_id) \
        .first()
    logging.info(
        f'Sauce quantity get with sauce id {entity.sauce_id} pizza_type id {pizza_type_id},',
    )
    return entity


def get_joined_sauce_quantities_by_pizza_type(
        pizza_type_id: uuid.UUID,
        db: Session,
):
    entities = db.query(PizzaTypeSauceQuantity) \
        .filter(PizzaTypeSauceQuantity.pizza_type_id == pizza_type_id)
    return entities.all()
