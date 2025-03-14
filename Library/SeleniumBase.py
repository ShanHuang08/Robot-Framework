from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from Robot_definition import log, log_color, log_img, run, fail
from time import time


class SeleniumBase():
    
    def Chrome_Web(self, driver_path):
        """File path should include `chromedriver.exe`"""
        self.driver = webdriver.Chrome(service=Service(driver_path))
        log(f'Launch Chrome_Web driver')
        return self.driver

    def Launch_WAP(self, driver_path):
        import os
        driver_name = os.path.basename(driver_path)
        service = Service(driver_path)
        option = Options()
        if 'chrome' in driver_name.lower():
            mobile_emulation = {"deviceName": "iPhone X"}
            option.add_experimental_option("mobileEmulation", mobile_emulation)
            self.driver = webdriver.Chrome(service=service, options=option)
            log(f'Launch <b style="color:blue">Chrome_WAP</b> driver')
        elif 'gecko' in driver_name.lower():
            mobile_emulation = {"deviceName": "iPhone X"}
            option.add_experimental_option("mobileEmulation", mobile_emulation)
            self.driver = webdriver.Firefox(service=service, options=option)
            log(f'Launch <b style="color:blue">Firefox_WAP</b> driver')
        return self.driver

    def Firefox_Web(self, path):
        self.driver = webdriver.Firefox(service=Service(path))
        log(f'Launch Firefox_Web driver')
        return self.driver

    def find_ID(self, value) -> WebElement:
        #AttributeError: 'NoneType' object has no attribute 'click' add -> -> WebElement and add return
        log(f'Launch find_ID to find {value}', level='DEBUG')
        return self.driver.find_element(By.ID, value=value)
    
    def find_Name(self, value) -> WebElement:
        log(f'Launch find_Name to find {value}', level='DEBUG')
        return self.driver.find_element(By.NAME, value=value)
    
    def find_xpath(self, value) -> WebElement:
        log(f'Launch find_xpath to find {value}', level='DEBUG')
        try:
            return self.driver.find_element(By.XPATH, value=value)
        except NoSuchElementException:
            log_color(f"Element {value} was not found.", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
        except ElementNotInteractableException as e:
            log(f"Element is not interactable: {e}")
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
        except TimeoutException:
            log_color(f"Element {value} was not clickable after 10 secs.", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
        except Exception as e:
            log_color(f"An unexpected error occurred: {e}", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
        
    
    def find_IDs(self, value) -> WebElement:
        log(f'Launch find_ID to find {value} list', level='DEBUG')
        return self.driver.find_elements(By.ID, value=value)
    
    def find_Names(self, value) -> WebElement:
        log(f'Launch find_Name to find {value} list', level='DEBUG')
        return self.driver.find_elements(By.NAME, value=value)

    def find_xpaths(self, value) -> WebElement:
        log(f'Launch find_xpath to find {value} list', level='DEBUG')
        try:
            return self.driver.find_elements(By.XPATH, value=value)
        except NoSuchElementException:
            log_color(f"Element {value} was not found.", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
        except ElementNotInteractableException as e:
            log(f"Element is not interactable: {e}")
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
        except TimeoutException:
            log_color(f"Element {value} was not clickable after 10 secs.", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
        except Exception as e:
            log_color(f"An unexpected error occurred: {e}", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
        

    def get_window_handles(self):
        """return list with handles. Cooperate with `switch_window()`"""
        return self.driver.window_handles
    
    def Click_it(self, method, value):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((method, value)))
            log(f"Click {value}")
            element.click()
        except ElementNotInteractableException as e:
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            fail(f"Element is not interactable: {e}")
        except TimeoutException:
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            fail(f"Element {value} was not clickable after 10 secs.", 'red', level='ERROR')
        except Exception as e:
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            fail(f"An unexpected error occurred: {e}", 'red', level='ERROR')


    def Wait_until_element_is_displayed(self, method, value, wait_secs=10):
        try:
            element = WebDriverWait(self.driver, wait_secs).until(
                EC.visibility_of_element_located((method, value)))
            log_color(f"Element {value} is displayed.", 'blue')
            return element
        except NoSuchElementException:
            log_color(f"Element {value} was not found.", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            return None
        except TimeoutException:
            log_color(f"Element {value} was not visible within {wait_secs} seconds.", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            return None
        except Exception as e:
            log_color(f"An unexpected error occurred: {e}", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            return None
    

    def Wait_until_element_is_enabled(self, method, value, wait_secs=10):
        try:
            element = WebDriverWait(self.driver, wait_secs).until(
                EC.element_to_be_clickable((method, value)))
            log_color(f"Element {value} does not enable.", 'blue')
            return element
        except NoSuchElementException:
            log_color(f"Element {value} was not found.", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            return None
        except TimeoutException:
            log_color(f"Element {value} did not enabled within {wait_secs} seconds.", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            return None
        except Exception as e:
            log_color(f"An unexpected error occurred: {e}", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            return None


    def Wait_until_page_Contain_element(self, method, value, wait_secs=10):
        try:
            element = WebDriverWait(self.driver, wait_secs).until(
                EC.presence_of_element_located((method, value)))
            log_color(f"Element {value} is detected.", 'blue')
            return element
        except NoSuchElementException:
            log_color(f"Element {value} was not found.", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            return None
        except TimeoutException:
            log_color(f"Element {value} did not detected within {wait_secs} seconds.", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            return None
        except Exception as e:
            log_color(f"An unexpected error occurred: {e}", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            return None
    

    def Wait_until_element_is_selected(self, method, value, wait_secs=10):
        try:
            element = WebDriverWait(self.driver, wait_secs).until(
                EC.element_located_to_be_selected((method, value)))
            log_color(f"Element {value} does not be selected.", 'blue')
            return element
        except NoSuchElementException:
            log_color(f"Element {value} was not found.", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            return None
        except TimeoutException:
            log_color(f"Element {value} did not selected within {wait_secs} seconds.", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            return None
        except Exception as e:
            log_color(f"An unexpected error occurred: {e}", 'red', level='ERROR')
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            return None
        

    def Save_Screenshot(self, filename):
        self.driver.save_screenshot(f"{filename}")
        log_img(filename)
    
    def Scroll_into_view_on_Base(self, locator):
        self.Wait_until_element_is_displayed(By.XPATH, locator)
        self.find_xpath(locator).location_once_scrolled_into_view
