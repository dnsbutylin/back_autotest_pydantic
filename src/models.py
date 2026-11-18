"""Pydantic-модели ответов.

UserResponse и OrderResponse сразу и проверяют данные, и описывают ответ:
тело запроса, JSON сервиса и строка из базы собираются одним классом.
Отдельной модели «на создание» нет.
"""

from typing import Self, Sequence

from faker import Faker
from pydantic import BaseModel, EmailStr, Field

fake = Faker()


class UserResponse(BaseModel):
    """Пользователь: и запрос на создание, и ответ, и строка users."""

    id: int | None = None
    username: str = Field(..., min_length=3, pattern=r"^[a-zA-Z0-9]")
    email: EmailStr
    age: int = Field(..., gt=0, lt=100)

    @classmethod
    def generate(cls) -> Self:
        """Собрать данные нового пользователя."""
        return cls(
            username=fake.user_name(),
            email=fake.email(),
            age=fake.random_int(min=1, max=99),
        )

    @classmethod
    def from_db_tuple(cls, db_tuple: Sequence) -> Self:
        """Собрать ответ из кортежа (id, username, email, age)."""
        keys = tuple(cls.model_fields)
        return cls.model_validate(dict(zip(keys, db_tuple)))

    def payload(self) -> dict:
        """Тело запроса без пустого id."""
        return self.model_dump(exclude_none=True)


class OrderResponse(BaseModel):
    """Заказ: и запрос на создание, и ответ, и строка orders."""

    id: int | None = None
    user_id: int
    product_name: str
    quantity: int = Field(..., gt=0)

    @classmethod
    def generate(cls, user_id: int) -> Self:
        """Собрать данные нового заказа."""
        return cls(
            user_id=user_id,
            product_name=fake.word(),
            quantity=fake.random_int(min=1, max=10),
        )

    @classmethod
    def from_db_tuple(cls, db_tuple: Sequence) -> Self:
        """Собрать ответ из кортежа (id, user_id, product_name, quantity)."""
        keys = tuple(cls.model_fields)
        return cls.model_validate(dict(zip(keys, db_tuple)))

    def payload(self) -> dict:
        """Тело запроса без пустого id."""
        return self.model_dump(exclude_none=True)


class UserError(BaseModel):
    """Ответ с текстом ошибки."""

    error: str
