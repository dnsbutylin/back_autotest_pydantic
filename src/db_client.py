"""Клиент к базе данных"""

import logging
from dataclasses import dataclass, field
from typing import Any, Self

import allure
import psycopg2
from psycopg2.extras import DictCursor

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class DataBaseMeta:
    """Коннектор к БД"""

    host: str
    port: int
    database: str
    user: str
    password: str
    conn: psycopg2.extensions.connection = field(init=False, default=None)
    cursor: psycopg2.extensions.cursor = field(init=False, default=None)

    def connect(self) -> None:
        """Коннект"""
        self.conn = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )
        logger.debug(f"Connection DB: {self.host}:{self.port} {self.database} {self.user}")
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        logger.debug("Create cursor")

    def __enter__(self) -> Self:
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # noqa: ANN001
        if self.cursor is not None:
            logger.debug("Close cursor")
            self.cursor.close()
        if self.conn is not None:
            logger.debug("Close connection")
            self.conn.close()

    def execute(self, string: str, *args) -> None:
        """Выполнить SQL"""
        logger.debug(f"Execute: {string} {args}")
        try:
            return self.cursor.execute(string, args)
        except Exception as err:
            logger.error(f"Execute error: {err}")
            raise err

    def fetchone(self) -> tuple[Any, ...]:
        """Получиль одно значение"""
        return self.cursor.fetchone()

    def fetchall(self) -> list[tuple[Any, ...]]:
        """Получить все значения"""
        return self.cursor.fetchall()

    def commit(self) -> None:
        """Коммит изменений"""
        logger.debug(f"Updated rows: {self.cursor.rowcount}")
        if self.cursor.rowcount:
            self.conn.commit()


class DataBaseClient(DataBaseMeta):
    """Клиент БД"""

    @allure.step("Получить карточку из базы данных по ID")
    def get_entity_by_id(self, entity_id: str) -> Any:
        """Получить карточку из базы данных по ID"""
        self.execute("SELECT * FROM public.entities WHERE id=%s", (entity_id,))
        return self.fetchone()

    @allure.step("Получить рандомную карточку из базы данных с type_code: '{type_code}'")
    def get_random_entity_by_type(self, type_code: str) -> Any:
        """Возвращает рандомную карточку"""
        self.execute("SELECT * FROM public.entities WHERE type_code=%s ORDER BY random() LIMIT 1", (type_code,))
        return self.fetchone()

    def removed_entities_by_inn(self, inns: tuple[str, ...]) -> None:
        """Удалить карточки по ИНН"""
        self.execute("DELETE FROM public.entities WHERE data->> 'inn' IN %s", inns)
        self.commit()

    def removed_entity_by_id(self, entity_id: str) -> None:
        """Удалить карточку по ID"""
        self.execute("DELETE FROM public.entities WHERE id=%s", (entity_id,))
        self.commit()
