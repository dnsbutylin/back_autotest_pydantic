"""Модуль для хранения пользовательских типов"""

from dataclasses import dataclass, field
from random import choice
from typing import Any, Generator, Iterable


class Missing(dict):
    """Словарь используемый для форматирования строк"""

    def __missing__(self, key: Any) -> str:
        return "{%s}" % key  # pylint: disable=C0209


class Constant:
    """Мета класс для классов констант"""

    @classmethod
    def as_iter(cls) -> Generator[tuple[str, Any], Any, None]:
        """Возвращает итератор"""
        return ((i, getattr(cls, i)) for i in dir(cls) if i.isupper() and not callable(getattr(cls, i, None)))

    @classmethod
    def as_dict(cls) -> dict[str, Any]:
        """Возвращает словарем константы"""
        return dict(cls.as_iter())

    @classmethod
    def as_tuple(cls) -> tuple[Any, ...]:
        """Возвращает кортежем константы"""
        return tuple(cls.values())

    @classmethod
    def keys(cls) -> Iterable[str]:
        """Возвращает ключи констант"""
        return cls.as_dict().keys()

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Возвращает значение константы по ключу"""
        return cls.as_dict().get(key, default)

    @classmethod
    def get_random_value(cls) -> Any:
        """Возвращает случаную константу"""
        return choice(cls.as_tuple())

    @classmethod
    def get_random_other(cls, value: Any, is_many: bool = False) -> Any:
        """
        Возвращает случайную константу исключая value
        :param value: Значение/список значений
        :param is_many: Флаг передан список значений
        """
        value = value if is_many else (value,)
        return choice([i for i in cls.values() if i not in value])

    @classmethod
    def values(cls) -> Iterable[Any]:
        """Возвращает ключи констант"""
        return cls.as_dict().values()


@dataclass(frozen=True, slots=True, kw_only=True)
class KeycloakSettings:
    """Настройки для keycloak"""

    host: str
    realm: str


@dataclass(frozen=True, slots=True, kw_only=True)
class ServiceSettings:
    """Настройки для сервисов"""

    host: str


@dataclass(frozen=True, slots=True, kw_only=True)
class KeycloakTokens:
    """Keycloak токены"""

    access_token: str
    id_token: str
    token_type: str


@dataclass(frozen=True, slots=True, kw_only=True)
class UserCredentials:
    """User Credentials dataclass"""

    keycloak_client_id: str
    keycloak_client_secret: str
    username: str
    password: str


@dataclass(frozen=True, slots=True, kw_only=True)
class DBSettings:
    """DB connection settings"""

    host: str
    port: int
    name: str
    user: str
    password: str = field(repr=False)

    def get(self) -> dict[str, str | int]:
        """Получить словарь"""
        return {
            "host": self.host,
            "port": self.port,
            "database": self.name,
            "user": self.user,
            "password": self.password,
        }


@dataclass(frozen=True, slots=True, kw_only=True)
class SparkSettings:
    """Настройки для подключения к спарку"""

    host: str
    login: str
    password: str = field(repr=False)
