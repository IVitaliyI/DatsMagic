from dataclasses import dataclass

class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

@dataclass
class WantedList:
    x: int
    y: int
    health: int
    killBounty: int
    shieldLeftMs: int
    status: str
    velX: int
    velY: int
    

@dataclass
class Constants(metaclass=MetaSingleton):
    maxAccel: int
    maxSpeed: int
    mapSizeX: int
    mapSizeY: int
    transportRadius: int
    wantedList: WantedList
    reviveTimeoutSec: int
    name: str
    points: int
    shieldCooldownMs: int
    shieldTimeMs: int
    attackDamage: int
    attackCooldownMs: int
    attackExplosionRadius: int
    attackRange: int

