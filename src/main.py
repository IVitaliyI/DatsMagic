# import time
# import requests
from dotenv import load_dotenv
import os
import time
import json

from Utils.Utils import DataSaver
from APIClient.APIClient import HTTPClientSync
from DataClasses.Map import Map 
# from Graphics.PrintMap import print_map, generate_random_array, draw_array


from Parser.Parser import Parser

load_dotenv()
TOKEN: str = os.getenv('TOKEN')
BASE_URL_TEST: str = 'https://games-test.datsteam.dev/'
BASE_URL_OSN: str = 'https://games.datsteam.dev/'
headers: dict = {"X-Auth-Token" : TOKEN}



def main():
    start_time = time.time()
    client: HTTPClientSync = HTTPClientSync(BASE_URL_TEST)
    while True:
        get_data = client.get(headers=headers)
        saver = DataSaver()
        saver.create_output_folder()
        saver.save_to_file('test1', get_data)
        post_data = client.post(headers=headers)
        saver.save_to_file('post', post_data)
        time.sleep(2)
    # print_map()
    

def generate_game_state(data_obj: Parser) -> Map:
    CONSTANTS = data_obj.parse_constants()
    gameMap: Map = Map(CONSTANTS.mapSizeX, CONSTANTS.mapSizeY) 
    # print(list(data_obj.parse_anomalies()))
    [gameMap.add_object(obj) for obj in data_obj.parse_anomalies()]
    [gameMap.add_object(obj) for obj in data_obj.parse_enemies()]
    [gameMap.add_object(obj) for obj in data_obj.parse_transports()]
    [gameMap.add_object(obj) for obj in data_obj.parse_bounties()]
    # map(gameMap.add_object, data_obj.parse_anomalies())

def test():
    with open('./buf/session_2024-10-11_21-01-45/post', 'r') as f:
        data_obj = Parser(json.load(f))
        generate_game_state(data_obj=data_obj)

if __name__ == "__main__":
    # main() # расскоментировать при начале работы
    test()