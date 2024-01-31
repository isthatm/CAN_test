import can
import time
import cantools
import sys
from enum import Enum
import logging
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
    def __init__(self, db_path, *args) -> None:
        self.db = db_handler.CAN_database(db_path)
        self.available_messages = [
            "MOTOR_CMD"
            "MOTOR_STATUS",
        ]
        self._args = [arg for arg in args]
        # print(self._args)
        self.actions = {
            TestServices.CHECK_DATA_FRAME:  (self._check_data_frame, self._args),
            TestServices.CHECK_DATA_LENGTH: (self._check_data_length, self._args),
            TestServices.CHECK_RANGE:  (self._check_range, self._args)
        }
    
    def proceed_test(self, test: Enum):
        action = self.actions.get(test)
        if action:
            selected_test, args = action
            selected_test(*args) 
        else:
            raise ValueError("Unknown service: {}".format(test.name))
        
    def _check_data_frame(self, node1: dict, node2: dict):
        """
            Required dict for this test:
            {
                node_name: "",
                is_sender: "",
                sending_msg_name: "",
                expected_receiving_msg: ""
            }
        """
        try:
            # Store node objects into a dictionary with the keys determine whether if it's a sender or not
            node_objs = {
                int(node["is_sender"]): can_node.CAN_Node(self.db, **node) for node in [node1, node2]
            }
            sending_node = node_objs[True]
            receiving_node = node_objs[False]

            if sending_node == receiving_node:
                raise ValueError("There can only be one sending/receiving node.")

            task = []
            task.append(sending_node.send_periodic(period=1, duration=5))

            while(True):
                received_msg = receiving_node.receive(time_out=1.5)
                if received_msg == None:
                    print("Timeout: No message is detected on the bus")
                    break
                res = receiving_node.check_data(received_msg)
                print(res)

        except KeyError as e:
            logging.error("Key {} is not defined by the dict of this test".format(e))

    def _check_data_length(self, node1: dict, node2: dict):
        pass

    def _check_range(self, node1: dict, node2: dict):
        pass

    def _is_supported(self, msg_name):
        if msg_name in self.available_messages:
            pass
        else:
            raise ValueError("Message - {}: is currently not supported")