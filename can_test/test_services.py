import can
import time
import cantools
from enum import Enum
from . import can_node, can_ops, db_handler

"""
    main.py function or robot framework will only communicate with this interface
    TODO: _is_supported() can be checked directly from data.json, currently it is 
          hard-coded in TestImplementation
"""

class TestServices(Enum):
    CHECK_DATA_FRAME = 1
    CHECK_DATA_LENGTH = 2
    CHECK_RANGE = 3


class TestImplementation:
    def __init__(self, db_path) -> None:
        self.db = db_handler.CAN_database(db_path)
        self.available_messages = [
            "MOTOR_CMD"
            "MOTOR_STATUS",
        ]
        self.tests = {
            TestServices.CHECK_DATA_FRAME: self._check_data_frame(),
            TestServices.CHECK_DATA_LENGTH: self._check_data_length(),
            TestServices.CHECK_DATA_FRAME: self._check_range()
        }
    
    def proceed_test(self, test: Enum):
        implemented_test = self.tests.get(test)
        implemented_test() 
        
    def _check_data_frame(self, node1_name, node2_name):
        Node1 = can_node.CAN_Node(node1_name, self.db)
        Node2 = can_node.CAN_Node(node2_name, self.db)

    def _check_data_length(self):
        pass

    def _check_range(self):
        pass

    def _is_supported(self, msg_name):
        if msg_name in self.available_messages:
            pass
        else:
            raise ValueError("Message - {}: is currently not supported")