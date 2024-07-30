"""Spark client"""

from .._meta import MetaCategory, category, request
from .._request import Request
from .._session import Session
from .presets import Presets


class AuthSpark(MetaCategory):
    """Ручки авторизации"""

    @request.post("/ifaxwebservice/rest/Authmethod")
    def auth(self) -> Request:
        """Авторизация в СПАРК"""

    @request.post("/ifaxwebservice/rest/End")
    def end(self) -> Request:
        """Разлогин"""


class DataSpark(MetaCategory):
    """Ручки получения данных"""

    @request.post("/ifaxwebservice/rest/GetCompanyExtendedReport")
    def get_company_extended_report(self) -> Request:
        """Получить данные по компании"""

    @request.post("/ifaxwebservice/rest/GetEntrepreneurReport")
    def get_entrepreneur_short_report(self) -> Request:
        """Получить данные по ИП"""


class SparkClient(Session):
    """Клиент для взаимоействия с сервисом СПАРК"""

    auth_data: dict[str, str]

    def set_auth_data(self, login: str, password: str) -> None:
        """Set Auth data"""
        self.auth_data = {"login": login, "password": password}

    @category(AuthSpark)
    def auth(self) -> AuthSpark:
        """Ручки авторизации"""

    @category(DataSpark)
    def data(self) -> DataSpark:
        """Ручки получения данных"""

    @property
    def presets(self) -> Presets:
        """Пресеты"""
        return Presets(self)
