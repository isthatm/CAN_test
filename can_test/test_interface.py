import sys
import logging
from can_test import can_node, db_handler

"""
    main.py function or robot framework will only communicate with this interface
    TODO: _is_supported() can be checked directly from data.json, currently it is 
          hard-coded in TestImplementation
"""

def set_interface(db_path, *args):
    return TestInterface(db_path, *args)


class TestInterface:
    def __init__(self, db_path, *args) -> None:
        self.db = db_handler.CAN_database(db_path)
        self.available_messages = [
            "MOTOR_CMD"
            "MOTOR_STATUS",
        ]
        self._args = [arg for arg in args]
        self.actions = {
            1:  (self._check_data_frame, self._args),
            2:  (self._check_data_length, self._args),
            3:  (self._check_range, self._args)
        }
    
    def proceed_test(self, test):
        action = self.actions.get(test)
        if action:
            selected_test, args = action
            selected_test(*args) 
        else:
            raise AttributeError("Unknown service: {} ----- {}")
        
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
            logging.error(e)
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