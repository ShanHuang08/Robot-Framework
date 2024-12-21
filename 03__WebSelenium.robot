*** Settings ***
Library    Cathay_TQA_Test.py

*** Test Cases ***
Cathay TQA Test
    [Tags]    Selenium
    Scrap_Cathay

Use Robot Keyword to run Cathay TQA Test
    [Tags]    SeleniumLibrary
    Robot_Keyword_Scrap_Cathay