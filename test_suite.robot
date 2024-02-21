*** Settings ***
Library   ./can_test/test_services.py   
Resource    test_keywords.robot


*** Variables ***
${DB_PATH}    ./Example.dbc 
${TEST_OBJ}

# Run by CLI: $python -m robot <path_to_robot>

*** Test Cases ***

# Expected to PASS
Data Frame Test 1
    [Tags]    Data frame CAN Test
    Set Test Variable    &{TEST_CASE_NODE_1}    node_name=MOTOR    is_sender=${True}    sending_msg_name=MOTOR_STATUS    expected_receiving_msg=None   

    # A node that is supposed to RECEIVE "MOTOR_STATUS" message
    Set Test Variable    &{EXPECTED_SIGNALS}    MOTOR_STATUS_wheel_error=${0}    MOTOR_STATUS_speed=${159}    
    Set Test Variable    &{EXPECTED_MSG}    MOTOR_STATUS=${EXPECTED_SIGNALS}   
    Set Test Variable    &{TEST_CASE_NODE_2}    node_name=DRIVER    is_sender=${False}    sending_msg_name=${None}    expected_receiving_msg=${EXPECTED_MSG}    
   
    Set Test Variable    ${TEST_NAME}    
    ${TEST_NAME}    Check Data Frame
    ${TEST_OBJ} =    Initialize Interface    ${DB_PATH}    ${TEST_CASE_NODE_1}    ${TEST_CASE_NODE_2}
    Log    ${TEST_OBJ}
    Run Test    ${TEST_OBJ}    ${TEST_NAME}
    

# Expected to FAIL - SENSOR is not MOTOR's recipient
Data Frame Test 2
    [Tags]    Data frame CAN Test
    Set Test Variable    &{TEST_CASE_NODE_1}    node_name=MOTOR    is_sender=${True}    sending_msg_name=MOTOR_STATUS    expected_receiving_msg=None   

    # A node that is supposed to NOT RECEIVE "MOTOR_STATUS" message
    Set Test Variable    &{EXPECTED_SIGNALS}    MOTOR_STATUS_wheel_error=${0}    MOTOR_STATUS_speed=${159}    
    Set Test Variable    &{EXPECTED_MSG}    MOTOR_STATUS=${EXPECTED_SIGNALS}   
    Set Test Variable    &{TEST_CASE_NODE_2}    node_name=SENSOR    is_sender=${False}    sending_msg_name=${None}    expected_receiving_msg=${EXPECTED_MSG}    
    
    Set Test Variable    ${TEST_NAME}    
    ${TEST_NAME}    Check Data Frame
    ${TEST_OBJ} =    Initialize Interface    ${DB_PATH}    ${TEST_CASE_NODE_1}    ${TEST_CASE_NODE_2}
    Run Test    ${TEST_OBJ}    ${TEST_NAME}


# Expected to FAIL - signal value is out of range
Data Frame Test 3
    [Tags]    Data frame CAN Test
    Set Test Variable    &{TEST_CASE_NODE_1}    node_name=MOTOR    is_sender=${True}    sending_msg_name=MOTOR_STATUS    expected_receiving_msg=None   

    # A node that is supposed to NOT RECEIVE "MOTOR_STATUS" message
    Set Test Variable    &{EXPECTED_SIGNALS}    MOTOR_STATUS_wheel_error=${10}    MOTOR_STATUS_speed=${159}    
    Set Test Variable    &{EXPECTED_MSG}    MOTOR_STATUS=${EXPECTED_SIGNALS}   
    Set Test Variable    &{TEST_CASE_NODE_2}    node_name=DRIVER    is_sender=${False}    sending_msg_name=${None}    expected_receiving_msg=${EXPECTED_MSG}    
    
    Set Test Variable    ${TEST_NAME}    
    ${TEST_NAME}    Check Data Frame
    ${TEST_OBJ} =    Initialize Interface    ${DB_PATH}    ${TEST_CASE_NODE_1}    ${TEST_CASE_NODE_2}
    Run Test    ${TEST_OBJ}    ${TEST_NAME}


