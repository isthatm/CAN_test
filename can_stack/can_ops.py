import can
import cantools
import isotp
import logging

from typing import Optional

"""
    TODO: 
        +) DiagnosticSessionControl (0x16) service
        +) Postive and negative response
"""

class Network:
    def __init__(self, channel: Optional[str] = None):
        self.channel = channel
        self.bus = can.interface.Bus(channel=self.channel,
                                     interface='virtual')   

    def init_isotp(self,
                   send_id,
                   recv_id, 
                   addr_mode: isotp.AddressingMode = isotp.AddressingMode.Normal_11bits):
        if (addr_mode not in [ isotp.AddressingMode.Normal_11bits,
                               isotp.AddressingMode.Normal_29bits]):
            self.error_handler(
                RuntimeError("This script only supports Normal_11bits and Normal_29bits \
                              addressing mode at the moment.")
                            )
        else:
            self.stack = isotp.CanStack(bus=self.bus, 
                                        address=isotp.Address(addr_mode, txid=send_id, rxid=recv_id),
                                        error_handler=self.error_handler())
            self.stack.start()
        
    def send_data_frame(self, msg):
        self.stack.send(msg)

    def receive_data_frame(self):
        received_msg = self.stack.recv()
        return received_msg        
    
    def error_handler(error):
        logging.error("Error occured: %s - %s" % (error.__class__.__name__, str(error)))

    def __del__(self):
        # pass
        # self.stack.stop()
        self.bus.shutdown()