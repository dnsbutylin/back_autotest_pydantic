from http import HTTPStatus

from src.cases import case, step
from src.constants import CardType
from src.schemas import LeasingObjectEntitySchema, VisitsHistorySchema


@case(id=14982, title="Получение только что созданной карточки ОЛ по ID")
def test_get_leasing_object_card(create_leasing_object_card, auth_ola_client):
    """Тест проверяет получение карточки ОЛ по ID и последующем отображение данной карточки в истории"""
    leasing_object, entity_id = create_leasing_object_card
    request = auth_ola_client.entities.get.leasing_object_id.path(id=entity_id)
    response = request(status=HTTPStatus.OK, schema=LeasingObjectEntitySchema, step_name="Получить карточку ОЛ по ID")
    with step("Проверить правильность отображения данных в полях", response=response):
        with step("Поле title соответствует переданному при создании ОЛ"):
            assert response.title == leasing_object.title
        with step("Поле identifier соответствует переданному при создании ОЛ"):
            assert response.identifier == leasing_object.identifier.value
        with step("Поле identifier_type соответствует переданному при создании ОЛ"):
            assert response.identifier_type == leasing_object.identifier.type
    with step("Проверить, что полученная карточка появилась и отображена первой в истории просмотров"):
        request = auth_ola_client.entities.get.visits_history
        response = request(status=HTTPStatus.OK, schema=[VisitsHistorySchema], step_name="Запросить историю просмотров")
        with step("Полученная карточка первая в истории просмотров"):
            assert response[0].entity.id == entity_id


@case(id=14983, title="Получение ранее созданной карточки ОЛ по ID")
def test_get_leasing_object_card_old(auth_ola_client, db_client):
    value = db_client.get_random_entity_by_type(type_code=CardType.LEASING_OBJECT)
    request = auth_ola_client.entities.get.leasing_object_id.path(id=value["id"])
    response = request(
        status=HTTPStatus.OK, schema=LeasingObjectEntitySchema, step_name="Получить карточку ОЛ по ID из БД"
    )
    with step("Проверить правильность отображения данных в полях", response=response):
        with step("Поле title соответствует данным в БД"):
            assert response.title == value["data"]["title"]
        with step("Поле identifier соответствует данным в БД"):
            assert response.identifier == value["data"]["identifier"]
        with step("Поле identifier_type соответствует данным в БД"):
            assert response.identifier_type == value["data"]["identifier_type"]
    with step("Проверить, что полученная карточка появилась и отображена первой в истории просмотров"):
        request = auth_ola_client.entities.get.visits_history
        response = request(status=HTTPStatus.OK, schema=[VisitsHistorySchema], step_name="Запросить историю просмотров")
        with step("Полученная карточка первая в истории просмотров"):
            assert response[0].entity.id == value["id"]
