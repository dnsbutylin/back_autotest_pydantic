# Auto-generate 2024-03-05 14:57:32 UTC

from ..._meta import MetaCategory
from ..._request import Request

class ComplainsPost(MetaCategory):
    @property
    def complaints(self) -> Request: ...

class Complaints(MetaCategory):
    @property
    def post(self) -> ComplainsPost: ...
