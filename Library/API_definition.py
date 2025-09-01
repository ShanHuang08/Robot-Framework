import requests
import urllib3
from Library.Robot_definition import log, log_color
urllib3.disable_warnings()
from time import perf_counter, sleep
import httpx

class API_Methods():
    def GET_Request(self, url, params=None, auth=None, timeout=20, retries=3, exp_code=None):
        """
        `params=None`, Default auth = `None`, timeout `20 secs`, retries `3 times`.
        """
        try:
            Get_data = requests.get(url=url, params=params, auth=auth, verify=False, timeout=timeout)
            if params:
                log(f"making GET request to {url}, params is {params} and expeted return {exp_code}")
            else:
                log(f"making GET request to {url} and expeted return {exp_code}")
            return Get_data
        except requests.exceptions.ConnectTimeout as e:
            log(f'ConnectTimeout: {e}')
            self.Retry_api(url, auth, retries)
        except requests.exceptions.Timeout as e:
            log(f'Timeout: {e}')
            self.Retry_api(url, auth, retries)
        except requests.exceptions.HTTPError as e:
            raise Exception(f'HTTPError: {e}')
        except requests.exceptions.ConnectionError as e:
            raise Exception(f'ConnectionError: {e}')
        except urllib3.exceptions.ReadTimeoutError as e:
            raise Exception(f'ReadTimeoutError: {e}')

        

    def PATCH_Request(self, url, auth, body, params=None,  timeout=10, exp_code=None):
        """
        `params=None`, Timeout `10 secs`, `json=body`
        """
        try:
            Patch_data = requests.patch(url=url, params=params, auth=auth, json=body, verify=False, timeout=timeout)
            if params:
                log(f"making PATCH request to {url} with params {params} and body {body} and expeted return {exp_code}")
            else:
                log(f"making PATCH request to {url} and body {body} and expeted return {exp_code}")
            return Patch_data
        except requests.exceptions.HTTPError as e:
            raise Exception(f'HTTPError: {e}')
        except requests.exceptions.ConnectTimeout as e:
            raise Exception(f'ConnectTimeout: {e}')
        except requests.exceptions.ConnectionError as e:
            raise Exception(f'ConnectionError: {e}')
        except requests.exceptions.Timeout as e:
            raise Exception(f'Timeout: {e}')

        


    def POST_Request(self, url, auth, body, params=None,  timeout=10, exp_code=None):
        """
        `params=None`, Timeout `10 secs`, Default body = `None` `json=body`
        """
        try:
            Post_data = requests.post(url=url, params=params, auth=auth, json=body, verify=False, timeout=timeout)
            if params:
                log(f"making POST request to {url} with params {params} and body {body} and expeted return {exp_code}")
            else:
                log(f"making POST request to {url} and body {body} and expeted return {exp_code}")
            return Post_data
        except requests.exceptions.HTTPError as e:
            raise Exception(f'HTTPError: {e}')
        except requests.exceptions.ConnectTimeout as e:
            raise Exception(f'ConnectTimeout: {e}')
        except requests.exceptions.ConnectionError as e:
            raise Exception(f'ConnectionError: {e}')
        except requests.exceptions.Timeout as e:
            raise Exception(f'Timeout: {e}')


    def PUT_Request(self, url, auth, body, params=None,  timeout=10, exp_code=None):
        """
        `params=None`, Timeout `10 secs`, Default body = `None` `json=body`
        """
        try:
            Put_data = requests.put(url=url, params=params, auth=auth, json=body, verify=False, timeout=timeout)
            if params:
                log(f"making PUT request to {url} with params {params} and body {body} and expeted return {exp_code}")
            else:
                log(f"making PUT request to {url} and body {body} and expeted return {exp_code}")
            return Put_data
        except requests.exceptions.HTTPError as e:
            raise Exception(f'HTTPError: {e}')
        except requests.exceptions.ConnectTimeout as e:
            raise Exception(f'ConnectTimeout: {e}')
        except requests.exceptions.ConnectionError as e:
            raise Exception(f'ConnectionError: {e}')
        except requests.exceptions.Timeout as e:
            raise Exception(f'Timeout: {e}')

        

    def DELETE_Request(self, url, auth,  exp_code=None):
        """
        `params=None`, Timeout `10 secs`
        """
        try:
            Delete_data = requests.delete(url=url, auth=auth, verify=False, timeout=10)
            log(f"making DELETE request to {url} and expeted return {exp_code}")
            return Delete_data
        except requests.exceptions.HTTPError as e:
            raise Exception(f'HTTPError: {e}')
        except requests.exceptions.ConnectTimeout as e:
            raise Exception(f'ConnectTimeout: {e}')
        except requests.exceptions.ConnectionError as e:
            raise Exception(f'ConnectionError: {e}')
        except requests.exceptions.Timeout as e:
            raise Exception(f'Timeout: {e}')



    def Check_if_status_code_match(self, actual:int, expect:int):
        """- Actual: `res.status_code`
           - Expect: `exp_status`
        """
        if actual != expect:
            log_color(f"Status code should be {expect} but it is {actual}", "red")
        else: log(f"Status code is expected: {actual}")
        return actual == expect


    def Retry_api(self, url, auth, retries:int):
        """Only support `GET_Request()` right now"""
        import requests
        success = []
        Fail_List = []
        print(f'Start to retry {url}')
        for retry in range(1, retries+1):
            print(f'Retry {retry} times, timeout 20 secs')
            try:
                res = requests.get(url, auth, verify=False, timeout=20) # Use GET_Request() will trigger infinity loop
                if res.status_code == 200: 
                    print('retry api success')
                    success.append(res)
                    return res
                else: 
                    Fail_List.append(str(retry)+'. '+str(res[0]))
                    continue        
            except requests.exceptions.HTTPError as e:
                print(f'HTTPError: {e}')
                continue
            except requests.exceptions.ConnectTimeout as e:
                print(f'ConnectTimeout: {e}')
                continue
            except requests.exceptions.ConnectionError as e:
                print(f'ConnectionError: {e}')
                continue
            except requests.exceptions.Timeout as e:
                print(f'Timeout: {e}')
                continue
            except urllib3.exceptions.ReadTimeoutError as e:
                print(f'ReadTimeoutError: {e}')
                continue
        if not success: 
            fail_list_str = '\n'.join(Fail_List)
            raise Exception(f"Retry api failed after {retries} times\n{fail_list_str}")


    def GET_Avg_Res_Time(self, url, count:int):
        """Utilize `httpx` to Calculate average api response time by count"""
        import asyncio
        Total_time = 0
        async def get_res_time():
            Total = 0
            async with httpx.AsyncClient(http2=True) as client:
                for _ in range(count):
                    start_time = perf_counter() * 1000
                    await client.get(url)
                    end_time = perf_counter() * 1000
                    elapsed_time = end_time - start_time - self.measure_overhead()
                    log(f"GET {url} url execution time = {"{:.4f}".format(elapsed_time)} ms")
                    Total+=(elapsed_time)
                return Total
        log(f"<b>===== Check Average Response Time for {count} times =====</b>")
        try:
            Total_time = asyncio.run(get_res_time()) 
        except Exception as e:
            log(f"Connection Error: {e}")
        log(f"<b>===== Check Average Response Time for {count} times =====</b>")
        return Total_time/count

    def measure_overhead(self):
        """Count the time of overhead"""
        start_time = perf_counter() * 1000
        end_time = perf_counter() * 1000
        overhead = end_time - start_time
        return overhead