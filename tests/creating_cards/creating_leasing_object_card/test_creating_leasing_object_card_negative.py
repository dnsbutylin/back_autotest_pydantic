from http import HTTPStatus

import pytest

from src.cases import case, step
from src.constants import (
    ErrorText,
    FieldsLength,
    LeasingObjectCardIdentifierRequiredField,
    LeasingObjectCardRequiredField,
)
from src.generators import LeasingObject, LeasingObjectIdentifier, fake, ru_letter
from src.schemas import ValidationErrorSchema

INVALID_TYPE = (1, [1, 2], {"a": 1}, True, 0.001)


@pytest.mark.parametrize("field", LeasingObjectCardRequiredField.as_tuple())
@case(id=14906, title="Создание карточки ОЛ. Не передаем обязательные поля")
def test_creating_leasing_object_card_not_required_field(auth_ola_client, field):
    leasing_object = LeasingObject(**{field: None})
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос без обязательного поля",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.REQUIRED}'"):
        assert response.errors[field] == ErrorText.REQUIRED


@pytest.mark.parametrize("field", LeasingObjectCardIdentifierRequiredField.as_tuple())
@case(id=14907, title="Создание карточки ОЛ. Не передаем обязательные поля в объекте identifier")
def test_creating_leasing_object_card_not_identifier_required_field(auth_ola_client, field):
    leasing_object = LeasingObject(identifier=LeasingObjectIdentifier(**{field: None}))
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос без обязательного поля",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors.identifier содержит ошибку '{ErrorText.REQUIRED}'"):
        assert response.errors.identifier[field] == ErrorText.REQUIRED


@case(id=14908, title="Создание карточки ОЛ. Невалидное значение типа объекта лизинга")
def test_creating_leasing_object_card_invalid_object_type(auth_ola_client):
    leasing_object = LeasingObject(identifier=LeasingObjectIdentifier(type=fake.word().upper()))
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с невалидным типом ОЛ",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors.identifier.type содержит ошибку '{ErrorText.MUST_BE_ONE_OF_ALLOWED_LEASING_OBJECT_TYPES}'"):
        assert response.errors.identifier.type[0] == ErrorText.MUST_BE_ONE_OF_ALLOWED_LEASING_OBJECT_TYPES


@case(id=14909, title=f"Ошибка при длине поля title менее: {FieldsLength.MIN_LENGTH}")
def test_creating_leasing_object_card_less_min_length_title(auth_ola_client):
    leasing_object = LeasingObject(title=ru_letter() * (FieldsLength.MIN_LENGTH - 1))
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name=f"Отправить запрос с длиной поля title {FieldsLength.MIN_LENGTH - 1}",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors.title содержит ошибку '{ErrorText.MUST_NOT_BE_EMPTY}'"):
        assert response.errors.title[0] == ErrorText.MUST_NOT_BE_EMPTY


@case(id=14910, title=f"Ошибка при длине поля identifier.value менее: {FieldsLength.MIN_LENGTH}")
def test_creating_leasing_object_card_less_min_length_identifier_value(auth_ola_client):
    leasing_object = LeasingObject(
        identifier=LeasingObjectIdentifier(value=ru_letter() * (FieldsLength.MIN_LENGTH - 1))
    )
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name=f"Отправить запрос с длиной поля title {FieldsLength.MIN_LENGTH - 1}",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors.identifier.value содержит ошибку '{ErrorText.MUST_NOT_BE_EMPTY}'"):
        assert response.errors.identifier.value[0] == ErrorText.MUST_NOT_BE_EMPTY


@pytest.mark.parametrize("value", INVALID_TYPE)
@case(id=14915, title="Создание карточки ОЛ. Невалидный тип данных поля title")
def test_creating_leasing_object_card_invalid_type_title(auth_ola_client, value):
    leasing_object = LeasingObject(title=value)
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с невалидным типом данных в поле title",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.EXPECTED_TYPE_STRING}'"):
        assert response.errors.title == ErrorText.EXPECTED_TYPE_STRING


@pytest.mark.parametrize("field", LeasingObjectIdentifier.class_fields())
@pytest.mark.parametrize("value", INVALID_TYPE)
@case(id=14916, title="Создание карточки ОЛ. Невалидный тип данных в полях identifier")
def test_creating_leasing_object_card_invalid_type_identifier_fields(auth_ola_client, value, field):
    leasing_object = LeasingObject(identifier=LeasingObjectIdentifier(**{field: value}))
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с невалидным типом данных в полях identifier",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.EXPECTED_TYPE_STRING}'"):
        assert response.errors.identifier[field] == ErrorText.EXPECTED_TYPE_STRING


@case(id=14917, title="Создание карточки ОЛ. Невалидный тип данных identifier")
@pytest.mark.parametrize("value", (1, [1, 2], "qwe", False, 0.001))
def test_creating_leasing_object_card_invalid_type_identifier(auth_ola_client, value):
    leasing_object = LeasingObject(identifier=value)
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с невалидным типом данных в полях identifier",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.EXPECTED_TYPE_STRING}'"):
        assert response.errors.identifier == ErrorText.EXPECTED_TYPE_MAP


@case(id=14918, title="Создание карточки ОЛ. Пустое тело запроса")
def test_creating_leasing_object_card_empty_body(auth_ola_client):
    request = auth_ola_client.entities.post.leasing_object.body({})
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с пустым телом запрос",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    for field in LeasingObjectCardRequiredField.as_tuple():
        with step(f"Поле errors.{field} содержит ошибку '{ErrorText.REQUIRED}'"):
            assert response.errors[field] == ErrorText.REQUIRED
