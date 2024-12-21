*** Settings ***
Library    Cathay_TQA_Test.py
Library    Cathay_TQA_Test_on_Robot.py

*** Test Cases ***
Cathay_TQA_Test
    Scrap_Cathay

Use Robot Keyword to run Cathay TQA Test
    Robot_Keyword_Scrap_Cathay