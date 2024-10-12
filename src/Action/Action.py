from math import sqrt
from abc import ABC, abstractmethod
import numpy as np
import json
from typing import Union

from Parser.Parser import Parser
from DataClasses.Carpet_airplane import OurCarpetAirplane, EnemyCarpetAirplane
from DataClasses.Gold import Gold
from DataClasses.Anomaly import Anomaly
from DataClasses.Constants import WantedList, Constants

from Utils.Utils import DataSaver



def euclidean_distance(x1: int, y1: int, x2: int, y2: int) -> float:
    """Евклидово расстояние между двумя точками."""
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

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
        transport_bounties_view: dict[str, list[Gold]] = {}
        for bount in self.data.parse_bounties():
            for transport in self.transports:
                if transport.id not in transport_bounties_view:
                    transport_bounties_view[transport.id] = []
                if transport.classification((bount.x, bount.y)):
                    transport_bounties_view[transport.id].append(bount)
        return transport_bounties_view
    
    def parse_enemies_view_transport(self):
        transport_enemies_view: dict[str, list[Gold]] = {}
        for bount in self.data.parse_enemies():
            for transport in self.transports:
                if transport.id not in transport_enemies_view:
                    transport_enemies_view[transport.id] = []
                if transport.classification((bount.x, bount.y)):
                    transport_enemies_view[transport.id].append(bount)
        return transport_enemies_view
    
    def parse_anomaly_view_transport(self):
        transport_anomaly_view: dict[str, list[Gold]] = {}
        for bount in self.data.parse_anomalies():
            for transport in self.transports:
                if transport.id not in transport_anomaly_view:
                    transport_anomaly_view[transport.id] = []
                if transport.classification((bount.x, bount.y)):
                    transport_anomaly_view[transport.id].append(bount)
        return transport_anomaly_view
    
    def parse_wanted_list_view_transport(self):
        transport_wanted_view: dict[str, list[Gold]] = {}
        for bount in self.data.parse_wanted_list():
            for transport in self.transports:
                if transport.id not in transport_wanted_view:
                    transport_wanted_view[transport.id] = []
                if transport.classification((bount.x, bount.y)):
                    transport_wanted_view[transport.id].append(bount)
        return transport_wanted_view

class CalculateMove(ABC):
    @abstractmethod
    def calculate(self, transport: OurCarpetAirplane,
                  anomalies: list[Anomaly],
                  enemies: list[EnemyCarpetAirplane],
                  bounties: list[Gold],
                  wanted_list: list[WantedList]):
        pass

class MaxValuePerDistanceStrategy(CalculateMove):
    def calculate(self, transport: OurCarpetAirplane,
                  anomalies: list[Anomaly],
                  enemies: list[EnemyCarpetAirplane],
                  bounties: list[Gold],
                  wanted_list: list[WantedList]):
        best_gold = None
        best_value_to_distance = float('-inf')
        
        for gold in bounties:
            distance = euclidean_distance(transport.x, transport.y, gold.x, gold.y)
            value_to_distance = gold.value / distance  # Отношение ценности к расстоянию
            
            if value_to_distance > best_value_to_distance:
                best_value_to_distance = value_to_distance
                best_gold = gold

        return best_gold

class AvoidObstaclesAndSeekStartegy(CalculateMove):
    def calculate(self, transport: OurCarpetAirplane,
                  anomalies: list[Anomaly],
                  enemies: list[EnemyCarpetAirplane],
                  bounties: list[Gold],
                  wanted_list: list[WantedList]):
        strategy = MaxValuePerDistanceStrategy()
        target = strategy.calculate(transport, anomalies, enemies, bounties, wanted_list)
        
        if not target:
            return np.array([0,0])
        
        target_vector = np.array([target.x - transport.x, target.y - transport.y])
        target_distance = np.linalg.norm(target_vector)
        if target_distance > 0:
            target_vector = target_vector / target_distance
        
        # Избегание препятствий
        avoidance_vector = np.array([0, 0])
        for anomaly in anomalies:
            to_anomaly = np.array([anomaly.x - transport.x, anomaly.y - transport.y])
            distance = np.linalg.norm(to_anomaly)
            if distance < 10:  # Радиус избегания
                avoidance_vector -= to_anomaly / (distance**2)  # Чем ближе, тем сильнее отталкивание
        
        # Комбинированный вектор
        combined_vector = target_vector + avoidance_vector
        return combined_vector
        
class OtherAlgorithm(CalculateMove):
    def calculate(self, transport: OurCarpetAirplane,
                  anomalies: list[Anomaly],
                  enemies: list[EnemyCarpetAirplane],
                  bounties: list[Gold],
                  wanted_list: list[WantedList]):
        return super().calculate(transport, anomalies, enemies, bounties, wanted_list)

