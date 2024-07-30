import json
import random
from http import HTTPStatus
from pathlib import Path
from typing import Callable

import allure
import pytest

from src.cases import step
from src.constants import LEType, LegalJsonField
from src.db_client import DataBaseClient
from src.generators import LeasingObject, LegalEntity, Person
from src.schemas import EntitySchema

# mypy: disable_error_code="union-attr,no-redef"


class Keys:
    COMP_FREE = "comp_free"
    COMP_BUSY = "comp__busy"
    IP_FREE = "ip_free"
    IP_BUSY = "ip_busy"


@pytest.fixture(scope="session")
def _load_legal_entity_data(root_path: Path, request: pytest.FixtureRequest, db_config):
    with (root_path / "files" / "comp.json").open("rb") as file:
        request.config.cache.set(Keys.COMP_FREE, json.loads(file.read()))
        request.config.cache.set(Keys.COMP_BUSY, [])
    with (root_path / "files" / "ip.json").open("rb") as file:
        request.config.cache.set(Keys.IP_FREE, json.loads(file.read()))
        request.config.cache.set(Keys.IP_BUSY, [])
    yield
    removed: set[str] = set()
    if removed_comp := request.config.cache.get(Keys.COMP_BUSY, []):
        removed.update(i[LegalJsonField.INN] for i in removed_comp)
    if removed_ip := request.config.cache.get(Keys.IP_BUSY, []):
        removed.update(i["inn"] for i in removed_ip)
    if removed:
        with DataBaseClient(**db_config.get()) as data_base:
            data_base.removed_entities_by_inn(inns=tuple(removed))


@pytest.fixture
def create_person_card(auth_ola_client) -> Callable[..., tuple[Person, str]]:
    """Создание каторчки ФЛ"""

    def _call(*, step_name: str | None = "Создать карточку ФЛ", **kwargs) -> tuple[Person, str]:
        with step(step_name):
            person = Person(**kwargs)
            requests = auth_ola_client.entities.post.person.body(person)
            response = requests(HTTPStatus.CREATED, schema=EntitySchema)
            with step("В ответе поле exists равно false"):
                assert response.exists is False
        return person, response.id

    return _call


@pytest.fixture
def legal_entity_data(  # noqa: CCR001
    request: pytest.FixtureRequest,
    _load_legal_entity_data,
) -> Callable[[str], LegalEntity]:
    """Возвращает данные для создания ФЛ"""

    def _call(ul_type: str) -> LegalEntity:
        if ul_type == LEType.COMP:
            free_data: list[dict] = request.config.cache.get(Keys.COMP_FREE, [])
            if not free_data:
                raise ValueError("Нет доступных данных для создания ЮЛ")
            value = free_data.pop(random.randint(0, len(free_data) - 1))
            request.config.cache.set(Keys.COMP_FREE, free_data)
            used_data: list[dict] = request.config.cache.get(Keys.COMP_BUSY, [])
            used_data.append(value)
            request.config.cache.set(Keys.COMP_BUSY, used_data)
            return LegalEntity(inn=value[LegalJsonField.INN], ogrn=value[LegalJsonField.OGRN])
        else:
            free_data: list[dict] = request.config.cache.get(Keys.IP_FREE, [])
            if not free_data:
                raise ValueError("Нет доступных данных для создания ЮЛ")
            value = free_data.pop(random.randint(0, len(free_data) - 1))
            request.config.cache.set(Keys.IP_FREE, free_data)
            used_data: list[dict] = request.config.cache.get(Keys.IP_BUSY, [])
            used_data.append(value)
            request.config.cache.set(Keys.IP_BUSY, used_data)
            return LegalEntity(inn=value["inn"], ogrn=value["ogrnip"])

    return _call


@pytest.fixture
def create_legal_entity(legal_entity_data, auth_ola_client) -> Callable[[str], tuple[LegalEntity, str]]:
    """Создать карточку ЮЛ"""

    @allure.step("Создать карточку ЮЛ ({ul_type})")
    def _call(ul_type: str) -> tuple[LegalEntity, str]:
        data = legal_entity_data(ul_type)
        request = auth_ola_client.entities.post.legal_entity.body(data)
        response = request(HTTPStatus.CREATED, step_name="Создать карточку ЮЛ", schema=EntitySchema)
        with step("В ответе поле exists равно false"):
            assert response.exists is False
        return data, response.id

    return _call


@pytest.fixture
def create_leasing_object_card(auth_ola_client) -> tuple[LeasingObject, str]:
    """Создание каторчки ОЛ"""
    leasing_object = LeasingObject()
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(HTTPStatus.CREATED, step_name="Создать карточку ОЛ", schema=EntitySchema)
    with step("В ответе поле exists равно false"):
        assert response.exists is False
    return leasing_object, response.id
