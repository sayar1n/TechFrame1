from locust import HttpUser, task, between
import random

class WebsiteUser(HttpUser):
    wait_time = between(0.2, 0.5)
    host = "http://localhost:8000"
    test_users = []
    auth_tokens = {}
    user_ids = {}

    def on_start(self):
        self.test_users = (
            [{"username": "manager_0", "email": "manager_0@example.com", "password": "testpass", "role": "manager"}] +
            [{"username": "observer_0", "email": "observer_0@example.com", "password": "testpass", "role": "observer"}] +
            [{"username": f"engineer_{i}", "email": f"engineer_{i}@example.com", "password": "testpass", "role": "engineer"} for i in range(1, 49)]
        )
        for user_data in self.test_users:
            with self.client.post("/users/", json=user_data, catch_response=True) as reg:
                if reg.status_code == 200:
                    self.user_ids[user_data["username"]] = reg.json()["id"]
                elif reg.status_code == 400 and "Username already taken" in reg.text:
                    reg.success()
            tok = self.client.post(
                "/token",
                data={
                    "username": user_data["username"],
                    "password": user_data["password"]
                }
            )
            if tok.status_code == 200:
                self.auth_tokens[user_data["username"]] = tok.json()["access_token"]

    def get_auth_headers(self, username):
        token = self.auth_tokens.get(username)
        return {"Authorization": f"Bearer {token}"} if token else {}

    @task(2)
    def get_root(self):
        self.client.get("/")

    @task(5)
    def get_me(self):
        user_data = random.choice(self.test_users)
        headers = self.get_auth_headers(user_data["username"])
        if headers:
            self.client.get("/users/me/", headers=headers, name="/users/me/")

    @task(5)
    def get_projects(self):
        user_data = random.choice(self.test_users)
        headers = self.get_auth_headers(user_data["username"])
        if headers:
            self.client.get("/projects/", headers=headers)

    @task(3)
    def create_and_get_project(self):
        user_data = random.choice(self.test_users)
        headers = self.get_auth_headers(user_data["username"])
        if not headers:
            return
        
        project_data = {"title": f"Project by {user_data['username']} {random.randint(1, 10000)}", "description": "Stress test project"}
        uid = self.user_ids.get(user_data["username"]) or self.client.get("/users/me/", headers=headers).json().get("id")
        response = self.client.post(
            f"/users/{uid}/projects/",
            headers=headers,
            json=project_data,
            name="/users/{user_id}/projects/ [create project]"
        )
        if response.status_code == 200:
            project_id = response.json()["id"]
            self.client.get(
                f"/projects/{project_id}",
                headers=headers,
                name="/projects/{project_id} [get project]"
            )

    @task(3)
    def get_defects(self):
        user_data = random.choice(self.test_users)
        headers = self.get_auth_headers(user_data["username"])
        if headers:
            self.client.get("/defects/", headers=headers)

    @task(1)
    def export_defects_csv(self):
        headers = self.get_auth_headers("manager_0") or self.get_auth_headers("observer_0")
        if headers:
            self.client.get("/reports/analytics/status-distribution", headers=headers)

    @task(1)
    def export_defects_xlsx(self):
        headers = self.get_auth_headers("manager_0") or self.get_auth_headers("observer_0")
        if headers:
            self.client.get("/reports/analytics/priority-distribution", headers=headers)
