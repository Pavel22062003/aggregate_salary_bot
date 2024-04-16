from pydantic import BaseModel, field_validator, ValidationInfo
from typing import Union
from enum import Enum
from datetime import datetime


class Types(str, Enum):
    HOUR = 'hour'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'


class ComeInData(BaseModel):
    dt_from: str
    dt_upto: str
    group_type: Union[Types]

    @field_validator('dt_from', 'dt_upto')
    @classmethod
    def check_date_format(cls, date: str, info: ValidationInfo):
        try:
            return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise ValueError("Date has invalid format")
