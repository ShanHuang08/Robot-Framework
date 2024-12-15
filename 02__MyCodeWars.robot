*** Settings ***
Library    CodeWars.py

Suite Setup    Gen Random Alstr
Suite Teardown    Gen Random Alstr
Test Timeout    5 minutes

*** Variables ***
@{ournames}=    Allen    Bob    Casey
@{numbers_1st}=    1    20    35

*** Keywords ***


*** Test Cases ***
Test Peak
    [Tags]    CodeWars    CodeWars_202312
    [Documentation]    CodeWars_202312
    Peak Best
    [Setup]    Gen Random Alstr
    [Teardown]    Gen Random Alstr
    
String Transition
    [Tags]    CodeWars    CodeWars_221109    
    [Documentation]    CodeWars_221109
    String Transition
        
Smash
    [Tags]    CodeWars    CodeWars_221110
    [Documentation]    CodeWars_221110
    Smash Run

Count By
    [Tags]    CodeWars    CodeWars_221111
    [Documentation]    CodeWars_221111
    ${x}=    Convert To Integer    1
    ${n}=    Convert To Integer    10
    Count By    ${x}    ${n}
    Count By Five Times

Average
    [Tags]    CodeWars    CodeWars_221111
    [Documentation]    CodeWars_221111 
    Count Average    ${numbers_1st}
    ${n21}=    Gen Digit    20
    ${n22}=    Gen Digit    40
    ${n23}=    Gen Digit    60
    ${numbers_2nd}=    Create List    ${n21}    ${n22}    ${n23}
    Count Average    ${numbers_2nd}

Sum Array
    [Tags]    CodeWars    CodeWars_221112
    [Documentation]    sum array exclude max and min value
    Sum Array    ${numbers_1st}
    Sum Array Run Three Times