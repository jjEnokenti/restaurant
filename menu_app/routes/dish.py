import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import menu_app.services.dish as dish_service
from menu_app.dependences import get_db
from menu_app.schemas import dish as d


dish_route = APIRouter()


@dish_route.get("/dishes", response_model=list[d.DishRead], status_code=200)
def get_all_dishes(submenu_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    get all dishes
    """
    dishes = dish_service.get_all(db, submenu_id)
    if not dishes:
        return []

    return dishes


@dish_route.get("/dishes/{dish_id}", response_model=d.DishRead, status_code=200)
def get_dish_by_id(dish_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    get single dish by id
    """
    dish = dish_service.get_single_by_id(db, dish_id)

    return dish


@dish_route.post("/dishes", response_model=d.DishRead, status_code=201)
def create_dish(submenu_id: uuid.UUID, create_data: d.DishCreate, db: Session = Depends(get_db)):
    """
    create new dish
    """
    new_dish = dish_service.create(db, submenu_id, create_data)

    return new_dish


@dish_route.patch("/dishes/{dish_id}", response_model=d.DishRead, status_code=200)
def update_dish_by_id(dish_id: uuid.UUID, update_data: d.DishUpdate, db: Session = Depends(get_db)):
    """
    update dish by id
    """
    updated_dish = dish_service.update(db, dish_id, update_data)

    return updated_dish


@dish_route.delete("/dishes/{dish_id}", status_code=200)
def delete_dish_by_id(dish_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    delete dish by id
    """
    dish_service.delete(db, dish_id)

    return f"dish {dish_id} was deleted"
