from abc import ABCMeta, abstractmethod
from typing import Optional
import json

from Parser.Parser import Parser
from DataClasses.Carpet_airplane import OurCarpetAirplane
from DataClasses.Gold import Gold

from Utils.Utils import DataSaver

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
        self.data: Parser = data_obj
        self.transports = list(data_obj.parse_transports())
        self.anomalies = self.parse_anomaly_view_transport()
        self.bounties = self.parse_bounderies_view_transport()
        self.constants = data_obj.parse_constants()
        # self.enemies = list(data_obj.parse_enemies())
        self.wanted_list = self.parse_wanted_list_view_transport()
        self.enemies = self.parse_enemies_view_transport()
    
    def parse_bounderies_view_transport(self):
        transport_bounties_view: dict[tuple[int,int], list[Gold]] = {}
        for bount in self.data.parse_bounties():
            for transport in self.transports:
                if transport.id not in transport_bounties_view:
                    transport_bounties_view[transport.id] = []
                if transport.classification((bount.x, bount.y)):
                    transport_bounties_view[transport.id].append(bount)
        return transport_bounties_view
    
    def parse_enemies_view_transport(self):
        transport_enemies_view: dict[tuple[int,int], list[Gold]] = {}
        for bount in self.data.parse_enemies():
            for transport in self.transports:
                if transport.id not in transport_enemies_view:
                    transport_enemies_view[transport.id] = []
                if transport.classification((bount.x, bount.y)):
                    transport_enemies_view[transport.id].append(bount)
        return transport_enemies_view
    
    def parse_anomaly_view_transport(self):
        transport_anomaly_view: dict[tuple[int,int], list[Gold]] = {}
        for bount in self.data.parse_anomalies():
            for transport in self.transports:
                if transport.id not in transport_anomaly_view:
                    transport_anomaly_view[transport.id] = []
                if transport.classification((bount.x, bount.y)):
                    transport_anomaly_view[transport.id].append(bount)
        return transport_anomaly_view
    
    def parse_wanted_list_view_transport(self):
        transport_wanted_view: dict[tuple[int,int], list[Gold]] = {}
        for bount in self.data.parse_wanted_list():
            for transport in self.transports:
                if transport.id not in transport_wanted_view:
                    transport_wanted_view[transport.id] = []
                if transport.classification((bount.x, bount.y)):
                    transport_wanted_view[transport.id].append(bount)
        return transport_wanted_view
        
    
        
class GameStateForOneTransport(GameState):
    def __init__(self, transport: OurCarpetAirplane) -> None:
        self.see_bounties = []
        # Необходимо один раз пройтись по bounties и классифицировать к какому ковру относятся те или иные монеты
        # Тоже самое можно сделать и с врагами