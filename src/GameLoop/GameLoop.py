import time
from typing import Optional

from APIClient.APIClient import HTTPClientSync
from Action.Action import GameState
from Parser.Parser import Parser
from Action.Action import StrategyChoiceClass

class GameLoop:
    def __init__(self, server_client: HTTPClientSync, controller: Optional[GameState] = None) -> None:
        self.server_client = server_client
        self.controller = controller
        self.running = True
        
    def start(self):
        last_control_update = time.time()
        tic: int = 0
        control_interval = 0.33

        while self.running:
            current_time = time.time()
            if tic == 0:
                data = self.server_client.post()
                if data:
                    self.controller = GameState(data_obj=Parser(data))
                last_server_update = current_time
                tic += 1
            
            if current_time - last_control_update >= control_interval:
                control_answer = StrategyChoiceClass().generate_response_server(self.controller.transports) # TODO: метод для генерации управления, возвращает ответ для сервера
                print(control_answer)
                data = self.server_client.post(data=control_answer)
                self.controller = GameState(data_obj=Parser(data))
                last_control_update = current_time
                tic += 1
                # print(time.time() - last_control_update)
            
            if tic == 10:
                self.stop()
                
            
    def stop(self):
        self.running = False
                