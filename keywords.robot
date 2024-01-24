*** Settings ***
Library    ./fun.py
Library    SeleniumLibrary

# *** Variables ***
# ${REPORT FILE}    ./Results


*** Keywords ***
Demo Assert ${DATA}
    Assert True    ${DATA}

Navigate to GitHub
    [Arguments]    ${MY_HOMEPAGE}
    Open Browser    ${MY_HOMEPAGE}     chrome

Add 
    [Documentation]    Keywords: This keyword uses normal
    ...                arguments
    
    [Arguments]    ${value1}    ${value2}
    ${result} =    Evaluate    ${value1} + ${value2}
    [Return]    ${result}

Subtract ${value1} from ${value2}
    [Documentation]    Keywords: This keyword uses embedded
    ...                arguments
    
    ${result} =    Evaluate    ${value2} - ${value1}
    [Return]    ${result}

