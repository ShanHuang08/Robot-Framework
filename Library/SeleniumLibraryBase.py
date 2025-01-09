from SeleniumLibrary import SeleniumLibrary
from Library.Robot_definition import log, run
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
import os
from time import sleep

class SeleniumLibBase():
    def __init__(self):
        self.se_lib = SeleniumLibrary()
    
    def Open_Browser_in_Mobile_View(self, url, driver_path):
        """Needs `url` and `Driver path`"""
        driver_name = os.path.basename(driver_path)
        if 'chrome' in driver_name.lower():
            self.se_lib.open_browser(url, 'chrome', executable_path=driver_path)
        elif 'gecko' in driver_name.lower():
            self.se_lib.open_browser(url, 'firefox', executable_path=driver_path)
        else: 
            raise ValueError(f"Invalid driver name: {driver_name} ((e.g., chromedriver or geckodriver))")
        
        self.se_lib.set_window_size(width=414, height=996)
        self.se_lib.execute_javascript('window.navigator.userAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) \
                                        AppleWebKit/605.1.1 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"')
    
    def Capture_a_Screenshot(self, filename):
        self.se_lib.capture_page_screenshot(filename)

    def Click_Element(self, locator, timeout=30):
        try:
            self.se_lib.wait_until_page_contains_element(locator)
            self.se_lib.element_should_be_visible(locator)
            self.se_lib.element_should_be_enabled(locator)
            self.se_lib.click_element(locator)
        except TimeoutException as e:
            log(f"Timeout waiting for element {locator} after {timeout} seconds.\n{e}", level='WARN')
            run('Capture_a_Screenshot', f'Click {locator} fail!')
            raise AssertionError(f"Timeout waiting for element {locator}")
        except ElementNotInteractableException as e:
            log(f"Element {locator} is not interactable (e.g., hidden or disabled).\n{e}", level='WARN')
            run('Capture_a_Screenshot', f'{locator} not interactable')
            raise AssertionError(f"Element {locator} is not interactable")
        except Exception as e:
            log(f"An unexpected error occurred while clicking {locator}: {e}", level='ERROR')
            run('Capture_a_Screenshot', f'Click {locator} unexpected error')
            raise AssertionError(f"An unexpected error occurred while clicking {locator}")
    
    def Input_to_Textfield(self, locator, text):
        try:
            self.se_lib.wait_until_page_contains_element(locator)
            self.se_lib.element_should_be_visible(locator)
            self.se_lib.element_should_be_enabled(locator)
            self.se_lib.input_text(locator, text)
        except ElementNotInteractableException as e:
            log(f"Element {locator} is not interactable (e.g., hidden or disabled).\n{e}", level='WARN')
            run('Capture_a_Screenshot', f'{locator} not interactable')
            raise AssertionError(f"Element {locator} is not interactable")        
        except Exception as e:
            log(f"An unexpected error occurred while clicking {locator}: {e}", level='ERROR')
            run('Capture_a_Screenshot', f'Click {locator} unexpected error')
            raise AssertionError(f"An unexpected error occurred while clicking {locator}")       


    def Scroll_into_view(self, locator):
        self.se_lib.wait_until_element_is_visible(locator)
        self.se_lib.scroll_element_into_view(locator)
        sleep(1)
  