import uuid
import logging

from sqlalchemy.orm import Session

from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.database.models import Dough


def create_dough(schema: DoughCreateSchema, db: Session):
    entity = Dough(**schema.dict())
    db.add(entity)
    db.commit()
    logging.info('dough created with name {} with id {} with stock {}'.format(entity.name, entity.id, entity.stock))
    return entity


def get_dough_by_id(dough_id: uuid.UUID, db: Session):
    entity = db.query(Dough).filter(Dough.id == dough_id).first()
    logging.info('Get dough by id successful with id {}'.format(dough_id))
    return entity


def get_dough_by_name(dough_name: str, db: Session):
    entity = db.query(Dough).filter(Dough.name == dough_name).first()
    logging.info('Get dough by id successful with name {}'.format(dough_name))

    return entity


def get_all_doughs(db: Session):
    logging.info('Get all dough done')
    return db.query(Dough).all()


def update_dough(dough: Dough, changed_dough: DoughCreateSchema, db: Session):
    for key, value in changed_dough.dict().items():
        setattr(dough, key, value)

    db.commit()
    db.refresh(dough)
    logging.info(
        f'Dough updated from dough name: {dough.name} from id: {dough.id} to dough name: {changed_dough.name}')
    return dough


def delete_dough_by_id(dough_id: uuid.UUID, db: Session):
    entity = get_dough_by_id(dough_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Delete dough by id successful with id {}'.format(dough_id))
