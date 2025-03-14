# TQA測試: Selenium
from selenium.webdriver.common.by import By
from time import sleep
from Library.SeleniumBase import SeleniumBase
from Library.SeleniumLibraryBase import SeleniumLibBase
from Library.Robot_definition import log, log_color, log_img, fail, run, use_globals_update_keywords
from Library.WebElements import Cathay_Xpath
from SeleniumLibrary import SeleniumLibrary


class Cathay(SeleniumLibBase, SeleniumBase):
    def __init__(self):
        self.chromedriver_path = 'C:\\Users\\Shan\\Workspace2\\chromedriver.exe'
        self.firefoxdriver_path = 'C:\\Users\\Shan\\Workspace2\\geckodriver.exe'
        self.url = "https://www.cathaybk.com.tw/cathaybk/"
        self.se_lib = SeleniumLibrary()
        self.timeout = 10

    def Scrap_Cathay(self):
        # options.add_argument("--headless")  
        # options.add_argument("--disable-gpu")  
        self.driver = self.Launch_WAP(self.chromedriver_path)

        # 1. 使用Chrome App到國泰世華銀行官網(https://www.cathaybk.com.tw/cathaybk/)並將畫面截圖。
        log(f'Access to <a href="{self.url}" target="_blank">{self.url}</a>')
        self.driver.get(self.url)
        self.Wait_until_element_is_displayed(By.XPATH, '/html')
        run('Save_Screenshot', 'App main page.png')
        # 2. 點選左上角選單，進入 個人金融 > 產品介紹 > 信用卡列表，需計算有幾個項目在信用卡選單下面，並將畫面截圖。
        self.Click_it(By.XPATH, Cathay_Xpath['Menu'])
        self.Click_it(By.XPATH, Cathay_Xpath['產品介紹'])
        self.Click_it(By.XPATH, Cathay_Xpath['信用卡'])

        self.Wait_until_page_Contain_element(By.XPATH, '//div[contains(@class, "is-L2open")]')
        self.Wait_until_element_is_displayed(By.XPATH, Cathay_Xpath['掛失信用卡'])
        
        card_services = self.find_xpaths(Cathay_Xpath['Card Service list'])
        if card_services:
            log(f"{len(card_services)} items are in the card services")
            for service in card_services:
                log(service.text)
        run('Save_Screenshot', 'credit card services list.png')
        # 3-1. 個人金融 > 產品介紹 > 信用卡 > 卡片介紹 > 計算頁面上所有(停發)信用卡數量
        self.Click_it(By.XPATH, Cathay_Xpath['卡片介紹'])
        
        attr = self.Check_BlockName('停發卡', 'Base')

        self.Wait_until_page_Contain_element(By.XPATH, f'//section[@data-anchor-block="{attr}"]//div[@class="cubre-m-compareCard__title"]')


        card_list = self.find_xpaths(f'//section[@data-anchor-block="{attr}"]//div[@class="cubre-m-compareCard__title"]')
        if card_list: log(f'所有停發信用卡有{len(card_list)}張')

        self.Wait_until_page_Contain_element(By.XPATH, f'//section[@data-anchor-block="{attr}"]//img')
        card_pics = self.find_xpaths(f'//section[@data-anchor-block="{attr}"]//img')
        card_links = []
        if card_pics:
            for pic in card_pics:
                image_src = pic.get_attribute("src")
                if 'png' in image_src: 
                    card_links.append(image_src)
        run('log_cards_img', card_links)
        # 3-2. 查看所有停發信用卡並截圖
        span_list = self.find_xpaths(f'//section[@data-anchor-block="{attr}"]//span[@role="button"]')
        log_color(f'Detect {len(span_list)} Span buttons', 'blue')
        # 比對信用卡數量和Span按鈕數量是否相同
        if len(card_list) == len(span_list):
            log_color('Card titles match with Span buttons', 'blue')
        else:
            fail('Card titles does not match with Span buttons', 'red')

        Total_screenshots = self.Get_screenshot_of_cards(span_list, attr)
        # 比對截圖數量跟信用卡數量
        if Total_screenshots == len(card_list):
            log_color('Captured screenshots match with Credit cards', 'blue')
        else:
            fail(f'Captured screenshots does not match with Credit cards\nScreenshots: {Total_screenshots}\nCredit cards: {len(card_list)}')        

        self.driver.quit()


    def Robot_Keyword_Scrap_Cathay(self):
        # 1. 使用Chrome App到國泰世華銀行官網(https://www.cathaybk.com.tw/cathaybk/)並將畫面截圖。
        self.Open_Browser_in_Mobile_View(self.url, driver_path=self.chromedriver_path) 
        self.se_lib.wait_until_element_is_visible('xpath:/html', timeout=self.timeout)
        run('Capture_a_Screenshot', 'main page.png')
        # 2. 點選左上角選單，進入 個人金融 > 產品介紹 > 信用卡列表，需計算有幾個項目在信用卡選單下面，並將畫面截圖。
        self.Click_Element('xpath:'+Cathay_Xpath['Menu'])
        self.Click_Element('xpath:'+Cathay_Xpath['產品介紹'])
        self.Click_Element('xpath:'+Cathay_Xpath['信用卡'])

        self.se_lib.wait_until_page_contains_element('xpath://div[contains(@class, "is-L2open")]', timeout=self.timeout)
        self.se_lib.wait_until_element_is_visible('xpath:'+Cathay_Xpath['掛失信用卡'], timeout=self.timeout)
        
        self.se_lib.wait_until_page_contains_element('xpath:'+Cathay_Xpath['Card Service list'], timeout=self.timeout)
        card_services = self.se_lib.get_webelements('xpath:'+Cathay_Xpath['Card Service list'])
        
        if card_services:
            log(f'{len(card_services)} card services have captured')
            for service in card_services:
                log(service.text)
        run('Capture_a_Screenshot', 'credit card services list.png')
        # 3-1. 個人金融 > 產品介紹 > 信用卡 > 卡片介紹 > 計算頁面上所有(停發)信用卡數量
        self.Click_Element('xpath:'+Cathay_Xpath['卡片介紹'])

        attr = self.Check_BlockName('停發卡', 'Robot')
        
        self.se_lib.wait_until_page_contains_element(f'xpath://section[@data-anchor-block="{attr}"]//div[@class="cubre-m-compareCard__title"]')

        card_list = self.se_lib.find_elements(f'xpath://section[@data-anchor-block="{attr}"]//div[@class="cubre-m-compareCard__title"]')
        if card_list: 
            log_color(f'所有停發信用卡有{len(card_list)}張', 'blue')
        
        self.se_lib.wait_until_page_contains_element(f'xpath://section[@data-anchor-block="{attr}"]//img', timeout=self.timeout)

        card_pics = self.se_lib.get_webelements(f'xpath://section[@data-anchor-block="{attr}"]//img')
        card_links = []
        for pic in card_pics:
            image_src = pic.get_attribute("src")
            if 'png' in image_src: 
                card_links.append(image_src)

        run('log_cards_img', card_links)

        # 3-2. 查看所有停發信用卡並截圖, 
        span_list = self.se_lib.get_webelements(f'xpath://section[@data-anchor-block="{attr}"]//span[@role="button"]')
        log_color(f'Detect {len(span_list)} Span buttons', 'blue')
        # 比對信用卡數量和Span按鈕數量是否相同
        if len(card_list) == len(span_list):
            log_color('Card titles match with Span buttons', 'blue')
        else:
            fail('Card titles does not match with Span buttons', 'red')

        Total_screenshots = self.Get_cards_screenshot(span_list, attr)
        # 比對截圖數量跟信用卡數量
        if Total_screenshots == len(card_list):
            log_color('Captured screenshots match with Credit cards', 'blue')
        else:
            fail(f'Captured screenshots does not match with Credit cards\nScreenshots: {Total_screenshots}\nCredit cards: {len(card_list)}')

        self.se_lib.close_all_browsers()


    def Check_BlockName(self, name, source):
        Ob_Tabs = []
        if source == 'Robot':
            Ob_Tabs = self.se_lib.find_elements('xpath:'+Cathay_Xpath['卡片介紹Tabs'])
        elif source == 'Base':
            Ob_Tabs = self.find_xpaths(Cathay_Xpath['卡片介紹Tabs'])
            log(Ob_Tabs)
        else:
            raise ValueError('Source param is incorrect!')

        attr = 'blockname0'
        for ob in Ob_Tabs:
            text = ob.get_attribute("textContent").strip()
            # log(text+str(ob.get_attribute("data-anchor-btn")))
            if text == name:
                attr = ob.get_attribute("data-anchor-btn")
                log(f'{text} use {attr}')
        return attr

    def log_cards_img(self, card_links):
        num = 1
        for link in card_links:
            ob_filename = f'Obsolete_card_{num}'
            log_color(ob_filename, 'blue')
            log_img(link)
            num+=1
    
    def Get_cards_screenshot(self, span_list, attr):
        self.Scroll_into_view(f'xpath://section[@data-anchor-block="{attr}"]//span[@aria-label="Go to slide 1"]')
        self.se_lib.wait_until_page_contains_element('xpath:'+Cathay_Xpath['停發卡Tab_active'], timeout=self.timeout)
        num = 0
        for i in range(1, len(span_list)+1):
            self.Click_Element(f'xpath://section[@data-anchor-block="{attr}"]//span[@aria-label="Go to slide {str(i)}"]')
            sleep(2)
            run('Capture_a_Screenshot', f'ob_card{str(i)}.png')
            num = i
        log_color(f'Captured total {num} screenshots', 'blue')
        return num
    
    def Get_screenshot_of_cards(self, span_list, attr):
        # Scroll into view
        self.Scroll_into_view_on_Base(f'//section[@data-anchor-block="{attr}"]')
        self.Wait_until_page_Contain_element(By.XPATH, Cathay_Xpath['停發卡Tab_active'])
        num = 0
        for i in range(1, len(span_list)+1):
            self.Click_it(By.XPATH, f'//section[@data-anchor-block="{attr}"]//span[@aria-label="Go to slide {str(i)}"]')
            sleep(2)
            run('Save_Screenshot', f'obsoleted_card{str(i)}.png')
            num = i
        log_color(f'Captured total {num} screenshots', 'blue')
        return num

    def Close_Browser(self):
        self.driver.quit()



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
    pass