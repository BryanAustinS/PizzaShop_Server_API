import uuid
import logging

from sqlalchemy.orm import Session

from app.api.v1.endpoints.topping.schemas import ToppingCreateSchema, ToppingListItemSchema
from app.database.models import Topping


def create_topping(schema: ToppingCreateSchema, db: Session):
    entity = Topping(**schema.dict())
    db.add(entity)
    db.commit()
    logging.info('Topping created with name {}'.format(entity.name))
    return entity


def get_topping_by_id(topping_id: uuid.UUID, db: Session):
    entity = db.query(Topping).filter(Topping.id == topping_id).first()
    logging.info('Get topping by id successful with id {}'.format(topping_id))
    return entity


def get_topping_by_name(topping_name: str, db: Session):
    entity = db.query(Topping).filter(Topping.name == topping_name).first()
    if entity:
        logging.info('Get topping by name successful with name: {} from topping id: {}'.format(topping_name, entity.id))
    else:
        logging.info('No topping found with name: {}'.format(topping_name))
    return entity


def get_all_toppings(db: Session):
    entities = db.query(Topping).all()
    if entities:
        return_entities = []  # NOSONAR
        for entity in entities:
            list_item_entity = ToppingListItemSchema(  # NOSONAR
                **{'id': entity.id, 'name': entity.name, 'price': entity.price, 'description': entity.description})
            return_entities.append(list_item_entity)
        return return_entities
    logging.info('Get all toppings done')
    return entities


def update_topping(topping: Topping, changed_topping: ToppingCreateSchema, db: Session):
    for key, value in changed_topping.dict().items():
        setattr(topping, key, value)

    db.commit()
    db.refresh(topping)
    logging.info('Topping updated from topping name: {} to topping name: {} that has amount of stock: {}'.format(
        topping.name, changed_topping.name, changed_topping.stock))
    return topping


def delete_topping_by_id(topping_id: uuid.UUID, db: Session):
    entity = get_topping_by_id(topping_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Delete topping by id successful with id{}'.format(topping_id))
