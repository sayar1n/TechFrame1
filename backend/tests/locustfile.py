from locust import HttpUser, task, between
import random

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)
    host = "http://localhost:8000"
    
    # Test data - in a real scenario, this would be generated or loaded securely
    test_users = [
        {"username": f"testuser_{i}", "email": f"test_{i}@example.com", "password": "testpass", "role": "engineer"} for i in range(50)
    ]
    auth_tokens = {}

    def on_start(self):
        # Register a few users for testing if they don't exist
        for user_data in self.test_users:
            try:
                # Try to register
                self.client.post("/users/", json=user_data)
            except Exception:
                pass # User likely already exists
            
            # Login to get a token
            response = self.client.post(
                "/token",
                data={
                    "username": user_data["username"],
                    "password": user_data["password"]
                }
            )
            if response.status_code == 200:
                self.auth_tokens[user_data["username"]] = response.json()["access_token"]

    def get_auth_headers(self, username):
        token = self.auth_tokens.get(username)
        return {"Authorization": f"Bearer {token}"} if token else {}

    @task(3)
    def get_root(self):
        self.client.get("/")

    @task(10)
    def login_and_get_me(self):
        user_data = random.choice(self.test_users)
        response = self.client.post(
            "/token",
            data={
                "username": user_data["username"],
                "password": user_data["password"]
            },
            name="/token [login]"
        )
        if response.status_code == 200:
            token = response.json()["access_token"]
            self.client.get(
                "/users/me/",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                name="/users/me/ [authenticated]"
            )

    @task(5)
    def get_projects(self):
        user_data = random.choice(self.test_users)
        headers = self.get_auth_headers(user_data["username"])
        if headers:
            self.client.get("/projects/", headers=headers)

    @task(2)
    def create_and_get_project(self):
        user_data = random.choice(self.test_users)
        headers = self.get_auth_headers(user_data["username"])
        if not headers:
            return
        
        project_data = {"title": f"Project by {user_data['username']} {random.randint(1, 10000)}", "description": "Stress test project"}
        response = self.client.post(
            f"/users/{user_data['id']}/projects/", # Note: user_data['id'] is not populated in test_users dict
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
        user_data = random.choice(self.test_users)
        # Only managers and observers can export, so pick a user with such role or assume one of the test users has it
        # For simplicity, we'll just try to export with a random user's token
        headers = self.get_auth_headers(user_data["username"])
        if headers:
            self.client.get("/reports/defects/export?format=csv", headers=headers)

    @task(1)
    def export_defects_xlsx(self):
        user_data = random.choice(self.test_users)
        headers = self.get_auth_headers(user_data["username"])
        if headers:
            self.client.get("/reports/defects/export?format=xlsx", headers=headers)
