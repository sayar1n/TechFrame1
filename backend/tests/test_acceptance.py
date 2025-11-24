import pytest
from fastapi.testclient import TestClient


def create_user(client: TestClient, username: str, email: str, password: str, role: str):
    r = client.post("/users/", json={"username": username, "email": email, "password": password, "role": role})
    assert r.status_code == 200
    return r.json()


def login_token(client: TestClient, username: str, password: str):
    r = client.post("/token", data={"username": username, "password": password})
    assert r.status_code == 200
    return r.json()["access_token"]


def auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}


def test_admin_endpoint_access_control(client: TestClient):
    manager = create_user(client, "manager_user", "manager@example.com", "pass", "manager")
    engineer = create_user(client, "engineer_user", "engineer@example.com", "pass", "engineer")

    manager_token = login_token(client, manager["username"], "pass")
    engineer_token = login_token(client, engineer["username"], "pass")

    r_ok = client.get("/admin/users/", headers=auth_headers(manager_token))
    assert r_ok.status_code == 200

    r_forbidden = client.get("/admin/users/", headers=auth_headers(engineer_token))
    assert r_forbidden.status_code == 403


def test_update_user_role_requires_manager_or_admin(client: TestClient):
    target = create_user(client, "target_user", "target@example.com", "pass", "engineer")
    manager = create_user(client, "role_manager", "role_manager@example.com", "pass", "manager")
    engineer = create_user(client, "role_engineer", "role_engineer@example.com", "pass", "engineer")

    manager_token = login_token(client, manager["username"], "pass")
    engineer_token = login_token(client, engineer["username"], "pass")

    r_ok = client.put(f"/users/{target['id']}/role", headers=auth_headers(manager_token), params={"new_role": "observer"})
    assert r_ok.status_code == 200
    assert r_ok.json()["role"] == "observer"

    r_forbidden = client.put(f"/users/{target['id']}/role", headers=auth_headers(engineer_token), params={"new_role": "manager"})
    assert r_forbidden.status_code == 403


def test_create_defect_global_role_restrictions(client: TestClient):
    manager = create_user(client, "def_manager", "def_manager@example.com", "pass", "manager")
    observer = create_user(client, "def_observer", "def_observer@example.com", "pass", "observer")
    engineer = create_user(client, "def_engineer", "def_engineer@example.com", "pass", "engineer")

    manager_token = login_token(client, manager["username"], "pass")
    observer_token = login_token(client, observer["username"], "pass")
    engineer_token = login_token(client, engineer["username"], "pass")

    r_proj = client.post(f"/users/{manager['id']}/projects/", headers=auth_headers(manager_token), json={"title": "Proj", "description": "Desc"})
    assert r_proj.status_code == 200
    project_id = r_proj.json()["id"]

    r_forbidden = client.post("/defects/", headers=auth_headers(observer_token), json={"title": "D1", "description": "", "project_id": project_id})
    assert r_forbidden.status_code == 403

    r_ok = client.post("/defects/", headers=auth_headers(engineer_token), json={"title": "D2", "description": "", "project_id": project_id})
    assert r_ok.status_code == 200


def test_analytics_access_for_roles(client: TestClient):
    manager = create_user(client, "an_manager", "an_manager@example.com", "pass", "manager")
    observer = create_user(client, "an_observer", "an_observer@example.com", "pass", "observer")
    engineer = create_user(client, "an_engineer", "an_engineer@example.com", "pass", "engineer")

    manager_token = login_token(client, manager["username"], "pass")
    observer_token = login_token(client, observer["username"], "pass")
    engineer_token = login_token(client, engineer["username"], "pass")

    for t in (manager_token, observer_token, engineer_token):
        r = client.get("/reports/analytics/status-distribution", headers=auth_headers(t))
        assert r.status_code == 200

        r2 = client.get("/reports/analytics/priority-distribution", headers=auth_headers(t))
        assert r2.status_code == 200


def test_delete_project_authorization(client: TestClient):
    owner = create_user(client, "own_engineer", "own_engineer@example.com", "pass", "engineer")
    manager = create_user(client, "mgr_user", "mgr_user@example.com", "pass", "manager")
    admin = create_user(client, "adm_user", "adm_user@example.com", "pass", "admin")

    owner_token = login_token(client, owner["username"], "pass")
    manager_token = login_token(client, manager["username"], "pass")
    admin_token = login_token(client, admin["username"], "pass")

    r_proj = client.post(f"/users/{owner['id']}/projects/", headers=auth_headers(owner_token), json={"title": "OwnerProj", "description": ""})
    assert r_proj.status_code == 200
    pid = r_proj.json()["id"]

    r_forbidden = client.delete(f"/projects/{pid}", headers=auth_headers(manager_token))
    assert r_forbidden.status_code == 403

    r_ok = client.delete(f"/projects/{pid}", headers=auth_headers(admin_token))
    assert r_ok.status_code == 204