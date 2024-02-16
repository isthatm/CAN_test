import can
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
    python-udsoncan/test/client/test_client.py
"""

DB_PATH = "./Example.dbc"


def data_frame_test(available_services: test_services.TestServices):
    
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
    tester = {
        "node_name": "TESTER",
        "TX_ID": 0x02,
        "RX_ID": 0x05,
        "sub_function": 3
        }
    server = {
        "node_name": "SERVER",
        "TX_ID": 0x05,
        "RX_ID": 0x02,
        }

    test_obj = test_interface.TestInterface(DB_PATH, tester, server)
    test_obj.proceed_test(available_services.CHECK_SERVICE_ECU_RESET)


if __name__ == '__main__':
    services = test_services.TestServices
    data_frame_test(services)
    uds_test_ECUReset(services)