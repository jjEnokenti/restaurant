import uuid

from fastapi import HTTPException, status, Depends

from menuapp.dao.schemas.dish import DishRead, DishCreate, DishUpdate
from menuapp.dao.dish import DishDao, get_dish_dao
from menuapp.exceptions.not_existent import ItemNotFound

__all__ = (
    'DishService',
    'get_dish_service',
)


class DishService:

    def __init__(self, dao: DishDao):
        self.dao = dao

    def get_all(self, submenu_id: uuid.UUID) -> list[DishRead]:
        """ get all dishes """

        try:
            with self.dao.session.begin():
                dishes = self.dao.get_all(
                    submenu_id=submenu_id
                )

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f"error message: {e}")
        else:
            return dishes

    def get_single_by_id(self, dish_id: uuid.UUID) -> DishRead:
        """ get single dish by id """

        try:
            with self.dao.session.begin():
                dish = self.dao.get_single_by_id(
                    dish_id=dish_id
                )

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f"error message: {e}")
        else:
            if not dish:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="dish not found")

            return dish

    def create(
            self,
            submenu_id: uuid.UUID,
            create_data: DishCreate
    ) -> DishCreate:
        """ insert new dish """

        try:
            with self.dao.session.begin():
                new_dish = self.dao.create(
                    submenu_id=submenu_id,
                    data=create_data
                )

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f"error message: {e}")
        else:
            return new_dish

    def update(
            self,
            dish_id: uuid.UUID,
            update_data: DishUpdate
    ) -> DishUpdate:
        """ update single dish by id """

        try:
            with self.dao.session.begin():
                updated_dish = self.dao.update(
                    dish_id=dish_id,
                    data=update_data
                )

            if updated_dish:
                raise ItemNotFound(f"dish with: id {dish_id} not found")

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f"error message: {e}")
        else:
            return updated_dish

    def delete(self, dish_id: uuid.UUID):
        """ delete single dish by id """

        try:
            with self.dao.session.begin():
                is_deleted = self.dao.delete(
                    dish_id=dish_id
                )

            if not is_deleted:
                raise ItemNotFound(f"dish with: id {dish_id} not found")

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f"error message: {e}")


def get_dish_service(
        dao: DishDao = Depends(get_dish_dao)
) -> DishService:
    return DishService(dao=dao)
