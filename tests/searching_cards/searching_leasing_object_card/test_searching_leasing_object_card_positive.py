from http import HTTPStatus

import pytest

from src.cases import case, step
from src.generators import LeasingObject, LeasingObjectIdentifier, fake
from src.schemas import EntitySchema, SearchEntitySchema


@case(id=14948, title="Поиск карточки ОЛ")
def test_searching_leasing_object_card(create_leasing_object_card, auth_ola_client):
    leasing_object, entity_id = create_leasing_object_card
    query = leasing_object.get_search_data()
    request = auth_ola_client.entities.get.leasing_object.query(**query)
    response = request(status=HTTPStatus.OK, schema=SearchEntitySchema, step_name="Отправить запрос на поиск ОЛ")
    with step("В ответе поле found равно true"):
        assert response.found is True
    with step("ID в ответе идентичен полученному при создании карточки"):
        assert response.id == entity_id


@pytest.mark.parametrize("symbol", ("qwe ewq", "#$%@", "-- DROP TABLE public.entities", "異體字", "😁🤘∌"))
@case(id=14949, title="Поиск карточки ОЛ с нестандартными символами в идентификаторе")
def test_searching_leasing_object_card_symbols(create_leasing_object_card, auth_ola_client, symbol):
    with step("Создать ОЛ с нестандартными символами", symbol=symbol):
        value = f"{fake.word()} {symbol}"
        leasing_object = LeasingObject(identifier=LeasingObjectIdentifier(value=value))
        request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
        response = request(status=HTTPStatus.CREATED, step_name="Создать карточку ОЛ", schema=EntitySchema)
        with step("В ответе поле exists равно false"):
            assert response.exists is False
        entity_id = response.id
    query = leasing_object.get_search_data()
    request = auth_ola_client.entities.get.leasing_object.query(**query)
    response = request(status=HTTPStatus.OK, schema=SearchEntitySchema, step_name="Отправить запрос на поиск ОЛ")
    with step("В ответе поле found равно true"):
        assert response.found is True
    with step("ID в ответе идентичен полученному при создании карточки"):
        assert response.id == entity_id
