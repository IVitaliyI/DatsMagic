import json

from DataClasses.Carpet_airplane import OurCarpetAirplane, EnemyCarpetAirplane
from DataClasses.Constants import Constants, WantedList
from DataClasses.Gold import Gold
from DataClasses.Anomaly import Anomaly

class Parser:
    
    def __init__(self, data: json) -> None:
        self.data = json.load(data)
    
    def parse_transports(self):
        for transports in self.data['transports']:
            yield OurCarpetAirplane(x=transports['x'],
                                    y=transports['y'],
                                    velX=transports["velocity"]['x'],
                                    velY=transports["velocity"]['y'],
                                    anomalyAccelerationX=transports['anomalyAcceleration']['x'],
                                    anomalyAccelerationY=transports['anomalyAcceleration']['y'],
                                    selfAccelerationX=transports['selfAcceleration']['x'],
                                    selfAccelerationY=transports['selfAcceleration']['y'],
                                    health=transports['health'],
                                    shieldCooldownMs=transports['shieldCooldownMs'],
                                    shieldLeftMs=transports['shieldLeftMs'],
                                    attackCooldownMs=transports['attackCooldownMs'],
                                    deathCount=transports['deathCount'],
                                    id=transports['id'],
                                    status=transports['status'],
                                    )
    
    def parse_enemies(self):
        for enemies in self.data['enemies']:
            yield EnemyCarpetAirplane(x=enemies['x'],
                                    y=enemies['y'],
                                    velX=enemies["velocity"]['x'],
                                    velY=enemies["velocity"]['y'],
                                    health=enemies['health'],
                                    shieldLeftMs=enemies['shieldLeftMs'],
                                    status=enemies['status'],
                                    )
    
    def parse_wanted_list(self):
        wantedList = self.data['wantedList']
        for wanted in wantedList:
            yield WantedList(x=wanted['x'],
                            y=wanted['y'],
                            health=wanted['health'],
                            shieldLeftMs=wanted['shieldLeftMs'],
                            status=wanted['status'],
                            velX=wanted['velocity']['x'],
                            velY=wanted['velocity']['y'],
                            killBounty=wanted['killBounty']
                            )
    
    def parse_constants(self):
        Constants(mapSizeX=self.data['mapSize']['x'],
                mapSizeX=self.data['mapSize']['y'],
                maxAccel=self.data['maxAccel'],
                maxSpeed=self.data['maxSpeed'],
                reviveTimeoutSec=self.data['reviveTimeoutSec'],
                transportRadius=self.data['transportRadius'],
                name=self.data['name'],
                points=self.data['points'],
                shieldCooldownMs=self.data['shieldCooldownMs'],
                shieldTimeMs=self.data['shieldTimeMs'],
                attackCooldownMs=self.data['attackCooldownMs'],
                attackDamage=self.data['attackDamage'],
                attackExplosionRadius=self.data['attackExplosionRadius'],
                attackRange=self.data['attackRange'])
    
    def parse_bounties(self):
        for gol in self.data['bounties']:
            yield Gold(
                    x=gol['x'],
                    y=gol['y'],
                    R=gol['radius'],
                    value=gol['points']
                )
    
    def parse_annomalies(self):
        for anom in self.data['anomalies']:
            yield Anomaly(
                x=anom['x'],
                y=anom['y'],
                velX=anom['velocity']['x'],
                velY=anom['velocity']['y'],
                strength=anom['strength'],
                R1=anom['radius'],
                R2=anom['effectiveRadius'],
                id=anom['id']
            )