import logging
from udsoncan.services import *

from . import test_interface, test_services

"""
    This module is only used for investigating UDS and CAN protocol, implementations on hardware requires modifications
"""

DB_PATH = "./Example.dbc"


def data_frame_test(available_services: test_services.TestServices):
    print("\n========== DATA FRAME TEST ==========")

    Node1 = {
        "node_name": "MOTOR",
        "is_sender": True,
        "sending_msg_name": "MOTOR_STATUS",
        "expected_receiving_msg": None
    }

    Node2 = {
        "node_name": "DRIVER",
        "is_sender": False,
        "sending_msg_name": None,
        "expected_receiving_msg": {
            "MOTOR_STATUS": { 
            "MOTOR_STATUS_wheel_error": 0,
            "MOTOR_STATUS_speed": 0x9F
            }
        }
    }

    test_obj = test_interface.TestInterface(DB_PATH, Node1, Node2)
    test_obj.proceed_test(available_services.CHECK_DATA_FRAME)

def uds_test_ECUReset(available_services: test_services.TestServices):
    print("\n========== UDS TEST - ECUReset ==========")

    tester = {
        "node_name": "TESTER",
        "TX_ID": 0x02,
        "RX_ID": 0x05,
        "sub_function": 4
        }
    server = {
        "node_name": "SERVER",
        "TX_ID": 0x05,
        "RX_ID": 0x02,
        "sub_function": None
        }

    test_obj = test_interface.TestInterface(DB_PATH, tester, server)
    test_obj.proceed_test(available_services.CHECK_SERVICE_ECUReset)

def uds_test_ReadDataByIdentifier1(available_services: test_services.TestServices):
    print("\n========== UDS TEST - ReadDataByIdentifier ==========")
    # didconfig is defined within test_interface
    tester = {
        "node_name": "TESTER",
        "TX_ID": 0x02,
        "RX_ID": 0x05,
        "did_list": [0xF190, 0xF18C, 0xF191]
        # "did_list": [0xF191]
        }
    server = {
        "node_name": "SERVER",
        "TX_ID": 0x05,
        "RX_ID": 0x02,
        "did_list": None

        }

    test_obj = test_interface.TestInterface(DB_PATH, tester, server)
    test_obj.proceed_test(available_services.CHECK_SERVICE_ReadDataByIdentifier)

def uds_test_ReadDataByIdentifier2(available_services: test_services.TestServices):
    print("\n========== UDS TEST - ReadDataByIdentifier ==========")
    # didconfig is defined within test_interface
    tester = {
        "node_name": "TESTER",
        "TX_ID": 0x02,
        "RX_ID": 0x05,
        # "did_list": [0xF190, 0xF18C, 0xF191]
        "did_list": [0xF191]
        }
    server = {
        "node_name": "SERVER",
        "TX_ID": 0x05,
        "RX_ID": 0x02,
        "did_list": None

        }

    test_obj = test_interface.TestInterface(DB_PATH, tester, server)
    test_obj.proceed_test(available_services.CHECK_SERVICE_ReadDataByIdentifier)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename="test_log.log", filemode='w')
    services = test_services.TestServices

    data_frame_test(services)
    uds_test_ECUReset(services)
    uds_test_ReadDataByIdentifier2(services)
    uds_test_ReadDataByIdentifier1(services)