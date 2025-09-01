from Library.API_definition import API_Methods
from Library.Robot_definition import log, log_color, fail, use_globals_update_keywords, run
from Library.SeleniumBase import SeleniumBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
from time import time, perf_counter, sleep
from random import sample, choice
import asyncio
import websockets


class Axiom_Auto_Test(API_Methods, SeleniumBase):
    def __init__(self):
        self.api_url = 'https://pokeapi.co/api/v2/pokemon/'
        self.exp_keys = ["name", "id", "height", "weight"] 
        self.exp_value = "pikachu"
        self.ws_uri = "wss://echo.websocket.org"
        # Selenium
        super().__init__()  # Make sure SeleniumBase.__init__() can be executed
        self.se_url = "https://www.saucedemo.com/"
        self._account = "standard_user"
        self._password = "secret_sauce"

    # API自動化測試
    def GET_Pokemon_Api_response(self, id_name=None, exp_code=304):
        """GET https://pokeapi.co/api/v2/pokemon/{id or name} api and check `JSON` response"""
        err = []
        test_case_start = time()
        self.api_url += str(id_name)

        res = self.GET_Request(self.api_url, exp_code=exp_code)

        if not self.Check_if_status_code_match(res.status_code, exp_code):
            err.append(f'Check status code failed! {res.status_code} != {exp_code}')

        if not self.Check_JSON_response(res.json(), self.exp_keys, self.exp_value):
            err.append('Response check failed!')
        
        Avg_res_Time = self.GET_Avg_Res_Time(self.api_url, 10)

        if Avg_res_Time > 500: 
            log_color(f'Average api response time is {"{:.4f}".format(Avg_res_Time)} ms, greater than 500 ms", "red')
            err.append(f"Average api response time is {Avg_res_Time} ms, greater than 500 ms")
        else:
            log(f'Average api response time is {"{:.4f}".format(Avg_res_Time)} ms')

        test_case_end = time()
        log(f'Test case executiion time: <b>{"{:.4f}".format(test_case_end - test_case_start)} secs</b>')
        self.Final_Test_result(err)


    def GET_Pokemon_Api_with_various_methods(self):
        """Utilize `GET`, `POST`, `PATCH`, `PUT`, `DELETE` methods to call https://pokeapi.co/api/v2/pokemon/pikachu api"""
        test_case_start = time()
        methods = [self.GET_Request, self.POST_Request, self.PATCH_Request, self.PUT_Request, self.DELETE_Request]
        exp_codes = [304, 404, 404, 404, 404]
        actual_codes = []
        Total_spent_time = 0

        for method, exp_code in zip(methods, exp_codes):
            start_time = perf_counter() * 1000
            if method == methods[0] or method == methods[-1]:
                res = method(self.api_url, auth=None, exp_code=exp_code)
            else:
                res = method(self.api_url, auth=None, body=None, exp_code=exp_code)
            end_time = perf_counter() * 1000
            elapsed_time = end_time - start_time - self.measure_overhead()
            Total_spent_time+=(elapsed_time)
            # Check if status code match on each method
            actual_codes.append(res.status_code)
            sleep(0.25)

        Avg_exe_Time = Total_spent_time / len(methods)
        if Avg_exe_Time > 500: 
            log_color(f'Average api response time is {"{:.4f}".format(Avg_exe_Time)} ms, greater than 500 ms', 'red')

        test_case_end = time()
        log(f'Test case executiion time: <b>{"{:.4f}".format(test_case_end - test_case_start)} secs</b>')
        log_color('Test PASS', color='blue') if actual_codes == exp_codes and Avg_exe_Time < 500 else fail(f'Test FAIL\n{actual_codes} != {exp_codes}')


    def Check_JSON_response(self, res:dict, exp_keys:list, exp_value:str):
        """Parse 2 layers of JSON. Check request response keys and values"""
        check = []
        try:
            log("<b>===== Response =====</b>")
            for key, value in res.items():
                if isinstance(value, list):
                    log(f'Parse {key} parent key:')
                    for dic in value:
                        for exp_key in exp_keys:
                            if dic.get(exp_key) == exp_value: # Only handle dict in list
                                log_color(f"-> {exp_key} = {dic[exp_key]}", "blue")
                                check.append({key : f"{exp_key} = {dic[exp_key]}"})

                elif isinstance(value, dict):
                    log(f'Parse {key} parent key:')
                    for k,v in value.items(): #Only handle dict in dict
                        for exp_key in exp_keys:
                            if k == exp_key and v == exp_value:
                                log_color(f"-> {k} = {v}", "blue")
                                check.append({key : f"{k} = {v}"})
                else:
                    if key in exp_keys: # 1st layer
                        log_color(f"{key} = {value}", "blue") 
                        check.append({f"{key} = {value}"})

            log("<b>===== Response =====</b>")
            log(check, level='DEBUG')
            return True if len(check) >= len(exp_keys) else False
        except json.decoder.JSONDecodeError as e:
            log_color(f"{e}\nCheck response format failed! {res}", level="ERROR")


    def Avg_Res_Time(self, count:int, exp_code):
        """Utitlze `requests` to Calculate average api response time by count"""
        Total_time = 0
        log(f"<b>===== Check Average Response Time for {count} times =====</b>")
        for i in range(count):
            start_time = perf_counter() * 1000
            res = self.GET_Request(self.api_url, exp_code=exp_code)
            end_time = perf_counter() * 1000
            elapsed_time = end_time - start_time - self.measure_overhead()
            log(f"GET {self.api_url} url execution time = {"{:.4f}".format(elapsed_time)} ms")
            Total_time+=(elapsed_time)
            sleep(0.25)
        log(f"<b>===== Check Average Response Time for {count} times =====</b>")
        return Total_time/count

    def Final_Test_result(self, err:list):
        if err:
            err_msg = '\n'.join(msg for msg in err)
            log_color('Test FAIL', color='red')
            fail(f'Error: {err_msg}')
        else: log_color('Test PASS', color='blue')

    
    # Websocket自動化測試
    # wss://echo.websocket.org/
    async def Websocket_Test(self):
        message = "Hi Axiom"
        messages = ["Message 1", "Message 2", "Message 3"]

        async with websockets.connect(self.ws_uri) as websocket:
            log('Websocket connection successful')

            await websocket.send(message)
            response = await websocket.recv()

            while response.startswith("Request served by"):
                response = await websocket.recv()

            assert response == message, f"Expected: <b>{message}</b> but get <b>{response}</b>"
            log(f"Receive correct respose: {response}")

            for msg in messages:
                await websocket.send(msg)
            received_messages = [await websocket.recv() for _ in messages]
            assert received_messages == messages, f"Expected messages order: <b>{messages}</b> but get <b>{received_messages}</b>"
            log(f"Messages order is correct: {received_messages}")

            await websocket.close()
    
    def Run_Websocket(self):
        asyncio.run(self.Websocket_Test())

    
    # Selenium test. Scrape https://www.saucedemo.com/ website

    def Swag_Labs_Web_Scrape(self, buy):
        """Scrape Swag Labs web page"""
        driver = self.Launch_Web('chrome')
        driver.get(self.se_url)
        driver.maximize_window()

        self.Login_Error_Test(driver)

        self.find_ID("user-name").send_keys(self._account)
        self.find_ID("password").send_keys(self._password)
        self.Click(By.ID, value='login-button')
        self.Wait_until_element_is_displayed('//div[@id="page_wrapper"]', '//div[@class="inventory_list"]/div')

        items = self.find_xpaths('//div[@class="inventory_list"]/div') # Check how manys items are listed
        log(f"{len(items)} items are existed")

        nums = sample(range(0, len(items)), int(buy)) # Avoid repeated number
        selected_items = [] # Stored picked items
        # Add items to cart
        for i in nums:
            locator = f'//a[@id="item_{i}_title_link"]'
            self.Wait_until_element_is_enabled(locator+'/parent::div/parent::div//button')
            self.Click(value=locator+'/parent::div/parent::div//button') # Add to chart
            item_name = self.find_xpath(locator+'/div').text # item name
            log(f"Pick up <b>{item_name}</b> to the the cart")
            selected_items.append(item_name)

        self.Click(value='//a[@class="shopping_cart_link"]') # Enter to Cart page
        self.Wait_until_element_is_displayed('//div[@id="contents_wrapper"]','//div[@class="cart_item"]','//a[@class="shopping_cart_link"]')
        run('Save_Screenshot', 'cart.png')
        # Check items in Cart page
        for i in nums:
            locator = f'//a[@id="item_{i}_title_link"]'
            Cart_item = self.find_xpath(locator+'/div').text
            if Cart_item in selected_items:
                log(f'<b>{Cart_item}</b> is added to chart')
            else: log_color(f'<b>{Cart_item}</b> should not exist', 'red')

        # Remove 1 item
        Selection = choice(nums)
        locator = f'//a[@id="item_{Selection}_title_link"]'
        Remove_item = self.find_xpath(locator+'/div').text
        log(f'Remove <b>{Remove_item}</b>')
        self.Click(value=locator+'/parent::div//button')
        selected_items.remove(Remove_item)

        # Show left items
        log_color(f'<b>{', '.join(selected_items)}</b> item left in the chart', 'blue')
        run('Save_Screenshot', 'cart2.png')

        # Enter to Checkout page
        self.Click(By.ID, value='checkout')
        self.Wait_until_element_is_enabled("first-name", "continue", method=By.ID)
        self.find_ID("first-name").send_keys("First Name")
        self.find_ID("last-name").send_keys("Last Name")
        self.find_ID("postal-code").send_keys("110")
        self.Click(By.ID, value='continue')

        # Enter to Overview page
        self.Wait_until_element_is_displayed('//div[@class="cart_item"]', '//div[@class="summary_info"]')
        summary_info = self.find_xpaths('//div[@class="summary_info"]/div')
        log(f'<b>Summary_info:</b>')

        for info in summary_info:
            text = info.get_attribute("textContent").strip() # Get all info
            if text not in ["CancelFinish"]:
                log(text)
            
        run('Save_Screenshot', 'Overview.png')
        self.Click(By.ID, value="finish")

        # Checkout: Complete
        self.Wait_until_element_is_displayed("checkout_complete_container", method=By.ID)
        Complete_title = self.find_xpath('//div[@class="header_secondary_container"]//span').text
        tks = self.find_xpath("//h2").text
        log(Complete_title+'\n'+tks)
        run('Save_Screenshot', 'Checkout_Complete.png')


    def Login_Error_Test(self, driver):
        Error_msgs = ["Epic sadface: Username is required",
                      "Epic sadface: Password is required",
                      "Epic sadface: Username and password do not match any user in this service"]
        Input_text = [("", self._password), (self._account, ""), (self._account, self._password[1:])]

        for msg, text in zip(Error_msgs, Input_text):
            self.find_ID("user-name").send_keys(text[0])
            sleep(0.5)
            self.find_ID("password").send_keys(text[1])
            self.Click(By.ID, value='login-button')

            err_msg = self.find_xpath("//h3").text
            log(f"<b>{err_msg}</b>")
            log("Error msg match") if err_msg == msg else log("Error msg does not match")
            # driver.execute_script('document.getElementById("user-name").value = "";') # Not work
            # driver.execute_script('document.getElementById("password").value = "";') # Not work
            driver.refresh()
            self.Wait_until_element_is_enabled('//div[@class="form_group"]//input')
        

use_globals_update_keywords(globals(), Axiom_Auto_Test()) # Import all keywords in Axiom_Auto_Test class to Robot Framework