from http import HTTPStatus
from uuid import uuid4

import pytest

from src.cases import case, step
from src.constants import ErrorText
from src.schemas import ErrorSchema, VisitsHistorySchema


@case(id=15011, title="Получение карточки ЮЛ по несуществующему ID")
def test_get_legal_entity_card_invalid_id(auth_ola_client):
    invalid_id = str(uuid4())
    request = auth_ola_client.entities.get.legal_entity_id.path(id=invalid_id)
    response = request(HTTPStatus.BAD_REQUEST, schema=ErrorSchema, step_name="Отправить запрос с несуществующим ID")
    with step(f"Текст ошибки в поле code: '{ErrorText.MISSING}'"):
        assert response.code == ErrorText.MISSING
    with step(f"Поле errors содержит ошибку '{ErrorText.REQUIRED}'"):
        assert response.message == ErrorText.MISSING_ENTITY
    with step("Проверить, что данный  ID не отобразился в истории"):
        request = auth_ola_client.entities.get.visits_history
        response = request(status=HTTPStatus.OK, schema=[VisitsHistorySchema], step_name="Запросить историю просмотров")
        with step("ID отсутствует в списке истории"):
            assert invalid_id not in [i.entity.id for i in response]


@pytest.mark.parametrize("symbol", ("qwe ewq", "@%#$", "-- DROP TABLE public.entities", "異體字", "😁🤘∌"))
@case(id=15012, title="Получение карточки ЮЛ. Передаем невалидный ID")
def test_get_legal_entity_card_invalid_value_id(auth_ola_client, symbol):
    request = auth_ola_client.entities.get.legal_entity_id.path(id=symbol)
    response = request(HTTPStatus.BAD_REQUEST, schema=ErrorSchema, step_name="Отправить запрос с невалидным ID")
    with step(f"Текст ошибки в поле code: '{ErrorText.MISSING}'"):
        assert response.code == ErrorText.MISSING
    with step(f"Поле errors содержит ошибку '{ErrorText.REQUIRED}'"):
        assert response.message == ErrorText.MISSING_ENTITY
