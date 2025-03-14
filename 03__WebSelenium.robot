*** Settings ***
Library    Cathay_Auto_Test.py

*** Test Cases ***
Cathay Auto Test
    [Tags]    Selenium
    Scrap_Cathay
    [Teardown]    Close_Browser

Use Robot Keyword to run Cathay Auto Test
    [Tags]    SeleniumLibrary
    Robot_Keyword_Scrap_Cathay