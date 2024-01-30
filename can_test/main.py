import can
import time
import cantools
from . import can_node, can_ops, db_handler, test_services


def main():
    demo_bus1 = can.interface.Bus(channel='test', interface='virtual', is_fd=False)
    demo_bus2 = can.interface.Bus(channel='test', interface='virtual', is_fd=False)
    
    #================ START ================
    db_path = "./Example.dbc"
    available_services = test_services.TestServices
    test_interface = test_services.TestImplementation(db_path)

    test_interface.proceed_test(available_services.CHECK_DATA_FRAME)
    
    tasks = []
    Node1 = can_node.CAN_Node("MOTOR", db)
    Node2 = can_node.CAN_Node("DRIVER", db)
    tasks.append(Node1.send_periodic("MOTOR_STATUS", 1, 5))

    expected_signals = {    
        "MOTOR_STATUS": { 
            "MOTOR_STATUS_wheel_error": 0,
            "MOTOR_STATUS_speed": 159
        }
    }
    # print(expected_signals.keys())

    while(True):
        received = Node2.receive(time_out=2)
        # print(received.data)
        res = Node2.check_data(received, expected_signals)
        if received == None:
            print("Timeout: No message is detected on the bus")
            break
        print(res)

    demo_bus1.shutdown()
    demo_bus2.shutdown()

if __name__ == '__main__':
    main()