class AttackStrategy(ABC):
    @abstractmethod
    def calculate(self, transport: OurCarpetAirplane,
                  enemies: list[EnemyCarpetAirplane],
                  wanted_list: list[WantedList]):
        pass

class AttackAllEnemies(AttackStrategy):
    def calculate(self, transport: OurCarpetAirplane, 
                  enemies: list[EnemyCarpetAirplane], 
                  wanted_list: list[WantedList]):
        wanted_list.sort(key=lambda x: x.health and self.can_attack(transport, x))
        enemies.sort(key=lambda x: x.health and self.can_attack(transport, x))
        if wanted_list != [] and wanted_list[0].health <= Constants().attackDamage:
            return wanted_list[0]
        if enemies != []:
            return enemies[0]
    
    @staticmethod
    def can_attack(transport: OurCarpetAirplane, enemy: Union[EnemyCarpetAirplane, WantedList]):
        if transport.attackCooldownMs != 0:
            return False
        if enemy.shieldLeftMs != 0:
            return False
        if euclidean_distance(transport.x, transport.y, enemy.x, enemy.y) > Constants().attackRange:
            return False
        return True

class ShieldStrategy(ABC):
    @abstractmethod
    def calculate(self, transport: OurCarpetAirplane,
                  enemies: list[EnemyCarpetAirplane]):
        pass

class AutoActivator(ShieldStrategy):
    def calculate(self, transport: OurCarpetAirplane, enemies: list[EnemyCarpetAirplane]):
        if transport.shieldCooldownMs == 0:
            for enemy in enemies:
                if self.can_attack(transport, enemy):
                    return True
        return False
    
    @staticmethod
    def can_attack(transport: OurCarpetAirplane, enemy: Union[EnemyCarpetAirplane, WantedList]):
        if transport.attackCooldownMs != 0:
            return False
        if enemy.shieldLeftMs != 0:
            return False
        if euclidean_distance(transport.x, transport.y, enemy.x + enemy.velX * 0.33, enemy.y + enemy.velY * 0.33) > Constants().attackRange + Constants().attackExplosionRadius:
            return False
        return True
    
class StrategyChoiceClass:
    def __init__(self, strategy: CalculateMove = None, attack_strategy: AttackStrategy = None, shield_strategy: ShieldStrategy = None):
        self.strategy: CalculateMove = strategy
        self.attack_strategy: AttackStrategy = attack_strategy
        self.shield_strategy: ShieldStrategy = shield_strategy
    
    def generate_response_server(self, carpetAirplanes: list[OurCarpetAirplane],
                                 anomalies: dict[str, Anomaly],
                                 boundies: dict[str, list[Gold]],
                                 enemies: dict[str, list[EnemyCarpetAirplane]],
                                 wanted:  dict[str, list[WantedList]]):
        response: dict[str, list] = {'transports': []}
        for carpet in carpetAirplanes:
            if carpet.status == 'alive':
                combined_vector: tuple[int, int] = self.strategy.calculate(transport=carpet, anomalies=anomalies[carpet.id],
                                        enemies=enemies[carpet.id],
                                        bounties=boundies[carpet.id],
                                        wanted_list=wanted.get(carpet.id, []))
                
                attack: Union[EnemyCarpetAirplane, WantedList] = self.attack_strategy.calculate(transport=carpet, 
                                                                         enemies=enemies[carpet.id], 
                                                                         wanted_list=wanted.get(carpet.id, []))
                shield: bool = self.shield_strategy.calculate(carpet, enemies[carpet.id])
                
                attack_coord = None
                if attack:
                    attack_coord = (round(attack.x + attack.velX * 0.33), round(attack.y + attack.velY * 0.33))
                    # print(attack)
                
                phys = PhysicCalculator(carpet, anomalies[carpet.id])
                if combined_vector is not None:
                    acc = combined_vector * 10
                    # print(acc)
                else:
                    acc = (0,0)
                # acc = phys.calculate_control(np.array([4500,4500]))
                
                data = self._generate_response_server_step(carpet.id, acc, attack=attack_coord, activateShield=shield)
                response["transports"].append(data)
        # print(response)
        return response
    
    @staticmethod
    def _generate_response_server_step(id: str, 
                                acc: tuple[float, float] = (0, 0), 
                                activateShield: bool = False, 
                                attack: tuple[int, int] = None):
        if attack != None:
            response = {
                    "acceleration": {"x": int(acc[0]), "y": int(acc[1])},
                    "activateShield": activateShield,
                    "attack": {"x": int(attack[0]), "y": int(attack[1])},
                    "id": id
            }
        else:
            response = {
                    "acceleration": {"x": int(acc[0]), "y": int(acc[1])},
                    "activateShield": activateShield,
                    "id": id
            }
        return response
        

