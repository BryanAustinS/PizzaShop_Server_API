import uuid
import logging

from sqlalchemy.orm import Session

from app.api.v1.endpoints.sauce.schemas import SauceCreateSchema
from app.database.models import Sauce


def create_sauce(schema: SauceCreateSchema, db: Session):
    entity = Sauce(**schema.dict())
    db.add(entity)
    db.commit()
    logging.info('Sauce created with name {}'.format(entity.name))
    return entity


def get_sauce_by_id(sauce_id: uuid.UUID, db: Session):
    entity = db.query(Sauce).filter(Sauce.id == sauce_id).first()
    logging.info('Get Sauce by id successful with id {}'.format(sauce_id))
    return entity


def get_sauce_by_name(sauce_name: str, db: Session):
    entity = db.query(Sauce).filter(Sauce.name == sauce_name).first()
    if entity:
        logging.info('Get sauce by name successful with name: {} from topping id: {}'.format(sauce_name, entity.id))
    else:
        logging.info('No sauce found with name {}'.format(sauce_name))
    return entity


def get_all_sauce(db: Session):
    return db.query(Sauce).all()


def update_sauce(sauce: Sauce, changed_sauce: SauceCreateSchema, db: Session):
    for key, value in changed_sauce.dict().items():
        setattr(sauce, key, value)

    db.commit()
    db.refresh(sauce)
    logging.info('Sauce updated from sauce name: {} to sauce name: {} that has amount of stock: {}'.format(
        sauce.name, changed_sauce.name, changed_sauce.stock,
    ))
    return sauce


def delete_sauce_by_id(sauce_id: uuid.UUID, db: Session):
    entity = get_sauce_by_id(sauce_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Delete sauce by id successful with id {}'.format(sauce_id))
