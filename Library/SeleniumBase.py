from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Robot_definition import log


class SeleniumBase():
    
    def Chrome_Web(self, path):
        """File path should include `chromedriver.exe`"""
        self.driver = webdriver.Chrome(service=Service(path))
        log(f'Launch Chrome_Web driver')
        return self.driver

    def Chrome_WAP(self, path):
        self.service = Service(path)
        self.option = Options()
        mobile_emulation = {"deviceName": "iPhone X"}
        self.option.add_experimental_option("mobileEmulation", mobile_emulation)
        self.driver = webdriver.Chrome(service=self.service, options=self.option)
        log(f'Launch hrome_WAP driver')
        return self.driver

    def Firefox_Web(self, path):
        self.driver = webdriver.Firefox(service=Service(path))
        log(f'Launch Firefox_Web driver')
        return self.driver

    def find_ID(self, value) -> WebElement:
        #AttributeError: 'NoneType' object has no attribute 'click' add -> -> WebElement and add return
        log(f'Launch find_ID to find {value}')
        return self.driver.find_element(By.ID, value=value)
    
    def find_Name(self, value) -> WebElement:
        log(f'Launch find_Name to find {value}')
        return self.driver.find_element(By.NAME, value=value)
    
    def find_xpath(self, value) -> WebElement:
        log(f'Launch find_xpath to find {value}')
        return self.driver.find_element(By.XPATH, value=value)
    
    def find_IDs(self, value) -> WebElement:
        log(f'Launch find_ID to find {value} list')
        return self.driver.find_elements(By.ID, value=value)
    
    def find_Names(self, value) -> WebElement:
        log(f'Launch find_Name to find {value} list')
        return self.driver.find_elements(By.NAME, value=value)

    def find_xpaths(self, value) -> WebElement:
        log(f'Launch find_xpath to find {value} list')
        return self.driver.find_elements(By.XPATH, value=value)

    def get_window_handles(self):
        """return list with handles. Cooperate with `switch_window()`"""
        return self.driver.window_handles
    
    def Click_Element(self, method, value):
        from selenium.common.exceptions import ElementNotInteractableException
        from time import time
        
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((method, value)))
            log(f"Click {value}")
            element.click()
        except ElementNotInteractableException as e:
            log(f"Element is not interactable: {e}")
            screenshot_name = f"Fail_screenshot_{int(time())}.png"
            self.driver.save_screenshot(screenshot_name)
            log(f"Screen has been save as: {screenshot_name}")

    def Save_Screenshot(self, method, value, filename, wait_secs=20):

        try:
            WebDriverWait(self.driver, wait_secs).until(
                EC.visibility_of_element_located((method, value)))
            is_element_displayed = self.driver.find_element(method, value).is_displayed()
            if is_element_displayed:
                log(f"Save screenshot as {filename}")
                self.driver.save_screenshot(filename)
            else: log(f"Element {value} does not display.")
        except:
            log(f"Element {value} is unable show up in {wait_secs} seconds")
            log(f"Save screenshot as Error_{filename}")
            self.driver.save_screenshot(f"Error_{filename}")