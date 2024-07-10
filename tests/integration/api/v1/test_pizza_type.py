import pytest

import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeCreateSchema
import app.api.v1.endpoints.dough.crud as dough_crud
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema

from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_pizza_type_create(db):
    # We need a dough object for PizzaTypeCreateSchema
    new_dough_name = 'DoughName_TEST'
    new_dough_price = 5.0
    new_dough_description = 'DoughDesc_TEST'
    new_dough_stock = 10
    dough_create = DoughCreateSchema(name=new_dough_name,
                                     price=new_dough_price,
                                     description=new_dough_description,
                                     stock=new_dough_stock)
    db_dough = dough_crud.create_dough(dough_create, db)
    new_dough_id = db_dough.id

    # Now pizza type
    new_pizza_type_name = 'test p_type name'
    new_pizza_type_price = 9
    new_pizza_type_description = 'test p_type desc'
    new_pizza_type_dough_id = new_dough_id
    number_of_pizza_types_before = len(pizza_type_crud.get_all_pizza_types(db))

    update_pizza_type_name = 'UPDATED p_type name'
    update_pizza_type_price = 10
    update_pizza_type_dough_id = new_dough_id
    update_pizza_type_description = 'UPDATED p_type desc'

    # Arrange: make new pizza type object
    pizza_type_create = PizzaTypeCreateSchema(name=new_pizza_type_name,
                                              price=new_pizza_type_price,
                                              description=new_pizza_type_description,
                                              dough_id=new_pizza_type_dough_id)
    pizza_type_update = PizzaTypeCreateSchema(name=update_pizza_type_name,
                                              price=update_pizza_type_price,
                                              description=update_pizza_type_description,
                                              dough_id=update_pizza_type_dough_id)

    # Act: add pizza type to database
    db_pizza_types = pizza_type_crud.create_pizza_type(pizza_type_create, db)
    created_pizza_types_id = db_pizza_types.id

    # Assert: one more pizza type in database
    pizza_types = pizza_type_crud.get_all_pizza_types(db)
    assert len(pizza_types) == number_of_pizza_types_before + 1

    # Act: re read pizza type form database
    read_pizza_type = pizza_type_crud.get_pizza_type_by_id(created_pizza_types_id, db)

    # Assert: correct pizza type was stored in database
    assert read_pizza_type.id == created_pizza_types_id
    assert read_pizza_type.name == new_pizza_type_name
    assert read_pizza_type.dough_id == new_pizza_type_dough_id

    # Act: update pizza type
    pizza_type_crud.update_pizza_type(read_pizza_type, pizza_type_update, db)

    # Assert: correct pizza type was updated
    updated_pizza_type = pizza_type_crud.get_pizza_type_by_name(update_pizza_type_name, db)
    assert updated_pizza_type is not None
    assert updated_pizza_type.name == update_pizza_type_name
    assert updated_pizza_type.dough_id == update_pizza_type_dough_id

    # Act: delete pizza type
    pizza_type_crud.delete_pizza_type_by_id(created_pizza_types_id, db)

    # Assert: correct number of pizza types in database after deletion
    pizza_types = pizza_type_crud.get_all_pizza_types(db)
    assert len(pizza_types) == number_of_pizza_types_before

    # Assert: correct pizza type is deleted in db
    deleted_pizza_type = pizza_type_crud.get_pizza_type_by_id(created_pizza_types_id, db)
    assert deleted_pizza_type is None

    # Assert: delete dough
    dough_crud.delete_dough_by_id(new_dough_id, db)

    # Check that dough is deleted
    deleted_dough = dough_crud.get_dough_by_id(new_dough_id, db)
    assert deleted_dough is None
