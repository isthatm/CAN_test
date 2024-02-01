*** Settings ***
Library    OperatingSystem
Library    can_test.test_interface


*** Keywords ***
Initialize Interface    
    [Arguments]    ${DB_PATH}    ${Node_1}    ${Node_2}   
    ${Interface}=    Set Interface    ${DB_PATH}    ${Node_1}    ${Node_2} 
    [Return]     ${Interface}

Run Test
    [Arguments]    ${SERVICE_OBJECT}    ${SERVICE_ENUM}     
    Call Method    ${SERVICE_OBJECT}    proceed_test    ${SERVICE_ENUM}    