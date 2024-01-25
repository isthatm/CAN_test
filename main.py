import can
from can_stack import can_node, can_ops, db_handler

def main():
    msg_1 = can.Message(data=[0x28, 0x05, 0x98], arbitration_id=0x100, is_extended_id=False)
    msg_2 = can.Message(data=[0x14, 0x06, 0x98], arbitration_id=0x101, is_extended_id=False)
    msg_3 = can.Message(data=[0x29, 0x05, 0x02], arbitration_id=0x111, is_extended_id=False)

    Bus = can_ops.Network(db_path="./Example.dbc", channel='demo')
    Bus.init_isotp()
    Node1 = can_node.CAN_Node()
    Node1.send_frame(msg_1)


if __name__ == '__main__':
    main()

