import can
import cantools

class CAN:
    def __init__(self, node_id, channel=None):
        self.node_id = node_id
        self.channel = channel
        self.bus = can.interface.Bus(channel=self.channel,
                                     interface='virtual')
    
    def send_msg(self, msg):
        self.bus.send(msg)

    def receive_msg(self):
        received_msg = self.bus.recv()
        return received_msg        
    
    def __del__(self):
        self.bus.shutdown()

def main():
    msg_1 = can.Message(data=[0x28, 0x05, 0x98, 0x28, 0x05, 0x98, 0x28, 0x05, 0x98, 0x28, 0x05, 0x98], arbitration_id=0x100, is_extended_id=False)
    msg_2 = can.Message(data=[0x14, 0x06, 0x98], arbitration_id=0x101, is_extended_id=False)
    msg_3 = can.Message(data=[0x29, 0x05, 0x02], arbitration_id=0x111, is_extended_id=False)

    print(msg_1)
    Node_1 = CAN(node_id=1, channel='demo')
    Node_2 = CAN(node_id=2, channel='demo')
    Node_3 = CAN(node_id=3, channel='demo')

    Node_1.send_msg(msg_1)
    res = Node_2.receive_msg()
    print(res)

if __name__ == '__main__':
    main()