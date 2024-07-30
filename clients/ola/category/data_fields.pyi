# Auto-generate 2024-03-05 14:57:32 UTC

from ..._meta import MetaCategory
from ..._request import Request

class DataFieldsPost(MetaCategory):
    @property
    def id_comment(self) -> Request: ...

class DataFields(MetaCategory):
    @property
    def post(self) -> DataFieldsPost: ...
