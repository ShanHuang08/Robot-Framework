# TQA測試: Selenium
from time import sleep
from Library.Robot_definition import log, use_globals_update_keywords, run
from Library.WebElements import Cathay_Xpath
from SeleniumLibrary import SeleniumLibrary

class Cathay():
    def __init__(self):
        self.chromedriver_path = 'C:\\Users\\Shan\\Workspace2\\chromedriver.exe'
        self.url = "https://www.cathaybk.com.tw/cathaybk/"
        self.se_lib = SeleniumLibrary()

    def Start_Chrome_in_Mobile_View(self):
        self.se_lib.open_browser(self.url, 'Chrome', executable_path=self.chromedriver_path)
        self.se_lib.set_window_size(width=414, height=996)
        self.se_lib.execute_javascript('window.navigator.userAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) \
                                        AppleWebKit/605.1.1 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"')

    def Take_Screenshot(self, filename):
        self.se_lib.capture_page_screenshot(filename)

    def Get_cards_screenshot(self, card_links):
        num = 1
        for link in card_links:
            ob_filename = f'Obsolete_card_{num}.png'
            self.se_lib.open_browser(link, 'Chrome', executable_path=self.chromedriver_path)
            sleep(2)
            run('Take_Screenshot', ob_filename)
            self.se_lib.close_browser()
            num+=1

    def Wait_and_Click_Element(self, locator):
        self.se_lib.wait_until_page_contains_element(locator)
        self.se_lib.click_element(locator)

    def Robot_Keyword_Scrap_Cathay(self):
        # options.add_argument("--headless")  
        # options.add_argument("--disable-gpu")  
        self.Start_Chrome_in_Mobile_View() 
        self.se_lib.wait_until_element_is_visible('xpath:/html')
        run('Take_Screenshot', 'main page.png')

        self.Wait_and_Click_Element('xpath:'+Cathay_Xpath['Menu'])
        self.Wait_and_Click_Element('xpath:'+Cathay_Xpath['產品介紹'])
        self.Wait_and_Click_Element('xpath:'+Cathay_Xpath['信用卡'])

        self.se_lib.wait_until_element_is_visible('xpath:'+Cathay_Xpath['掛失信用卡'])
        run('Take_Screenshot', 'credit card list.png')

        self.se_lib.wait_until_page_contains_element('xpath:'+Cathay_Xpath['Card Service list'])
        card_services = self.se_lib.get_webelements('xpath:'+Cathay_Xpath['Card Service list'])

        if card_services:
            log(f'{len(card_services)} card services have captured')
            for service in card_services:
                log(service.text)
        
        self.Wait_and_Click_Element('xpath:'+Cathay_Xpath['卡片介紹'])

        self.se_lib.wait_until_page_contains_element('xpath:'+Cathay_Xpath['已停發'])
        card_list = self.se_lib.get_webelements('xpath:'+Cathay_Xpath['已停發'])
        if card_list: log(f'所有停發信用卡有{len(card_list)}張')
        
        self.se_lib.wait_until_page_contains_element('xpath:'+Cathay_Xpath['已停發圖片連結'])
        card_pics = self.se_lib.get_webelements('xpath:'+Cathay_Xpath['已停發圖片連結'])
        card_links = []
        for pic in card_pics:
            image_src = pic.get_attribute("src")
            if 'png' in image_src: 
                card_links.append(image_src)

        self.Get_cards_screenshot(card_links)
        # Not finish yet...

        self.se_lib.close_all_browsers()

use_globals_update_keywords(Cathay(), globals())       

if __name__=='__main__':
    # 自動化測試
    Cathay().Robot_Keyword_Scrap_Cathay()