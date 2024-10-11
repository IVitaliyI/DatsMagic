import networkx as nx
import enum

from dataclasses import dataclass

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

@dataclass
class EnemyCarpetAirplane:
    x: int
    y: int
    velX: float
    velY: float
    health: int
    shieldLeftMs: int
    status: str