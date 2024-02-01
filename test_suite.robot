*** Settings ***
Library   ./can_test/services.py   
Resource    test_keywords.robot


*** Variables ***
${DB_PATH}    ./Example.dbc 
${TEST_OBJ}


*** Test Cases ***
Data Frame Test
    Set Test Variable    ${TEST_NAME}    
    ${TEST_NAME}    Check Data Frame
    Set Test Variable    &{TEST_CASE_NODE_1}    node_name=MOTOR    is_sender=${True}    sending_msg_name=MOTOR_STATUS    expected_receiving_msg=None   

    Set Test Variable    &{EXPECTED_SIGNALS}    MOTOR_STATUS_wheel_error=${0}    MOTOR_STATUS_speed=${159}
    Set Test Variable    &{EXPECTED_MSG}    MOTOR_STATUS=${EXPECTED_SIGNALS}   
    Set Test Variable    &{TEST_CASE_NODE_2}    node_name=DRIVER    is_sender=${False}    sending_msg_name=${None}    expected_receiving_msg=${EXPECTED_MSG}    
    
    ${TEST_OBJ}=    Initialize Interface    ${DB_PATH}    ${TEST_CASE_NODE_1}    ${TEST_CASE_NODE_2}
    Run Test    ${TEST_OBJ}    ${TEST_NAME}

    
    
    
    