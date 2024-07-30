# Auto-generate 2024-03-05 14:57:32 UTC

from ..._meta import MetaCategory
from ..._request import Request

class NegativeGet(MetaCategory):
    @property
    def id_comments(self) -> Request: ...
    @property
    def id_complaints(self) -> Request: ...

class NegativePost(MetaCategory):
    @property
    def id_comment(self) -> Request: ...

class Negatives(MetaCategory):
    @property
    def get(self) -> NegativeGet: ...
    @property
    def post(self) -> NegativePost: ...
