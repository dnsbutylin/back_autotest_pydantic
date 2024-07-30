from datetime import date, timedelta
from http import HTTPStatus
from string import printable
from typing import Final

import pytest

from src.cases import case, step
from src.constants import ALLOWED_CHARACTERS, DATE_FORMAT, ErrorText, FieldsLength, PersonCardRequiredField
from src.generators import Person, fake, ru_letter
from src.schemas import ValidationErrorSchema

FIELD: Final[tuple[str, ...]] = ("lastname", "firstname", "middlename")


@case(id=14866, title="Создание карточки ФЛ. Не передаем обязательное поле")
@pytest.mark.parametrize("field", PersonCardRequiredField.as_tuple())
def test_create_person_card_not_required_field(auth_ola_client, field):
    person = Person(**{field: None})
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос без обязательного поля",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.REQUIRED}'"):
        assert response.errors[field] == ErrorText.REQUIRED


@case(id=14868, title=f"Ошибка при длине полей менее: {FieldsLength.MIN_LENGTH}")
@pytest.mark.parametrize("field", FIELD)
def test_create_person_less_min_length_field(auth_ola_client, field):
    """Тест проверяет, что если поля менее 1 символа, то API вернет ошибку"""
    person = Person(**{field: ru_letter() * (FieldsLength.MIN_LENGTH - 1)})
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name=f"Отправить запрос с длиной поля: {FieldsLength.MIN_LENGTH - 1}",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.MUST_NOT_BE_EMPTY}'"):
        assert response.errors[field][0] == ErrorText.MUST_NOT_BE_EMPTY


@case(id=14869, title=f"Ошибка при длине полей более: {FieldsLength.MAX_LENGTH}")
@pytest.mark.parametrize("field", FIELD)
def test_create_person_more_max_length_field(auth_ola_client, field):
    """Тест проверяет, что если поля более 100 символа, то API вернет ошибку"""
    person = Person(**{field: ru_letter() * (FieldsLength.MAX_LENGTH + 1)})
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name=f"Отправить запрос с длиной поля: {FieldsLength.MAX_LENGTH + 1}",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    error_text = ErrorText.MORE_THAN_MAX_LEN.format(length=FieldsLength.MAX_LENGTH)
    with step(f"Поле errors содержит ошибку '{error_text}'"):
        assert response.errors[field][0] == error_text


@case(id=14870, title="Создание карточки ФЛ. Недопустимые символы в полях")
@pytest.mark.parametrize("field", FIELD)
@pytest.mark.parametrize("symbol", (i for i in printable if i not in ALLOWED_CHARACTERS))
def test_create_person_invalid_symbols(auth_ola_client, field, symbol):
    """Тест проверяет получение ошибки от API при попытке создать ФЛ c недопустимыми символами"""
    person = Person(**{field: f"{fake.last_name()}{symbol}{fake.last_name()}"})
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с недопустимым символом",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.INVALID_FORMAT}'"):
        assert response.errors[field][0] == ErrorText.INVALID_FORMAT


@case(id=14872, title="Создание карточки ФЛ. Невозможность использовать резрешенные символы в начале или конце строки")
@pytest.mark.parametrize("field", FIELD)
@pytest.mark.parametrize("symbol", ALLOWED_CHARACTERS)
@pytest.mark.parametrize("is_start", (True, False))
def test_create_person_no_start_end_symbols(auth_ola_client, field, symbol, is_start):
    """Тест проверяет что разрешенные символы в ФИО не могут использоваться в начале или конце строки"""
    person = Person(**{field: f"{symbol}Иван" if is_start else f"Иван{symbol}"})
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с символом в начале или конце строки",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    error_text = ErrorText.MUST_NOT_START_WITH_SYMBOL if is_start else ErrorText.MUST_NOT_END_WITH_SYMBOL
    with step(f"Поле errors содержит ошибку '{error_text}'"):
        assert response.errors[field][0] == error_text.format(symbol=symbol)


