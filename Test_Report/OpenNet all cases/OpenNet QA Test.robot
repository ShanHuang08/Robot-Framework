*** Settings ***
Library    OpenNet_QA_Test.py

*** Variables ***
${Folder_Name}=    Test_Report

*** Test Cases ***
Twitch Streamer Check 
    [Documentation]    Go to Twitch main page as WAP view,
    ...                Click the search icon,
    ...                Input StarCraft II to search,
    ...                Scroll down 2 times,
    ...                Select one random streamer,
    ...                on the streamer page wait until all is load and take a screenshot
    [Setup]    Check Network Connection
    Twitch Scrape

GET Basic Standard IP Lookup positive
    [Documentation]    {access_key : valid testkey} return 200 with JSON body, check data type of each response value    
    GET_Basic_Standard_IP_Lookup_positive

GET Basic Standard IP Lookup negative
    [Documentation]    {access_key : invalid testkey}, compare whether response is correct
    GET_Basic_Standard_IP_Lookup_negative

Set Valid and Invalid Hostname
    [Documentation]    {access_key : valid testkey, hostname : 1} return 200, response should contain hostname key, 
    ...                {access_key : valid testkey, hostname : 0} return 200, response should NOT contain hostname key
    Set_Valid_and_Invalid_Hostname

