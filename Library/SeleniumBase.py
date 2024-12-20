from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class SeleniumBase():
    
    def Chrome_Web(self):
        """chromedriver.exe"""
        self.driver = webdriver.Chrome(service=self.service)
        return self.driver

    def Chrome_WAP(self, path):
        self.service = Service(path)
        self.option = Options()
        mobile_emulation = {"deviceName": "iPhone X"}
        self.option.add_experimental_option("mobileEmulation", mobile_emulation)
        self.driver = webdriver.Chrome(service=self.service, options=self.option)
        return self.driver

    def Firefox_Web(self, path):
        self.driver = webdriver.Firefox(service=Service(path+'geckodriver.exe'))
        return self.driver

    def find_ID(self, value) -> WebElement:
        #AttributeError: 'NoneType' object has no attribute 'click' add -> -> WebElement and add return
        return self.driver.find_element(By.ID, value=value)
    
    def find_Name(self, value) -> WebElement:
        return self.driver.find_element(By.NAME, value=value)
    
    def find_xpath(self, value) -> WebElement:
        return self.driver.find_element(By.XPATH, value=value)
    
    def find_IDs(self, value) -> WebElement:
        return self.driver.find_elements(By.ID, value=value)
    
    def find_Names(self, value) -> WebElement:
        return self.driver.find_elements(By.NAME, value=value)

    def find_xpaths(self, value) -> WebElement:
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
            element.click()
        except ElementNotInteractableException as e:
            print(f"Element is not interactable: {e}")
            screenshot_name = f"Fail_screenshot_{int(time())}.png"
            self.driver.save_screenshot(screenshot_name)
            print(f"Screen has been save as: {screenshot_name}")

    def Save_Screenshot(self, method, value, filename, wait_secs=20):

        try:
            WebDriverWait(self.driver, wait_secs).until(
                EC.element_to_be_clickable((method, value)))
            is_element_displayed = self.driver.find_element(method, value).is_displayed()
            if is_element_displayed:
                self.driver.save_screenshot(filename)
            else: print(f"Element {value} does not display.")
        except:
            print(f"Element {value} is unable show up in {wait_secs} seconds")
            self.driver.save_screenshot(f"Error_{filename}")