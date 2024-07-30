# Auto-generate 2024-03-05 14:57:32 UTC

from ..._meta import MetaCategory
from ..._request import Request

class CompaniesGet(MetaCategory):
    @property
    def id_contacts(self) -> Request: ...

class Companies(MetaCategory):
    @property
    def get(self) -> CompaniesGet: ...
