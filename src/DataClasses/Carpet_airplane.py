import networkx as nx
import enum

from dataclasses import dataclass
from math import sqrt

from DataClasses.Constants import Constants

@dataclass
class OurCarpetAirplane:
    x: int
    y: int
    velX: float
    velY: float
    anomalyAccelerationX: float
    anomalyAccelerationY: float
    selfAccelerationX: float
    selfAccelerationY: float
    health: int
    shieldCooldownMs: int
    shieldLeftMs: int
    attackCooldownMs: int
    deathCount: int
    id: str
    status: str
    
    def euclidean_distance(self, coord: tuple[int, int]):
        return sqrt((self.x - coord[0]) ** 2 + (self.y - coord[0]) ** 2)

    def classification(self, coord: tuple[int, int]):
        if abs(self.x - coord[0]) <= 350 and abs(self.y - coord[1]) <= 350:
            return True
        return False
    
@dataclass
class EnemyCarpetAirplane:
    x: int
    y: int
    velX: float
    velY: float
    health: int
    shieldLeftMs: int
    status: str