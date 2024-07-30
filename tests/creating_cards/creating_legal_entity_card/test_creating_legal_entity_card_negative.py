from http import HTTPStatus
from typing import Final

import pytest

from src.cases import case, step
from src.constants import ErrorText, LEType, LegalEntityCardRequiredField
from src.generators import LegalEntity, replace_int
from src.schemas import ErrorSchema, ValidationErrorSchema

INVALID_VALUES: Final[tuple[str, ...]] = ("111", "asdd", "@@@--", "-- DROP TABLE public.entities")


@pytest.mark.parametrize("field", LegalEntityCardRequiredField.as_tuple())
@case(id=14897, title="Создание карточки ЮЛ. Не передаем обязательное поле")
def test_creating_legal_entity_card_not_required_field(auth_ola_client, field):
    legal_entity = LegalEntity(**{field: None})
    request = auth_ola_client.entities.post.legal_entity.body(legal_entity)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        step_name="Отправить запрос без обязательного поля",
        schema=ValidationErrorSchema,
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.REQUIRED}'"):
        assert response.errors[field] == ErrorText.REQUIRED


@case(id=14899, title="Создание карточки ЮЛ. Запрос с пустым телом")
def test_creating_legal_entity_card_empty_body(auth_ola_client):
    request = auth_ola_client.entities.post.legal_entity.body({})
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        step_name="Отправить запрос c пустым телом",
        schema=ValidationErrorSchema,
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.REQUIRED}'"):
        assert response.errors.inn == ErrorText.REQUIRED


@pytest.mark.parametrize("value", INVALID_VALUES)
@case(id=14900, title="Создание карточки ЮЛ. Передаем невалидный ИНН")
def test_creating_legal_entity_card_invalid_inn(auth_ola_client, value):
    request = auth_ola_client.entities.post.legal_entity.body(inn=value)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        step_name="Отправить запрос c невалидным ИНН",
        schema=ValidationErrorSchema,
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.INVALID_FORMAT}'"):
        assert response.errors.inn[0] == ErrorText.INVALID_FORMAT


@pytest.mark.parametrize("le_type", LEType.as_tuple())
@pytest.mark.parametrize("value", INVALID_VALUES)
@case(id=14901, title="Создание карточки ЮЛ. Передаем невалидный ОГРН")
def test_creating_legal_entity_card_invalid_ogrn(auth_ola_client, value, legal_entity_data, le_type):
    legal_entity = legal_entity_data(le_type).as_dict()
    legal_entity["ogrn"] = value
    request = auth_ola_client.entities.post.legal_entity.body(**legal_entity)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        step_name="Отправить запрос c валидным ИНН и невалидным ОГРН",
        schema=ValidationErrorSchema,
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.INVALID_FORMAT}'"):
        assert response.errors.ogrn[0] == ErrorText.INVALID_FORMAT


@case(id=14902, title="Создание карточки ЮЛ. Невалидный тип данных")
@pytest.mark.parametrize("value", (1, [1, 1], {"a": 1}, False))
@pytest.mark.parametrize("field", LegalEntity.class_fields())
def test_creating_legal_entity_card_invalid_type(auth_ola_client, value, field):
    legal_entity = LegalEntity(**{field: value})
    request = auth_ola_client.entities.post.legal_entity.body(legal_entity)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        step_name="Отправить запрос невалидным типом данных",
        schema=ValidationErrorSchema,
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.INVALID_FORMAT}'"):
        assert response.errors[field] == ErrorText.EXPECTED_TYPE_STRING


@case(id=14903, title="Создание карточки ЮЛ. Передаем данные несуществующей организации")
def test_creating_legal_entity_card_missing_entity(auth_ola_client):
    """Тест проверяет, что если передать данные ЮЛ которых нет в СПАРК то мы получаем ошибку"""
    request = auth_ola_client.entities.post.legal_entity.body(LegalEntity())
    response = request(
        status=HTTPStatus.BAD_REQUEST,
        step_name="Отправить запрос с валидными, но не существующими ИНН и ОГРН",
        schema=ErrorSchema,
    )
    with step(f"Поле code содержит ошибку: '{ErrorText.MISSING}'"):
        assert response.code == ErrorText.MISSING
    with step(f"Поле message содержит ошибку: '{ErrorText.MISSING_ENTITY}'"):
        assert response.message == ErrorText.MISSING_ENTITY


@pytest.mark.parametrize("le_type", LEType.as_tuple())
@case(id=14933, title="Создание карточки ЮЛ. Ошибка в хеш сумме ИНН")
def test_creating_legal_entity_card_inn_error_sum(auth_ola_client, legal_entity_data, le_type):
    legal_entity = legal_entity_data(le_type)
    data = legal_entity.as_dict()
    data["inn"] = replace_int(data["inn"])
    request = auth_ola_client.entities.post.legal_entity.body(**data)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        step_name="Отправить запрос c невалидным ИНН",
        schema=ValidationErrorSchema,
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.INVALID_FORMAT}'"):
        assert response.errors.inn[0] == ErrorText.INVALID_FORMAT


@pytest.mark.parametrize("le_type", LEType.as_tuple())
@case(id=14934, title="Создание карточки ЮЛ. Ошибка в хеш сумме ОГРН")
def test_creating_legal_entity_card_ogrn_error_sum(auth_ola_client, legal_entity_data, le_type):
    legal_entity = legal_entity_data(le_type)
    data = legal_entity.as_dict()
    data["ogrn"] = replace_int(data["ogrn"])
    request = auth_ola_client.entities.post.legal_entity.body(**data)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        step_name="Отправить запрос c невалидным ИНН",
        schema=ValidationErrorSchema,
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.INVALID_FORMAT}'"):
        assert response.errors.ogrn[0] == ErrorText.INVALID_FORMAT
