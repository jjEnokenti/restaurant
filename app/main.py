from fastapi import FastAPI, APIRouter

from app.routes import menu, submenu, dish


def create_app():
    app = FastAPI(
        title="Restaurant menu API",
        description="FastApi project",
        version='0.1.1'
    )

    main_route = APIRouter(prefix="/api/v1")

    main_route.include_router(
        menu.menu_route,
        tags=['menus']
    )
    main_route.include_router(
        submenu.submenu_route,
        prefix="/menus/{menu_id}",
        tags=['submenus']
    )
    main_route.include_router(
        dish.dish_route,
        prefix="/menus/{menu_id}/submenus/{submenu_id}",
        tags=['dishes']
    )

    app.include_router(main_route)
    return app
