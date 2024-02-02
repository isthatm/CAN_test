"""
    This script contains supported test cases. New cases should be appended to TestServices(Enum)
"""

from enum import Enum
import copy


class TestServices(Enum):
    CHECK_DATA_FRAME = 1
    CHECK_DATA_LENGTH = 2
    CHECK_RANGE = 3


class services:
    def check_data_frame(self):
        return copy.copy(TestServices.CHECK_DATA_FRAME)
    
    def check_data_length(self):
        return copy.deepcopy(TestServices.CHECK_DATA_LENGTH)
    
    def check_range(self):
        return copy.deepcopy(TestServices.CHECK_RANGE)