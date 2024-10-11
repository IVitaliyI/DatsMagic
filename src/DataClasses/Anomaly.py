from dataclasses import dataclass

@dataclass
class Anomaly:
    x: int
    y: int
    velX : float
    velY: float
    R1: int
    R2: int
    strength: int
    
    
    