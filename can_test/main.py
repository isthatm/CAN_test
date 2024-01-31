import can
import time
import cantools
from . import can_node, can_ops, db_handler, test_services


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

    kwargs = {"Node1": Node1, "Node2": Node2}
    available_services = test_services.TestServices
    test_interface = test_services.TestImplementation(db_path, Node1, Node2)
    test_interface.proceed_test(available_services.CHECK_DATA_FRAME)

if __name__ == '__main__':
    main()

