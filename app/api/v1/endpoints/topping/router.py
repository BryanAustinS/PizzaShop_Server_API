import uuid
import logging
from typing import List

from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import app.api.v1.endpoints.topping.crud as topping_crud
from app.api.v1.endpoints.topping.schemas import ToppingSchema, ToppingCreateSchema, ToppingListItemSchema
from app.database.connection import SessionLocal

router = APIRouter()

TOPPING_NOT_FOUND = 'ToppingNotFound'


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('', response_model=List[ToppingListItemSchema], tags=['topping'])
def get_all_toppings(db: Session = Depends(get_db)):
    toppings = topping_crud.get_all_toppings(db)
    return toppings


@router.post('', response_model=ToppingSchema, status_code=status.HTTP_201_CREATED, tags=['topping'])
def create_topping(topping: ToppingCreateSchema,
                   request: Request,
                   db: Session = Depends(get_db),
                   ):
    topping_found = topping_crud.get_topping_by_name(topping.name, db)

    if topping_found:
        url = request.url_for('get_topping', topping_id=topping_found.id)
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

    new_topping = topping_crud.create_topping(topping, db)
    return new_topping


@router.put('/{topping_id}', response_model=ToppingSchema, tags=['topping'])
def update_topping(
        topping_id: uuid.UUID,
        changed_topping: ToppingCreateSchema,
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
):
    topping_found = topping_crud.get_topping_by_id(topping_id, db)
    updated_topping = None

    if topping_found:
        if topping_found.name == changed_topping.name:
            topping_crud.update_topping(topping_found, changed_topping, db)
            logging.info('Topping updated with topping name {}'.format(topping_found.name))
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            topping_name_found = topping_crud.get_topping_by_name(changed_topping.name, db)
            if topping_name_found:
                url = request.url_for('get_topping', topping_id=topping_name_found.id)
                return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
            else:
                updated_topping = topping_crud.create_topping(changed_topping, db)
                response.status_code = status.HTTP_201_CREATED
    else:
        logging.error('Topping could not be found and could not be updated. Id: {}'.format(topping_id))
        raise HTTPException(status_code=404, detail=TOPPING_NOT_FOUND)
    logging.info('Topping updated with topping name {}'.format(updated_topping.name))
    return updated_topping


@router.get('/{topping_id}', response_model=ToppingSchema, tags=['topping'])
def get_topping(topping_id: uuid.UUID,
                response: Response,
                db: Session = Depends(get_db),
                ):
    topping = topping_crud.get_topping_by_id(topping_id, db)

    if not topping:
        logging.error('Topping could not be found and could not be retrieved. Id: {}'.format(topping_id))
        raise HTTPException(status_code=404, detail=TOPPING_NOT_FOUND)
    return topping


@router.delete('/{topping_id}', response_model=None, tags=['topping'])
def delete_topping(topping_id: uuid.UUID, db: Session = Depends(get_db)):
    topping = topping_crud.get_topping_by_id(topping_id, db)

    if not topping:
        logging.error('Topping could not be found and could not be deleted. Id: {}'.format(topping_id))
        raise HTTPException(status_code=404, detail=TOPPING_NOT_FOUND)
    topping_crud.delete_topping_by_id(topping_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
