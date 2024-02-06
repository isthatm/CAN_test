*** Settings ***
Library   ./can_test/test_services.py   
Resource    test_keywords.robot


*** Variables ***
${DB_PATH}    ./Example.dbc 
${TEST_OBJ}


*** Test Cases ***
Data Frame Test 1
    [Tags]    Normal CAN Test
    Set Test Variable    &{TEST_CASE_NODE_1}    node_name=MOTOR    is_sender=${True}    sending_msg_name=MOTOR_STATUS    expected_receiving_msg=None   

    # A node that is supposed to RECEIVE "MOTOR_STATUS" message
    Set Test Variable    &{EXPECTED_SIGNALS}    MOTOR_STATUS_wheel_error=${0}    MOTOR_STATUS_speed=${159}    
    Set Test Variable    &{EXPECTED_MSG}    MOTOR_STATUS=${EXPECTED_SIGNALS}   
    Set Test Variable    &{TEST_CASE_NODE_2}    node_name=DRIVER    is_sender=${False}    sending_msg_name=${None}    expected_receiving_msg=${EXPECTED_MSG}    
   
    Set Test Variable    ${TEST_NAME}    
    ${TEST_NAME}    Check Data Frame
    ${TEST_OBJ} =    Initialize Interface    ${DB_PATH}    ${TEST_CASE_NODE_1}    ${TEST_CASE_NODE_2}
    Run Test    ${TEST_OBJ}    ${TEST_NAME}

Data Frame Test 2
    [Tags]    Normal CAN Test
    Set Test Variable    &{TEST_CASE_NODE_1}    node_name=MOTOR    is_sender=${True}    sending_msg_name=MOTOR_STATUS    expected_receiving_msg=None   

    # A node that is supposed to NOT RECEIVE "MOTOR_STATUS" message
    Set Test Variable    &{EXPECTED_SIGNALS}    MOTOR_STATUS_wheel_error=${0}    MOTOR_STATUS_speed=${159}    
    Set Test Variable    &{EXPECTED_MSG}    MOTOR_STATUS=${EXPECTED_SIGNALS}   
    Set Test Variable    &{TEST_CASE_NODE_2}    node_name=SENSOR    is_sender=${False}    sending_msg_name=${None}    expected_receiving_msg=${EXPECTED_MSG}    
    
    Set Test Variable    ${TEST_NAME}    
    ${TEST_NAME}    Check Data Frame
    ${TEST_OBJ} =    Initialize Interface    ${DB_PATH}    ${TEST_CASE_NODE_1}    ${TEST_CASE_NODE_2}
    Run Test    ${TEST_OBJ}    ${TEST_NAME}