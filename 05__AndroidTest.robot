*** Settings ***
Library    android_test.py


Suite Setup    Check_device_connection

*** Test Cases ***
Open whether Live
    Open Weather Forcast Live