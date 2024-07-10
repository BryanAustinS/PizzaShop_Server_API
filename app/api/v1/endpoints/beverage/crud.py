import uuid
import logging

from sqlalchemy.orm import Session

from app.api.v1.endpoints.beverage.schemas import BeverageCreateSchema
from app.database.models import Beverage


def create_beverage(schema: BeverageCreateSchema, db: Session):
    entity = Beverage(**schema.dict())
    db.add(entity)
    db.commit()
    logging.info('Beverage created with name {} with id: {} with stock: {}'.format(entity.name, entity.id,
                                                                                   entity.stock))
    return entity


def get_beverage_by_id(beverage_id: uuid.UUID, db: Session):
    entity = db.query(Beverage).filter(Beverage.id == beverage_id).first()
    logging.info('Get beverage by id successful with id{}'.format(beverage_id))
    return entity


def get_beverage_by_name(beverage_name: str, db: Session):
    entity = db.query(Beverage).filter(Beverage.name == beverage_name).first()
    logging.info('Get beverage by name successful with name{}'.format(beverage_name))

    return entity


def get_all_beverages(db: Session):
    logging.info('Get all beverages done')
    return db.query(Beverage).all()


def update_beverage(beverage: Beverage, changed_beverage: BeverageCreateSchema, db: Session):
    for key, value in changed_beverage.dict().items():
        setattr(beverage, key, value)

    db.commit()
    db.refresh(beverage)
    logging.info(
        f'Beverage updated with beverage id {beverage.id} from name: {beverage.name} to name: {changed_beverage.name}')

    return beverage


def delete_beverage_by_id(beverage_id: uuid.UUID, db: Session):
    entity = get_beverage_by_id(beverage_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Delete beverage by id successful with id{}'.format(beverage_id))
