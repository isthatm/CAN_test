"""
    This script contains supported test cases. New cases should be appended to TestServices(Enum)
"""

from enum import Enum
import copy


class TestServices(Enum):
    CHECK_DATA_FRAME = 1
    CHECK_SERVICE_ECUReset = 2
    CHECK_SERVICE_ReadDataByIdentifier = 3


class test_services:
    def check_data_frame(self):
        return copy.copy(TestServices.CHECK_DATA_FRAME)
    
    def check_service_ECUReset(self):
        return copy.copy(TestServices.CHECK_SERVICE_ECUReset)
    
    def check_service_ReadDataByIdentifier(self):
        return copy.copy(TestServices.CHECK_SERVICE_ReadDataByIdentifier)