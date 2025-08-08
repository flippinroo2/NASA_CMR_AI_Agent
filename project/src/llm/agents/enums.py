from enum import Enum

class CMR_QUERY_INTENTION_ENUM(Enum):
    EXPLORATORY = 1
    ANALYTICAL = 2
    SPECIFIC_DATA = 3

    def __str__(self):
        return f"CMR_QUERY_INTENTION_ENUM.{self.name}"
    
    def __repr__(self):
        return f"CMR_QUERY_INTENTION_ENUM.{self.name}"