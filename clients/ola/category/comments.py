"""Раздел comments"""

from ..._meta import MetaCategory, category, request
from ..._request import Request


class CommentsPost(MetaCategory):
    """POST"""

    @request.post("/comments/{id}/reaction")
    def id_reaction(self) -> Request:
        """Реакция на комментарий"""


class Comments(MetaCategory):
    """Раздел comments"""

    @category(CommentsPost)
    def post(self) -> CommentsPost:
        """POST"""
