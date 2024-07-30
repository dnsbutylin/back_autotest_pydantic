from http import HTTPStatus

import pytest

from src.cases import case, step
from src.constants import LEType
from src.schemas import SearchEntitySchema


@pytest.mark.parametrize("le_type", LEType.as_tuple())
@case(id=14925, title="Поиск карточки ЮЛ по ИНН и ОГРН одновременно")
def test_searching_legal_entity_card(auth_ola_client, create_legal_entity, le_type):
    data, entity_id = create_legal_entity(le_type)
    request = auth_ola_client.entities.get.legal_entity.query(data)
    response = request(HTTPStatus.OK, schema=SearchEntitySchema, step_name="Отправить запрос с полями inn и ogrn")
    with step("В ответе поле found равно true"):
        assert response.found is True
    with step("ID в ответе идентичен полученному при создании карточки"):
        assert response.id == entity_id


@case(id=14926, title="Поиск карточки ЮЛ только по ИНН")
@pytest.mark.parametrize("le_type", LEType.as_tuple())
def test_searching_legal_entity_card_only_inn(auth_ola_client, create_legal_entity, le_type):
    """Тест проверяет, что карточку ЮЛ можно найти только по ИНН"""
    data, entity_id = create_legal_entity(le_type)
    request = auth_ola_client.entities.get.legal_entity.query(inn=data.inn)
    response = request(HTTPStatus.OK, schema=SearchEntitySchema, step_name="Отправить запрос только с inn")
    with step("В ответе поле found равно true"):
        assert response.found is True
    with step("ID в ответе идентичен полученному при создании карточки"):
        assert response.id == entity_id
