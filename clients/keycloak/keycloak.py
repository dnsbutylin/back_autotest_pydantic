"""Keycloak Client"""

from .._meta import MetaCategory, request
from .._request import Request
from .._session import Session
from .presets import Presets


class KeycloakGet(MetaCategory):
    """Get запросы"""

    @request.get("/auth/realms/{realm}")
    def realm_info(self) -> Request:
        """Get realm info"""

    @request.get("/auth/realms/{realm}/protocol/openid-connect/certs")
    def realm_certs(self) -> Request:
        """Get realm certs"""


class KeycloakPost(MetaCategory):
    """Post запросы"""

    @request.post("/auth/realms/{realm}/protocol/openid-connect/token")
    def token(self) -> Request:
        """Получение токена"""

    @request.post("/auth/realms/{realm}/protocol/openid-connect/token/introspect")
    def token_introspect(self) -> Request:
        """Introspect access token"""

    @request.post("/auth/realms/{realm}/protocol/openid-connect/userinfo")
    def userinfo(self) -> Request:
        """Get real user info"""


class KeycloakClient(Session):
    """Клиент для взаимодейстия с Keycloak"""

    @property
    def get(self) -> KeycloakGet:
        """GET Requests"""
        return KeycloakGet(self)

    @property
    def post(self) -> KeycloakPost:
        """POST Requests"""
        return KeycloakPost(self)

    @property
    def presets(self) -> Presets:
        """Presets"""
        return Presets(self)
