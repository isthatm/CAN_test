import can
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
from udsoncan.Response import Response 
from udsoncan.services import *
import udsoncan.configs
import isotp
from functools import partial
import threading

from . import test_interface, test_services, can_node, db_handler
from udsoncan import Response

"""
    python-udsoncan/test/client/test_client.py
"""



def data_frame_test():
    db_path = "./Example.dbc"
    
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

    available_services = test_services.TestServices
    test_obj = test_interface.TestInterface(db_path, Node1, Node2)
    test_obj.proceed_test(available_services.CHECK_DATA_FRAME)

def uds_test():
    TX_ID = 0x02
    RX_ID = 0x05
    kwargs1 = {"node_name": "TESTER"}
    kwargs2 = {"node_name": "SERVER"}

    db = db_handler.CAN_database("./Example.dbc")
    Node1 = can_node.CAN_Node(db, **kwargs1)
    Node2 = can_node.CAN_Node(db, **kwargs2)

    Node1.init_isotp(recv_id=0x121, send_id=0x120)
    Node2.init_isotp(recv_id=0x120, send_id=0x121)
    
    req = ECUReset.make_request(reset_type=4)
    Node1.send_diag_request(req)
    data=[0x51, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x51, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                   ]
    Node2.get_diag_request()


if __name__ == '__main__':
    # main()
    uds_test()