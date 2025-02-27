from Library.android_definition import UI_autoFunctions
from Library.Robot_definition import log, log_color, run, use_globals_update_keywords, fail
from time import sleep


class UI_Test(UI_autoFunctions):

    def Open_Weather_forcast_live(self):
        """Open `com.accurate.weather.forecast.live` app"""
        App_name = 'com.accurate.weather.forecast.live'
        self.d.press("home")
        sleep(1)

        # Launch app
        self.d.app_start(App_name)
        log(f'Launch {App_name}')
        sleep(5) #Loading time

        # Skip AD pages
        self.Skip_AD_pages()
        
        # Skip upgrade page
        if self.d(text="高級專業版").exists:
            log('Skip upgrade page')
            self.Wait_for_Element_and_Click(timeout=5, resourceId=App_name + ":id/iv_close")

        # Skip rate pop-up dialog
        if self.d(resourceId=App_name + ":id/rate_close").exists:
            log("Skip rate pop-up dialog")
            self.Wait_for_Element_and_Click(timeout=5, resourceId=App_name + ":id/rate_close")

        # Check APP main page
        Check_Main_page = self.Wait_for_Element(text="未來2小時預報", resourceId=App_name + ":id/btn_radar")
        if Check_Main_page:
            log_color('Weather Forcast App has launched sucessfully', 'blue')
            run('Screenshot_with_log_img', 'Weather_Forcast_App.png')
            self.Get_Current_Weather_Content()

        # Exit app
        self.Exit_Weather_Live(resourceId=App_name + ":id/btn_exit")

    def Check_device_connection(self):
        check = self.is_device_alive()
        if not check:
            fail('Device is offline!')

use_globals_update_keywords(UI_Test(), globals())