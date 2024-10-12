import json
import os
import time
from Parser.Parser import Parser
from Graphics.Visualizator import Visualizator
from DataClasses.Map import Map

def generate_game_state(data_obj: Parser) -> Map:
    CONSTANTS = data_obj.parse_constants()
    gameMap = Map(CONSTANTS.mapSizeX, CONSTANTS.mapSizeY)
    [gameMap.add_object(obj) for obj in data_obj.parse_anomalies()]
    [gameMap.add_object(obj) for obj in data_obj.parse_enemies()]
    [gameMap.add_object(obj) for obj in data_obj.parse_transports()]
    [gameMap.add_object(obj) for obj in data_obj.parse_bounties()]
    print(gameMap)
    return gameMap

def main():
    visualizer = Visualizator()
    for root, dirs, files in os.walk('./buf/round3'):
        for index, file in enumerate(files):
            if index % 2 == 0:  # Проверяем, является ли индекс четным
                file_path = os.path.join(root, file)
                print(file_path)
                with open(file_path, 'r') as f:
                    data_obj = Parser(json.load(f))
                    game_map = generate_game_state(data_obj=data_obj)
                    visualizer.visualize_objects(game_map.objects)
                    time.sleep(1)
                
if __name__ == "__main__":
    print("Запуск программы")  # Отладочный принт
    main()