import pytest

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


def test_dough_create_read_delete(db):
    number_of_doughs_before = len(dough_crud.get_all_doughs(db))

    new_dough_name = 'Test doughs name'
    new_dough_price = 10
    new_dough_description = 'Test doughs desc'
    new_dough_stock = 100

    update_dough_name = 'Test updated dough name'
    update_dough_price = 6
    update_dough_description = 'Test updated dough description'
    update_dough_stock = 50

    dough_create = DoughCreateSchema(name=new_dough_name, price=new_dough_price,
                                     description=new_dough_description, stock=new_dough_stock)
    dough_update = DoughCreateSchema(name=update_dough_name, price=update_dough_price,
                                     description=update_dough_description, stock=update_dough_stock)

    # Act: Add dough to database
    db_dough = dough_crud.create_dough(dough_create, db)
    created_dough_id = db_dough.id

    # Assert: One more dough in database
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == number_of_doughs_before + 1

    # Act: Re-read dough from database
    read_dough = dough_crud.get_dough_by_id(created_dough_id, db)

    # Assert: Correct dough was stored in database
    assert read_dough.id == created_dough_id
    assert read_dough.name == new_dough_name

    assert read_dough.price == new_dough_price
    assert read_dough.description == new_dough_description
    assert read_dough.stock == new_dough_stock

    # Act: Update dough
    dough_crud.update_dough(read_dough, dough_update, db)

    # Assert: Correct dough name was updated
    updated_dough = dough_crud.get_dough_by_id(created_dough_id, db)
    assert updated_dough.name == update_dough_name
    assert updated_dough.price == update_dough_price
    assert updated_dough.description == update_dough_description
    assert updated_dough.stock == update_dough_stock

    # Act: Delete dough
    dough_crud.delete_dough_by_id(created_dough_id, db)

    # Assert: Correct number of doughs in database after deletion
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == number_of_doughs_before

    # Assert: Correct dough was deleted from database
    deleted_dough = dough_crud.get_dough_by_id(created_dough_id, db)
    assert deleted_dough is None
