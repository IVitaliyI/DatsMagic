from math import sqrt
from abc import ABC, abstractmethod
import numpy as np


from Parser.Parser import Parser
from DataClasses.Carpet_airplane import OurCarpetAirplane
from DataClasses.Gold import Gold
from DataClasses.Anomaly import Anomaly

from Utils.Utils import DataSaver

def generate_response_server(id: str, 
                                acc: tuple[float, float] = (0, 0), 
                                activateShield: bool = False, 
                                attack: tuple[int, int] = None):
    if attack != None:
        response = {
            "transports": {
                "acceleration": {"x": acc[0], "y": acc[1]},
                "activateShield": activateShield,
                "attack": {"x": attack[0], "y": attack[1]},
                "id": id
            }
        }
    else:
        response = {
            "transports": {
                "acceleration": {"x": acc[0], "y": acc[1]},
                "activateShield": activateShield,
                "id": id
            }
        }
    return response

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
        transport_bounties_view: dict[tuple[int,int], list[Gold]] = {}
        for bount in self.data.parse_bounties():
            for transport in self.transports:
                if transport.id not in transport_bounties_view:
                    transport_bounties_view[transport.id] = []
                if transport.classification((bount.x, bount.y)):
                    transport_bounties_view[transport.id].append(bount)
        return transport_bounties_view
    
    def parse_enemies_view_transport(self):
        transport_enemies_view: dict[tuple[int,int], list[Gold]] = {}
        for bount in self.data.parse_enemies():
            for transport in self.transports:
                if transport.id not in transport_enemies_view:
                    transport_enemies_view[transport.id] = []
                if transport.classification((bount.x, bount.y)):
                    transport_enemies_view[transport.id].append(bount)
        return transport_enemies_view
    
    def parse_anomaly_view_transport(self):
        transport_anomaly_view: dict[tuple[int,int], list[Gold]] = {}
        for bount in self.data.parse_anomalies():
            for transport in self.transports:
                if transport.id not in transport_anomaly_view:
                    transport_anomaly_view[transport.id] = []
                if transport.classification((bount.x, bount.y)):
                    transport_anomaly_view[transport.id].append(bount)
        return transport_anomaly_view
    
    def parse_wanted_list_view_transport(self):
        transport_wanted_view: dict[tuple[int,int], list[Gold]] = {}
        for bount in self.data.parse_wanted_list():
            for transport in self.transports:
                if transport.id not in transport_wanted_view:
                    transport_wanted_view[transport.id] = []
                if transport.classification((bount.x, bount.y)):
                    transport_wanted_view[transport.id].append(bount)
        return transport_wanted_view
        
    
        
class GameStateForOneTransport(GameState):
    def __init__(self, transport: OurCarpetAirplane) -> None:
        self.see_bounties = []
        # Необходимо один раз пройтись по bounties и классифицировать к какому ковру относятся те или иные монеты
        # Тоже самое можно сделать и с врагами
        
class ActionStrategy(ABC):
    @abstractmethod
    def choose_next_gold(self, current_x: int, current_y: int, remaining_gold: list[Gold]) -> Gold:
        pass

class MaxValuePerDistanceStrategy(ActionStrategy):
    def choose_next_gold(self, current_x: int, current_y: int, remaining_gold: list[Gold]) -> Gold:
        best_gold = None
        best_value_to_distance = float('-inf')
        
        for gold in remaining_gold:
            distance = euclidean_distance(current_x, current_y, gold.x, gold.y)
            value_to_distance = gold.value / distance  # Отношение ценности к расстоянию
            
            if value_to_distance > best_value_to_distance:
                best_value_to_distance = value_to_distance
                best_gold = gold

        return best_gold

class ClosestGoldStrategy(ActionStrategy):
    def choose_next_gold(self, current_x: int, current_y: int, remaining_gold: list[Gold]) -> Gold:
        best_gold = None
        min_distance = float('inf')
        
        for gold in remaining_gold:
            distance = euclidean_distance(current_x, current_y, gold.x, gold.y)
            if distance < min_distance:
                min_distance = distance
                best_gold = gold

        return best_gold

