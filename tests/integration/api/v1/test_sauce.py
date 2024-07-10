import pytest

import app.api.v1.endpoints.sauce.crud as sauce_crud
from app.api.v1.endpoints.sauce.schemas import SauceCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_topping_create_read_delete(db):
    number_of_sauce_before = len(sauce_crud.get_all_sauce(db))

    new_sauce_name = 'Test Sauce name'
    new_sauce_price = 10
    new_sauce_description = 'Test sauce description'

    update_sauce_name = 'Test updated sauce name'
    update_sauce_price = 6
    update_sauce_description = 'Test updated sauce description'

    stock = 5

    # Arrange: Instantiate a new topping object
    sauce_create = SauceCreateSchema(name=new_sauce_name, price=new_sauce_price,
                                     description=new_sauce_description, stock=stock)

    sauce_update = SauceCreateSchema(name=update_sauce_name, price=update_sauce_price,
                                     description=update_sauce_description, stock=stock)

    # Act: Add sauce to database
    db_sauce = sauce_crud.create_sauce(sauce_create, db)
    created_sauce_id = db_sauce.id

    # Assert: One more sauce in database
    sauces = sauce_crud.get_all_sauce(db)
    assert len(sauces) == number_of_sauce_before + 1

    # Act: Re-read sauce from database
    read_sauce = sauce_crud.get_sauce_by_id(created_sauce_id, db)

    # Assert: Correct sauce was stored in database
    assert read_sauce.id == created_sauce_id
    assert read_sauce.name == new_sauce_name
    assert read_sauce.price == new_sauce_price
    assert read_sauce.description == new_sauce_description

    # Act: Update sauce
    sauce_crud.update_sauce(read_sauce, sauce_update, db)

    # Assert: Correct sauce name was updated
    updated_sauce = sauce_crud.get_sauce_by_name(update_sauce_name, db)
    assert updated_sauce is not None
    assert updated_sauce.name == update_sauce_name
    assert updated_sauce.price == update_sauce_price
    assert updated_sauce.description == update_sauce_description

    # Act: Delete topping
    sauce_crud.delete_sauce_by_id(created_sauce_id, db)

    # Assert: Correct number of toppings in database after deletion
    sauces = sauce_crud.get_all_sauce(db)
    assert len(sauces) == number_of_sauce_before

    # Assert: Correct topping was deleted from database
    deleted_topping = sauce_crud.get_sauce_by_id(created_sauce_id, db)
    assert deleted_topping is None
