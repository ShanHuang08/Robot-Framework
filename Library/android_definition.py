import uiautomator2 as ui_auto
from Popen_test import Cmd_Runner
from adbutils import AdbError
from Library.Robot_definition import log, log_color, log_img, run, use_globals_update_keywords
from time import sleep
import os

class UI_autoFunctions(Cmd_Runner):
    def __init__(self):
        self.d_id = self.Get_device_id()
        self.d = self.Connect_Device()
        self.debug = True # Debug only


    def adb_path(self):
        from shutil import which
        exe = which("adb")
        # print(exe)
        return exe

    def Check_adb_env(self):
        """Check if adb environment has existed"""
        if self.adb_path() is not None:
            check = self.Check_call('adb version')
            return check
        else:
            err_msg = 'No adb enviornment found'
            raise AdbError(err_msg)

    def is_device_alive(self):
        if self.Check_adb_env():
            check = self.Run_cmd('adb devices')
            if self.d_id is None: 
                log_color(f'Device is offline!', 'red')
                return False
            return True

    def Get_device_id(self):
        """Get device id on single case"""
        import re
        output = self.Run_cmd("adb devices")
        match = re.search(r"(\S+)\s+device", output.stdout)
        if match:
            for mat in match.string.split('\n'):
                if '\tdevice' in mat:
                    return mat.split('\t')[0]
        else: print(f'No device detected\n{output.stdout}')


    def Get_device_id_after_pair_completed(self, ip_port, pair_code):
        """adb pair return `guid`, use `guid` as **arg** to run this function"""
        if self.Check_adb_env():
            d_id = self.pair_device(ip_port, pair_code)
            device_id = None
            output = self.Run_cmd('adb devices')
            if d_id in output.stdout:
                for out in output.stdout.splitlines():
                    if d_id in out:
                        device_id = out.split('\t')[0]
                return device_id
            else: 
                print(f'{d_id} is not detected\n{output.stdout}')

    def pair_device(self, ip_port, pair_code):
        """cmd" `adb pair ip:port`
        
        Input pair code"""
        pair = False
        guid=None
        cmd = 'adb pair ' + ip_port
        output = self.Run_cmd(cmd, data_in=pair_code)
        if 'Successfully paired to' in output.stdout: 
            pair=True
            guid = output.stdout.split('=')[-1][:-1] 
            print(f'GUID={guid}') # GUID=adb-39071FDJG0037M-mFgVOc

        if pair:
            print(f"Return code: {output.returncode}\nOutput: {output.stdout}")
            return guid
        else:
            if output.stderr:
                print(f"Return code: {output.returncode}\nError: {output.stderr}")
                return None
            else:
                print(f"Return code: {output.returncode}\nOutput: {output.stdout}")
                return None


    def Connect_Device(self):
        """Connect device and return d"""
        
        if self.is_device_alive():
            d = ui_auto.connect(self.d_id)
            return d
        else:
            raise ConnectionError("Device is disconnected")

    def Wait_for_Element(self, timeout=10, **element):
        """
        Wait foe element appear

        :param d: UIAutomator object

        :param element: send dict format elements, like text="AD", resourceId="xxx"

        `d(**{"text": "AD"}).exists == d(text="AD").exists`
        """
        for _ in range(timeout * 2): 
            if all(self.d(**{key: value}).exists for key, value in element.items()):
                log(f"Find elements")
                return True
            sleep(0.5)

        log_color(f"Fail_to_detect_elements", "red")
        if self.debug: 
            log_color('Collect hierarchy file and stop', 'red')
            self.Dump_hierarchy_to_file() #Debug only
            run('Screenshot_with_log_img', 'Fail_to_detect_elements.png')
            exit() #Debug only
        else: run('Screenshot_with_log_img', 'Fail_to_detect_elements.png')
        return False
            

    def Wait_for_Element_and_Click(self, timeout=10, **element):
        """Wait for element exist and click it"""
        for _ in range(timeout*2):
            for key, value in element.items():
                if 'text' in key:
                    if self.d(text=value).exists:
                        self.d(text=value).click()
                        break
                elif 'resourceId' in key:
                    if self.d(resourceId=value).exists:
                        self.d(resourceId=value).click()
                        break
                elif 'description' in key:
                    if self.d(description=value).exists:
                        self.d(escription=value).click()
                        break
                sleep(0.5)
            
    def Check_device_on_HomeScreen(self, times=2):
        """Check **com.google.android.apps.nexuslauncher:id/launcher** exist"""
        for _ in range(times): 
            if self.d(resourceId="com.google.android.apps.nexuslauncher:id/launcher").exists:
                log("Device is on Home screen")
                return True
            sleep(0.5)
    
        log_color('Device is not on home screen', 'red')
        return False

    def Skip_AD_pages(self):
        if self.d(text="廣告").exists:
            log('Skipping static AD')
            self.Wait_for_Element_and_Click(text="繼續使用應用程式")
            log('Skip AD completed')
        elif self.d(resourceId="Cocos3dGameContainer").exists:
            log('Skipping Game AD')
            sleep(10)
            self.Wait_for_Element_and_Click(description="Close Ad")
            self.Wait_for_Element_and_Click(description="Close Ad")
            # d.click(0.942, 0.073)
            log('Skip AD completed')
        elif self.d(text="View Master Template").exists:
            log('Skipping Game AD')
            sleep(5)
            self.d.click(0.937, 0.029)
            log('Skip AD completed')        


    def Get_Current_Weather_Content(self):
        """Collect weather information"""
        Cur_time = self.d(resourceId="com.accurate.weather.forecast.live:id/tc_time").get_text()
        Location = self.d(resourceId="com.accurate.weather.forecast.live:id/tv_location").get_text()
        Cur_Whether = self.d(resourceId="com.accurate.weather.forecast.live:id/tv_weather_desc").get_text()
        Temp1 = self.d(resourceId="com.accurate.weather.forecast.live:id/tv_temp").get_text()
        Temp2 = self.d(resourceId="com.accurate.weather.forecast.live:id/tv_temp_unit").get_text()
        CurTemp = Temp1 + Temp2
        Body_temp = self.d(resourceId="com.accurate.weather.forecast.live:id/tv_reel_temp").get_text()
        Min_Temp = self.d(resourceId="com.accurate.weather.forecast.live:id/tv_min_temp").get_text()
        Max_Temp = self.d(resourceId="com.accurate.weather.forecast.live:id/tv_max_temp").get_text()

        # d.swipe_ext()
        log_color('\n=============Content=============\n', 'blue')
        log(f"Time: {Cur_time}\nLocation: {Location}\nWeather: {Cur_Whether}\nTemperture: {CurTemp} ({Min_Temp}-{Max_Temp}) \
                \nBody Temp: {Body_temp}")
        log_color('\n=================================', 'blue')

    def Exit_Weather_Live(self, **element):
        """`d(**{"text": "AD"}).exists == d(text="AD").exists`"""
        try:
            self.d.press("back")
            log('Exit App')
            sleep(0.5)
            if not self.Check_device_on_HomeScreen(times=1):
                for key, value in element.items():
                    self.d(**{key: value}).click()
            self.Check_device_on_HomeScreen()
        except:
            log_color('Exit app fail\nSave error screenshot', color='red')
            run('Screenshot_with_log_img', 'Exit app fail.png')

    def Exit_App(self, retry=3):
        check = False
        self.d.press("back")
        log('Exit App')
        sleep(0.5)
        for _ in range(retry):
            check = self.Check_device_on_HomeScreen(times=1)
            if check:
                break
            self.d.press("back")

        if not check:
            log_color('Exit app fail\nSave error screenshot', color='red')
            run('Screenshot_with_log_img', 'Exit app fail.png')


    def Dump_hierarchy_to_file(self):
        page_elements = self.d.dump_hierarchy()
        filename = 'dump_hierarchy.xml'
        xml_file = open(filename, mode='w', encoding='utf-8')
        xml_file.write(page_elements)
        xml_file.close()

        if os.path.exists(filename):
            print(f"{filename} has been generated")
        else: print('File generate failed')

    def Screenshot_with_log_img(self, filename:str):
        """Take screenshot and log png"""
        if '.png' in filename:
            self.d.screenshot(filename)
            current_directory = os.getcwd()
            src = current_directory + '\\' +filename
            log_img(src)
        else: log_color('File name format is incorrect\nCan not capture screenshot', color='red')

use_globals_update_keywords(UI_autoFunctions(), globals())
