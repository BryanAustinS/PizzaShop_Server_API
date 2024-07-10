import uuid
from typing import List, TypeVar
import logging

from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import app.api.v1.endpoints.dough.crud as dough_crud
import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
import app.api.v1.endpoints.topping.crud as topping_crud
import app.api.v1.endpoints.sauce.crud as sauce_crud
from app.api.v1.endpoints.dough.schemas import DoughSchema
from app.api.v1.endpoints.pizza_type.schemas import \
    JoinedPizzaTypeQuantitySchema, \
    PizzaTypeSchema, \
    PizzaTypeCreateSchema, \
    PizzaTypeToppingQuantityCreateSchema, PizzaTypeSauceQuantityCreateSchema
from app.database.connection import SessionLocal

router = APIRouter()

PIZZA_NOT_FOUND = 'Pizza not found'  # NOSONAR
PIZZA_TOPPING_NOT_FOUND = 'Pizza topping not found'  # NOSONAR
PIZZA_TYPE_NOT_FOUND_LOG = 'Pizza type could not be found. Id: {}'
PIZZA_SAUCE_NOT_FOUND = 'Pizza sauce could not be found'


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('', response_model=List[PizzaTypeSchema], tags=['pizza_type'])
def get_all_pizza_types(db: Session = Depends(get_db)):
    pizza_types = pizza_type_crud.get_all_pizza_types(db)
    logging.info('all pizza_types retrieved successfully')
    return pizza_types


@router.post('', response_model=PizzaTypeSchema, tags=['pizza_type'])
def create_pizza_type(
        pizza_type: PizzaTypeCreateSchema, request: Request,
        response: Response, db: Session = Depends(get_db),
):
    pizza_type_found = pizza_type_crud.get_pizza_type_by_name(pizza_type.name, db)

    if pizza_type_found:
        url = request.url_for('get_pizza_type', pizza_type_id=pizza_type_found.id)
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

    dough = dough_crud.get_dough_by_id(pizza_type.dough_id, db)
    if not dough:
        logging.error('Pizza could not be created because Dough could not be found Id: {}'.format(pizza_type.dough_id))
        raise HTTPException(status_code=404, detail=PIZZA_NOT_FOUND)

    new_pizza_type = pizza_type_crud.create_pizza_type(pizza_type, db)
    response.status_code = status.HTTP_201_CREATED
    return new_pizza_type


@router.put('/{pizza_type_id}', response_model=PizzaTypeSchema, tags=['pizza_type'])
def update_pizza_type(
        pizza_type_id: uuid.UUID,
        changed_pizza_type: PizzaTypeCreateSchema,
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
):
    pizza_type_found = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)
    updated_pizza_type = None

    if pizza_type_found:
        if pizza_type_found.name == changed_pizza_type.name:
            pizza_type_crud.update_pizza_type(pizza_type_found, changed_pizza_type, db)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            pizza_type_name_found = pizza_type_crud.get_pizza_type_by_name(changed_pizza_type.name, db)
            if pizza_type_name_found:
                url = request.url_for('get_pizza_type', pizza_type_id=pizza_type_name_found.id)
                return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
            else:
                updated_pizza_type = pizza_type_crud.create_pizza_type(changed_pizza_type, db)
                response.status_code = status.HTTP_201_CREATED
    else:
        logging.error('Pizza type could not be found and could not be updated. Id: {}'.format(pizza_type_id))
        raise HTTPException(status_code=404, detail=PIZZA_NOT_FOUND)

    return updated_pizza_type


@router.get('/{pizza_type_id}', response_model=PizzaTypeSchema, tags=['pizza_type'])
def get_pizza_type(
        pizza_type_id: uuid.UUID,
        db: Session = Depends(get_db),
):
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)

    if not pizza_type:
        logging.error('Pizza type could not be found and could not be retrieved. Id: {}'.format(pizza_type_id))
        raise HTTPException(status_code=404, detail=PIZZA_NOT_FOUND)

    return pizza_type


@router.delete('/{pizza_type_id}', response_model=None, tags=['pizza_type'])
def delete_pizza_type(pizza_type_id: uuid.UUID,
                      db: Session = Depends(get_db),
                      ):
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)

    if not pizza_type:
        logging.error('Pizza type could not be found and could not be deleted. Id: {}'.format(pizza_type_id))
        raise HTTPException(status_code=404, detail=PIZZA_NOT_FOUND)

    pizza_type_crud.delete_pizza_type_by_id(pizza_type_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Due to mypy error, this workaround is needed for Union
# see pull request https://github.com/python/mypy/pull/8779
# should be fixed in near future
MyPyEitherItem = TypeVar(
    'MyPyEitherItem',
    List[PizzaTypeToppingQuantityCreateSchema],
    List[PizzaTypeSauceQuantityCreateSchema],
    List[JoinedPizzaTypeQuantitySchema],
    None,
)


@router.get(
    '/{pizza_type_id}/toppings',
    response_model=MyPyEitherItem,
    tags=['pizza_type'],
)
def get_pizza_type_toppings(
        pizza_type_id: uuid.UUID,
        response: Response,
        db: Session = Depends(get_db),
        join: bool = False,
):
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)

    if not pizza_type:
        logging.error('pizza_type could not be found and could not be retrieved id {}'.format(pizza_type_id))
        raise HTTPException(status_code=404, detail=PIZZA_NOT_FOUND)

    toppings = pizza_type.toppings
    if join:
        toppings = pizza_type_crud.get_joined_topping_quantities_by_pizza_type(pizza_type.id, db)

    return toppings


