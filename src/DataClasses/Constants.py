from dataclasses import dataclass

class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

@dataclass
class Constants(metaclass=MetaSingleton):
    maxAccel: int
    maxSpeed: int
    mapSize: int
    transportRadius: int
    wantedList: int
    reviveTimeoutSec: int