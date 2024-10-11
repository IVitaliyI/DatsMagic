import networkx as nx
import enum

from dataclasses import dataclass

@dataclass
class CarpetAirplane:
    velocity: int
    anomalyAcceleration: int
    selfAcceleration: int
    health: int
    shieldCooldownMs: int
    shieldLeftMs: int
    attackCooldownMs: int
    deathCount: int
    id: int
    status: int
    flag: str = 'Enemy'