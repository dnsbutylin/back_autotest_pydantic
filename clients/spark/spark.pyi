# Auto-generate 2024-03-05 10:26:51 UTC

from .._meta import MetaCategory
from .._request import Request
from .._session import Session
from .presets import Presets

class AuthSpark(MetaCategory):
    @property
    def auth(self) -> Request: ...
    @property
    def end(self) -> Request: ...

class DataSpark(MetaCategory):
    @property
    def get_company_extended_report(self) -> Request: ...
    @property
    def get_entrepreneur_short_report(self) -> Request: ...

class SparkClient(Session):

    auth_data: dict[str, str]

    def set_auth_data(self, login: str, password: str) -> None: ...
    @property
    def auth(self) -> AuthSpark: ...
    @property
    def data(self) -> DataSpark: ...
    @property
    def presets(self) -> Presets: ...
