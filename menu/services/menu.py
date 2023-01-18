from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from menu.models import Menu


def get_all(db: Session):
    """
    get all menus from db
    """
    try:
        menus = db.query(Menu).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
    else:
        return menus


def get_single_by_id(db: Session, menu_id):
    """
    get single menu by id from db
    """
    try:
        menu = db.query(Menu).get(menu_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
    else:
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"menu not found")

        return menu


def create(db: Session, create_data):
    """
    insert new menu into db
    """
    try:
        new_menu = Menu(**create_data.dict())
        db.add(new_menu)
        db.commit()
        db.refresh(new_menu)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
    else:
        return new_menu


def update(db: Session, menu_id, update_data):
    """
    update single menu by id into db
    """
    try:
        menu_query = db.query(Menu).filter(Menu.id == menu_id)
        updated_menu = menu_query.first()

        if not updated_menu:
            raise ValueError(f"menu with: id {menu_id} not found")

        menu_query.update(update_data.dict(exclude_unset=True))
        db.commit()
        db.refresh(updated_menu)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
    else:
        return updated_menu


def delete(db: Session, menu_id):
    """
    delete single menu by id from db
    """
    try:
        menu_query = db.query(Menu)
        menu = menu_query.get(menu_id)
        if not menu:
            raise ValueError(f"menu with: id {menu_id} not found")

        db.delete(menu)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"error message: {e}")
