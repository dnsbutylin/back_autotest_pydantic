# Auto-generate 2024-03-05 14:57:32 UTC

from .._meta import MetaCategory
from .._request import Request
from .._session import Session
from .presets import Presets

class KeycloakGet(MetaCategory):
    @property
    def realm_info(self) -> Request: ...
    @property
    def realm_certs(self) -> Request: ...

class KeycloakPost(MetaCategory):
    @property
    def token(self) -> Request: ...
    @property
    def token_introspect(self) -> Request: ...
    @property
    def userinfo(self) -> Request: ...

class KeycloakClient(Session):
    @property
    def get(self) -> KeycloakGet: ...
    @property
    def post(self) -> KeycloakPost: ...
    @property
    def presets(self) -> Presets: ...
