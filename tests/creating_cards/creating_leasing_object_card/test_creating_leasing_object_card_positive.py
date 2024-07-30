from http import HTTPStatus

import pytest

from src.cases import case, step
from src.constants import CardType, FieldsLength, LeasingObjectType
from src.generators import LeasingObject, LeasingObjectIdentifier, fake, ru_letter
from src.schemas import EntitySchema

# mypy: disable_error_code=union-attr


@pytest.fixture
def check_db(db_client):
    """Проверить в базе, что данные соответствуют переданным"""

    def _call(entity_id: str, leasing_object: LeasingObject) -> None:
        result = db_client.get_entity_by_id(entity_id=entity_id)
        with step(f"Тип карточки: {CardType.LEASING_OBJECT}"):
            assert result["type_code"] == CardType.LEASING_OBJECT
        with step("Все поля в базе соответствуют переданным при создании"):
            with step("Поле title соответствует переданному"):
                assert result["data"]["title"] == leasing_object.title
            with step("Поле identifier соответствует переданному"):
                assert result["data"]["identifier"] == leasing_object.identifier.value
            with step("Поле identifier_type соответствует переданному"):
                assert result["data"]["identifier_type"] == leasing_object.identifier.type
        db_client.removed_entity_by_id(entity_id)

    return _call


@case(id=14904, title="Создание карточки ОЛ")
def test_creating_leasing_object_card(auth_ola_client, check_db):
    leasing_object = LeasingObject()
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(HTTPStatus.CREATED, step_name="Создать карточку ОЛ", schema=EntitySchema)
    with step("В ответе поле exists равно false"):
        assert response.exists is False
    check_db(entity_id=response.id, leasing_object=leasing_object)


@case(id=14905, title="Создание карточки ОЛ. Все доступные типы объектов лизинга")
@pytest.mark.parametrize("leasing_type", LeasingObjectType.as_tuple())
def test_creating_leasing_object_card_all_types(auth_ola_client, check_db, leasing_type):
    leasing_object = LeasingObject(identifier=LeasingObjectIdentifier(type=leasing_type))
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(HTTPStatus.CREATED, step_name="Создать карточку ОЛ", schema=EntitySchema)
    with step("В ответе поле exists равно false"):
        assert response.exists is False
    check_db(entity_id=response.id, leasing_object=leasing_object)


@pytest.mark.parametrize("length", (FieldsLength.MIN_LENGTH, 200, 10000))
@case(id=14911, title="Создание карточки ОЛ. Нет ограничения на длину поля title")
def test_creating_leasing_object_card_title_length(auth_ola_client, check_db, length):
    leasing_object = LeasingObject(title=ru_letter() * length)
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(status=HTTPStatus.CREATED, step_name="Создать карточку ОЛ", schema=EntitySchema)
    with step("В ответе поле exists равно false"):
        assert response.exists is False
    check_db(entity_id=response.id, leasing_object=leasing_object)


@pytest.mark.parametrize("length", (FieldsLength.MIN_LENGTH, 200, 10000))
@case(id=14912, title="Создание карточки ОЛ. Нет ограничения на длину поля identifier.value")
def test_creating_leasing_object_card_identifier_value_length(auth_ola_client, check_db, length):
    leasing_object = LeasingObject(identifier=LeasingObjectIdentifier(value=ru_letter() * length))
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(status=HTTPStatus.CREATED, step_name="Создать карточку ОЛ", schema=EntitySchema)
    with step("В ответе поле exists равно false"):
        assert response.exists is False
    check_db(entity_id=response.id, leasing_object=leasing_object)


@pytest.mark.parametrize("field", ("title", "identifier.value"))
@pytest.mark.parametrize("symbol", ("qwe ewq", "#$%@", "-- DROP TABLE public.entities", "異體字", "😁🤘∌"))
@case(id=14913, title="Создание карточки ОЛ. Нет ограничения на символы")
def test_creating_leasing_object_card_any_symbols(auth_ola_client, field, symbol, check_db):
    value = f"{fake.word()} {symbol}"
    leasing_object = (
        LeasingObject(title=value)
        if field == "title"
        else LeasingObject(identifier=LeasingObjectIdentifier(value=value))
    )
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(status=HTTPStatus.CREATED, step_name="Создать карточку ОЛ", schema=EntitySchema)
    with step("В ответе поле exists равно false"):
        assert response.exists is False
    check_db(entity_id=response.id, leasing_object=leasing_object)


@case(id=14914, title="Создание карточки ОЛ. Создание уже существующего ОЛ")
def test_double_creating_leasing_object_card(auth_ola_client, create_leasing_object_card):
    """Тест проверяет, что при попытке создать ОЛ которое уже есть в системе ему вернутся данные которые уже заведены"""
    leasing_object, entity_id = create_leasing_object_card
    request = auth_ola_client.entities.post.leasing_object.body(leasing_object)
    response = request(HTTPStatus.CREATED, step_name="Повторно отправить данные ОЛ на создание", schema=EntitySchema)
    with step("В ответе поле exists равно true"):
        assert response.exists is True
    with step("ID в ответе идентичен первому"):
        assert response.id == entity_id
