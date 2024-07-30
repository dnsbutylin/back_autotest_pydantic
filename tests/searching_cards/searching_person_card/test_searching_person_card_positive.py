from http import HTTPStatus

import pytest

from src.cases import case, step
from src.constants import ALLOWED_CHARACTERS, PersonCardRequiredField
from src.generators import date_of_birth, fake, russian_passport
from src.schemas import SearchEntitySchema


@case(id=14924, title="Поиск карточки ФЛ по всем полям указанных при создании карточки")
def test_searching_person_card(auth_ola_client, create_person_card):
    person, entity_id = create_person_card()
    request = auth_ola_client.entities.get.person.query(person)
    response = request(HTTPStatus.OK, schema=SearchEntitySchema, step_name="Отправить запрос на поиск ФЛ")
    with step("В ответе поле found равно true"):
        assert response.found is True
    with step("ID в ответе соответствует ID полученном при создании"):
        assert response.id == entity_id


@case(id=14922, title="Поиск карточки ФЛ только по обязательным полям")
def test_searching_person_card_only_required_field(auth_ola_client, create_person_card):
    person, entity_id = create_person_card()
    query = {k: v for k, v in person.as_dict().items() if k in PersonCardRequiredField.as_tuple()}
    request = auth_ola_client.entities.get.person.query(**query)
    response = request(HTTPStatus.OK, schema=SearchEntitySchema, step_name="Отправить запрос на поиск ФЛ")
    with step("В ответе поле found равно true"):
        assert response.found is True
    with step("ID в ответе соответствует ID полученном при создании"):
        assert response.id == entity_id


@case(id=14996, title="Поиск карточки ФЛ. Поиск с инн")
def test_searching_person_card_no_inn(auth_ola_client, create_person_card):
    """
    Тест проверяет, что если ФЛ заведено в систему без ИНН, а при поиске ФЛ ИНН указан,
    то карточка будет найдена
    """
    person, entity_id = create_person_card(inn=None, step_name="Создать новое ФЛ без ИНН")
    query = person.as_dict()
    query.inn = fake.individuals_inn()
    request = auth_ola_client.entities.get.person.query(person)
    response = request(
        status=HTTPStatus.OK, schema=SearchEntitySchema, step_name="Отправить запрос на поиск ФЛ с указанием ИНН"
    )
    with step("В ответе поле found равно true"):
        assert response.found is True
    with step("ID в ответе соответствует ID полученном при создании"):
        assert response.id == entity_id


@case(id=14997, title="Поиск карточки ФЛ c неверными ФИО")
def test_searching_person_card_invalid_lfm(create_person_card, auth_ola_client):
    """
    Тест проверяет, что если при поиске указать неверные ФИО но верные паспорт и дату рождения,
    то карточка будет найдена
    """
    person, entity_id = create_person_card()
    query = person.as_dict()
    query.lastname = fake.last_name()
    query.firstname = fake.first_name()
    query.firstname = fake.middle_name()
    del query["inn"]
    request = auth_ola_client.entities.get.person.query(**query)
    response = request(
        status=HTTPStatus.OK,
        schema=SearchEntitySchema,
        step_name="Отправить запрос на поиск ФЛ с указанием неверных ФИО",
    )
    with step("В ответе поле found равно true"):
        assert response.found is True
    with step("ID в ответе соответствует ID полученном при создании"):
        assert response.id == entity_id


@case(id=14999, title="Поиск карточки ФЛ. Запрос с неверным паспортом но с ИНН")
def test_searching_person_card_invalid_passport(create_person_card, auth_ola_client):
    """Тест проверяет, что если в поиске указать неверный паспорт но верный ИНН то карточка будет найдена"""
    person, entity_id = create_person_card()
    query = person.as_dict()
    query.russian_passport = russian_passport()
    request = auth_ola_client.entities.get.person.query(**query)
    response = request(
        status=HTTPStatus.OK,
        schema=SearchEntitySchema,
        step_name="Отправить запрос на поиск ФЛ с указанием неверного паспорта",
    )
    with step("В ответе поле found равно true"):
        assert response.found is True
    with step("ID в ответе соответствует ID полученном при создании"):
        assert response.id == entity_id


@case(id=15003, title="Поиск карточки ФЛ. Запрос с неверной датой рождения но с ИНН")
def test_searching_person_card_invalid_birthdate(create_person_card, auth_ola_client):
    """Тест проверяет, что если в поиске указать неверную дату рождения но верный ИНН то карточка будет найдена"""
    person, entity_id = create_person_card()
    query = person.as_dict()
    query.birthdate = date_of_birth()
    request = auth_ola_client.entities.get.person.query(**query)
    response = request(
        status=HTTPStatus.OK,
        schema=SearchEntitySchema,
        step_name="Отправить запрос на поиск ФЛ с указанием неверной даты рождения",
    )
    with step("В ответе поле found равно true"):
        assert response.found is True
    with step("ID в ответе соответствует ID полученном при создании"):
        assert response.id == entity_id


@pytest.mark.parametrize("field", ("lastname", "firstname", "middlename"))
@pytest.mark.parametrize("symbol", ALLOWED_CHARACTERS)
@case(id=15008, title="Поиск карточки ФЛ. Запрос с дополнительными символами в ФИО")
def test_searching_person_valid_symbols(create_person_card, auth_ola_client, field, symbol):
    """Тест проверяет, что при поиске ФЛ можно использовать те же символы, что и при создании"""
    person, entity_id = create_person_card(**{field: f"{fake.last_name()}{symbol}{fake.last_name()}"})
    request = auth_ola_client.entities.get.person.query(person)
    response = request(HTTPStatus.OK, schema=SearchEntitySchema, step_name="Отправить запрос на поиск ФЛ")
    with step("В ответе поле found равно true"):
        assert response.found is True
    with step("ID в ответе соответствует ID полученном при создании"):
        assert response.id == entity_id
