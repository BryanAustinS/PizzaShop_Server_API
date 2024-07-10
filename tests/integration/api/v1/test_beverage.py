import pytest

import app.api.v1.endpoints.beverage.crud as beverage_crud
from app.api.v1.endpoints.beverage.schemas import BeverageCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_beverage_create_read_delete(db):
    new_beverage_name = 'test'
    new_beverage_price = 8
    new_beverage_description = 'Pepsi'
    new_beverage_stock = 10
    number_of_beverages_before = len(beverage_crud.get_all_beverages(db))
    update_beverage_name = 'Cola'
    update_beverage_price = 8.5
    update_beverage_description = 'Cola'
    update_beverage_stock = 25

    # Arrange: Instantiate a new beverage object
    beverage_create = BeverageCreateSchema(name=new_beverage_name,
                                           price=new_beverage_price,
                                           description=new_beverage_description,
                                           stock=new_beverage_stock)

    beverage_update = BeverageCreateSchema(name=update_beverage_name,
                                           price=update_beverage_price,
                                           description=update_beverage_description,
                                           stock=update_beverage_stock)

    # Act: Add beverage to database
    db_beverage = beverage_crud.create_beverage(beverage_create, db)
    created_beverage_id = db_beverage.id

    # Assert: One more beverage in database
    beverages = beverage_crud.get_all_beverages(db)
    assert len(beverages) == number_of_beverages_before + 1

    # Act: Re-read beverage from database
    read_beverage = beverage_crud.get_beverage_by_id(created_beverage_id, db)

    # Assert: Correct beverage was stored in database
    assert read_beverage.id == created_beverage_id
    assert read_beverage.name == new_beverage_name

    # Act: Update Beverage
    beverage_crud.update_beverage(read_beverage, beverage_update, db)

    # Assert: Correct beverage name was updated
    assert beverage_crud.get_beverage_by_name(update_beverage_name, db) == read_beverage

    # Act: Delete beverage
    beverage_crud.delete_beverage_by_id(created_beverage_id, db)

    # Assert: Correct number of beverage in database after deletion
    beverages = beverage_crud.get_all_beverages(db)
    assert len(beverages) == number_of_beverages_before

    # Assert: Correct user was deleted from database
    deleted_beverage = beverage_crud.get_beverage_by_id(created_beverage_id, db)
    assert deleted_beverage is None
