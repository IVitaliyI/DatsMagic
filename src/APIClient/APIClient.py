import aiohttp
import asyncio
from typing import Optional, Union

from Utils.Utils import Logger


class HTTPClient:
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


# async def main():
#     # Инициализация клиента
#     client = HTTPClient(base_url="https://api.example.com",
#                         headers={"Authorization": "Bearer YOUR_TOKEN"})

#     # Пример одиночного GET запроса
#     response = await client.request("GET", "/data", params={"id": 1})
#     print(response)

#     # Пример нескольких запросов
#     requests = [
#         {"method": "GET", "endpoint": "/data", "params": {"id": 1}},
#         {"method": "POST", "endpoint": "/update",
#           "data": {"id": 1, "value": "new"}}
#     ]

#     responses = await client.bulk_request(requests)
#     print(responses)
