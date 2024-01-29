import can
import time
from . import can_node, can_ops, db_handler


def main():
    db = db_handler.CAN_database("./Example.dbc")
    msg_1 = can.Message(data=[0x28, 0x05, 0x98], arbitration_id=0x100, is_extended_id=False)
    msg_2 = can.Message(data=[0x14, 0x06, 0x98], arbitration_id=0x101, is_extended_id=False)
    msg_3 = can.Message(data=[3,3,3,3,3,3,3,3], arbitration_id=0x111, is_extended_id=False, check=True)
    
    demo_bus1 = can.interface.Bus(channel='test', interface='virtual', is_fd=False)
    demo_bus2 = can.interface.Bus(channel='test', interface='virtual', is_fd=False)
    
    demo_bus1.send(msg_3)
    recv_data = demo_bus2.recv()
    print(recv_data)
    demo_bus1.shutdown()
    demo_bus2.shutdown()
    # tasks = []
    # Node1 = can_node.CAN_Node("MOTOR", db)
    # Node2 = can_node.CAN_Node("DRIVER", db)
    # tasks.append(Node1.send_periodic("MOTOR_STATUS", 1, 5))
    # while(True):
    #     received = Node2.receive(time_out=2)
    #     print(received)
    #     if received == None:
    #         print("Timeout: No message is detected on the bus")
    #         break


if __name__ == '__main__':
    main()

