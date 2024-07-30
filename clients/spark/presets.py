"""SPARK Presets"""

from http import HTTPStatus

import allure
from box import Box


class Presets:
    """Presets class"""

    def __init__(self, client) -> None:  # noqa: ANN001
        self._client = client

    def __enter__(self) -> None:
        request = self._client.auth.auth.body(**self._client.auth_data)
        request(HTTPStatus.OK, handler=None)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        self._client.auth.end(HTTPStatus.OK, handler=None)

    @allure.step("Получить данные компании из СПАРКа")
    def get_company_data(self, inn: str) -> Box:
        """Получить данные компании"""
        with self:
            request = self._client.data.get_company_extended_report.body(inn=inn)
            response = request(HTTPStatus.OK)
        return response

    @allure.step("Получить данные ИП из СПАРКа")
    def get_ip_data(self, inn: str) -> Box:
        """Получить данные ИП"""
        with self:
            request = self._client.data.get_entrepreneur_short_report.body(inn=inn)
            response = request(HTTPStatus.OK)
        return response
