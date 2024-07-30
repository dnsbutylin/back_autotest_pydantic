from http import HTTPStatus

import pytest

from src.cases import case, step
from src.constants import CardType, LEType, LegalEntityCardRequiredField
from src.generators import LegalEntity
from src.schemas import EntitySchema


@pytest.mark.parametrize("le_type", LEType.as_tuple())
@case(id=14882, title="Создание карточки ЮЛ")
def test_creating_legal_entity_card(auth_ola_client, db_client, legal_entity_data, le_type):
    """Тест проверяет успешное создание карточек ЮЛ (ЮЛ и ИП)"""
    data = legal_entity_data(le_type)
    request = auth_ola_client.entities.post.legal_entity.body(data)
    response = request(HTTPStatus.CREATED, step_name="Создать карточку ЮЛ", schema=EntitySchema)
    with step("В ответе поле exists равно false"):
        assert response.exists is False
    result = db_client.get_entity_by_id(entity_id=response.id)
    with step(f"Тип карточки: {CardType.LEGAL_ENTITY}"):
        assert result["type_code"] == CardType.LEGAL_ENTITY
    with step("Все поля в базе соответствуют переданным при создании"):
        for key, value in data.items():
            with step(f"Проверить поле: {key}"):
                assert result["data"][key] == value, f"Поле {key} не соответствует переданному значению"


@pytest.mark.parametrize("le_type", LEType.as_tuple())
@case(id=14886, title="Создание карточки ЮЛ. Создание уже существующего ЮЛ")
def test_double_creating_legal_entity_card(auth_ola_client, create_legal_entity, le_type):
    """Тест проверяет, что при попытке создать ЮЛ которое уже есть в системе ему вернутся данные которые уже заведены"""
    legal_entity, entity_id = create_legal_entity(le_type)
    request = auth_ola_client.entities.post.legal_entity.body(legal_entity)
    response = request(
        status=HTTPStatus.CREATED,
        step_name="Повторно отправить данные ЮЛ на создание карточки",
        schema=EntitySchema,
    )
    with step("В ответе поле exists равно true"):
        assert response.exists is True
    with step("ID в ответе идентичен первому"):
        assert response.id == entity_id


@pytest.mark.parametrize("le_type", LEType.as_tuple())
@pytest.mark.parametrize(
    "field",
    (i for i in LegalEntity.class_fields() if i not in LegalEntityCardRequiredField.as_tuple()),
)
@case(id=14898, title="Создание карточки ЮЛ. Не передаем опциональные поля")
def test_creating_legal_entity_card_not_optional_field(auth_ola_client, legal_entity_data, db_client, field, le_type):
    """
    Тест проверяет, что если в запросе отправить только ИНН то ФЛ успешно создастся, а ОГРН автоматически подтянется
    """
    le_data = legal_entity_data(le_type)
    new_legal_entity = le_data.as_dict()
    del new_legal_entity[field]
    request = auth_ola_client.entities.post.legal_entity.body(**new_legal_entity)
    response = request(
        status=HTTPStatus.CREATED,
        step_name="Отправить запрос на создание ЮЛ без опционального поля",
        schema=EntitySchema,
    )
    with step("В ответе поле exists равно false"):
        assert response.exists is False
    result = db_client.get_entity_by_id(entity_id=response.id)
    with step(f"Тип карточки: {CardType.LEGAL_ENTITY}"):
        assert result["type_code"] == CardType.LEGAL_ENTITY
    with step("Поле inn соответствует переданному"):
        assert le_data.inn == result["data"]["inn"]
    with step("Поле ogrn соответствует ожидаемому"):
        assert le_data.ogrn == result["data"]["ogrn"]
