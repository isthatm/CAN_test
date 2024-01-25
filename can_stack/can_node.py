import can
from .can_ops import Network
from . import db_handler

from typing import Optional

"""
    TODO:
        +) Define which session each node supports
"""

class CAN_Node (Network):
    def __init__(self) -> None:
        self.supported_sessions = []
    
    def send_frame(frame: can.Message):
        
        super().send_msg(frame)