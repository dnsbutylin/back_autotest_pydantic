"""Генераторы"""

import random
from dataclasses import asdict, dataclass, field
from typing import Any, Iterator

from box import Box
from faker import Faker

from .constants import DATE_FORMAT, LeasingObjectType

# mypy: disable_error_code=arg-type

fake = Faker("ru_RU")


def date_of_birth(min_age: int = 18, max_age: int = 80, date_format: str = DATE_FORMAT) -> str:
    """Генерация даты рождения"""
    return fake.date_of_birth(minimum_age=min_age, maximum_age=max_age).strftime(date_format)


def russian_passport() -> str:
    """Генератор паспорта"""
    return fake.bothify("#" * 10)


def ru_letter() -> str:
    """Возвращает одну букву"""
    return random.choice(tuple(fake.word()))


def replace_int(value: str) -> str:
    """Заменяет значение числа в строке"""
    count = random.randint(0, 5)
    char_int = int(value[count])
    char_int += 1
    if char_int > 9:
        char_int //= 10
    value_list = list(value)
    value_list[count] = str(char_int)
    return "".join(value_list)


@dataclass
class DataClassGen:
    """Базовый датакласс для генерации данных"""

    @classmethod
    def class_fields(cls) -> tuple[str, ...]:
        """Возвращает поля датакласса"""
        return tuple(cls.__dataclass_fields__.keys())  # pylint: disable=no-member

    def as_dict(self, missing_none: bool = True) -> dict[str, Any]:
        """
        Возвращает словарь
        :param missing_none: Удалить все None значения
        """
        return asdict(  # type: ignore[call-overload]
            obj=self,
            dict_factory=(lambda x: Box({k: v for k, v in x if v is not None})) if missing_none else Box,
        )

    def items(self) -> Iterator[tuple[str, Any]]:
        """Итератор по датаклассу"""
        for key, value in self.as_dict().items():
            yield key, value


@dataclass
class Person(DataClassGen):
    """Генератор данных для регистрации ФЛ"""

    lastname: str | None = field(default_factory=fake.last_name)
    firstname: str | None = field(default_factory=fake.first_name)
    middlename: str | None = field(default_factory=fake.middle_name)
    russian_passport: str | None = field(default_factory=russian_passport)
    birthdate: str | None = field(default_factory=date_of_birth)
    inn: str | None = field(default_factory=fake.individuals_inn)

    def items(self) -> Iterator[tuple[str, Any]]:
        """Переопределяет поле отличающееся в базе"""
        for key, value in super().items():
            if key == "russian_passport":
                key = "passport_number"
            yield key, value


@dataclass
class LegalEntity(DataClassGen):
    """Генератор данных для регистрации ЮЛ"""

    inn: str | None = field(default_factory=fake.businesses_inn)
    ogrn: str | None = field(default_factory=fake.businesses_ogrn)


@dataclass
class LeasingObjectIdentifier(DataClassGen):
    """Вложенный объект для регистрации OЛ"""

    value: str | None = field(default_factory=fake.vin)
    type: str | None = field(default=LeasingObjectType.TRANSPORTATION_VEHICLE_OTHER)


@dataclass
class LeasingObject(DataClassGen):
    """Генератор данных для регистрации OЛ"""

    title: str | None = field(default_factory=lambda: fake.sentence(nb_words=4))
    identifier: LeasingObjectIdentifier | None = field(default_factory=LeasingObjectIdentifier)

    def get_search_data(self) -> dict[str, str]:
        """Получить значения для поиска"""
        return {
            "identifier": self.identifier.value,  # type: ignore
            "identifier_type": self.identifier.type,  # type: ignore
        }
