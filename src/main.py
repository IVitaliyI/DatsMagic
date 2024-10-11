# import time
# import requests
from dotenv import load_dotenv
import os
import time
import asyncio

from APIClient.APIClient import HTTPClient

load_dotenv()
TOKEN: str = os.getenv("TOKEN")
BASE_URL: str = 'example.com'

async def main():
    start_time = time.time()
    client: HTTPClient = HTTPClient(BASE_URL, {"Authorization" : TOKEN})
    requests: list[dict[str, str]] = [{"method": "GET",
                       "endpoint": "/data", "params": {"id": 1}},
                      {"method": "POST",
                       "endpoint": "/update", "data": {"id": 1, "value": "new"}}]
    responses = await client.bulk_request(requests=requests)


if __name__ == "__main__":
    print("Hello world!")
    # asyncio.run(main())