@case(id=14873, title="Создание карточки ФЛ. Передаем невалидный тип данных")
@pytest.mark.parametrize("value", (1, [1, 2], {"a": 1}, True, 0.001))
@pytest.mark.parametrize("field", Person.class_fields())
def test_create_person_invalid_types(auth_ola_client, field, value):
    """Тест проверяет что API ответит ошибкой если в поля передать другой тип данных"""
    person = Person(**{field: value})
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с невалидным типом данных",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.EXPECTED_TYPE_STRING}'"):
        assert response.errors[field] == ErrorText.EXPECTED_TYPE_STRING


@pytest.mark.parametrize("value", ("712327833", "31570891660", "646966A670", "6336 834725", "1862-747709"))
@case(id=14874, title="Создание карточки ФЛ. Передаем невалидный паспорт")
def test_create_person_invalid_passport(auth_ola_client, value):
    """Тест проверяет, что API ответит ошибкой при попытке создать ФЛ c невалидным форматом паспорта"""
    person = Person(russian_passport=value)
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с невалидным паспортом",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors.russian_passport содержит ошибку '{ErrorText.INVALID_FORMAT}'"):
        assert response.errors.russian_passport[0] == ErrorText.INVALID_FORMAT


@pytest.mark.parametrize("value", ("1885014092721", "88262626866", "C93534835580", "151812 748244", "60628-2308542"))
@case(id=14875, title="Создание карточки ФЛ. Передаем невалидный ИНН")
def test_create_person_invalid_inn(auth_ola_client, value):
    """Тест проверяет, что API ответит ошибкой при попытке создать ФЛ c невалидным форматом ИНН"""
    person = Person(inn=value)
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с невалидным ИНН",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors.inn содержит ошибку '{ErrorText.INVALID_FORMAT}'"):
        assert response.errors.inn[0] == ErrorText.INVALID_FORMAT


@case(id=14876, title="Создание карточки ФЛ. Передаем ИНН компании")
def test_create_person_company_inn(auth_ola_client):
    """Тест проверяет, что API ответит ошибкой при попытке создать ФЛ c ИНН ЮЛ"""
    person = Person(inn=fake.businesses_inn())
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с ЮЛ ИНН",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors.inn содержит ошибку '{ErrorText.INVALID_FORMAT}'"):
        assert response.errors.inn[0] == ErrorText.INVALID_FORMAT


@pytest.mark.parametrize("value", ("1", "йцуйцу", "qweqwe", "@20@12", "12--12--12"))
@case(id=14877, title="Создание карточки ФЛ. Передаем невалидную дату рождения")
def test_create_person_invalid_birthdate(auth_ola_client, value):
    """Тест проверяет, что API ответит ошибкой при попытке создать ФЛ c невалидной датой рождения"""
    person = Person(birthdate=value)
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с невалидной датой рождения",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors.birthdate содержит ошибку '{ErrorText.INVALID_BIRTHDATE}'"):
        assert response.errors.birthdate[0] == ErrorText.INVALID_BIRTHDATE


@pytest.mark.parametrize("value", ("%d.%m.%Y", "%m-%d-%Y", "%m/%d/%Y", "%d-%m-%Y", "%d/%m/%Y"))
@case(id=14878, title="Создание карточки ФЛ. Передаем невалидный формат даты рождения")
def test_create_person_invalid_format_birthdate(auth_ola_client, value):
    """Тест проверяет, что API ответит ошибкой при попытке создать ФЛ c невалидным форматом даты рождения"""
    person = Person(birthdate=fake.date_of_birth(minimum_age=18, maximum_age=80).strftime(value))
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с невалидным форматом даты рождения",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors.birthdate содержит ошибку '{ErrorText.INVALID_BIRTHDATE}'"):
        assert response.errors.birthdate[0] == ErrorText.INVALID_BIRTHDATE


@case(id=14879, title="Создание карточки ФЛ. Передаем дату рождения в будущем")
def test_create_person_birthdate_in_the_future(auth_ola_client):
    """Тест проверяет невозможность создать ФЛ с датой рождения в будущем"""
    person = Person(birthdate=(date.today() + timedelta(days=1)).strftime(DATE_FORMAT))
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с датой рождения now + 1 day",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors.birthdate содержит ошибку '{ErrorText.MUST_NOT_BE_IN_THE_FUTURE}'"):
        assert response.errors.birthdate[0] == ErrorText.MUST_NOT_BE_IN_THE_FUTURE
