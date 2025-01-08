*** Settings ***
Library    OpenNet_QA_Test.py

*** Variables ***
${Folder_Name}=    Tester

*** Test Cases ***
OpenNet QA Test
    [Setup]    Check Network Connection
    Twitch Scrape
