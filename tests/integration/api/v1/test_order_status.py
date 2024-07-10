import pytest

import app.api.v1.endpoints.user.crud as user_crud
import app.api.v1.endpoints.order.crud as order_crud
from app.api.v1.endpoints.user.schemas import UserCreateSchema
from app.api.v1.endpoints.order.schemas import OrderCreateSchema, OrderStatus
from app.api.v1.endpoints.order.address.schemas import AddressCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_order_create_read_delete(db):
    new_street = 'street'
    new_post_code = '123456'
    new_house_number = 1
    new_country = 'country'
    new_town = 'town'
    new_first_name = 'first'
    new_last_name = 'last'
    new_user_name = 'test'

    number_of_users_before = len(user_crud.get_all_users(db))
    number_of_orders_before = len(order_crud.get_all_orders(db))

    user = UserCreateSchema(username=new_user_name)
    db_user = user_crud.create_user(user, db)
    created_user_id = db_user.id
    order_status_transmitted = OrderStatus.TRANSMITTED
    order_status_preparing = OrderStatus.PREPARING

    order = OrderCreateSchema(address=AddressCreateSchema(street=new_street, post_code=new_post_code,
                                                          house_number=new_house_number, country=new_country,
                                                          town=new_town,
                                                          first_name=new_first_name, last_name=new_last_name),
                              user_id=created_user_id)

    # Act: Add order to database
    db_order_status = order_crud.create_order(order, db)
    created_order_id = db_order_status.id

    # Assert: One more order and one more user in database
    orders = order_crud.get_all_orders(db)
    users = user_crud.get_all_users(db)
    assert len(orders) == number_of_orders_before + 1
    assert len(users) == number_of_users_before + 1

    # Act: Re-read order from database
    read_order = order_crud.get_order_by_id(created_order_id, db)

    # Assert: Correct order was stored in database
    assert read_order.id == created_order_id

    # Act: Read number of order by status TRANSMITTED
    read_orders_transmitted = order_crud.get_all_order_by_status(order_status_transmitted, db)

    # Assert: Correct number of order by status TRANSMITTED
    assert len(read_orders_transmitted) == number_of_orders_before + 1

    # Act: Update order status
    preparing_order = order_crud.update_order_status(read_order, order_status_preparing, db)

    # Assert: Correct order's status was updated
    assert preparing_order.order_status == order_status_preparing

    # Act: Read number of order by status PREPARING
    read_orders_preparing = order_crud.get_all_order_by_status(order_status_preparing, db)

    # Assert: Correct number of order by status PREPARING
    assert len(read_orders_preparing) == 1

    # Act: Delete order
    order_crud.delete_order_by_id(created_order_id, db)

    # Assert: Correct number of orders in database after deletion
    orders = order_crud.get_all_orders(db)
    assert len(orders) == number_of_orders_before

    # Assert: Correct order was deleted from database
    deleted_order = order_crud.get_order_by_id(created_order_id, db)
    assert deleted_order is None
