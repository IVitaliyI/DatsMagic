# import time
# import requests
from dotenv import load_dotenv
import os
import time
import asyncio

from APIClient.APIClient import HTTPClient

load_dotenv()
TOKEN: str = os.getenv("TOKEN")
BASE_URL_TEST: str = 'http://localhost:8000'
BASE_URL_OSN: str = 'http://localhost:8000'

async def main():
    start_time = time.time()
    client: HTTPClient = HTTPClient(BASE_URL, {"Authorization" : TOKEN})
    requests: list[dict] = [{"method": "GET",
                       "endpoint": "/data", "params": {"id": 1}},
                      {"method": "POST",
                       "endpoint": "/update", "data": {"id": 1, "value": "new"}}]
    responses = await client.bulk_request(requests=requests)


if __name__ == "__main__":
    asyncio.run(main()) # расскоментировать при начале работы
