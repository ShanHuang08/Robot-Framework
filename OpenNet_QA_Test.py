from Library.Robot_definition import log, run, fail, use_globals_update_keywords
from Library.SeleniumLibraryBase import SeleniumLibBase, SeleniumLibrary
from Library.BaseFunctions import basic_func
from Library.Robot_definition import get_lib_instance
from time import sleep

class Twitch_test(SeleniumLibBase):
    def __init__(self):
        self.chromedriver_path = 'C:\\Users\\Shan\\Workspace2\\chromedriver.exe'
        self.firefoxdriver_path = 'C:\\Users\\Shan\\Workspace2\\geckodriver.exe'
        self.se_lib = SeleniumLibrary()
        self.url = "https://m.twitch.tv/"
        get_lib_instance('SeleniumLibBase', all_=True)
        
    
    def Check_Network_Connection(self):
        """Utilize ping to check connection"""
        check, output = basic_func.Check_ipaddr(self.url)
        if not check: 
            fail(f'Unable to connect {self.url}\nOutput: {output}')


    def Twitch_Scrape(self):
        self.Open_Browser_in_Mobile_View(self.url, driver_path=self.chromedriver_path)
        self.se_lib.wait_until_element_is_visible('xpath:/html')
        run('Capture_a_Screenshot', 'main page.png')
        self.se_lib.get_session_id()
        sleep(5)
        self.se_lib.close_all_browsers()




use_globals_update_keywords(Twitch_test(), globals())