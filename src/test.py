import json
import os
import time
from Parser.Parser import Parser
from Graphics.Visualizator import Visualizator
from main import generate_game_state


def main():
    for root, dirs, files in os.walk('C:/Users/kiril/Desktop/hacaton/DatsMagic/buf/round3'):
        for index, file in enumerate(files):
            if index % 2 == 0:  # Проверяем, является ли индекс четным
                file_path = os.path.join(root, file)
                print(file_path)
                with open(file_path, 'r') as f:
                    data_obj = Parser(json.load(f))
                    game_map = generate_game_state(data_obj=data_obj)
                    visualizer = Visualizator()
                    visualizer.visualize_objects(game_map.objects)
                    print('boom')
                    time.sleep(1)
                
if __name__ == "__main__":
    print("Запуск программы")  # Отладочный принт
    main()