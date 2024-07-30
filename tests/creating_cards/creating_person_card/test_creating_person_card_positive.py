from http import HTTPStatus
from typing import Final

import pytest

from src.cases import case, step
from src.constants import ALLOWED_CHARACTERS, CardType, FieldsLength, PersonCardRequiredField
from src.generators import Person, fake, ru_letter
from src.schemas import EntitySchema

FIELD: Final[tuple[str, ...]] = ("lastname", "firstname", "middlename")


@case(id=14858, title="Создание карточки ФЛ")
def test_create_person_card(auth_ola_client, db_client):
    """Тест создает новое ФЛ через API и проверяет, что данные появились в базе данных"""
    person = Person()
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(HTTPStatus.CREATED, step_name="Создать карточку ФЛ", schema=EntitySchema)
    with step("В ответе поле exists равно false"):
        assert response.exists is False
    result = db_client.get_entity_by_id(entity_id=response.id)
    with step(f"Тип карточки: {CardType.PERSON}"):
        assert result["type_code"] == CardType.PERSON
    with step("Все поля в базе соответствуют переданным при создании"):
        for key, value in person.items():
            with step(f"Проверить поле: {key}"):
                assert result["data"][key] == value, f"Поле {key} не соответствует переданному значению"


@case(id=14865, title="Создание карточки ФЛ. Не передаем опциональные поля")
@pytest.mark.parametrize("field", (i for i in Person.class_fields() if i not in PersonCardRequiredField.as_tuple()))
def test_create_person_card_not_optional_field(auth_ola_client, db_client, field):
    """Тест создает новое ФЛ через API не передавая опциональные поля и проверяет, что данные появились в базе данных"""
    person = Person(**{field: None})
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(HTTPStatus.CREATED, step_name="Создать карточку ФЛ", schema=EntitySchema)
    with step("В ответе поле exists равно false"):
        assert response.exists is False
    result = db_client.get_entity_by_id(entity_id=response.id)
    with step(f"Тип карточки: {CardType.PERSON}"):
        assert result["type_code"] == CardType.PERSON
    with step("Все поля в базе соответствуют переданным при создании"):
        for key, value in person.items():
            with step(f"Проверить поле: {key}"):
                assert result["data"][key] == value, f"Поле {key} не соответствует переданному значению"
    with step("Не переданное поле в базе имеет значение null"):
        assert result["data"][field] is None


@case(id=14867, title="Создание карточки ФЛ. Передаем поля максимальной и минимальной длины")
@pytest.mark.parametrize("field", FIELD)
@pytest.mark.parametrize("length", (FieldsLength.MIN_LENGTH, FieldsLength.MAX_LENGTH))
def test_create_person_card_min_max_length_field(auth_ola_client, db_client, field, length):
    person = Person(**{field: ru_letter() * length})
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(HTTPStatus.CREATED, step_name="Создать карточку ФЛ", schema=EntitySchema)
    with step("В ответе поле exists равно false"):
        assert response.exists is False
    result = db_client.get_entity_by_id(entity_id=response.id)
    with step(f"Тип карточки: {CardType.PERSON}"):
        assert result["type_code"] == CardType.PERSON
    with step("Все поля в базе соответствуют переданным при создании"):
        for key, value in person.items():
            with step(f"Проверить поле: {key}"):
                assert result["data"][key] == value, f"Поле {key} не соответствует переданному значению"


@case(id=14871, title="Создание карточки ФЛ. Дополнительные символы")
@pytest.mark.parametrize("field", FIELD)
@pytest.mark.parametrize("symbol", ALLOWED_CHARACTERS)
def test_create_person_valid_symbols(auth_ola_client, db_client, field, symbol):
    """Тест создает новое ФЛ через API c разрешенными символами и проверяет, что данные отобразились в базе"""
    person = Person(**{field: f"{fake.last_name()}{symbol}{fake.last_name()}"})
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(HTTPStatus.CREATED, step_name="Создать карточку ФЛ", schema=EntitySchema)
    with step("В ответе поле exists равно false"):
        assert response.exists is False
    result = db_client.get_entity_by_id(entity_id=response.id)
    with step(f"Тип карточки: {CardType.PERSON}"):
        assert result["type_code"] == CardType.PERSON
    with step("Все поля в базе соответствуют переданным при создании"):
        for key, value in person.items():
            with step(f"Проверить поле: {key}"):
                assert result["data"][key] == value, f"Поле {key} не соответствует переданному значению"


@case(id=14880, title="Создание карточки ФЛ. Создание уже существующего ФЛ")
def test_double_create_person(auth_ola_client, create_person_card):
    """
    Тест проверяет, что если в системе уже есть ФЛ c данными, то при попытке создать такого же,
    новая карточка не будет создана, а вернут уже существующего
    """
    person, entity_id = create_person_card()
    requests = auth_ola_client.entities.post.person.body(person)
    response = requests(
        status=HTTPStatus.CREATED, step_name="Повторно отправить данные ФЛ на создание карточки", schema=EntitySchema
    )
    with step("В ответе поле exists равно true"):
        assert response.exists is True
    with step("ID в ответе идентичен первому"):
        assert response.id == entity_id


@case(id=14881, title="Создание карточки ФЛ. Отличие в одно поле")
@pytest.mark.parametrize("field", Person.class_fields())
def test_create_person_other_value(auth_ola_client, create_person_card, db_client, field):
    """Тест проверяет, что при создании нового ФЛ в данных есть хоть малейшее отличие, то данное ФЛ считается новым"""
    person, entity_id = create_person_card()
    data = person.as_dict()
    del data[field]
    new_person = Person(**data)
    requests = auth_ola_client.entities.post.person.body(new_person)
    response = requests(
        status=HTTPStatus.CREATED,
        step_name="Создать ФЛ с идентичными данными но отличным только 1 полем",
        schema=EntitySchema,
    )
    with step("В ответе поле exists равно false"):
        assert response.exists is False
    with step("ID в ответе не идентичен первому"):
        assert response.id != entity_id
    result = db_client.get_entity_by_id(entity_id=response.id)
    with step(f"Тип карточки: {CardType.PERSON}"):
        assert result["type_code"] == CardType.PERSON
    with step("Все поля в базе соответствуют переданным при создании"):
        for key, value in new_person.items():
            with step(f"Проверить поле: {key}"):
                assert result["data"][key] == value, f"Поле {key} не соответствует переданному значению"
