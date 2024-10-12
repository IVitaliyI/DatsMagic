from dotenv import load_dotenv
import os

from GameLoop.GameLoop import GameLoop
from APIClient.APIClient import HTTPClientSync

load_dotenv()
TOKEN = os.getenv('TOKEN')
BASE_URL_TEST = 'https://games-test.datsteam.dev/'
BASE_URL_OSN = 'https://games.datsteam.dev/'
headers = {"X-Auth-Token": TOKEN}

def main():
    server = HTTPClientSync(BASE_URL_TEST, headers=headers)
    game = GameLoop(server_client=server, vizualizer=True)
    try:
        game.start()
    except KeyboardInterrupt:
        game.stop()

if __name__ == "__main__":
    main()