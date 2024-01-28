import can
from .can_ops import Network
from . import db_handler

import json
from .db_handler import CAN_database
from typing import Optional

"""
    TODO:
        +) Define which session each node supports
        +) use send_periodic by python-can
"""

RECORDED_DATA_PATH = r"./can_stack/data.json"

class CAN_Node ():
    def __init__(self,  node_name: str, 
                 bus: can.BusABC, 
                 data_base: CAN_database) -> None:
        self.bus = bus
        self.data_base = data_base
        self.node_name = node_name
        self.supported_sessions = []
    
    def send_periodic(self, msg_name: str):
        """
            Sends periodic message on the bus - OSI LV1,2
        """
        frame = self._pack_frame(msg_name)
        pass
        # self.bus.send_periodic(frame)
    
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
        data_frame = []
        with open(RECORDED_DATA_PATH) as file:
            signal_values = json.loads(file.read())

        for msg in self.data_base.list_messages():
            if msg.name == msg_name:
                print(msg.signals)
                pass
        
        # print(signals["MOTOR_CMD"][0]["VALUE"])
        # print(self.data_base.list_messages()[3].signals[0].__dict__)
