import can
import isotp
import logging
import json
from threading import Thread

import udsoncan.connections as connections
import udsoncan.configs
from udsoncan.client import Client
from udsoncan import Request, Response

from .db_handler import CAN_database
from typing import List, Union


"""
    TODO:
        +) Define which session each node supports 
        +) IDs that a node support can be added to filters

"""

RECORDED_DATA_PATH = r"./can_test/data.json"


class CAN_Node:
    def __init__(self, 
                 data_base: CAN_database,
                 channel: str = 'test',
                 interface: str = 'virtual',
                 **kwargs):
        """
            Notes: `node` should be specified when implementing test 
                    using pure python-can. In such case each bus is 
                    considered a node.
        """
        # Initialize DATA LINK LAYER
        self.bus = can.interface.Bus(channel=channel, interface=interface) 
        self.data_base = data_base
        self.kwargs = kwargs
        self.expected_msgs = self.data_base.list_receiving_msg(self.kwargs["node_name"])
        # NOTE: Here the 'can_id's are scattered and small in numbers. Therfore,
        #       0xFF is explicitly set => filter the one message specified by 'can_id'.
        #       Nonetheless, 'can_mask' can be set such that a range of IDs can be filtered
        self.expected_id = list(
            map(lambda id: {'can_id': id.frame_id, 'can_mask': 0xFF}, self.expected_msgs)
                                )
        self.bus.set_filters(self.expected_id)
    
    def init_isotp(self,
                   send_id: int,
                   recv_id: int, 
                   addr_mode: isotp.AddressingMode = isotp.AddressingMode.Normal_11bits) -> isotp.CanStack:
        """ Initialize Transport and Network layers """
        if (addr_mode not in [ isotp.AddressingMode.Normal_11bits,
                               isotp.AddressingMode.Normal_29bits]):
            self._error_handler(
                RuntimeError("This script only supports Normal_11bits and Normal_29bits \
                              addressing mode at the moment.")
                            )
        else:
            self.stack = isotp.CanStack(bus=self.bus, 
                                        address=isotp.Address(addr_mode, txid=send_id, rxid=recv_id),
                                        error_handler=self._error_handler)
        
    def send_isotp_msg(self, msg):
        """ Send a can message through CAN-TP layer - OSI LV3,4 """
        self.stack.send(msg)     
    
    def send(self, msg_name):
        """ Send a can message on the bus - OSI LV1,2 """
        can_frame = self._pack_frame(msg_name)
        self.bus.send(can_frame)
     
    def send_periodic(self, 
                      period: int, 
                      duration: int) -> List[can.CyclicSendTaskABC]:
        """ Sends periodic message on the bus - OSI LV1,2 """
        can_frame = self._pack_frame(self.kwargs["sending_msg_name"])
        task = self.bus.send_periodic(msgs=can_frame, period=period, duration=duration)
        assert isinstance(task, can.CyclicSendTaskABC)
        return task   

    def send_diag_request(self, request: Request):
        if not getattr(self ,'stack', False):
            raise RuntimeError("The network layer - CANTp has not been initialized")
        
        connection = connections.PythonIsoTpConnection(self.stack)
        thread = Thread(target=self._run_diag_request_sender, args=(connection, request))
        thread.start()

    def _run_diag_request_sender(self, conn: connections, request: Request):
        uds_config = udsoncan.configs.default_client_config.copy()
        uds_config["p2_timeout"] = 3 

        with Client(conn, uds_config) as client:
            self.diag_response = client.send_request(request)
 
    def receive_isotp_msg(self, timeout):
        """ Get a can message from CAN-TP layer - OSI LV3,4 """
        received_msg = self.stack.recv(block=True, timeout=timeout, )
        return received_msg   

    def receive(self, time_out: int=1) -> Union[can.Message, None]:
        """
            Read CAN frames that sent on the bus. Returns a can.Message or 
            None on timeout - OSI LV1,2
            : param time_out: seconds to wait for a message, the default value is 1
            : returns:  a can.Message on successful receipt or None if no message is recorded
        """
        msg = self.bus.recv(timeout=time_out)
        return msg

    def check_data(self, arriving_msg: can.Message) -> Union[can.Message, None]:
        if arriving_msg != None:
            try:
                db_msg = self.data_base.db.get_message_by_frame_id(arriving_msg.arbitration_id)
                expected_msg: dict = self.kwargs["expected_receiving_msg"]

                self._check_input_signal_size(expected_msg)

                expected_msg_name = list(expected_msg.keys())[0]
                expected_signals: dict = expected_msg.get(expected_msg_name)

                if all([isinstance(sig_val, int) for _, sig_val in expected_signals.items()]):
                    expected_frame = db_msg.encode(expected_signals, scaling=False)
                    assert arriving_msg.data == expected_frame
                    return arriving_msg.data
                else:
                    raise ValueError("Signal values must be integers.")
                
            except AssertionError as error:
                self._error_handler(error)
                raise AssertionError("The receiving data frame is not identical to the expected one.")
            
        return None

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
        data_formatter, check_pack = {}, {}

        with open(RECORDED_DATA_PATH) as file:
            signal_values = json.loads(file.read())

        check_pack[msg_name] = signal_values[msg_name]
        self._check_input_signal_size(check_pack)
        msg = self.data_base.db.get_message_by_name(msg_name)

        for signal_name, signal_value in signal_values[msg_name].items():
            data_formatter[signal_name] = int(signal_value, 10)
        encoded_data_frame = msg.encode(data_formatter, scaling=False)
        can_frame = can.Message(data=encoded_data_frame, 
                                arbitration_id=msg.frame_id, 
                                is_extended_id=False, 
                                check=True)
        return can_frame   
    
    def _check_input_signal_size(self, msg: dict):
        """
            Prevent the user input value to be overflown
        """
        msg_name = list(msg.keys())[0]
        comparing_signals = msg[msg_name]
        for signal in self.data_base.db.get_message_by_name(msg_name).signals:
            if int(comparing_signals[signal.name]) <= 2**(signal.length):
                pass
            else:
                raise OverflowError("%s: %s. Consider another input value that can be represented with %s byte(s)" % 
                                  (signal.name, comparing_signals[signal.name], signal.length))
    
    @staticmethod
    def _error_handler(error):
        logging.error(" Error occured: %s - %s" % (error.__class__.__name__, str(error)))
        
    def __del__(self):
        if hasattr(self, 'stack'):
            self.stack.stop()
        self.bus.shutdown()


if __name__ == '__main__':
    print(can.Message.__dict__)
    pass