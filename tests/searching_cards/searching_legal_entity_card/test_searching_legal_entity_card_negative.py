from http import HTTPStatus
from typing import Final

import pytest

from src.cases import case, step
from src.constants import ErrorText, LEType, LegalEntityCardRequiredField
from src.generators import fake
from src.schemas import SearchEntitySchema, ValidationErrorSchema

INVALID_VALUES: Final[tuple[str, ...]] = ("111", "asdd", "@@@--", "-- DROP TABLE public.entities")


@case(id=14927, title="Поиск карточки ЮЛ. Не передаем поля поиска")
def test_searching_legal_entity_card_no_field(auth_ola_client):
    request = auth_ola_client.entities.get.legal_entity
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос не передавая поля поиска",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors.inn содержит ошибку '{ErrorText.REQUIRED}'"):
        assert response.errors.inn == ErrorText.REQUIRED


@pytest.mark.parametrize("field", LegalEntityCardRequiredField.as_tuple())
@pytest.mark.parametrize("le_type", LEType.as_tuple())
@case(id=14928, title="Поиск карточки ЮЛ. Не передаем обязательные поля")
def test_searching_legal_entity_card_no_required_field(auth_ola_client, create_legal_entity, le_type, field):
    data, _ = create_legal_entity(le_type)
    query = data.as_dict()
    del query[field]
    request = auth_ola_client.entities.get.legal_entity.query(**query)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос не передавая одно из обязательных полей",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.REQUIRED}'"):
        assert response.errors[field] == ErrorText.REQUIRED


@pytest.mark.parametrize("le_type", LEType.as_tuple())
@case(id=14929, title="Поиск отсутствующей в базе карточки ЮЛ по ИНН")
def test_searching_legal_entity_card_no_entity(auth_ola_client, le_type):
    inn = fake.businesses_inn() if le_type == LEType.COMP else fake.individuals_inn()
    request = auth_ola_client.entities.get.legal_entity.query(inn=inn)
    response = request(
        status=HTTPStatus.OK, schema=SearchEntitySchema, step_name="Отправить запрос с отсутствующим в базе inn"
    )
    with step("В ответе поле found равно false"):
        assert response.found is False
    with step("В поле ID пустая строка"):
        assert response.id == ""


@pytest.mark.parametrize("le_type", LEType.as_tuple())
@case(id=14930, title="Поиск карточки ЮЛ. Передаем верный ИНН и не верный ОГРН")
def test_searching_legal_entity_card_ogrn_error(auth_ola_client, create_legal_entity, le_type):
    """Тест проверяет, что если в поля поиска ввести верный ИНН но сделать ошибку в ОГРН то ЮЛ не найдется"""
    data, _ = create_legal_entity(le_type)
    query = data.as_dict()
    query["ogrn"] = fake.businesses_ogrn() if le_type == LEType.COMP else fake.individuals_ogrn()
    request = auth_ola_client.entities.get.legal_entity.query(**query)
    response = request(
        status=HTTPStatus.OK, schema=SearchEntitySchema, step_name="Отправить запрос с верным inn и неверным ogrn"
    )
    with step("В ответе поле found равно false"):
        assert response.found is False
    with step("В поле ID пустая строка"):
        assert response.id == ""


@pytest.mark.parametrize("value", INVALID_VALUES)
@case(id=14931, title="Поиск карточки ЮЛ. Невалидный ИНН")
def test_searching_legal_entity_card_invalid_inn(auth_ola_client, value):
    request = auth_ola_client.entities.get.legal_entity.query(inn=value)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с невалидным ИНН",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors.inn содержит ошибку '{ErrorText.INVALID_FORMAT}'"):
        assert response.errors.inn[0] == ErrorText.INVALID_FORMAT


@pytest.mark.parametrize("value", INVALID_VALUES)
@case(id=14932, title="Поиск карточки ЮЛ. Невалидный ОГРН")
def test_searching_legal_entity_card_invalid_ogrn(auth_ola_client, value):
    request = auth_ola_client.entities.get.legal_entity.query(inn=fake.businesses_inn(), ogrn=value)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с невалидным ОГРН",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors.ogrn содержит ошибку '{ErrorText.INVALID_FORMAT}'"):
        assert response.errors.ogrn[0] == ErrorText.INVALID_FORMAT


@pytest.mark.parametrize("le_type", LEType.as_tuple())
@case(id=14935, title="Поиск карточки ЮЛ. Передаем неверный ИНН и верный ОГРН")
def test_searching_legal_entity_card_inn_error(auth_ola_client, create_legal_entity, le_type):
    """Тест проверяет, что если в поля поиска ввести не верный ИНН но верный ОГРН то ЮЛ не найдется"""
    data, _ = create_legal_entity(le_type)
    query = data.as_dict()
    query["inn"] = fake.businesses_inn() if le_type == LEType.COMP else fake.individuals_inn()
    request = auth_ola_client.entities.get.legal_entity.query(**query)
    response = request(
        status=HTTPStatus.OK, schema=SearchEntitySchema, step_name="Отправить запрос с неверным inn и верным ogrn"
    )
    with step("В ответе поле found равно false"):
        assert response.found is False
    with step("В поле ID пустая строка"):
        assert response.id == ""
