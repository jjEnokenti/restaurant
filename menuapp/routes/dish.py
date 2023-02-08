import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import menuapp.services.dish as dish_service
from menuapp.dependences import get_db
from menuapp.dao.schemas import dish as d

dish_route = APIRouter()


@dish_route.get(
    "/dishes",
    response_model=list[d.DishRead],
    status_code=status.HTTP_200_OK
)
def get_all_dishes(
        submenu_id: uuid.UUID,
        db: Session = Depends(get_db)
):
    """
    get all dishes
    """
    dishes = dish_service.get_all(db, submenu_id)
    if not dishes:
        return []

    return dishes


@dish_route.get(
    "/dishes/{dish_id}",
    response_model=d.DishRead,
    status_code=status.HTTP_200_OK
)
def get_dish_by_id(dish_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    get single dish by id
    """

    return dish_service.get_single_by_id(db, dish_id)


@dish_route.post(
    "/dishes",
    response_model=d.DishRead,
    status_code=status.HTTP_201_CREATED
)
def create_dish(
        submenu_id: uuid.UUID,
        create_data: d.DishCreate,
        db: Session = Depends(get_db)
):
    """
    create new dish
    """

    return dish_service.create(db, submenu_id, create_data)


@dish_route.patch(
    "/dishes/{dish_id}",
    response_model=d.DishRead,
    status_code=status.HTTP_200_OK
)
def update_dish_by_id(
        dish_id: uuid.UUID,
        update_data: d.DishUpdate,
        db: Session = Depends(get_db)
):
    """
    update dish by id
    """

    return dish_service.update(db, dish_id, update_data)


@dish_route.delete(
    "/dishes/{dish_id}",
    status_code=status.HTTP_200_OK
)
def delete_dish_by_id(
        dish_id: uuid.UUID,
        db: Session = Depends(get_db)
):
    """
    delete dish by id
    """
    dish_service.delete(db, dish_id)

    return f"dish {dish_id} was deleted"
