"""Раздел complaints"""

from ..._meta import MetaCategory, category, request
from ..._request import Request


class ComplainsPost(MetaCategory):
    """POST"""

    @request.post("/complaints")
    def complaints(self) -> Request:
        """Добавить голоса к негативам в карточке"""


class Complaints(MetaCategory):
    """Раздел complaints"""

    @category(ComplainsPost)
    def post(self) -> ComplainsPost:
        """POST"""
