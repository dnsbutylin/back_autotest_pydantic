from http import HTTPStatus

import pytest

from src.cases import case, step
from src.constants import ErrorText, LeasingObjectType, SearchLeasingObjectCardRequiredField
from src.generators import LeasingObject, fake
from src.schemas import SearchEntitySchema, ValidationErrorSchema


@case(id=14950, title="Поиск карточки ОЛ. Не передаем поля поиска")
def test_searching_leasing_object_card_no_fields(auth_ola_client):
    request = auth_ola_client.entities.get.leasing_object
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос не передавая поля поиска",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    for field in SearchLeasingObjectCardRequiredField.as_tuple():
        with step(f"Поле errors.{field} содержит ошибку '{ErrorText.REQUIRED}'"):
            assert response.errors[field] == ErrorText.REQUIRED


@pytest.mark.parametrize("field", SearchLeasingObjectCardRequiredField.as_tuple())
@case(id=14951, title="Поиск карточки ОЛ. Не передаем обязательное поле")
def test_searching_leasing_object_card_no_required_field(auth_ola_client, field):
    leasing_object = LeasingObject().get_search_data()
    del leasing_object[field]
    request = auth_ola_client.entities.get.leasing_object.query(**leasing_object)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос не передавая обязательное поле",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.REQUIRED}'"):
        assert response.errors[field] == ErrorText.REQUIRED


@case(id=14952, title="Поиск отсутствующего в системе ОЛ")
def test_searching_leasing_object_card_no_entity(auth_ola_client):
    leasing_object = LeasingObject().get_search_data()
    request = auth_ola_client.entities.get.leasing_object.query(**leasing_object)
    response = request(
        status=HTTPStatus.OK,
        schema=SearchEntitySchema,
        step_name="Отправить запрос на поиск отсутствующего в системе ОЛ",
    )
    with step("В ответе поле found равно false"):
        assert response.found is False
    with step("В поле ID пустая строка"):
        assert response.id == ""


@case(id=14953, title="Поиск карточки ОЛ. Передаем другой тип идентификатора")
def test_searching_leasing_object_card_invalid_identifier_type(create_leasing_object_card, auth_ola_client):
    """
    Тест проверяет, что если правильно передать идентификатор но неверно указать его тип, то система на найдет ОЛ
    """
    leasing_object, _ = create_leasing_object_card
    query = leasing_object.get_search_data()
    query["identifier_type"] = LeasingObjectType.get_random_other(query["identifier_type"])
    request = auth_ola_client.entities.get.leasing_object.query(**query)
    response = request(
        status=HTTPStatus.OK, schema=SearchEntitySchema, step_name="Отправить запрос с измененным типом идентификатора"
    )
    with step("В ответе поле found равно false"):
        assert response.found is False
    with step("В поле ID пустая строка"):
        assert response.id == ""


@case(id=14954, title="Поиск карточки ОЛ. Передаем другой идентификатор")
def test_searching_leasing_object_card_invalid_identifier(create_leasing_object_card, auth_ola_client):
    leasing_object, _ = create_leasing_object_card
    query = leasing_object.get_search_data()
    query["identifier"] = fake.vin()
    request = auth_ola_client.entities.get.leasing_object.query(**query)
    response = request(
        status=HTTPStatus.OK, schema=SearchEntitySchema, step_name="Отправить запрос с измененным идентификатором"
    )
    with step("В ответе поле found равно false"):
        assert response.found is False
    with step("В поле ID пустая строка"):
        assert response.id == ""


@case(id=14955, title="Поиск карточки ОЛ. Передаем невалидный тип идентификатора")
def test_searching_leasing_object_card_invalid_value_identifier_type(create_leasing_object_card, auth_ola_client):
    query = LeasingObject().get_search_data()
    query["identifier_type"] = fake.word()
    request = auth_ola_client.entities.get.leasing_object.query(**query)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос c невалидным типом идентификатора",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.REQUIRED}'"):
        assert response.errors.identifier_type[0] == ErrorText.MUST_BE_ONE_OF_ALLOWED_LEASING_OBJECT_TYPES
