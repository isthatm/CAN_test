import can
import logging
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
from udsoncan.Response import Response 
from udsoncan.services import *
import udsoncan.configs
import isotp
from functools import partial

from . import test_interface, test_services, can_node, db_handler
from udsoncan import Response

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
            "MOTOR_STATUS_speed": 159
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
        }

    test_obj = test_interface.TestInterface(DB_PATH, tester, server)
    test_obj.proceed_test(available_services.CHECK_SERVICE_ECUReset)

def uds_test_ReadDataByIdentifier(available_services: test_services.TestServices):
    print("\n========== UDS TEST - ReadDataByIdentifier ==========")

    tester = {
        "node_name": "TESTER",
        "TX_ID": 0x02,
        "RX_ID": 0x05,
        "did_list": [0xF190]
        }
    server = {
        "node_name": "SERVER",
        "TX_ID": 0x05,
        "RX_ID": 0x02,
        }

    test_obj = test_interface.TestInterface(DB_PATH, tester, server)
    test_obj.proceed_test(available_services.CHECK_SERVICE_ReadDataByIdentifier)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode='w')
    services = test_services.TestServices

    # data_frame_test(services)
    # uds_test_ECUReset(services)
    uds_test_ReadDataByIdentifier(services)