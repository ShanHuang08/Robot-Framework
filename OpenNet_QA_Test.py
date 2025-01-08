from Library.Robot_definition import log, run, fail, use_globals_update_keywords
from Library.SeleniumLibraryBase import SeleniumLibBase, SeleniumLibrary
from Library.BaseFunctions import basic_func
from Library.Robot_definition import get_lib_instance
from robot.api.deco import keyword
from time import sleep
import os, subprocess

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

    @keyword('Move files to ${Folder_Name} folder')
    def Move_files_to_report_folder(Folder):
        output = subprocess.run('cd', shell=True, capture_output=True, universal_newlines=True)
        directory = output.stdout.splitlines()
        # Folder_loc = Folder_loc = os.path.join(directory[0], Folder)
        Folder_loc = f'"{directory[0]}\\{Folder}"'
        if not os.path.isdir(Folder_loc):
            os.mkdir(Folder)
        else: print(f"{Folder} already existed")

        files = os.listdir(directory[0])
        # Move files to folder
        for file in files:
            try:
                if any(file.endswith(typ) for typ in ['png', 'html', 'xml', 'txt']):
                    print(file)
                    print(f'move {file} {Folder_loc}')
                    subprocess.run(f'move {file} {Folder_loc}', shell=True, capture_output=True, universal_newlines=True)
            except FileNotFoundError as e:
                print(f'FileNotFoundError: {e}')
                continue

    def Twitch_Scrape(self):
        """Utilize Robot Framework as a test runner"""
        # Go to Twitch main page as WAP view
        self.Open_Browser_in_Mobile_View(self.url, driver_path=self.chromedriver_path)
        self.se_lib.wait_until_element_is_visible('xpath:/html')
        run('Capture_a_Screenshot', 'main page.png')
        # Click the search icon

        # Input StarCraft II to search

        # Scroll down 2 times

        # Select one random streamer

        # on the streamer page wait until all is load and take a screenshot
        # (Need to handle modal or pop-up created by specific streamers)

        sleep(5)
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
                print(f"{key} key has branches:\n")
                for k, v in value.items():
                    # print(k, type(v))
                    for d_typ, typ_s in zip(data_type, type_string):
                        if isinstance(v, d_typ):
                            branch_keys.append(f"{k} : {typ_s} in {key} key")

        main_result = '\n'.join(k for k in main_keys)
        branch_result = '\n'.join(k for k in branch_keys)
        print(f"====== Main Keys ======\n{main_result}\n")
        print(f"====== Branch Keys ======\n{branch_result}")




use_globals_update_keywords(Twitch_test(), globals())