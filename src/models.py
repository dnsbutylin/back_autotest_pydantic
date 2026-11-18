"""Единственный класс на валидацию данных и описание сущности.

Раньше пользователь, заказ и ошибка были разрезаны на отдельные модели
запроса и ответа. Contract заменяет их все: одни и те же поля и правила
проверяют тело запроса, JSON ответа и строку из базы.
"""

from typing import ClassVar, Self, Sequence

from faker import Faker
from pydantic import BaseModel, ConfigDict, EmailStr, Field

fake = Faker()


class Contract(BaseModel):
    """Контракт пользователя, заказа или ошибки.

    Пустые поля не участвуют в проверке: у пользователя нет product_name,
    у заказа нет email, у ошибки заполнен только error. Ограничения
    срабатывают на тех полях, которые реально переданы.
    """

    model_config = ConfigDict(extra="ignore")

    id: int | None = None
    username: str | None = Field(default=None, min_length=3, pattern=r"^[a-zA-Z0-9]")
    email: EmailStr | None = None
    age: int | None = Field(default=None, gt=0, lt=100)
    user_id: int | None = None
    product_name: str | None = None
    quantity: int | None = Field(default=None, gt=0)
    error: str | None = None

    USER_ROW: ClassVar[tuple[str, ...]] = ("id", "username", "email", "age")
    ORDER_ROW: ClassVar[tuple[str, ...]] = ("id", "user_id", "product_name", "quantity")

    @classmethod
    def user(cls) -> Self:
        """Собрать контракт нового пользователя."""
        return cls(
            username=fake.user_name(),
            email=fake.email(),
            age=fake.random_int(min=1, max=99),
        )

    @classmethod
    def order(cls, user_id: int) -> Self:
        """Собрать контракт нового заказа."""
        return cls(
            user_id=user_id,
            product_name=fake.word(),
            quantity=fake.random_int(min=1, max=10),
        )

    @classmethod
    def from_db_tuple(cls, db_tuple: Sequence, fields: Sequence[str]) -> Self:
        """Собрать контракт из строки БД. fields задаёт порядок колонок."""
        return cls.model_validate(dict(zip(fields, db_tuple)))

    def payload(self) -> dict:
        """Тело запроса: только заполненные поля, без текста ошибки."""
        return self.model_dump(exclude_none=True, exclude={"error"})

    def matches(self, other: "Contract", *fields: str) -> bool:
        """Сравнить контракты по названным полям."""
        keys = set(fields)
        return self.model_dump(include=keys) == other.model_dump(include=keys)
