from fastapi.testclient import TestClient

from tests.conftest import engine, Base


class TestSubmenu:
    create_data = {
        "title": "Submenu 1",
        "description": "Description 1"
    }
    update_data = {
        "title": "Update submenu 1"
    }

    def test_create_menu_for_submenu(self, test_client: TestClient):
        Base.metadata.create_all(bind=engine)
        response = test_client.post(
            '/api/v1/menus',
            json={
                "title": "Menu 1",
                "description": "Description 1"
            },
            follow_redirects=True
        )

        assert response.status_code == 201
        assert response.headers.get("content-type") == "application/json"
        assert isinstance(response.json(), dict)
        assert isinstance(response.json().get("id"), str)
        assert response.json().get("title") == "Menu 1"
        assert response.json().get("description") == "Description 1"

    def test_get_submenu_empty_list(self, test_client: TestClient):
        menu_id = test_client.get(
            '/api/v1/menus',
            follow_redirects=True
        ).json()[0].get("id")
        response = test_client.get(
            f'/api/v1/menus/{menu_id}/submenus',
            follow_redirects=True
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_post_submenu_create(self, test_client: TestClient):
        menu_id = test_client.get(
            '/api/v1/menus',
            follow_redirects=True
        ).json()[0].get("id")
        response = test_client.post(
            f'/api/v1/menus/{menu_id}/submenus',
            json=self.create_data,
            follow_redirects=True
        )

        assert response.status_code == 201
        assert response.headers.get("content-type") == "application/json"
        assert isinstance(response.json(), dict)
        assert isinstance(response.json().get("id"), str)
        assert response.json().get("title") == "Submenu 1"
        assert response.json().get("description") == "Description 1"

    def test_get_submenu_list(self, test_client: TestClient):
        menu_id = test_client.get(
            '/api/v1/menus',
            follow_redirects=True
        ).json()[0].get("id")
        response = test_client.get(
            f'/api/v1/menus/{menu_id}/submenus',
            follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert isinstance(response.json(), list)

    def test_get_submenu_by_id(self, test_client: TestClient):
        menu_id = test_client.get(
            '/api/v1/menus',
            follow_redirects=True
        ).json()[0].get("id")
        submenu_id = test_client.get(
            f'/api/v1/menus/{menu_id}/submenus',
            follow_redirects=True
        ).json()[0].get("id")
        response = test_client.get(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
            follow_redirects=True
        )

        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/json"
        assert len(response.json()) > 0
        assert isinstance(response.json(), dict)
        assert isinstance(response.json().get("id"), str)
        assert response.json().get("title") == "Submenu 1"
        assert response.json().get("description") == "Description 1"

    def test_patch_submenu_by_id(self, test_client: TestClient):
        menu_id = test_client.get(
            '/api/v1/menus',
            follow_redirects=True
        ).json()[0].get("id")
        submenu_id = test_client.get(
            f'/api/v1/menus/{menu_id}/submenus',
            follow_redirects=True
        ).json()[0].get("id")
        response = test_client.patch(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
            json=self.update_data,
            follow_redirects=True
        )

        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/json"
        assert len(response.json()) > 0
        assert isinstance(response.json(), dict)
        assert isinstance(response.json().get("id"), str)
        assert response.json().get("title") == "Update submenu 1"
        assert response.json().get("description") == "Description 1"

    def test_delete_submenu(self, test_client: TestClient):
        menu_id = test_client.get(
            '/api/v1/menus',
            follow_redirects=True
        ).json()[0].get("id")
        submenu_id = test_client.get(
            f'/api/v1/menus/{menu_id}/submenus',
            follow_redirects=True
        ).json()[0].get("id")
        response = test_client.delete(
            f'/api/v1/menus/{menu_id}/submenus/{submenu_id}',
            follow_redirects=True
        )

        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/json"

    def test_get_submenu_by_id_empty(self, test_client: TestClient):
        menu_id = test_client.get(
            '/api/v1/menus',
            follow_redirects=True
        ).json()[0].get("id")
        response = test_client.get(
            f'''/api/v1/menus/
            {menu_id}/submenus/
            5372d4ba-1e98-4b37-b1fe-29856c0e6220''',
            follow_redirects=True)

        assert response.json().get("detail") == "submenu not found"
        assert response.status_code == 404

        Base.metadata.drop_all(bind=engine)
