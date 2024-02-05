import can
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
from udsoncan.Response import Response 
from udsoncan.services import *
import udsoncan.configs
import isotp
import threading

from . import test_interface, test_services, can_node, db_handler
from udsoncan import Response

"""
    python-udsoncan/test/client/test_client.py
"""



def main():
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

def uds_demo():
    kwargs = {"node_name": "TESTER"}
    db = db_handler.CAN_database("./Example.dbc")
    Node1 = can_node.CAN_Node(db, **kwargs)
    Node1.init_isotp(recv_id=0x05, send_id=0x28)
    req = ECUReset.make_request(reset_type=1)
    Node2 = can.interface.Bus(channel = 'test', interface='virtual')
    Node1.send_diag_request(req)
    while True:
        recv_msg = Node2.recv(timeout=5)
        if recv_msg == None:
            break
        print(recv_msg)
    Node2.shutdown()


if __name__ == '__main__':
    # main()
    uds_demo()