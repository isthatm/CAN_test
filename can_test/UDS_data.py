"""
    This script abides by ISO 14229-1:2020 standard
"""

from udsoncan import services
from udsoncan.BaseService import BaseSubfunction
from udsoncan.services import *
from udsoncan.common.dids import DataIdentifier
from udsoncan import Response, Request
from typing import Union, Tuple
import inspect
import struct
import sys

#TODO: Error when the service is not supported by the defined session

class SupportedServices:
    
    @classmethod
    def service_resp(cls, service: services, recv_payload: bytearray) -> Tuple[Response.Code, bytearray]:
        """
            : param service: Requires service as an input to compare with the supported services by this script
            
            : returns: a byte array if the service is supported, otherwise -1 
        """
        try:
            cls.supported_services = {
                services.DiagnosticSessionControl: cls.resp_DiagnosticSessionControl,
                services.ReadDataByIdentifier: cls.resp_ReadDataByIdentifier,
                services.ECUReset: cls.resp_ECUReset
            }
            resp_code, resp_data = cls.supported_services[service](recv_payload)
            return (resp_code, resp_data)
        
        except KeyError:
            return (Response.Code.ServiceNotSupported, bytearray())

    @staticmethod
    def resp_DiagnosticSessionControl():
        P2_SERVER_MAX = 5 # timeout of the activated session  
        P2_STAR_SERVER_MAX = 2 # Add two more seconds on receiving NRC 0x78  
    
    @staticmethod
    def resp_ReadDataByIdentifier(recv_payload: bytearray) -> Tuple[Response.Code, bytearray]:
        SUPPORTED_DIDS = {
            DataIdentifier.VIN: [0x57, 0x30, 0x4C, 0x30, 
                                 0x30, 0x30, 0x30, 0x34,
                                 0x33, 0x4D, 0x42, 0x35, 
                                 0x34, 0x31, 0x33, 0x32, 0x36],
            DataIdentifier.ECUSerialNumber: [0x41, 0x42, 0x43, 0x44]
        }

        request = Request.from_payload(recv_payload)
        offset, supported_did_flag = 0, 0
        resp_data = bytearray()

        while True:
            if len(request.data) <= offset:
                break

            request_did_bytes = request.data[offset:offset + 2]
            did = struct.unpack('>H', request_did_bytes)[0] 

            is_supported_did = did in list(SUPPORTED_DIDS.keys())
            if is_supported_did:
                supported_did_flag += 1
                resp_data.extend(
                    request_did_bytes + bytearray(SUPPORTED_DIDS[did])
                )
            else:
                supported_did_flag -= 1
            offset += 2

        # Supported NRC
        if len(request.data) < 2 or len(request.data) % 2: # NRC 13: Minimum length and DID format check
            return (Response.Code.IncorrectMessageLengthOrInvalidFormat, bytearray()) 
        # Placeholder: NRC 33
        if supported_did_flag < 0: # NRC 31: None of the requested DIDs are supported by this server 
            return (Response.Code.RequestOutOfRange, bytearray())
        if len(resp_data) > 4095: # NRC 14: Response to long
            return (Response.Code.ResponseTooLong, bytearray())
        
        # Positive response
        return (Response.Code.PositiveResponse, resp_data)
        
    @staticmethod
    def resp_ECUReset(recv_payload: bytearray) -> Tuple[Response.Code, bytearray]:
        REQUEST_EXPECTED_LENGTH = 2 # bytes
        POWER_DOWN_TIME = 0x1C # 28 seconds

        request = Request.from_payload(recv_payload)

        add_list_sub_fun()
        sub_funcs = ECUReset.ResetType.list_sub_fun()
        sub_func_availability = list(
            map(lambda sub_func: sub_func[1] == request.subfunction, sub_funcs)
        )

        # Suporrted NRC
        if not any(sub_func_availability):
            return (Response.Code.SubFunctionNotSupported, bytearray())
        elif len(recv_payload) > REQUEST_EXPECTED_LENGTH:
            return (Response.Code.IncorrectMessageLengthOrInvalidFormat, bytearray())
        
        # Positive response
        resp_data = [request.subfunction] + [POWER_DOWN_TIME]
        return (Response.Code.PositiveResponse, bytearray(resp_data))
    

def add_list_sub_fun():
    BaseSubfunction.list_sub_fun = classmethod(list_sub_fun)

def list_sub_fun(cls):
    """ Filters class attributes excluding private, protected attributes and methods"""
    sub_fun_list = []
    for member in inspect.getmembers(cls, lambda member: not (inspect.isroutine(member))):
        if not member[0].startswith('_'):
            sub_fun_list.append(member)
    return sub_fun_list