import can
import json
import isotp
import logging

from .db_handler import CAN_database
from typing import List, Dict, Optional


"""
    TODO:
        +) Apply filter to nodes
        +) Define which session each node supports
"""

RECORDED_DATA_PATH = r"./can_stack/data.json"

class CAN_Node ():
    def __init__(self, node_name: str, 
                 data_base: CAN_database,
                 channel: str = 'test',
                 interface: str = 'virtual'):
        """
            Notes: `node` should be specified when implementing test 
                    using pure python-can. In such case each bus is 
                    considered a node.
        """
        self.bus =  can.interface.Bus(channel=channel, 
                                      interface=interface) 
        self.data_base = data_base
        self.node_name = node_name
        self.expected_msgs = self.data_base.list_receiving_msg(node_name)
        # NOTE: Here the 'can_id's are scattered and small in numbers. Therfore,
        #       0xFF is explicitly set => filter the one message specified by 'can_id'.
        #       Nonetheless, 'can_mask' can be set such that a range of IDs can be filtered
        self.expected_id = list(
            map(lambda id: {'can_id': id.frame_id, 'can_mask': 0xFF}, self.expected_msgs)
                                )
        self.bus.set_filters(self.expected_id)
    
    def init_isotp(self,
                   send_id,
                   recv_id, 
                   addr_mode: isotp.AddressingMode = isotp.AddressingMode.Normal_11bits):
        if (addr_mode not in [ isotp.AddressingMode.Normal_11bits,
                               isotp.AddressingMode.Normal_29bits]):
            self._error_handler(
                RuntimeError("This script only supports Normal_11bits and Normal_29bits \
                              addressing mode at the moment.")
                            )
        else:
            self.stack = isotp.CanStack(bus=self.bus, 
                                        address=isotp.Address(addr_mode, txid=send_id, rxid=recv_id),
                                        error_handler=self.error_handler())
            self.stack.start()
        
    def send_isotp_msg(self, msg):
        """ Send a can message through CAN-TP layer - OSI LV3,4 """
        self.stack.send(msg)     
    
    def send(self, msg_name):
        """ Send a can message on the bus - OSI LV1,2 """
        can_frame = self._pack_frame(msg_name)
        self.bus.send(can_frame)
     
    def send_periodic(self, msg_name: str, 
                      period: int, 
                      duration: int) -> List[can.CyclicSendTaskABC]:
        """ Sends periodic message on the bus - OSI LV1,2 """
        can_frame = self._pack_frame(msg_name)
        task = self.bus.send_periodic(msgs=can_frame, period=period, duration=duration)
        assert isinstance(task, can.CyclicSendTaskABC)
        return task    
    
    def receive_data_frame(self):
        """ Get a can message from CAN-TP layer - OSI LV3,4 """
        received_msg = self.stack.recv()
        return received_msg   

    def receive(self, time_out):
        """
            Read CAN frames that sent on the bus. Returns a can.Message or 
            None on timeout
        """
        msg = self.bus.recv(timeout=time_out)
        return msg

    def _pack_frame(self, msg_name: str) -> can.Message:
        """
            Packs a CAN frame whose infor data frame and message's
            arbitration ID are predefined within a .json file.

            :param msg_name: This name must follow the message_name in the 
                            .json file
            :type msg_name: str

            :return: a non-extended CAN frame
            :return type: can.Message
        """
        data_formatter = {}
        with open(RECORDED_DATA_PATH) as file:
            signal_values = json.loads(file.read())

        msg = self.data_base.db.get_message_by_name(msg_name)
        for signal in signal_values[msg_name]:
            data_formatter[signal["SIGNAL_NAME"]] = int(signal["VALUE"], 10)
        data_frame = msg.encode(data_formatter, scaling=False)
        can_frame = can.Message(data=data_frame, arbitration_id=msg.frame_id, is_extended_id=False, check=True)
        return can_frame   
    
    def _error_handler(error):
        logging.error("Error occured: %s - %s" % (error.__class__.__name__, str(error)))
        
    def __del__(self):
        if getattr(self, 'stack', None):
            self.stack.stop()
        self.bus.shutdown()