class GoldCollector:
    def __init__(self, strategy: ActionStrategy):
        self.strategy = strategy

    def collect_gold(self, gold_list: list[Gold], transport: OurCarpetAirplane) -> list[Gold]:
        path = []  # Путь, по которому идёт сбор монеток
        remaining_gold = gold_list.copy()  # Оставшиеся монетки
        current_x, current_y = transport.x, transport.y
        for _ in range(5):
            # Выбираем следующую монетку согласно выбранной стратегии
            next_gold = self.strategy.choose_next_gold(current_x, current_y, remaining_gold)
            if next_gold is None:
                break
            
            # Перемещаемся к выбранной монетке
            path.append(next_gold)
            current_x, current_y = next_gold.x, next_gold.y
            remaining_gold.remove(next_gold)

        return path

class PhysicCalculator:
    def __init__(self, transport: OurCarpetAirplane, anomaly: list[Anomaly]):
        self.transport: OurCarpetAirplane = transport
        self.anomaly: list[Anomaly] = anomaly

    def external_acceleration(self) -> np.ndarray:
        """
        Задаёт внешнее ускорение в зависимости от времени.
        Пример: меняющееся внешнее ускорение в зависимости от времени.
        """
        strength: float = 0
        napr: np.array = np.array([0,0])
        for anom in self.anomaly:
            strength = anom.strength ** 2 / euclidean_distance(self.transport.x, self.transport.y, anom.x, anom.y) ** 2 * np.sign(anom.strength) #TODO: необходимо проверить а будет ли влиять аномалия
            vector = np.array([anom.x - self.transport.x, anom.y - self.transport.y])
            napr += vector / np.linalg.norm(vector) * strength 
        return napr

    def motion_equation(self, r: np.ndarray, v: np.ndarray, a_control: np.ndarray, t: float, dt: float) -> tuple:
        """
        Рассчитывает новое положение и скорость с учётом внешнего и управляющего ускорений.
        
        r: np.ndarray - текущая позиция (x, y)
        v: np.ndarray - текущая скорость (vx, vy)
        a_control: np.ndarray - управляющее ускорение (ax, ay)
        t: float - текущее время
        dt: float - шаг по времени
        
        Возвращает новое положение и скорость.
        """
        a_ext = self.external_acceleration()  # Внешнее ускорение
        
        if n := np.linalg.norm(a_ext) > 10:
            a_ext = a_ext / n * 10
        
        total_acceleration = a_control + a_ext  # Суммарное ускорение
        
        # Обновляем скорость: v(t+dt) = v(t) + a_total * dt
        new_v = v + total_acceleration * dt
        
        # Обновляем положение: r(t+dt) = r(t) + v(t) * dt
        new_r = r + new_v * dt
        
        return new_r, new_v

    def simulate_motion(self, r0, v0, rf, max_acceleration, dt=0.33, tolerance=5):
        """
        Симулирует движение объекта до достижения целевой точки с учётом внешних сил и управляющего ускорения.
        
        r0: np.array - начальное положение (x, y)
        v0: np.array - начальная скорость (vx, vy)
        rf: np.array - целевая позиция (x, y)
        max_acceleration: float - максимальное управляющее ускорение
        dt: float - шаг по времени
        tolerance: float - допустимая ошибка для достижения цели
        
        Возвращает траекторию движения объекта и финальную скорость.
        """
        trajectory = [r0]
        t = 0
        current_r = r0
        current_v = v0
        
        while np.linalg.norm(current_r - rf) > tolerance:
            # Направление к цели
            direction_to_target = (rf - current_r) / np.linalg.norm(rf - current_r)
            
            # Рассчитываем управляющее ускорение в направлении цели
            a_control = direction_to_target * max_acceleration
            
            # Обновляем положение и скорость
            current_r, current_v = self.motion_equation(current_r, current_v, a_control, t, dt)
            
            # Сохраняем траекторию
            trajectory.append(current_r)
            
            # Обновляем время
            t += dt
        
        return np.array(trajectory), current_v