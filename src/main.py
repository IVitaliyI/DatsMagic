from dotenv import load_dotenv
import os
import time
import json
from Utils.Utils import DataSaver
from APIClient.APIClient import HTTPClientSync
from DataClasses.Map import Map
from Parser.Parser import Parser
from Graphics.Visualizator import Visualizator

load_dotenv()
TOKEN = os.getenv('TOKEN')
BASE_URL_TEST = 'https://games-test.datsteam.dev/'
BASE_URL_OSN = 'https://games.datsteam.dev/'
headers = {"X-Auth-Token": TOKEN}

def main():
    print("Запуск main функции")  # Отладочный принт
    start_time = time.time()
    client = HTTPClientSync(BASE_URL_TEST)
    visualizer = Visualizator()
    
    while True:
        get_data = client.get(headers=headers)
        data_obj = Parser(get_data)
        game_map = generate_game_state(data_obj)
        visualizer.visualize_objects(game_map.objects)
        
        saver = DataSaver()
        saver.create_output_folder()
        saver.save_to_file('test1', get_data)
        post_data = client.post(headers=headers)
        saver.save_to_file('post', post_data)
        time.sleep(2)

def generate_game_state(data_obj: Parser) -> Map:
    CONSTANTS = data_obj.parse_constants()
    gameMap = Map(CONSTANTS.mapSizeX, CONSTANTS.mapSizeY)
    [gameMap.add_object(obj) for obj in data_obj.parse_anomalies()]
    [gameMap.add_object(obj) for obj in data_obj.parse_enemies()]
    [gameMap.add_object(obj) for obj in data_obj.parse_transports()]
    [gameMap.add_object(obj) for obj in data_obj.parse_bounties()]
<<<<<<< HEAD
    print(gameMap)  # Отладочный принт
    return gameMap
=======
    # map(gameMap.add_object, data_obj.parse_anomalies())
>>>>>>> 2dbb69b643e0ebd3d77f966ba5a3285e97d886a1

def test():
    print("Запуск test функции")  # Отладочный принт
    with open(r'C:\Users\kiril\Desktop\hacaton\DatsMagic\buf\round3\session_2024-10-11_21-25-42\post', 'r') as f:
        data_obj = Parser(json.load(f))
        game_map = generate_game_state(data_obj=data_obj)
        visualizer = Visualizator()
        visualizer.visualize_objects(game_map.objects)

if __name__ == "__main__":
    print("Запуск программы")  # Отладочный принт
    test()