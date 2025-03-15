from SeleniumLibrary import SeleniumLibrary
from Robot_definition import log, log_color, run
from SeleniumBase import SeleniumBase
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, SessionNotCreatedException, WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver import ChromeOptions
from time import sleep

class SeleniumLibBase():
    def __init__(self):
        self.se_lib = SeleniumLibrary()
        self.chromedriver_path = 'C:\\Users\\Shan\\Workspace2\\chromedriver.exe'
        self.firefoxdriver_path = 'C:\\Users\\Shan\\Workspace2\\geckodriver.exe'
    
    def Open_Browser_in_Mobile_View(self, url, driver_name):
        """Needs `url` and `Driver name` : 'chrome' or 'firefox'"""
        try:
            if 'chrome' in driver_name.lower():
                log('Launch <b style="color: blue">Chrome</b> browser')
                self.se_lib.open_browser(url, 'chrome', options=ChromeOptions(), service=ChromeService(self.chromedriver_path))
            elif 'firefox' in driver_name.lower():
                log('Launch <b style="color: blue">Firefox</b> browser')
                self.se_lib.open_browser(url, 'firefox', executable_path=self.firefoxdriver_path)
            else: 
                raise ValueError(f"Invalid driver name: {driver_name}")
            
            self.se_lib.set_window_size(width=414, height=996)
            self.se_lib.execute_javascript('window.navigator.userAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) \
                                            AppleWebKit/605.1.1 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"')
        except SessionNotCreatedException as e:
            log_color(e, 'red', level='ERROR')
        except WebDriverException as e:
            log_color(e, 'red', level='ERROR')
    
    def Capture_a_Screenshot(self, filename):
        self.se_lib.capture_page_screenshot(filename)

    def Click_Element(self, locator, timeout=30):
        try:
            self.se_lib.wait_until_page_contains_element(locator, timeout=timeout)
            self.se_lib.wait_until_element_is_visible(locator, timeout=timeout)
            self.se_lib.wait_until_element_is_enabled(locator, timeout=timeout)
            self.se_lib.click_element(locator)
        except TimeoutException as e:
            log(f"Timeout waiting for element {locator} after {timeout} seconds.\n{e}", level='WARN')
            run('Capture_a_Screenshot', 'Click Element fail.png')
            raise AssertionError(f"Timeout waiting for element {locator}")
        except ElementNotInteractableException as e:
            log(f"Element {locator} is not interactable (e.g., hidden or disabled).\n{e}", level='WARN')
            run('Capture_a_Screenshot', 'Click Element is not interactable.png')
            raise AssertionError(f"Element {locator} is not interactable")
        except Exception as e:
            log(f"An unexpected error occurred while clicking {locator}: {e}", level='ERROR')
            run('Capture_a_Screenshot', 'Click element but got unexpected error.png')
            raise AssertionError(f"An unexpected error occurred while clicking {locator}")
    
    def Input_to_Textfield(self, locator, text, timeout=10):
        try:
            self.se_lib.wait_until_page_contains_element(locator, timeout=timeout)
            self.se_lib.wait_until_element_is_visible(locator, timeout=timeout)
            self.se_lib.wait_until_element_is_enabled(locator, timeout=timeout)
            self.se_lib.input_text(locator, text)
        except ElementNotInteractableException as e:
            log(f"Element {locator} is not interactable (e.g., hidden or disabled).\n{e}", level='WARN')
            run('Capture_a_Screenshot', 'Input element not interactable.png')
            raise AssertionError(f"Element {locator} is not interactable")        
        except Exception as e:
            log(f"An unexpected error occurred while clicking {locator}: {e}", level='ERROR')
            run('Capture_a_Screenshot', 'Input element got unexpected error.png')
            raise AssertionError(f"An unexpected error occurred while clicking {locator}")       


    def Scroll_into_view(self, locator):
        self.se_lib.wait_until_element_is_visible(locator)
        self.se_lib.scroll_element_into_view(locator)
        sleep(1)
    
    def Close_down_all_browsers(self):
        self.se_lib.close_all_browsers()
        SeleniumBase().Close_browsers()
  