# import time
# import requests
from dotenv import load_dotenv
import os
import time

from APIClient.APIClient import HTTPClientSync

load_dotenv()
TOKEN: str = os.getenv("TOKEN")
BASE_URL_TEST: str = 'https://games-test.datsteam.dev/'
BASE_URL_OSN: str = 'https://games.datsteam.dev/'
headers: dict = {"TOKEN" : TOKEN}



def main():
    start_time = time.time()
    client: HTTPClientSync = HTTPClientSync(BASE_URL_TEST)
    data = client.get(headers=headers)
    print(data)
    


if __name__ == "__main__":
    main() # расскоментировать при начале работы
