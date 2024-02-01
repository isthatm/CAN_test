"""
    This script contains supported test cases. New cases should be appended to TestServices(Enum)
"""

from enum import Enum


class TestServices(Enum):
    CHECK_DATA_FRAME = 1
    CHECK_DATA_LENGTH = 2
    CHECK_RANGE = 3


class services:
    def check_data_frame(self):
        return TestServices.CHECK_DATA_FRAME.value
    
    def check_data_length(self):
        return TestServices.CHECK_DATA_LENGTH.value
    
    def check_range(self):
        return TestServices.CHECK_RANGE.value