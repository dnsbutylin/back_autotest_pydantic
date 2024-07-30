from http import HTTPStatus

from src.cases import case, step
from src.constants import LEType
from src.func import compare_spark_company, compare_spark_ip
from src.schemas import LegalEntitySchema, VisitsHistorySchema


@case(id=15009, title="Получение карточки ЮЛ. Запрос компании")
def test_get_legal_entity_card(create_legal_entity, auth_ola_client, spark_client):
    legal_entity, entity_id = create_legal_entity(LEType.COMP)
    request = auth_ola_client.entities.get.legal_entity_id.path(id=entity_id)
    response = request(HTTPStatus.OK, schema=LegalEntitySchema, step_name="Получить данные ЮЛ по ID")
    spark_data = spark_client.presets.get_company_data(legal_entity.inn)
    with step("ЮЛ найдено в СПАРКе"):
        assert spark_data.data
    compare_spark_company(spark_data.data[0], response)
    with step("Проверить, что полученная карточка появилась и отображена первой в истории просмотров"):
        request = auth_ola_client.entities.get.visits_history
        response = request(status=HTTPStatus.OK, schema=[VisitsHistorySchema], step_name="Запросить историю просмотров")
        with step("Полученная карточка первая в истории просмотров"):
            assert response[0].entity.id == entity_id


@case(id=15010, title="Получение карточки ЮЛ. Запрос ИП")
def test_get_legal_entity_card_ip(create_legal_entity, auth_ola_client, spark_client):
    legal_entity, entity_id = create_legal_entity(LEType.IP)
    request = auth_ola_client.entities.get.legal_entity_id.path(id=entity_id)
    response = request(HTTPStatus.OK, schema=LegalEntitySchema, step_name="Получить данные ЮЛ по ID")
    spark_data = spark_client.presets.get_ip_data(legal_entity.inn)
    with step("ЮЛ найдено в СПАРКе"):
        assert spark_data.data
    compare_spark_ip(spark_data.data[0], response)
    with step("Проверить, что полученная карточка появилась и отображена первой в истории просмотров"):
        request = auth_ola_client.entities.get.visits_history
        response = request(status=HTTPStatus.OK, schema=[VisitsHistorySchema], step_name="Запросить историю просмотров")
        with step("Полученная карточка первая в истории просмотров"):
            assert response[0].entity.id == entity_id
