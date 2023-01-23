from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from menu_app.models import submenu as s, dish as d


__all__ = [
    "get_all",
    "get_single_by_id",
    "create",
    "update",
    "delete"
]


def get_all(db: Session, menu_id):
    """
    get all submenus from db
    """
    try:
        submenus_query = db.query(
            s.Submenu.id,
            s.Submenu.title,
            s.Submenu.description,
            func.count(d.Dish.id).label("dishes_count")
        ). \
            group_by(s.Submenu.id). \
            outerjoin(d.Dish, d.Dish.submenu_id == s.Submenu.id). \
            filter(s.Submenu.menu_id == menu_id)

        submenus = submenus_query.all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
    else:
        return submenus


def get_single_by_id(db: Session, submenu_id):
    """
    get single submenu by id from db
    """
    try:

        submenu_query = db.query(
            s.Submenu.id,
            s.Submenu.title,
            s.Submenu.description,
            func.count(d.Dish.id).label("dishes_count")
        ). \
            group_by(s.Submenu.id). \
            outerjoin(d.Dish, d.Dish.submenu_id == s.Submenu.id). \
            filter(s.Submenu.id == submenu_id)

        submenu = submenu_query.first()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
    else:
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="submenu not found")

        return submenu


def create(db: Session, menu_id, create_data):
    """
    insert new submenu into db
    """
    try:
        new_submenu = s.Submenu(**create_data.dict(), menu_id=menu_id)
        db.add(new_submenu)
        db.commit()
        db.refresh(new_submenu)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
    else:
        return new_submenu


def update(db: Session, submenu_id, update_data):
    """
    update single submenu by id into db
    """
    try:
        submenu_query = db.query(s.Submenu).filter(s.Submenu.id == submenu_id)
        updated_submenu = submenu_query.first()

        if not updated_submenu:
            raise ValueError(f"submenu with: id {submenu_id} not found")

        submenu_query.update(update_data.dict(exclude_unset=True))
        db.commit()
        db.refresh(updated_submenu)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
    else:
        return updated_submenu


def delete(db: Session, submenu_id):
    """
    delete single submenu by id from db
    """
    try:
        submenu = db.query(s.Submenu).get(submenu_id)

        if not submenu:
            raise ValueError(f"submenu with: id {submenu_id} not found")

        db.delete(submenu)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
