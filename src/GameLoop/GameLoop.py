import time
from typing import Optional

from APIClient.APIClient import HTTPClientSync
from Action.Action import GameState
from Parser.Parser import Parser
from Action.Action import StrategyChoiceClass, MaxValuePerDistanceStrategy

from Graphics.Visualizator import Visualizator

class GameLoop:
    def __init__(self, server_client: HTTPClientSync, controller: Optional[GameState] = None, vizualizer: bool = False) -> None:
        self.server_client = server_client
        self.controller = controller
        self.running = True
        self.vizualizer = vizualizer
        
    def start(self):
        last_control_update = time.time()
        tic: int = 0
        control_interval = 0.33
        if self.vizualizer:    
            viz = Visualizator()

        while self.running:
            current_time = time.time()
            if tic == 0:
                data = self.server_client.post()
                if data:
                    buf_viz = Parser(data)
                    self.controller = GameState(data_obj=buf_viz)
                last_server_update = current_time
                tic += 1
            
            if current_time - last_control_update >= control_interval:
                control_answer = StrategyChoiceClass(MaxValuePerDistanceStrategy()).generate_response_server(self.controller.transports,
                                                                                self.controller.anomalies,
                                                                                self.controller.bounties,
                                                                                self.controller.enemies) # TODO: метод для генерации управления, возвращает ответ для сервера
                data = self.server_client.post(data=control_answer)
                buf_viz = Parser(data)
                self.controller = GameState(data_obj=buf_viz)
                last_control_update = current_time
                tic += 1
                # print(time.time() - last_control_update)
            
            if self.vizualizer:
                viz.visualize_objects(Visualizator.generate_game_state(buf_viz))
                
            # if tic == 10:
            #     self.stop()
                
            
    def stop(self):
        self.running = False
                