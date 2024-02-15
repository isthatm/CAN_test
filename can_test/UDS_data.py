from udsoncan import services
from udsoncan.BaseService import BaseSubfunction
from udsoncan.services import *
from udsoncan import Response
from typing import Union, Tuple
import types
import inspect

class SupportedServices:
    
    @classmethod
    def service_resp(cls, service: services) -> Tuple[Response.Code, bytearray]:
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
            resp_data = cls.supported_services[service]()
            return (Response.Code.PositiveResponse, resp_data)
        
        except KeyError:
            return (Response.Code.ServiceNotSupported, bytearray())

    @staticmethod
    def resp_DiagnosticSessionControl():
        pass
    
    @staticmethod
    def resp_ReadDataByIdentifier():
        pass

    @staticmethod
    def resp_ECUReset():
        default_data = bytearray([0x28, 0x05])
        return default_data
    

    