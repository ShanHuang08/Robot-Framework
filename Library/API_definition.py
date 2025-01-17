import requests
import urllib3
from Library.Robot_definition import log
urllib3.disable_warnings()

class API_Methods():
    def GET_Request(self, url, params=None, auth=None, timeout=20, retries=3, exp_code=None):
        """
        `params=None`, Default auth = `None`, timeout `20 secs`, retries `3 times`.
        """
        try:
            Get_data = requests.get(url=url, params=params, auth=auth, verify=False, timeout=timeout)
            log(f"making GET request {url}, params is {params} and expeted return {exp_code}")
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
        
        else:
            if exp_code and (Get_data.status_code != int(exp_code)):
                raise Exception(f"Status code should be {exp_code} but it is {Get_data.status_code}\nResponse body:")
        return Get_data

    def PATCH_Request(self, url, auth, body, params=None,  timeout=10, exp_code=None):
        """
        `params=None`, Timeout `10 secs`, `json=body`
        """
        try:
            Patch_data = requests.patch(url=url, params=params, auth=auth, json=body, verify=False, timeout=timeout)
            log(f"making PATCH request {url} withp params {params} and body {body} and expeted return {exp_code}")
            
        except requests.exceptions.HTTPError as e:
            raise Exception(f'HTTPError: {e}')
        except requests.exceptions.ConnectTimeout as e:
            raise Exception(f'ConnectTimeout: {e}')
        except requests.exceptions.ConnectionError as e:
            raise Exception(f'ConnectionError: {e}')
        except requests.exceptions.Timeout as e:
            raise Exception(f'Timeout: {e}')
        else:
            if exp_code and (Patch_data.status_code != int(exp_code)):
                raise Exception(f"Status code should be {exp_code} but it is {Patch_data.status_code}\nResponse body:")
        return Patch_data


    def POST_Request(self, url, auth, body, params=None,  timeout=10, exp_code=None):
        """
        `params=None`, Timeout `10 secs`, Default body = `None` `json=body`
        """
        try:
            Post_data = requests.post(url=url, params=params, auth=auth, json=body, verify=False, timeout=timeout)
            log(f"making POST request {url} withp params {params} and body {body} and expeted return {exp_code}")
            
        except requests.exceptions.HTTPError as e:
            raise Exception(f'HTTPError: {e}')
        except requests.exceptions.ConnectTimeout as e:
            raise Exception(f'ConnectTimeout: {e}')
        except requests.exceptions.ConnectionError as e:
            raise Exception(f'ConnectionError: {e}')
        except requests.exceptions.Timeout as e:
            raise Exception(f'Timeout: {e}')
        else:
            if exp_code and (Post_data.status_code != int(exp_code)):
                raise Exception(f"Status code should be {exp_code} but it is {Post_data.status_code}\nResponse body:")
        return Post_data

    def DELETE_Request(self, url, auth, params=None,  exp_code=None):
        """
        `params=None`, Timeout `10 secs`
        """
        try:
            Delete_data = requests.delete(url=url, params=params, auth=auth, verify=False, timeout=10, exp_code=None)
            log(f"making DELETE request {url}, params is {params} and expeted return {exp_code}")
        except requests.exceptions.HTTPError as e:
            raise Exception(f'HTTPError: {e}')
        except requests.exceptions.ConnectTimeout as e:
            raise Exception(f'ConnectTimeout: {e}')
        except requests.exceptions.ConnectionError as e:
            raise Exception(f'ConnectionError: {e}')
        except requests.exceptions.Timeout as e:
            raise Exception(f'Timeout: {e}')
        else:
            if exp_code and (Delete_data.status_code != int(exp_code)):
                raise Exception(f"Status code should be {exp_code} but it is {Delete_data.status_code}\nResponse body:")
        return Delete_data


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