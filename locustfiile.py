from locust import HttpUser, task, between

class ExternalApiUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://pokeapi.co" # 設定host

    @task
    def get_data(self):
        self.client.get("/api/v2/pokemon/") # 設定api路徑
        self.client.get("/api/v2/pokemon/25")