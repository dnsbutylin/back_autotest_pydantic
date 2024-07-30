from http import HTTPStatus
from string import printable

import pytest

from src.cases import case, step
from src.constants import ALLOWED_CHARACTERS, ErrorText, PersonCardRequiredField
from src.generators import Person, date_of_birth, fake, russian_passport
from src.schemas import ErrorSchema, SearchEntitySchema, ValidationErrorSchema


@case(id=14921, title="Поиск карточки ФЛ. Запрос без полей поиска")
def test_searching_person_card_no_all_required_fields(auth_ola_client):
    request = auth_ola_client.entities.get.person
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос без полей поиска",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    for field in PersonCardRequiredField.as_tuple():
        with step(f"Поле 'errors.{field}' содержит ошибку: '{ErrorText.REQUIRED}'"):
            assert response.errors[field] == ErrorText.REQUIRED


@pytest.mark.parametrize("field", PersonCardRequiredField.as_tuple())
@case(id=14923, title="Поиск карточки ФЛ. Запрос без полей поиска")
def test_searching_person_card_no_required_field(auth_ola_client, field):
    person = Person()
    query = person.as_dict()
    del query[field]
    request = auth_ola_client.entities.get.person.query(**query)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос без полей поиска",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле 'errors' содержит ошибку: '{ErrorText.REQUIRED}'"):
        assert response.errors[field] == ErrorText.REQUIRED


@case(id=15000, title="Поиск карточки ФЛ. Запрос с неверным паспортом без ИНН")
def test_searching_person_card_invalid_russian_passport_no_inn(auth_ola_client, create_person_card):
    """Тест проверяет, что если в поиске не указывать ИНН и указать неверный паспорт, то карточка не будет найдена"""
    person, entity_id = create_person_card()
    query = person.as_dict()
    query.russian_passport = russian_passport()
    del query["inn"]
    request = auth_ola_client.entities.get.person.query(**query)
    response = request(
        status=HTTPStatus.OK,
        schema=SearchEntitySchema,
        step_name="Отправить запрос без поля inn и с другим паспортом",
    )
    with step("В ответе поле found равно false"):
        assert response.found is False
    with step("В поле ID пустая строка"):
        assert response.id == ""


@case(id=15001, title="Поиск карточки ФЛ. Результат поиска содержит более 1 карточки")
def test_searching_person_card_too_many_persons_found(auth_ola_client, create_person_card):
    """
    Тест проверяет, что если в поиске указать данные под которые попадают более 1 карточки,
    то сиситема ответит ошибкой 'too many persons found'
    """
    person1, _ = create_person_card(step_name="Создать ФЛ 1")
    person2, _ = create_person_card(step_name="Создать ФЛ 2")
    query = person1.as_dict()
    query.inn = person2.inn
    request = auth_ola_client.entities.get.person.query(**query)
    response = request(
        status=HTTPStatus.BAD_REQUEST,
        schema=ErrorSchema,
        step_name="Отправить запрос на поиск где все основные поля будут от ФЛ 1, а ИНН от ФЛ 2",
    )
    with step(f"Поле code содержит ошибку: '{ErrorText.TOO_MANY}'"):
        assert response.code == ErrorText.TOO_MANY
    with step(f"Поле message содержит ошибку: '{ErrorText.TOO_MANY_PERSONS_FOUND}'"):
        assert response.message == ErrorText.TOO_MANY_PERSONS_FOUND


@case(id=15002, title="Поиск карточки ФЛ. Запрос с неверной датой рождения без ИНН")
def test_searching_person_card_invalid_birthdate_no_inn(auth_ola_client, create_person_card):
    """
    Тест проверяет, что если в поиске не указывать ИНН и указать неверную дату рождения, то карточка не будет найдена
    """
    person, entity_id = create_person_card()
    query = person.as_dict()
    query.birthdate = date_of_birth()
    del query["inn"]
    request = auth_ola_client.entities.get.person.query(**query)
    response = request(
        status=HTTPStatus.OK,
        schema=SearchEntitySchema,
        step_name="Отправить запрос без поля inn и с другой датой рождения",
    )
    with step("В ответе поле found равно false"):
        assert response.found is False
    with step("В поле ID пустая строка"):
        assert response.id == ""


@pytest.mark.parametrize("field", ("russian_passport", "inn"))
@pytest.mark.parametrize("value", ("qwe", "135091892", "---", "@%$#"))
@case(id=15004, title="Поиск карточки ФЛ. Невалидное значение в полях паспорт и ИНН")
def test_searching_person_card_passport_and_inn_validation(auth_ola_client, value, field):
    person = Person(**{field: value})
    request = auth_ola_client.entities.get.person.query(person)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с невалидным значением поля",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле 'errors' содержит ошибку: '{ErrorText.INVALID_FORMAT}'"):
        assert response.errors[field][0] == ErrorText.INVALID_FORMAT


@case(id=15005, title="Поиск карточки ФЛ. Невалидное значение даты рождения")
@pytest.mark.parametrize("value", ("1", "йцуйцу", "qweqwe", "@20@12", "12--12--12"))
def test_searching_person_card_invalid_birthdate(auth_ola_client, value):
    person = Person(birthdate=value)
    request = auth_ola_client.entities.get.person.query(person)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с невалидной датой рождения",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле 'errors' содержит ошибку: '{ErrorText.INVALID_BIRTHDATE}'"):
        assert response.errors.birthdate[0] == ErrorText.INVALID_BIRTHDATE


@case(id=15006, title="Поиск карточки ФЛ. Невалидный формат даты рождения")
@pytest.mark.parametrize("date_format", ("%d.%m.%Y", "%m-%d-%Y", "%m/%d/%Y", "%d-%m-%Y", "%d/%m/%Y"))
def test_searching_person_card_invalid_format_birthdate(auth_ola_client, date_format):
    person = Person(birthdate=date_of_birth(date_format=date_format))
    request = auth_ola_client.entities.get.person.query(person)
    response = request(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с невалидным форматом даты рождения",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле 'errors' содержит ошибку: '{ErrorText.INVALID_BIRTHDATE}'"):
        assert response.errors.birthdate[0] == ErrorText.INVALID_BIRTHDATE


@case(id=15007, title="Поиск карточки ФЛ. Недопустимые символы в полях")
@pytest.mark.parametrize("field", ("lastname", "firstname", "middlename"))
@pytest.mark.parametrize("symbol", (i for i in printable if i not in ALLOWED_CHARACTERS))
def test_searching_person_invalid_symbols(auth_ola_client, field, symbol):
    """Тест проверяет получение ошибки от API при попытке получить ФЛ c недопустимыми символами"""
    person = Person(**{field: f"{fake.last_name()}{symbol}{fake.last_name()}"})
    requests = auth_ola_client.entities.get.person.query(person)
    response = requests(
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        schema=ValidationErrorSchema,
        step_name="Отправить запрос с недопустимым символом",
    )
    with step(f"Текст ошибки в поле message: '{ErrorText.VALIDATION_ERROR}'"):
        assert response.message == ErrorText.VALIDATION_ERROR
    with step(f"Поле errors содержит ошибку '{ErrorText.INVALID_FORMAT}'"):
        assert response.errors[field][0] == ErrorText.INVALID_FORMAT
