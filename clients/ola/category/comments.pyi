# Auto-generate 2024-03-05 14:57:32 UTC

from ..._meta import MetaCategory
from ..._request import Request

class CommentsPost(MetaCategory):
    @property
    def id_reaction(self) -> Request: ...

class Comments(MetaCategory):
    @property
    def post(self) -> CommentsPost: ...
