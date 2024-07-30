"""Типы данных для marshmallow"""

from marshmallow.validate import Regexp
from marshmallow_dataclass import NewType

DateTime = NewType(
    name="DateTime",
    typ=str,
    validate=Regexp(
        r"^\d{4}-\d{2}-\d{2}T?\s?\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}$",
        error="Invalid datetime",
    ),
)

Date = NewType(
    name="Date",
    typ=str,
    validate=Regexp(
        r"^\d{4}-\d{2}-\d{2}$",
        error="Invalid date",
    ),
)
