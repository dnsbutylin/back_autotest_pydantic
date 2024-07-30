from http import HTTPStatus

from src.cases import case, step
from src.constants import CardType
from src.schemas import PersonEntitySchema, VisitsHistorySchema


@case(id=14988, title="Получение только что созданной карточки ФЛ по ID")
def test_get_person_card(auth_ola_client, create_person_card):
    person, entity_id = create_person_card()
    request = auth_ola_client.entities.get.person_id.path(id=entity_id)
    response = request(status=HTTPStatus.OK, schema=PersonEntitySchema, step_name="Получить карточку ФЛ по ID")
    with step("Проверить правильность отображения данных в полях", response=response):
        with step("Поле firstname соответствует переданному при создании ФЛ"):
            assert response.firstname == person.firstname
        with step("Поле lastname соответствует переданному при создании ФЛ"):
            assert response.lastname == person.lastname
        with step("Поле middlename соответствует переданному при создании ФЛ"):
            assert response.middlename == person.middlename
        with step("Поле birthdate соответствует переданному при создании ФЛ"):
            assert response.birthdate == person.birthdate
        with step("Поле russian_passport соответствует переданному при создании ФЛ"):
            assert response.russian_passport == person.russian_passport
        with step("Поле inn соответствует переданному при создании ФЛ"):
            assert response.inn == person.inn
    with step("Проверить, что полученная карточка появилась и отображена первой в истории просмотров"):
        request = auth_ola_client.entities.get.visits_history
        response = request(status=HTTPStatus.OK, schema=[VisitsHistorySchema], step_name="Запросить историю просмотров")
        with step("Полученная карточка первая в истории просмотров"):
            assert response[0].entity.id == entity_id


@case(id=14989, title="Получение ранее созданной карточки ФЛ по ID")
def test_get_person_card_old(auth_ola_client, db_client):
    value = db_client.get_random_entity_by_type(type_code=CardType.PERSON)
    request = auth_ola_client.entities.get.person_id.path(id=value["id"])
    response = request(status=HTTPStatus.OK, schema=PersonEntitySchema, step_name="Получить карточку ФЛ по ID")
    with step("Проверить правильность отображения данных в полях", response=response):
        with step("Поле inn соответствует данным в БД"):
            assert response.inn == value["data"]["inn"]
        with step("Поле lastname соответствует данным в БД"):
            assert response.lastname == value["data"]["lastname"]
        with step("Поле birthdate соответствует данным в БД"):
            assert response.birthdate == value["data"]["birthdate"]
        with step("Поле firstname соответствует данным в БД"):
            assert response.firstname == value["data"]["firstname"]
        with step("Поле middlename соответствует данным в БД"):
            assert response.middlename == value["data"]["middlename"]
        with step("Поле russian_passport соответствует данным в БД"):
            assert response.russian_passport == value["data"]["passport_number"]
    with step("Проверить, что полученная карточка появилась и отображена первой в истории просмотров"):
        request = auth_ola_client.entities.get.visits_history
        response = request(status=HTTPStatus.OK, schema=[VisitsHistorySchema], step_name="Запросить историю просмотров")
        with step("Полученная карточка первая в истории просмотров"):
            assert response[0].entity.id == value["id"]
