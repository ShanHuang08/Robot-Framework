*** Settings ***
Library    android_test.py
Library    Library/API_definition.py


Suite Setup    Check_device_connection

*** Test Cases ***
Open whether Live
    Open Weather Forcast Live
    [Teardown]    Run Keyword If Test Failed    Exit Weather Live