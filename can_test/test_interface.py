import sys

from can_test import can_node, db_handler, test_services

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
            2:  (self._check_service_ECUReset, self._args),
            3:  (self._check_range, self._args)
        }
        
    def proceed_test(self, test: test_services.TestServices):
        action = self.actions[test.value]
        if action:
            selected_test, args = action
            selected_test(*args) 
        else:
            raise KeyError("Unknown service: {}".format(test))
        
    def _check_data_frame(self, node1: dict, node2: dict):
        """
            This test validates the sent/received data frame abiding by the following criteria:
                +) The frame is available in database
                +) The signal values are within the number of bytes designated
                +) The received frame is identical to the sent one  
            Required dict for this test:
            {
                node_name: "",
                is_sender: "",
                sending_msg_name: "",
                expected_receiving_msg: ""
            }
        """
        DEFAULT_TEST_PERIOD = 1
        DEFAULT_TEST_DURATION = 5

        try:
            node_objs = {
                int(node["is_sender"]): can_node.CAN_Node(self.db, **node) for node in [node1, node2]
            }
            sending_node = node_objs[True]
            receiving_node = node_objs[False]

            if sending_node == receiving_node:
                raise ValueError("There can only be one sending/receiving node.")

            rx_buffer = []
            sending_node.send_periodic(period=DEFAULT_TEST_PERIOD, duration=DEFAULT_TEST_DURATION)

            while(True): 
                received_msg = receiving_node.receive(time_out=1.5)
                
                if received_msg == None:
                    #TODO: raise TimeoutError based on actual time
                    if(len(rx_buffer) < (DEFAULT_TEST_DURATION // DEFAULT_TEST_PERIOD) + 1):
                        raise TimeoutError("No message is detected on the bus.")
                    else:
                        break
                
                rx_buffer.append(received_msg)
                res = receiving_node.check_data(received_msg)
                print(res)

        except KeyError as e:
            raise KeyError("Key {} is not defined by the dict of this test OR not available in the database".format(e))

    def _check_service_ECUReset(self, tester: dict, server: dict):
        pass

    def _check_range(self, node1: dict, node2: dict):
        pass