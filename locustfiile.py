from locust import HttpUser, task, between, events
from logging import info, error, warning

class ExternalApiUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://pokeapi.co" # Setup host
    api_v2 = "/api/v2/pokemon/"


    def url_connection(self, url, retry=5):
        """Check if url is reachable, return True/False"""
        import requests, time
        for _ in range(retry):
            res = requests.get(url) # requests.get() won't be recognized by locust
            if res.status_code == 200:
                info(f"{url} Connected.")
                return True
            time.sleep(2)
        error(f"Cannot connect to {url}\nStatus code: {res.status_code}\nResponse: {res.text}")
        return False
    
    def api_judgement(self, api, response, max_response_time=500):
        """For `request()`. Check if response is valid, return True/False"""
        if response.status_code != 200:
            error(f"{api} Status code is not 200 but {response.status_code}")
            return False
        elif response.elapsed.total_seconds() * 1000 > max_response_time:
            warning(f"{api} response time: {response.elapsed.total_seconds()*1000}ms > {max_response_time}ms.")
            return False
        return True
                
    def get_pokemon_apis(self, amount:int):
        """Utilize `get()` to test pokemon APIs"""
        if self.url_connection(self.host + self.api_v2):
            for i in range(0, amount):
                api = self.api_v2 if i == 0 else f"{self.api_v2}{i}"
                with self.client.get(api, catch_response=True) as res:
                    res.failure(f"API {api} test failed") if not self.api_judgement(api, res, 150) else res.success()

    
    def test_pokemon_apis(self, amount:int):
        """Utilize `request()` to test pokemon APIs"""
        if self.url_connection(self.host + self.api_v2):
            for i in range(0, amount):
                api = self.api_v2 if i == 0 else f"{self.api_v2}{i}"
                with self.client.request("GET", api, catch_response=True) as response:
                    response.failure(f"API {api} test failed") if not self.api_judgement(api, response, 150) else response.success()


    @task
    def task_pokemon_one(self):
        self.test_pokemon_apis(10)
