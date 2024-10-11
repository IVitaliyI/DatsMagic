import networkx as nx
import enum

from dataclasses import dataclass

class Status(enum.Enum):
    alive: 0
    dead: 1

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