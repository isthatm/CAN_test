import can
from .can_ops import Network
from . import db_handler

import json
from typing import Optional

"""
    TODO:
        +) Define which session each node supports
        +) use send_periodic by python-can
"""

class CAN_Node ():
    def __init__(self,  node_name: str, bus: can.BusABC) -> None:
        self.bus = bus
        self.node_name = node_name
        self.supported_sessions = []
    
    def send_periodic(self, msg_name: str):
        """
            Send periodic message on the bus - OSI LV1,2
        """
        frame = self._pack_frame(msg_name)
        pass
        # self.bus.send_periodic(frame)
    
    def _pack_frame(self, msg_name):
        data_frame = []  
        with open("./data.json", "r") as file:
            signals = file[msg_name]
        print(signals)
        pass
