"""Описание marshmallow объектов для валидации тела ответа"""

from dataclasses import dataclass, field
from typing import Any

from marshmallow.validate import OneOf

from .constants import CardType, LeasingObjectType
from .marshmallow_types import Date, DateTime

# mypy: disable_error_code=valid-type
# pylint: disable=invalid-name,too-many-instance-attributes,missing-class-docstring


@dataclass
class Schema:
    """Родитель для наследования"""


@dataclass
class ValidationErrorSchema(Schema):
    """Ошибка validation error"""

    message: str
    errors: dict[str, str | list[str] | dict[str, str] | dict[str, list[str]]]


@dataclass
class ErrorSchema(Schema):
    """Ошибка от СПАРКа"""

    code: str
    message: str


@dataclass
class _VisitsHistoryEntitySchema(Schema):
    """Block entity"""

    id: str
    name: str | None  # TODO Deprecated: Поле должно быть удалено после переезда фронта на новое поле Title.
    title: str
    type: str = field(metadata={"validate": OneOf(CardType.as_tuple())})


@dataclass
class VisitsHistorySchema(Schema):
    """GET /entities/visits/history | list"""

    entity: _VisitsHistoryEntitySchema
    visited_at: DateTime


@dataclass
class EntitySchema(Schema):
    """
    POST /entities/person
    POST /entities/leasing-object
    POST /entities/legal-entity
    """

    id: str
    exists: bool


@dataclass
class SearchEntitySchema(Schema):
    """
    GET /entities/legal-entity
    GET /entities/leasing-object
    """

    id: str
    found: bool


@dataclass
class LeasingObjectEntitySchema(Schema):
    """
    GET /entities/leasing-object/{id}
    """

    id: str
    title: str
    identifier: str
    identifier_type: str = field(metadata={"validate": OneOf(LeasingObjectType.as_tuple())})
    comments: list[Any]


@dataclass
class PersonEntitySchema(Schema):
    """
    GET /entities/person/{id}
    """

    id: str
    firstname: str
    lastname: str
    middlename: str | None = field(metadata={"required": True})
    russian_passport: str
    birthdate: Date
    inn: str | None = field(metadata={"required": True})
    data_fields: dict[str, Any]
    comments: list[Any]


@dataclass
class _AuthorizedCapital(Schema):
    actual_date: str
    value: int


@dataclass
class _CodeName(Schema):
    code: str
    name: str


@dataclass
class LegalEntitySchema(Schema):
    """
    GET /entities/legal-entity/{id}
    """

    id: str
    inn: str
    ogrn: str
    full_name: str
    short_name: str
    email: str | None = field(metadata={"required": True})
    website: str | None = field(metadata={"required": True})
    registration_date: Date
    staff_number: int | None = field(metadata={"required": True})
    authorized_capital: _AuthorizedCapital
    okfs: _CodeName
    main_okved: _CodeName
    data_fields: dict[str, Any]
    comments: list[Any]
