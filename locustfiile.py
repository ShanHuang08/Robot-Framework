from locust import HttpUser, task, between, events
from logging import info

class ExternalApiUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://pokeapi.co" # 設定host


    def url_connection(self, url):
        """Check if url is reachable, return True/False"""
        import time
        for _ in range(3):
            res = self.client.get(url)
            if res.status_code == 200:
                info(f"{url} Connection established.")
                return
            time.sleep(2)
        info(f"Cannot connect to {url}\nStatus code: {res.status_code}\nResponse: {res.text}")
                
    def test_pokemon_apis(self, amount:int):
        """Test pokemon APIs"""
        self.url_connection(self.host)
        api1 = self.client.get("/api/v2/pokemon/")
        if api1.status_code != 200:
            api1.failure(f"Status code is not 200 but {api1.status_code}")
        # else: api1.success() # Not support manual success, get() auto handle it.
        # api1.elapsed.total_seconds()

        for i in range(1, amount):
            apis = self.client.get(f"/api/v2/pokemon/{i}")
            if apis.status_code != 200:
                info(f"Status code is not 200 but {apis.status_code}")

    @task
    def task_pokemon_one(self):
        self.test_pokemon_apis(10)
