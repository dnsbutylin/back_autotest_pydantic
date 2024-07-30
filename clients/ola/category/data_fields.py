"""Раздел data-fields"""

from ..._meta import MetaCategory, category, request
from ..._request import Request


class DataFieldsPost(MetaCategory):
    """POST"""

    @request.post("/data-fields/{id}/comment")
    def id_comment(self) -> Request:
        """Добавить комментарий к Data Field"""


class DataFields(MetaCategory):
    """Раздел data-fields"""

    @category(DataFieldsPost)
    def post(self) -> DataFieldsPost:
        """POST"""
