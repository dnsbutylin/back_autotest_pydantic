"""Раздел entities"""

from ..._meta import MetaCategory, category, request
from ..._request import Request


class EntitiesPost(MetaCategory):
    """POST Entities"""

    @request.post("/entities/person")
    def person(self) -> Request:
        """Создание карточки физического лица"""

    @request.post("/entities/legal-entity")
    def legal_entity(self) -> Request:
        """Создание карточки юридического лица"""

    @request.post("/entities/leasing-object")
    def leasing_object(self) -> Request:
        """Создание карточки объекта лизинга"""

    @request.post("/entities/{id}/comment")
    def id_comment(self) -> Request:
        """Добавление комментария к карточке"""

    @request.post("/entities/{id}/data-field")
    def id_data_field(self) -> Request:
        """Добавление карточке Data Field и комментария"""


class EntitiesGet(MetaCategory):
    """GET Entities"""

    @request.get("/entities/{id}/negatives")
    def id_negatives(self) -> Request:
        """Получить негативы к карточке"""

    @request.get("/entities/person/{id}")
    def person_id(self) -> Request:
        """Получить карточку физического лица по ID"""

    @request.get("/entities/legal-entity/{id}")
    def legal_entity_id(self) -> Request:
        """Получить карточку юридического лица по ID"""

    @request.get("/entities/leasing-object/{id}")
    def leasing_object_id(self) -> Request:
        """Получить карточку объекта лизинга по ID"""

    @request.get("/entities/person")
    def person(self) -> Request:
        """Поиск карточки физического лица по полям"""

    @request.get("/entities/legal-entity")
    def legal_entity(self) -> Request:
        """Поиск карточки юридического лица по полям"""

    @request.get("/entities/leasing-object")
    def leasing_object(self) -> Request:
        """Поиск карточки объекта лизинга по полям"""

    @request.get("/entities/visits/history")
    def visits_history(self) -> Request:
        """Получение истории посещенных карточек"""


class Entities(MetaCategory):
    """Раздел Entities"""

    @category(EntitiesPost)
    def post(self) -> EntitiesPost:
        """POST Entities"""

    @category(EntitiesGet)
    def get(self) -> EntitiesGet:
        """GET Entities"""
