from abc import ABCMeta, abstractmethod
from typing import Optional

from Parser.Parser import Parser
from DataClasses.Carpet_airplane import OurCarpetAirplane

def generate_response_server(id: str, 
                                acc: tuple[float, float] = (0, 0), 
                                activateShield: bool = False, 
                                attack: tuple[int, int] = None):
    if attack != None:
        response = {
            "transports": {
                "acceleration": {"x": acc[0], "y": acc[1]},
                "activateShield": activateShield,
                "attack": {"x": attack[0], "y": attack[1]},
                "id": id
            }
        }
    else:
        response = {
            "transports": {
                "acceleration": {"x": acc[0], "y": acc[1]},
                "activateShield": activateShield,
                "id": id
            }
        }
    return response

class GameState:
    def __init__(self, data_obj: Parser) -> None:
        self.anomalies = list(data_obj.parse_anomalies())
        self.bounties = list(data_obj.parse_bounties())
        self.constants = data_obj.parse_constants()
        self.enemies = list(data_obj.parse_enemies())
        self.transports = list(data_obj.parse_transports())
        self.wanted_list = list(data_obj.parse_wanted_list())
    
class GameStateForOneTransport(GameState):
    def __init__(self, transport: OurCarpetAirplane) -> None:
        self.see_bounties = []
        # Необходимо один раз пройтись по bounties и классифицировать к какому ковру относятся те или иные монеты
        # Тоже самое можно сделать и с врагами