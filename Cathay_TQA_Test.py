# TQA測試: Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from Library.SeleniumBase import SeleniumBase

class Cathay(SeleniumBase):

    def Scrap_Cathay(self):
        self.chromedriver_path = 'C:\\Users\\Shan\\Workspace2\\chromedriver.exe'
        # options.add_argument("--headless")  
        # options.add_argument("--disable-gpu")  
        self.driver = self.Chrome_WAP(self.chromedriver_path)

        # 1. 使用Chrome App到國泰世華銀行官網(https://www.cathaybk.com.tw/cathaybk/)並將畫面截圖。
        self.driver.get("https://www.cathaybk.com.tw/cathaybk/")
        self.Save_Screenshot(By.XPATH, '/html', filename='main page.png')

        # 2. 點選左上角選單，進入 個人金融 > 產品介紹 > 信用卡列表，需計算有幾個項目在信用卡選單下面，並將畫面截圖。
        self.Click_Element(By.XPATH, value='//a[@class="cubre-a-burger"]')
        self.Click_Element(By.XPATH, value='//div[@class="cubre-o-nav__content"]//*[contains(text(),"產品介紹")]')
        self.Click_Element(By.XPATH, value='//div[@class="cubre-o-menuLinkList__btn"]//*[contains(text(),"信用卡")]')
        self.Save_Screenshot(By.XPATH, '//*[contains(text(),"掛失信用卡")]', filename='credit card list.png')
        # card_services = driver.find_elements(By.XPATH, value='//div[@class="cubre-a-menuSortBtn" and contains(@class, "cubre-u-mbOnly")]/a') #It's not working
        card_services = self.find_xpaths(value='/html/body/div[1]/header/div/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[1]/div[2]/a')
        if card_services:
            print(f"{len(card_services)} items are in the card services")
            for service in card_services:
                print(service.text)

        # 3. 個人金融 > 產品介紹 > 信用卡 > 卡片介紹 > 計算頁面上所有(停發)信用卡數量並截圖
        self.Click_Element(By.XPATH, '//a[contains(text(),"卡片介紹")]')

        # card_list = driver.find_elements(By.XPATH, value='//div[@class="cubre-m-compareCard -credit"]/div[@class="cubre-m-compareCard__title"]')
        card_list = self.find_xpaths(value='//*[contains(text(), "已停發")]')
        if card_list: print(f'所有停發信用卡有{len(card_list)}張')

        # card_pics = driver.find_elements(By.XPATH, value='//div[@class="cubre-m-compareCard__pic"]/img')
        card_pics = self.find_xpaths(value='//div[contains(text(), "已停發")]/..//img')
        card_links = []
        if card_pics:
            for pic in card_pics:
                image_src = pic.get_attribute("src")
                if 'png' in image_src: 
                    # print(image_src)
                    card_links.append(image_src)
        self.Get_cards_screenshot(card_links)
        self.driver.quit()

    def Get_cards_screenshot(self, card_links):
        num = 1
        for link in card_links:
            ob_filename = f'Obsolete_card_{num}.png'
            self.driver.get(link)
            sleep(2)
            self.Save_Screenshot(By.XPATH, '/html', ob_filename)
            num+=1

# TQA測試: 程式邏輯題目
import random
def question1(input_list:list):
    """
    - Input: [35, 46, 57, 91, 29]
    - Output: [53, 64, 75, 19, 92]
    """
    def reverse_double_digit(digit:int):
        digit = str(digit)
        if len(digit) == 2: return int(str(digit[-1]) + str(digit[0]))
    output_list = [reverse_double_digit(num) for num in input_list]
    print(output_list)


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
    print(answer)


def question3(n:int):
    """
    - Input: 0-100
    - Output: The last order is {num}
    """
    if 0 <= n <= 100:
        num = 1
        for i in range(n):
            if i % 3 != 0:
                num+=1
        print(f"The last order is {num}")
    else: print('n range should be between 0 to 100')

if __name__=='__main__':
    # 程式邏輯題目
    # question1([35, 46, 57, 91, 29])
    # question2("Hello welcome to Cathay 60th year anniversary")
    # question3(random.randint(0, 100))
    # 自動化測試
    Cathay().Scrap_Cathay()