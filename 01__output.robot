*** Settings ***
Library    Robot_Methods_with_class.py
Library    Collections
# Library    Robot_Methods.py

Suite Setup    Print Time
Suite Teardown    Gen Two Lists
Test Timeout    5 minutes

*** Variables ***
@{ournames}=    Allen    Bob    Casey

*** Keywords ***
Gen Two Lists
    ${List1}=    Gen Loop List
    ${List2}=    Gen Loop List
    Set Suite Variable    ${List1}
    Set Suite Variable    ${List2}
    ${Full_List}=    Combine Lists    ${List1}    ${List2}
    [Return]    ${Full_List}

*** Test Cases ***
My Test
    Test Run
    Test Errors
    # Type Error Test
    # Print Fruit
        [Tags]    output    <a href="https://www.google.com">Google</a>
        [Documentation]    test1doc
        [Setup]    Print Time
        [Teardown]    Print Time
My Test2
    Test Even Max
    Test Run Many
        [Tags]    output
        [Documentation]    test2doc
Robot Loop case
    [Tags]    output
    [Documentation]    Loops in Robot
    FOR    ${name}    IN    @{ournames}
        Log Color    ${name}    blue
    END
    FOR    ${i}    IN RANGE    1    10
        Logs    ${i}
    END
    FOR    ${i}    IN    3    2    1
        FOR    ${j}    IN    1    2    3
            Logs    Current Number is: ${j}
        END
    END

Py Loop case
    [Tags]    output
    [Documentation]    Loops in Robot, Lists in Python
    ${x}=    Convert To Integer    10
    ${nums}=    Gen Loop List    
    FOR    ${element}    IN    @{nums}
        Print Time
    END

Print Time
    [Tags]    output
    Print Time

Show Two Lists
    [Tags]    output
    [Documentation]    Practice Keywords in Robot
    @{TwoLists}=    Gen Two Lists
    FOR    ${element}    IN   @{TwoLists}
        IF    ${element} > 10
            Log    ${element}
            Cars
        END        
    END
    FOR    ${element}    IN    @{List2}
        Log    ${element}
    END

Zip Methods Comparison
    [Tags]    output
    [Documentation]    3 methods process time Comparison that transfer 2 lists to dict
    Zip Performance Comparison