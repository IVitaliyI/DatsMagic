from dataclasses import dataclass
from typing import Union
import networkx as nx

from DataClasses.Anomaly import Anomaly
from DataClasses.Carpet_airplane import EnemyCarpetAirplane, OurCarpetAirplane
from DataClasses.Gold import Gold

class Map:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        # Словарь для хранения объектов по координатам (x, y)
        self.objects = {}
    
    def add_object(self, obj: Union[Anomaly, EnemyCarpetAirplane, OurCarpetAirplane, Gold]):
        self.objects[(obj.x, obj.y)] = obj
        
    def remove_object(self, x: int, y: int):
        if (x, y) in self.objects:
            del self.objects[(x, y)]
    
    def get_object(self, x: int, y: int):
        return self.objects.get((x, y), None)
    
    