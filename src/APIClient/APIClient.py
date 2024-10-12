import aiohttp
import asyncio
from typing import Optional, Union

import requests
import json
from Utils.Utils import Logger


class HTTPClientAsync:
    def __init__(self, base_url: str, headers: Optional[dict] = None) -> None:
        self.base_url = base_url
        self.headers = headers or {}

    async def _get(
        self,
        session: aiohttp.ClientSession,
        endpoint: str,
        params: Optional[dict] = None,
    ):
        url = self.base_url + endpoint
        async with session.get(url, params=params) as response:
            response.raise_for_status()
        return await response.json()

    async def _post(
        self,
        session: aiohttp.ClientSession,
        endpoint: str,
        data: Optional[dict] = None
    ):
        url = self.base_url + endpoint
        async with session.post(url, json=data) as response:
            response.raise_for_status()
            return await response.json()

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ):
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                if method.upper() == "GET":
                    return await self._get(session, endpoint, params)
                elif method.upper() == "POST":
                    return await self._post(session, endpoint, data)
                else:
                    ValueError(f"Unsupported method: {method}")
        except aiohttp.ClientError as e:
            Logger.log_error(f"Request to {endpoint} failed: {str(e)}")

    async def bulk_request(self,
                           requests: list[dict[str, Union[str, dict]]]):
        """
        Асинхронное выполнение нескольких запросов (GET или POST).
        requests: список запросов вида [{"method": "GET",
        "endpoint": "/path", "params": {...}}, {...}]
        """
        tasks = []
        async with aiohttp.ClientSession(headers=self.headers) as session:
            for req in requests:
                method = req.get("method", "GET").upper()
                endpoint = req.get("endpoint")
                params = req.get("params", {})
                data = req.get("data", {})

                if method == "GET":
                    tasks.append(self._get(session, endpoint, params))
                elif method == "POST":
                    tasks.append(self._post(session, endpoint, data))

            responses = await asyncio.gather(*tasks)
        return responses

class HTTPClientSync:
    def __init__(self, base_url, headers):
        """Инициализация клиента с базовым URL сервера."""
        self.base_url = base_url
        self.headers = headers
        self.session = requests.Session()  # Создание сессии для повторного использования соединений

    def get(self, params=None):
        """
        Выполняем GET-запрос к серверу.

        :param endpoint: Точка доступа (например, '/game/state').
        :param params: Параметры запроса (если есть).
        :param headers: Заголовки запроса (если нужны).
        :return: Ответ сервера в формате JSON или None в случае ошибки.
        """
        endpoint: str = 'rounds/magcarp'
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params, headers=self.headers)
            response.raise_for_status()  # Проверяем успешность ответа (статус 200)
            return response.json()  # Предполагаем, что сервер возвращает JSON
        except requests.RequestException as e:
            print(f"Ошибка при выполнении GET-запроса: {e}")
            return None

    def post(self, data=None):
        """
        Выполняем POST-запрос к серверу.

        :param endpoint: Точка доступа (например, '/game/action').
        :param data: Данные для отправки в формате JSON (или другом).
        :param headers: Заголовки запроса (если нужны).
        :return: Ответ сервера в формате JSON или None в случае ошибки.
        """
        
        endpoint: str = 'play/magcarp/player/move'
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.post(url, json=data, headers=self.headers)
            response.raise_for_status()  # Проверяем успешность ответа (статус 200)
            return response.json()  # Предполагаем, что сервер возвращает JSON
        except requests.RequestException as e:
            print(f"Ошибка при выполнении POST-запроса: {e}")
            return None

    def close(self):
        """Закрываем сессию при завершении работы."""
        self.session.close()
