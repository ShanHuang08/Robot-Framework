# TQA測試: Selenium
from selenium.webdriver.common.by import By
from time import sleep
from Library.SeleniumBase import SeleniumBase
from Library.SeleniumLibraryBase import SeleniumLibBase
from Library.Robot_definition import log, run, use_globals_update_keywords, get_lib_instance
from Library.WebElements import Cathay_Xpath
from SeleniumLibrary import SeleniumLibrary


class Cathay(SeleniumLibBase):
    def __init__(self):
        self.chromedriver_path = 'C:\\Users\\Shan\\Workspace2\\chromedriver.exe'
        self.firefoxdriver_path = 'C:\\Users\\Shan\\Workspace2\\geckodriver.exe'
        self.url = "https://www.cathaybk.com.tw/cathaybk/"
        self.se_lib = SeleniumLibrary()
        self.se_base = SeleniumBase()
        get_lib_instance('SeleniumLibBase', all_=True)

    def Scrap_Cathay(self):
        # options.add_argument("--headless")  
        # options.add_argument("--disable-gpu")  
        self.driver = self.se_base.Chrome_WAP(self.chromedriver_path)

        # 1. 使用Chrome App到國泰世華銀行官網(https://www.cathaybk.com.tw/cathaybk/)並將畫面截圖。
        log(f'Access to {self.url}')
        self.driver.get(self.url)
        self.se_base.Save_Screenshot(By.XPATH, '/html', filename='main page.png')

        # 2. 點選左上角選單，進入 個人金融 > 產品介紹 > 信用卡列表，需計算有幾個項目在信用卡選單下面，並將畫面截圖。
        self.se_base.Click_Element(By.XPATH, Cathay_Xpath['Menu'])
        self.se_base.Click_Element(By.XPATH, Cathay_Xpath['產品介紹'])
        self.se_base.Click_Element(By.XPATH, Cathay_Xpath['信用卡'])
        self.se_base.Save_Screenshot(By.XPATH, Cathay_Xpath['掛失信用卡'], filename='credit card service list.png')
        # card_services = driver.find_elements(By.XPATH, value='//div[@class="cubre-a-menuSortBtn" and contains(@class, "cubre-u-mbOnly")]/a') #It's not working
        card_services = self.se_base.find_xpaths(value=Cathay_Xpath['Card Service list'])
        if card_services:
            log(f"{len(card_services)} items are in the card services")
            for service in card_services:
                log(service.text)

        # 3. 個人金融 > 產品介紹 > 信用卡 > 卡片介紹 > 計算頁面上所有(停發)信用卡數量並截圖
        self.se_base.Click_Element(By.XPATH, Cathay_Xpath['卡片介紹'])

        # card_list = driver.find_elements(By.XPATH, value='//div[@class="cubre-m-compareCard -credit"]/div[@class="cubre-m-compareCard__title"]')
        card_list = self.se_base.find_xpaths(value=Cathay_Xpath['已停發'])
        if card_list: log(f'所有停發信用卡有{len(card_list)}張')

        # card_pics = driver.find_elements(By.XPATH, value='//div[@class="cubre-m-compareCard__pic"]/img')
        card_pics = self.se_base.find_xpaths(value=Cathay_Xpath['已停發圖片連結'])
        card_links = []
        if card_pics:
            for pic in card_pics:
                image_src = pic.get_attribute("src")
                if 'png' in image_src: 
                    # print(image_src)
                    card_links.append(image_src)
        self.se_base.Get_Card_Screenshots(card_links)
        self.driver.quit()


    def Get_cards_screenshot(self, card_links):
        num = 1
        for link in card_links:
            ob_filename = f'Obsolete_card_{num}.png'
            self.Open_Browser_in_Mobile_View(link, driver_path=self.chromedriver_path) 
            sleep(2)
            run('Capture_a_Screenshot', ob_filename)
            self.se_lib.close_browser()
            num+=1

    def Robot_Keyword_Scrap_Cathay(self):
        self.Open_Browser_in_Mobile_View(self.url, driver_path=self.chromedriver_path) 
        self.se_lib.wait_until_element_is_visible('xpath:/html')
        run('Capture_a_Screenshot', 'main page.png')

        self.Click_Element('xpath:'+Cathay_Xpath['Menu'])
        self.Click_Element('xpath:'+Cathay_Xpath['產品介紹'])
        self.Click_Element('xpath:'+Cathay_Xpath['信用卡'])

        self.se_lib.wait_until_element_is_visible('xpath:'+Cathay_Xpath['掛失信用卡'])
        run('Capture_a_Screenshot', 'credit card list.png')

        self.se_lib.wait_until_page_contains_element('xpath:'+Cathay_Xpath['Card Service list'])
        card_services = self.se_lib.get_webelements('xpath:'+Cathay_Xpath['Card Service list'])

        if card_services:
            log(f'{len(card_services)} card services have captured')
            for service in card_services:
                log(service.text)
        
        self.Click_Element('xpath:'+Cathay_Xpath['卡片介紹'])

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
        # log(card_links, level='DEBUG')
        self.Get_cards_screenshot(card_links)
        self.se_lib.close_all_browsers()

use_globals_update_keywords(Cathay(), globals())

# TQA測試: 程式邏輯題目
def question1(input_list:list):
    """
    - Input: [35, 46, 57, 91, 29]
    - Output: [53, 64, 75, 19, 92]
    """
    def reverse_double_digit(digit:int):
        digit = str(digit)
        if len(digit) == 2: return int(str(digit[-1]) + str(digit[0]))
    output_list = [reverse_double_digit(num) for num in input_list]
    return output_list


def question2(input_text:str):
    """
    - Input: "Hello welcome to Cathay 60th year anniversary"
    - Output: digit and al counts
    """
    exclude = []
    text_dict = {}
    input_text = input_text.upper()
    input_text = ''.join(text for text in input_text if text != ' ')

    for text in input_text:
        if text not in exclude:
            text_dict[text] = input_text.count(text)
            exclude.append(text)
    sorted_list = sorted(text_dict.items())
    answer = '\n'.join(ans[0]+' '+str(ans[1]) for ans in sorted_list)
    return answer


def question3(n:int):
    """
    - Input: 0-100
    - Output: The last order is {num}
    """
    if not 0 <= n <= 100: 
        print('n range should be between 0 to 100')
    else: 
        num = 1
        for i in range(n):
            if i % 3 != 0:
                num+=1
        print(f"The last order is {num}")


if __name__=='__main__':
    # 程式邏輯題目
    # question1([35, 46, 57, 91, 29])
    # question2("Hello welcome to Cathay 60th year anniversary")
    # question3(random.randint(0, 100))
    # 自動化測試
    Cathay().Scrap_Cathay()