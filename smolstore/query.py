# -*- coding: utf-8 -*-
from enum import auto
from enum import Enum


class ComparisonType(Enum):
    EQUAL = auto()
    NOT_EQUAL = auto()


class Query:
    def __init__(self, field, comparison_type: ComparisonType, value):
        self.field = field
        self.comparison_type = comparison_type
        self.value = value
