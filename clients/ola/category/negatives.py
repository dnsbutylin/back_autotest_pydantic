"""Раздел negatives"""

from ..._meta import MetaCategory, category, request
from ..._request import Request


class NegativeGet(MetaCategory):
    """GET"""

    @request.get("/negatives/{id}/comments")
    def id_comments(self) -> Request:
        """Получить комментарии к негативу"""

    @request.get("/negatives/{id}/complaints")
    def id_complaints(self) -> Request:
        """Получить жалобы к негативу"""


class NegativePost(MetaCategory):
    """POST"""

    @request.post("/negatives/{id}/comment")
    def id_comment(self) -> Request:
        """Добавить комментарий к негативу"""


class Negatives(MetaCategory):
    """Раздел negatives"""

    @category(NegativeGet)
    def get(self) -> NegativeGet:
        """GET"""

    @category(NegativePost)
    def post(self) -> NegativePost:
        """POST"""
