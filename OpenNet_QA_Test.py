from Library.Robot_definition import log, log_color, run, fail, get_lib_instance, use_globals_update_keywords
from Library.SeleniumLibraryBase import SeleniumLibBase, SeleniumLibrary
from Library.BaseFunctions import basic_func
from Library.WebElements import Twitch_Xpath
from Library.API_definition import API_Methods
import json

class Twitch_test(SeleniumLibBase):
    def __init__(self):
        self.chromedriver_path = 'C:\\Users\\Shan\\Workspace2\\chromedriver.exe'
        self.firefoxdriver_path = 'C:\\Users\\Shan\\Workspace2\\geckodriver.exe'
        self.se_lib = SeleniumLibrary()
        self.url = "https://m.twitch.tv/"
        get_lib_instance('SeleniumLibBase', all_=True)
        self.api = API_Methods()
        self.api_url = 'https://api.ipstack.com/134.201.250.155'
        
    
    def Check_Network_Connection(self):
        """Utilize ping to check connection"""
        check, output = basic_func.Check_ipaddr(self.url)
        if not check: 
            fail(f'Unable to connect {self.url}\nOutput: {output}')

    def Twitch_Scrape(self):
        """Utilize Robot Framework as a test runner"""
        # Go to Twitch main page as WAP view
        self.Open_Browser_in_Mobile_View(self.url, driver_path=self.chromedriver_path)
        self.se_lib.wait_until_element_is_visible('xpath:/html')
        run('Capture_a_Screenshot', 'main page.png')

        # Click the search icon
        self.Click_Element('xpath:'+Twitch_Xpath["Click Browse"])

        # Input StarCraft II to search
        self.Click_Element('xpath:'+Twitch_Xpath["Search input field"])
        run('Input_to_Textfield', 'xpath:'+Twitch_Xpath["Search input field"], 'StarCraft II')
        self.se_lib.wait_until_element_is_visible('xpath:'+Twitch_Xpath["StarCraft II icon"], timeout=10)
        run('Capture_a_Screenshot', 'Searching.png')
        self.Click_Element('xpath:'+Twitch_Xpath["StarCraft II title"])

        # Wait until follow button is visible
        self.se_lib.wait_until_element_is_visible('xpath:'+Twitch_Xpath["Follow button"])

        # Wait until 1st and 2nd videos are visible
        self.se_lib.wait_until_element_is_visible('xpath:'+Twitch_Xpath["3rd video pic"], timeout=10)
        run('Capture_a_Screenshot', 'StarCraft II.png')

        Title = self.se_lib.get_text('xpath:'+Twitch_Xpath["h1 title"]) # StarCraft II
        descri = self.se_lib.get_webelements('xpath:'+Twitch_Xpath["Description"]) #Audiences and Followers

        log_color(f'<h1>Category Title: {Title}</h1>', color='blue')
        descri_list = [des.text for des in descri]
        log(f'<h2>{descri_list[0]} audiences\n{descri_list[-1]} followers</h2>')
  
        # Scroll down 2 times
        run('Scroll_into_view', Twitch_Xpath["4th video pic"])
        run('Capture_a_Screenshot', 'Stream3.png')
        run('Scroll_into_view', Twitch_Xpath["5th video pic"])
        run('Capture_a_Screenshot', 'Stream4.png')

        # Select one random streamer
        run('Click_Element', Twitch_Xpath["5th video pic"])

        # on the streamer page wait until all is load and take a screenshot
        # (Need to handle modal or pop-up created by specific streamers)
        # Check video controller
        self.se_lib.wait_until_element_is_visible('xpath:'+Twitch_Xpath["Video Controller"], timeout=10)
        # Check video controller is hidden
        try:
            self.se_lib.wait_until_element_is_visible('xpath:'+Twitch_Xpath["Check controller is hidden"], timeout=10)
        except:
            self.se_lib.wait_until_element_is_visible('xpath:'+Twitch_Xpath["Check controller div is hidden"], timeout=10)
        run('Capture_a_Screenshot', 'Live Streaming.png')
        self.se_lib.close_all_browsers()
    
  
    def GET_Basic_Standard_IP_Lookup_positive(self):
        err = []
        url = self.inspect_url(self.api_url)
        key = "access_key"
        value = 'e5a62f828501ddd4e33acfd3949f81f3'
        exp_status = 200
        exp_url = self.expect_url(url, {key : value})

        res = self.api.GET_Request(url, params={key : value}, exp_code=exp_status)
        # Check status code
        if not self.Check_if_status_code_match(res.status_code, exp_status): 
            err.append(f'Check status code failed! {res.status_code} != {exp_status}')

        # Check url match as expected
        if not self.Check_param_urls(res.url, exp_url): 
            err.append(f'Check access key failed! {res.url} != {exp_url}')

        # Check res format
        try:
            if not self.is_res_JSON(res.json()): 
                err.append(f"Check response format failed!")

        # Check response keys
            invalid = self.Get_keys_from_response(res.json())
            if invalid: 
                log('<b>Response keys comparison failed!</b>', level='ERROR')
                err.append("Response keys comparison failed!")
        except json.decoder.JSONDecodeError as e:
            log(f"{e}\nCheck response format failed! {res.text}")
            err.append("Check response format failed!")
        
        self.Final_Test_result(err)


    def GET_Basic_Standard_IP_Lookup_negative(self):
        err = []
        url = self.inspect_url(self.api_url)

        Test_params = [({'access_key' : 'key'}, 200),
                       ({'access_key' : '123'}, 200),
                       ({'access_key' : ''}, 200)
                       ]
        for param, exp_status in Test_params:
            exp_url = self.expect_url(url, param) # *arg_list seperate list content

            res = self.api.GET_Request(url, params=param, exp_code=exp_status)
            # Check status code
            if not self.Check_if_status_code_match(res.status_code, exp_status): 
                err.append(f'Check status code failed! {res.status_code} != {exp_status}')

            # Check url match as expected
            if not self.Check_param_urls(res.url, exp_url): 
                err.append(f'Check access key failed! {res.url} != {exp_url}')            
          
            # Check res format
            try:
                if not self.is_res_JSON(res.json()): 
                    err.append(f"Check response format failed!")

            # Check response values
                response = res.json()
                value = ''.join(v for v in param.values())
                if value == '':
                    exp_value = [False, 101, "missing_access_key", "You have not supplied an API Access Key. [Required format: access_key=YOUR_ACCESS_KEY]"]
                else:
                    exp_value = [False, 101, "invalid_access_key", "You have not supplied a valid API Access Key. [Technical Support: support@apilayer.com]"]
                checking_result = self.Check_err_res_value(response, exp_value)
                if checking_result: log(f'All response values are correct! on {param}')
                else: err.append(f"Check response values failed! {param}")
            except json.decoder.JSONDecodeError as e:
                log(f"{e}\nCheck response format failed! {res.text}")
                err.append("Check response format failed!")

        self.Final_Test_result(err)


    def Set_Valid_and_Invalid_Hostname(self):
        err = []
        url = self.inspect_url(self.api_url)
        key = 'e5a62f828501ddd4e33acfd3949f81f3'

        Test_params = [({'access_key' : key, 'hostname' : 1}, 200),
                       ({'access_key' : key, 'hostname' : 0}, 200),
                       ({'access_key' : key, 'hostname' : 123}, 200)
                       ]

        for param, exp_status in Test_params:
            exp_url = self.expect_url(url, param)

            res = self.api.GET_Request(url, params=param, exp_code=exp_status)       
            # Check status code
            if not self.Check_if_status_code_match(res.status_code, exp_status): 
                err.append(f'Check status code failed! {res.status_code} != {exp_status}')            

            # Check url match as expected
            if not self.Check_param_urls(res.url, exp_url): 
                err.append(f'Check access key failed! {res.url} != {exp_url}')              

            # Check res format
            try:
                if not self.is_res_JSON(res.json()): 
                    err.append(f"Response is NOT JSON format.")
    
                # Check hostname key and value
                response = res.json()
                if param["hostname"] in [1, 0]: #valid
                    if response.get("hostname"): 
                        log(f'Find hostname in response: hostname : {res.json()["hostname"]}')
                    else:
                        if param["hostname"] in [1]: 
                            log(f"Can not find key hostname on {param}\n{response}", level='ERROR')
                            err.append(f"Can not find key hostname on {param}")
                        else: log(f"Can not find key hostname on {param}")
                else: #invalid
                    if not response.get("hostname"): 
                        log(f'hostname not in response\nCheck error values')
                        exp_value = [False, 301, "parameter_invalid", "hostname should be 1 or 0"]
                        checking_result = self.Check_err_res_value(response, exp_value)
                        if checking_result: log(f'All response values are correct! on {param}')
                        else: err.append("Check hostname key fail on invalid param")
                    else:
                        log(f"hostname key should not display\n{response}", level='ERROR')
            except json.decoder.JSONDecodeError as e:
                log(f"{e}\nCheck response format failed! {res.text}")
                err.append("Check response format failed!")

        self.Final_Test_result(err)


    def Check_if_status_code_match(self, actual, expect):
        """- Actual: `res.status_code`
           - Expect: `exp_status`
        """
        if actual == expect: log(f'Status code {actual} is expected')
        else: log(f"<b>Status code should be {expect} but it is {actual}</b>", level='ERROR')
        return actual == expect

    def Check_param_urls(self, actual, expect):
        """- Actual: `res.url`
           - Expect: `exp_url`
        """
        if actual == expect: log(f'<b>Correct url: {actual}</b>')
        else: log(f'Url is Not match: {actual} != {expect}', level='ERROR')
        return actual == expect

    def is_res_JSON(self, res):
        """Check if response is JSON format"""
        if isinstance(res, dict): 
            log('Response is JSON format.')
            log(res, level='DEBUG')
        else: log('<b>Response is NOT JSON format.</b>')
        return isinstance(res, dict)

    def inspect_url(self, url:str):
        """Return url with correct protocol"""
        if not url.startswith('https://'): # e.g. http://abc.com
            protocols = ['http', 'ftp', 'smb', 'icmp', 'telnet', ':']
            for typ in protocols:
                if url.startswith(typ):
                    url = url[len(typ):]
            # Add https protocol
            if url.startswith('//'): url = 'https:' + url
            elif url.startswith('/'): url = 'https:/' + url
            else: url = 'https://' + url
        return url

    def expect_url(self, url:str, arg:dict):
        """Return expected url after GET api with single and mutiple params"""
        url = self.inspect_url(url)
        if url.endswith('/'): url = url[:-1]
        # print(arg)
        num = 1
        for key, value in arg.items():
            if num == 1:
                url+=f"?{key}={value}"
            else:
                url+=f"&{key}={value}"
            num+=1
        return url


    def Get_keys_from_response(self, response:dict):
        """Check all keys data type and compare key length"""
        main_keys = []
        exp_main_length = 15
        branch_keys = []
        exp_branch_length = 9
        data_type = [str, list, int, float, bool, dict]
        type_string = ['str', 'list', 'int', 'float', 'booling', 'dict']
        for key, value in response.items():
            # print(key, type(value))
            for d_typ, typ_s in zip(data_type, type_string):
                if isinstance(value, d_typ):
                    main_keys.append(f"{key} : {typ_s}")

            if isinstance(value, dict):
                log(f"{key} key has branches:\n")
                for k, v in value.items():
                    # print(k, type(v))
                    for d_typ, typ_s in zip(data_type, type_string):
                        if isinstance(v, d_typ):
                            branch_keys.append(f"{k} : {typ_s} in {key} key")

        def Compare_length(List, exp_length):
            """`main keys` and `branch keys` length comparison"""
            actual = len(List)
            return f"Keys length Match:\nactual:{actual}, expect:{exp_length}" if actual == exp_length else \
                f"Keys length NOT Match:\nactual:{actual}, expect:{exp_length}"
        # Output
        Compare_main = Compare_length(main_keys, exp_main_length)
        Compare_branch = Compare_length(branch_keys, exp_branch_length)
        main_result = '\n'.join(k for k in main_keys)
        branch_result = '\n'.join(k for k in branch_keys)
        log(f"<b>====== Main Keys ======</b>\n{Compare_main}\n{main_result}\n")
        log(f"<b>====== Branch Keys ======</b>\n{Compare_branch}\n{branch_result}")

        invalid_judge = ['NOT Match' in Compare_main, 'NOT Match' in Compare_branch]
        return True in invalid_judge


    def Check_err_res_value(self, response:dict, exp_value:list):
        """Check all keys value fits expect data"""
        err = []
        exp_main_length = 1
        exp_branch_length = 3
        len_exp = exp_main_length + exp_branch_length
        if len(exp_value) < len_exp:
            raise IndexError(f'Invalid exp_value length! {len(exp_value)} < {len_exp}')

        num = 0
        for key, value in response.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    # print(res[key][k])
                    if response[key][k] == exp_value[num]:
                        log(f'value in {k} key is Match')
                    else:
                        log(f'value in {k} key is NOT Match\n{response[key][k]} != {exp_value[num]}', level='ERROR')
                        err.append(f'value in {k} key is NOT Match')  
                    num+=1                  
            else:
                # print(res[key])
                if response[key] == exp_value[num]:
                    log(f'value in {key} key is Match')
                else: 
                    log(f'value in {key} key is NOT Match\n{response[key]} != {exp_value[num]}', level='ERROR')
                    err.append(f'value in {key} key is NOT Match')
            num+=1
            log(err, level='DEBUG')
        return len(err) == 0

    def Final_Test_result(self, err:list):
        if err:
            err_msg = '\n'.join(msg for msg in err)
            log_color('Test FAIL', color='red')
            fail(f'Error: {err_msg}')
        else: log_color('Test PASS', color='blue')


use_globals_update_keywords(Twitch_test(), globals())