# Expected to PASS
ECUReset Test 1
    [Tags]    UDS
    Set Test Variable    &{TEST_CASE_NODE_1}    node_name=TESTER    TX_ID=${0x02}    RX_ID=${0x05}    sub_function=${4}   
    Set Test Variable    &{TEST_CASE_NODE_2}    node_name=SERVER    TX_ID=${0x05}    RX_ID=${0x02}    sub_function=${None}    
    
    Set Test Variable    ${TEST_NAME}    
    ${TEST_NAME}    Check Service ECUReset
    ${TEST_OBJ} =    Initialize Interface    ${DB_PATH}    ${TEST_CASE_NODE_1}    ${TEST_CASE_NODE_2}
    Run Test    ${TEST_OBJ}    ${TEST_NAME}


# Expected to FAIL - Subfunction is not supported
ECUReset Test 2
    [Tags]    UDS
    Set Test Variable    &{TEST_CASE_NODE_1}    node_name=TESTER    TX_ID=${0x02}    RX_ID=${0x05}    sub_function=${7}   
    Set Test Variable    &{TEST_CASE_NODE_2}    node_name=SERVER    TX_ID=${0x05}    RX_ID=${0x02}    sub_function=${None}    
    
    Set Test Variable    ${TEST_NAME}    
    ${TEST_NAME}    Check Service ECUReset
    ${TEST_OBJ} =    Initialize Interface    ${DB_PATH}    ${TEST_CASE_NODE_1}    ${TEST_CASE_NODE_2}
    Run Test    ${TEST_OBJ}    ${TEST_NAME}

# Expected to PASS
ReadDataByIdentifier Test 1
    [Tags]    UDS
    Set Test Variable    @{TEST_DID_LIST}    ${0xF190}    ${0xF18C}    ${0xF191}
    Set Test Variable    &{TEST_CASE_NODE_1}    node_name=TESTER    TX_ID=${0x02}    RX_ID=${0x05}    did_list=${TEST_DID_LIST}  
    Set Test Variable    &{TEST_CASE_NODE_2}    node_name=SERVER    TX_ID=${0x05}    RX_ID=${0x02}    did_list=${None}    
    
    Set Test Variable    ${TEST_NAME}    
    ${TEST_NAME}    Check Service ReadDataByIdentifier
    ${TEST_OBJ} =    Initialize Interface    ${DB_PATH}    ${TEST_CASE_NODE_1}    ${TEST_CASE_NODE_2}
    Run Test    ${TEST_OBJ}    ${TEST_NAME}


# Expected to FAIL - None of the requested DIDs is supported
ReadDataByIdentifier Test 2
    [Tags]    UDS
    Set Test Variable    @{TEST_DID_LIST}    ${0xF191}
    Set Test Variable    &{TEST_CASE_NODE_1}    node_name=TESTER    TX_ID=${0x02}    RX_ID=${0x05}    did_list=${TEST_DID_LIST}  
    Set Test Variable    &{TEST_CASE_NODE_2}    node_name=SERVER    TX_ID=${0x05}    RX_ID=${0x02}    did_list=${None}    
    
    Set Test Variable    ${TEST_NAME}    
    ${TEST_NAME}    Check Service ReadDataByIdentifier
    ${TEST_OBJ} =    Initialize Interface    ${DB_PATH}    ${TEST_CASE_NODE_1}    ${TEST_CASE_NODE_2}
    Run Test    ${TEST_OBJ}    ${TEST_NAME}


# Expected to FAIL - Invalid length
ReadDataByIdentifier Test 3
    [Tags]    UDS
    Set Test Variable    @{TEST_DID_LIST}    ${0xF1}
    Set Test Variable    &{TEST_CASE_NODE_1}    node_name=TESTER    TX_ID=${0x02}    RX_ID=${0x05}    did_list=${TEST_DID_LIST}  
    Set Test Variable    &{TEST_CASE_NODE_2}    node_name=SERVER    TX_ID=${0x05}    RX_ID=${0x02}    did_list=${None}    
    
    Set Test Variable    ${TEST_NAME}    
    ${TEST_NAME}    Check Service ReadDataByIdentifier
    ${TEST_OBJ} =    Initialize Interface    ${DB_PATH}    ${TEST_CASE_NODE_1}    ${TEST_CASE_NODE_2}
    Run Test    ${TEST_OBJ}    ${TEST_NAME}