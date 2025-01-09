from Library.Robot_definition import log, log_color, run, fail, use_globals_update_keywords
from Library.SeleniumLibraryBase import SeleniumLibBase, SeleniumLibrary
from Library.BaseFunctions import basic_func
from Library.Robot_definition import get_lib_instance
from Library.WebElements import Twitch_Xpath


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
        self.se_lib.wait_until_element_is_visible('xpath:'+Twitch_Xpath["Check controller is hidden"], timeout=20)
        run('Capture_a_Screenshot', 'Live Streaming.png')
        self.se_lib.close_all_browsers()
    

    def Get_keys_from_response(response):
        main_keys = []
        branch_keys = []
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

        main_result = '\n'.join(k for k in main_keys)
        branch_result = '\n'.join(k for k in branch_keys)
        log(f"====== Main Keys ======\n{main_result}\n")
        log(f"====== Branch Keys ======\n{branch_result}")




use_globals_update_keywords(Twitch_test(), globals())