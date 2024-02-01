from . import services, test_interface


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

    available_services = services.TestServices
    test_obj = test_interface.TestInterface(db_path, Node1, Node2)
    test_obj.proceed_test(available_services.CHECK_DATA_FRAME.value)


if __name__ == '__main__':
    main()