class PhysicCalculator:
    def __init__(self, transport: OurCarpetAirplane, 
                 anomaly: list[Anomaly]):
        self.transport: OurCarpetAirplane = transport
        self.anomaly: list[Anomaly] = anomaly

    # @staticmethod
    # def external_acceleration_id_point(coord: tuple[float, float], anomaly: list[Anomaly] = []) -> np.ndarray:
    #     """
    #     Задаёт внешнее ускорение в зависимости от времени.
    #     Пример: меняющееся внешнее ускорение в зависимости от времени.
    #     """
    #     strength: float = 0
    #     napr: np.array = np.array([0,0])
    #     for anom in anomaly:
    #         strength = anom.strength ** 2 / euclidean_distance(coord[0], coord[1], anom.x, anom.y) ** 2 * np.sign(anom.strength) #TODO: необходимо проверить а будет ли влиять аномалия
    #         vector = np.array([anom.x - coord[0], anom.y - coord[1]])
    #         napr += vector / np.linalg.norm(vector) * strength 
    #     return napr

    def motion_model(self, t, dt, a_ctrl: np.array = np.array([0,0])):
        """
        Модель движения объекта с учётом внешних и управляющих ускорений.
        
        position: np.array([x, y]) - текущее положение объекта
        velocity: np.array([vx, vy]) - текущая скорость объекта
        a_ctrl: np.array([ax, ay]) - управляющее ускорение
        t: float - текущее время
        dt: float - шаг по времени
        
        Возвращает новое положение и скорость объекта.
        """
        a_ext = np.array([self.transport.anomalyAccelerationX, self.transport.anomalyAccelerationY])  # Внешнее ускорение
        
        # Суммарное ускорение
        total_acceleration = a_ctrl + a_ext
        
        # Обновляем скорость: v(t+dt) = v(t) + a_total * dt
        new_velocity = np.array([self.transport.velX, self.transport.velY]) + total_acceleration * dt
        
        # Обновляем положение: r(t+dt) = r(t) + v(t) * dt
        new_position = np.array([self.transport.x, self.transport.y]) + new_velocity * dt
        
        return new_position, new_velocity

    def calculate_control(self, target_position, k_p=2, k_d=0.5):
        """
        Рассчитывает управляющее ускорение для движения к цели.
        
        position: np.array([x, y]) - текущее положение объекта
        target_position: np.array([x, y]) - целевая точка
        velocity: np.array([vx, vy]) - текущая скорость объекта
        k_p: float - коэффициент пропорционального усиления
        
        Возвращает управляющее ускорение.
        """
        # Ошибка в положении (разница между целевой и текущей позицией)
        error_position = target_position - np.array([self.transport.x, self.transport.y])
        
        # Внешнее ускорение в текущем положении
        a_ext = np.array([self.transport.anomalyAccelerationX, self.transport.anomalyAccelerationY])
        
        # Пропорциональный контроллер: корректировка с учётом внешнего ускорения
        a_ctrl = k_p * error_position + k_d * np.array([-self.transport.velX, -self.transport.velY])
        # print(a_ctrl)
        if np.linalg.norm(a_ctrl) >= 10:
            return a_ctrl / np.linalg.norm(a_ctrl) * 10
        return a_ctrl
    
    

    # def simulate_trajectory(self, target_position, dt=0.33):
    #     """
    #     Симуляция движения объекта для достижения цели с учётом управляющих и внешних сил.
        
    #     start_position: np.array([x, y]) - начальная позиция объекта
    #     start_velocity: np.array([vx, vy]) - начальная скорость объекта
    #     target_position: np.array([x, y]) - целевая точка
    #     max_time: float - максимальное время симуляции
    #     dt: float - шаг по времени
        
    #     Возвращает траекторию движения и финальное состояние объекта (положение и скорость).
    #     """
    #     trajectory = [np.array([self.transport.x, self.transport.y])]
    #     position = np.array([self.transport.x, self.transport.y])
    #     velocity = np.array([self.transport.velX, self.transport.velY])
    #     t = 0
        
    #     # Рассчитываем управляющее ускорение
    #     a_ctrl = self.calculate_control(target_position)
        
    #     # Обновляем положение и скорость объекта
    #     position, velocity = self.motion_model(t, dt, a_ctrl)
        
    #     # Сохраняем траекторию
    #     trajectory.append(position)
        
    #     # Обновляем время
    #     t += dt
        
    #     return np.array(trajectory), position, velocity