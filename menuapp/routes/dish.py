import uuid

from fastapi import APIRouter, Depends, status

from menuapp.dao.schemas import dish as d
from menuapp.services.dish import DishService, get_dish_service

dish_route = APIRouter()


@dish_route.get(
    "/dishes",
    response_model=list[d.DishRead],
    summary='get dishes',
    description='returns response all dishes or empty list',
    status_code=status.HTTP_200_OK
)
def get_all_dishes(
        submenu_id: uuid.UUID,
        dish_service: DishService = Depends(get_dish_service)
) -> list[d.DishRead]:
    dishes = dish_service.get_all(submenu_id=submenu_id)

    if not dishes:
        return []

    return dishes


@dish_route.get(
    "/dishes/{dish_id}",
    response_model=d.DishRead,
    summary='get single dish by id',
    description='returns detailed response a dish by id',
    status_code=status.HTTP_200_OK
)
def get_dish_by_id(
        dish_id: uuid.UUID,
        dish_service: DishService = Depends(get_dish_service)
) -> d.DishRead:
    return dish_service.get_single_by_id(dish_id=dish_id)


@dish_route.post(
    "/dishes",
    response_model=d.DishRead,
    summary='create new dish',
    description='return detailed response with a new dish',
    status_code=status.HTTP_201_CREATED
)
def create_dish(
        submenu_id: uuid.UUID,
        create_data: d.DishCreate,
        dish_service: DishService = Depends(get_dish_service)
) -> d.DishCreate:
    return dish_service.create(
        submenu_id=submenu_id,
        create_data=create_data
    )


@dish_route.patch(
    "/dishes/{dish_id}",
    response_model=d.DishRead,
    summary='update dish by id',
    description='returns detailed response with updated dish',
    status_code=status.HTTP_200_OK
)
def update_dish_by_id(
        dish_id: uuid.UUID,
        update_data: d.DishUpdate,
        dish_service: DishService = Depends(get_dish_service)
) -> d.DishUpdate:
    return dish_service.update(
        dish_id=dish_id,
        update_data=update_data
    )


@dish_route.delete(
    "/dishes/{dish_id}",
    summary='delete dish by id',
    description='delete dish by id, return status response information',
    status_code=status.HTTP_200_OK
)
def delete_dish_by_id(
        dish_id: uuid.UUID,
        dish_service: DishService = Depends(get_dish_service)
) -> str:
    dish_service.delete(dish_id=dish_id)

    return f"dish {dish_id} was deleted"
