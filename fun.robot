*** Settings ***
Library    OperatingSystem
Library    SeleniumLibrary
Resource    keywords.robot


*** Variables ***
# For python import library test
${DATA_IN}    ${1}
${REPORT_FILE}    ./Results

# For web navigation test
${MY_HOMEPAGE}    https://github.com/

# Demonstration for user-defined keywords
${VALUE_1}    3
${VALUE_2}    4


*** Test Cases ***
My Goto Place
    Navigate to GitHub    ${MY_HOMEPAGE}

Check Data In
    Comment    Do some thing cool
    Demo Assert ${DATA_IN}
    Log To Console    Output to console: ${REPORT FILE}

Verify Adding Function
    [Tags]    Mathmetical operations    
    ${result} =    Add    ${VALUE_1}    ${VALUE_2}
    Log    Addition: ${VALUE_1} + ${VALUE_2} = ${result}

Verify Subtractting Function
    [Tags]    Mathematical operations
    [Setup]    Log    This is the beginning of the SUBTRACTION test     

    ${result} =    Subtract ${VALUE_1} from ${VALUE_2}
    Log    Subtraction: ${VALUE_2} - ${VALUE_1} = ${result}

    [Teardown]    Log    This is the end of the SUBTRACTION test