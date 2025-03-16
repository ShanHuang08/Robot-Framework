from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, SessionNotCreatedException, WebDriverException
from Robot_definition import log, log_color, log_img, run, fail
from time import time
from Library.BaseFunctions import basic_func

class SeleniumBase():
    def __init__(self):
        self.chromedriver_path = 'C:\\Users\\Shan\\Workspace2\\chromedriver.exe'
        self.firefoxdriver_path = 'C:\\Users\\Shan\\Workspace2\\geckodriver.exe'
    
    def Launch_Web(self, driver_name):
        """File path should include `chromedriver.exe`"""
        try:
            if 'chrome' in driver_name.lower():
                self.driver = webdriver.Chrome(service=Service(self.chromedriver_path), options=Options())
                log(f'Launch <b style="color:blue">Chrome_Web</b> driver')
            elif 'firefox' in driver_name.lower():
                self.driver = webdriver.Firefox(service=Service(self.firefoxdriver_path), options=Options())
                log(f'Launch <b style="color:blue">Firefox_Web</b> driver')
            return self.driver
        except SessionNotCreatedException as e:
            log_color(e, 'red', level='ERROR')
        except WebDriverException as e:
            log_color(e, 'red', level='ERROR')


    def Launch_WAP(self, driver_name):
        """Launch WAP"""
        options = Options()
        # options.add_argument("--headless")  
        # options.add_argument("--disable-gpu")  
        try:
            if 'chrome' in driver_name.lower():
                mobile_emulation = {"deviceName": "iPhone X"}
                options.add_experimental_option("mobileEmulation", mobile_emulation)
                self.driver = webdriver.Chrome(service=Service(self.chromedriver_path), options=options)
                log(f'Launch <b style="color:blue">Chrome_WAP</b> driver')
            elif 'firefox' in driver_name.lower():
                mobile_emulation = {"deviceName": "iPhone X"}
                options.add_experimental_option("mobileEmulation", mobile_emulation)
                self.driver = webdriver.Firefox(service=Service(self.firefoxdriver_path), options=options)
                log(f'Launch <b style="color:blue">Firefox_WAP</b> driver')
            return self.driver
        except SessionNotCreatedException as e:
            log_color(e, 'red', level='ERROR')
        except WebDriverException as e:
            log_color(e, 'red', level='ERROR')


    def find_ID(self, value) -> WebElement:
        #AttributeError: 'NoneType' object has no attribute 'click' add -> -> WebElement and add return
        try:
            log(f'Launch find_ID to find {value}', level='DEBUG')
            return self.driver.find_element(By.ID, value=value)
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

    def find_Name(self, value) -> WebElement:
        try:
            log(f'Launch find_Name to find {value}', level='DEBUG')
            return self.driver.find_element(By.NAME, value=value)
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
        try:
            log(f'Launch find_ID to find {value} list', level='DEBUG')
            return self.driver.find_elements(By.ID, value=value)
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
    
    def find_Names(self, value) -> WebElement:
        try:
            log(f'Launch find_Name to find {value} list', level='DEBUG')
            return self.driver.find_elements(By.NAME, value=value)
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
    
    def Click(self, method=By.XPATH, value=''):
        """`method` default value is XPATH"""
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
            fail(f"Element {value} was not clickable after 10 secs.")
        except Exception as e:
            run('Save_Screenshot', f"Fail_screenshot_{int(time())}.png")
            fail(f"An unexpected error occurred: {e}")


    def Wait_until_element_is_displayed(self, method=By.XPATH, value='', wait_secs=10):
        """`method` default value is XPATH"""
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
    

    def Wait_until_element_is_enabled(self, method=By.XPATH, value='', wait_secs=10):
        """`method` default value is XPATH"""
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


    def Wait_until_page_Contain_element(self, method=By.XPATH, value='', wait_secs=10):
        """`method` default value is XPATH"""
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
    

    def Wait_until_element_is_selected(self, method=By.XPATH, value='', wait_secs=10):
        """`method` default value is XPATH"""
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
    
    def Scrolled_into_view(self, locator):
        self.Wait_until_element_is_displayed(value=locator)
        self.find_xpath(locator).location_once_scrolled_into_view
        log(f'Scroll into {locator}')

    def Close_browsers(self):
        self.driver.close()
