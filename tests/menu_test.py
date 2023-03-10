import pytest
from httpx import AsyncClient

from run import app


@pytest.fixture(scope='module')
async def test_client():
    async with AsyncClient(app=app, base_url='http://test') as cl:
        yield cl


class TestMenu:
    response_data = {
        "title": "Menu 1",
        "description": "Description 1",
        "submenus_count": 0,
        "dishes_count": 0
    }
    create_data = {
        "title": "Menu 1",
        "description": "Description 1"
    }
    update_data = {
        "title": "Update menu 1"
    }

    async def test_get_menu_empty_list(self, test_client: AsyncClient):
        response = await test_client.get(
            '/api/v1/menus/',
            follow_redirects=True
        )
        assert response.status_code == 200
        assert response.json() == []

    async def test_post_menu_create(self, test_client: AsyncClient):
        response = await test_client.post(
            '/api/v1/menus/',
            json=self.create_data,
            follow_redirects=True
        )

        assert response.status_code == 201
        assert response.headers.get("content-type") == "application/json"
        assert isinstance(response.json(), dict)
        assert isinstance(response.json().get("id"), str)
        assert response.json().get("title") == "Menu 1"
        assert response.json().get("description") == "Description 1"

    async def test_get_menu_list(self, test_client: AsyncClient):
        response = await test_client.get(
            '/api/v1/menus/',
            follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert isinstance(response.json(), list)

    async def test_get_menu_by_id(self, test_client: AsyncClient):
        menu = await test_client.get(
            '/api/v1/menus/',
            follow_redirects=True
        )
        menu_id = menu.json()[0].get("id")

        response = await test_client.get(
            f'/api/v1/menus/{menu_id}/',
            follow_redirects=True
        )

        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/json"
        assert len(response.json()) > 0
        assert isinstance(response.json(), dict)
        assert isinstance(response.json().get("id"), str)
        assert response.json().get("title") == "Menu 1"
        assert response.json().get("description") == "Description 1"

    async def test_patch_menu_by_id(self, test_client: AsyncClient):
        menu = await test_client.get(
            '/api/v1/menus/',
            follow_redirects=True
        )
        menu_id = menu.json()[0].get("id")

        response = await test_client.patch(
            f'/api/v1/menus/{menu_id}/',
            json=self.update_data,
            follow_redirects=True
        )

        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/json"
        assert len(response.json()) > 0
        assert isinstance(response.json(), dict)
        assert isinstance(response.json().get("id"), str)
        assert response.json().get("title") == "Update menu 1"
        assert response.json().get("description") == "Description 1"

    async def test_delete_menu(self, test_client: AsyncClient):
        menu = await test_client.get(
            '/api/v1/menus/',
            follow_redirects=True
        )
        menu_id = menu.json()[0].get("id")

        response = await test_client.delete(
            f'/api/v1/menus/{menu_id}/',
            follow_redirects=True
        )

        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/json"

    async def test_get_menu_by_id_empty(self, test_client: AsyncClient):
        response = await test_client.get(
            '/api/v1/menus/5372d4ba-1e98-4b37-b1fe-29856c0e6220/',
            follow_redirects=True
        )

        assert response.json().get("detail") == "menu not found"
        assert response.status_code == 404
