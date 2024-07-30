"""Раздел companies"""

from ..._meta import MetaCategory, category, request
from ..._request import Request


class CompaniesGet(MetaCategory):
    """GET"""

    @request.get("/companies/{id}/contacts")
    def id_contacts(self) -> Request:
        """Получение списка контактых лиц организации"""


class Companies(MetaCategory):
    """Раздел companies"""

    @category(CompaniesGet)
    def get(self) -> CompaniesGet:
        """GET"""
