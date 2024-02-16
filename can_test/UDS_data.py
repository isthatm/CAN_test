"""
    This script abides by ISO 14229-1:2020 standard
"""

from udsoncan import services
from udsoncan.BaseService import BaseSubfunction
from udsoncan.services import *
from udsoncan import Response, Request
from typing import Union, Tuple
import inspect

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
        pass
    
    @staticmethod
    def resp_ReadDataByIdentifier():
        pass

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
        
        resp_data = [POWER_DOWN_TIME]
        return (Response.Code.PositiveResponse, bytearray(resp_data))
    

def add_list_sub_fun():
    BaseSubfunction.list_sub_fun = classmethod(list_sub_fun)

def list_sub_fun(cls):
    """ Filters class attributes excluding methods, private and protected ones """
    sub_fun_list = []
    for member in inspect.getmembers(cls, lambda member: not (inspect.isroutine(member))):
        if not member[0].startswith('_'):
            sub_fun_list.append(member)
    return sub_fun_list


    

    