@router.post(
    '/{pizza_type_id}/toppings',
    response_model=PizzaTypeToppingQuantityCreateSchema,
    status_code=status.HTTP_201_CREATED,
    tags=['pizza_type'],
)
def create_pizza_type_topping(
        pizza_type_id: uuid.UUID,
        topping_quantity: PizzaTypeToppingQuantityCreateSchema,
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
):
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)
    if not pizza_type:
        logging.error(
            f'pizza type could not be created: id {pizza_type_id}, {topping_quantity.topping_id}')
        raise HTTPException(status_code=404, detail=PIZZA_NOT_FOUND)

    if not topping_crud.get_topping_by_id(topping_quantity.topping_id, db):
        logging.error(
            f'topping could not be found. Id: {topping_quantity.topping_id} with pizza_type id {pizza_type.id}')
        raise HTTPException(status_code=404, detail=PIZZA_TOPPING_NOT_FOUND)

    topping_quantity_found = pizza_type_crud.get_topping_quantity_by_id(pizza_type_id, topping_quantity.topping_id, db)
    if topping_quantity_found:
        url = request.url_for('get_pizza_type_toppings', pizza_type_id=topping_quantity_found.pizza_type_id)
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

    new_topping_quantity = pizza_type_crud.create_topping_quantity(pizza_type, topping_quantity, db)
    return new_topping_quantity


@router.get(
    '/{pizza_type_id}/dough',
    response_model=DoughSchema,
    tags=['pizza_type'],
)
def get_pizza_type_dough(
        pizza_type_id: uuid.UUID,
        response: Response,
        db: Session = Depends(get_db),
):
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)

    if not pizza_type:
        logging.error('dough could not be retrieved because pizza_type could not be found id {}'.format(
            pizza_type_id))
        raise HTTPException(status_code=404, detail=PIZZA_NOT_FOUND)

    dough = pizza_type.dough

    return dough


@router.get(
    '/{pizza_type_id}/sauces',
    response_model=MyPyEitherItem,
    tags=['pizza_type'],
)
def get_pizza_type_sauces(
        pizza_type_id: uuid.UUID,
        response: Response,
        db: Session = Depends(get_db),
        join: bool = False,
):
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)
    if not pizza_type:
        logging.error('pizza_type could not be found and could not be retrieved id {}'.format(pizza_type_id))
        raise HTTPException(status_code=404, detail=PIZZA_NOT_FOUND)

    sauces = pizza_type.sauces
    if not sauces:
        logging.error('Sauce cannot be retrieved')

    if join:
        sauces = pizza_type_crud.get_joined_sauce_quantities_by_pizza_type(pizza_type.id, db)

    return sauces


@router.post(
    '/{pizza_type_id}/sauces',
    response_model=PizzaTypeSauceQuantityCreateSchema,
    status_code=status.HTTP_201_CREATED,
    tags=['pizza_type'],
)
def create_pizza_type_sauce(
        pizza_type_id: uuid.UUID,
        sauce_quantity: PizzaTypeSauceQuantityCreateSchema,
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
):
    pizza_type = pizza_type_crud.get_pizza_type_by_id(pizza_type_id, db)
    if not pizza_type:
        logging.error(
            f'Pizza type could not be found id {pizza_type_id}, sauce id {sauce_quantity.sauce_id}')
        raise HTTPException(status_code=404, detail=PIZZA_NOT_FOUND)

    if not sauce_crud.get_sauce_by_id(sauce_quantity.sauce_id, db):
        logging.error(
            f'Sauce could not be found. Id: {sauce_quantity.sauce_id} with pizza_type id {pizza_type.id}')
        raise HTTPException(status_code=404, detail=PIZZA_SAUCE_NOT_FOUND)

    sauce_quantity_found = pizza_type_crud.get_sauce_quantity_by_id(pizza_type_id, sauce_quantity.sauce_id, db)
    if sauce_quantity_found:
        url = request.url_for('get_pizza_type_sauces', pizza_type_id=sauce_quantity_found.pizza_type_id)
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

    new_sauce_quantity = pizza_type_crud.create_sauce_quantity(pizza_type, sauce_quantity, db)
    return new_sauce_quantity
