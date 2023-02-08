from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from menuapp.dao.models import dish as d

__all__ = [
    "get_all",
    "get_single_by_id",
    "create",
    "update",
    "delete"
]


def get_all(db: Session, submenu_id):
    """
    get all dishes from db
    """
    try:
        dishes = db.query(d.Dish).filter(d.Dish.submenu_id == submenu_id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
    else:
        return dishes


def get_single_by_id(db: Session, dish_id):
    """
    get single dish by id from db
    """
    try:

        dish = db.query(d.Dish).filter(d.Dish.id == dish_id).first()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
    else:
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="dish not found")

        return dish


def create(db: Session, submenu_id, create_data):
    """
    insert new dish into db
    """
    try:
        new_dish = d.Dish(**create_data.dict(), submenu_id=submenu_id)
        db.add(new_dish)
        db.commit()
        db.refresh(new_dish)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
    else:
        return new_dish


def update(db: Session, dish_id, update_data):
    """
    update single dish by id into db
    """
    try:
        dish_query = db.query(d.Dish).filter(d.Dish.id == dish_id)
        updated_dish = dish_query.first()

        if not updated_dish:
            raise ValueError(f"dish with: id {dish_id} not found")

        dish_query.update(update_data.dict(exclude_unset=True))
        db.commit()
        db.refresh(updated_dish)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
    else:
        return updated_dish


def delete(db: Session, dish_id):
    """
    delete single dish by id from db
    """
    try:
        dish = db.query(d.Dish).get(dish_id)

        if not dish:
            raise ValueError(f"dish with: id {dish_id} not found")

        db.delete(dish)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
