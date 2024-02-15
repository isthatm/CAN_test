"""
    This script contains supported test cases. New cases should be appended to TestServices(Enum)
"""

from enum import Enum
import copy


class TestServices(Enum):
    CHECK_DATA_FRAME = 1
    CHECK_SERVICE_0x22 = 2
    CHECK_RANGE = 3


class test_services:
    def check_data_frame(self):
        return copy.copy(TestServices.CHECK_DATA_FRAME)
    
    def check_service_0x22(self):
        return copy.deepcopy(TestServices.CHECK_SERVICE_0x22)
    
    def check_range(self):
        return copy.deepcopy(TestServices.CHECK_RANGE)