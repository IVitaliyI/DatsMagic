import pygame
import sys
import time
from DataClasses.Anomaly import Anomaly
from DataClasses.Gold import Gold
from DataClasses.Carpet_airplane import OurCarpetAirplane, EnemyCarpetAirplane
from DataClasses.Map import Map
from Parser.Parser import Parser

class Visualizator:
    def __init__(self, window_size=(700, 700), update_time=2):
        self.window_size = window_size
        self.update_time = update_time
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('Визуализация координат')

    def visualize_objects(self, objects: Map):
        # Определение масштаба, чтобы все объекты помещались на экране
        scale_x = self.window_size[0] / 25000
        scale_y = self.window_size[1] / 25000
        scale = min(scale_x, scale_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        
        self.screen.fill((0, 0, 0))
        
        for coords, obj in objects.objects.items():
            scaled_coords = int(coords[0] + 5100) * scale, int(coords[1] + 5100) * scale
            if isinstance(obj, Anomaly):
                color = (255, 255, 255)
                pygame.draw.circle(self.screen, color, scaled_coords, 1)
                pygame.draw.circle(self.screen, color, scaled_coords, int(obj.R2 * scale), 1)
            elif isinstance(obj, OurCarpetAirplane):
                color = (0, 255, 0)
                pygame.draw.circle(self.screen, color, scaled_coords, 1)
            elif isinstance(obj, EnemyCarpetAirplane):
                color = (255, 0, 0)
                pygame.draw.circle(self.screen, color, scaled_coords, 1)
            elif isinstance(obj, Gold):
                color = (255, 215, 0)
                pygame.draw.circle(self.screen, color, scaled_coords, 1)
                pygame.draw.circle(self.screen, color, scaled_coords, int(obj.R * scale), 1)

        pygame.display.flip()

    @staticmethod
    def generate_game_state(data_obj: Parser) -> Map:
        CONSTANTS = data_obj.parse_constants()
        gameMap = Map(CONSTANTS.mapSizeX, CONSTANTS.mapSizeY)
        [gameMap.add_object(obj) for obj in data_obj.parse_anomalies()]
        [gameMap.add_object(obj) for obj in data_obj.parse_enemies()]
        [gameMap.add_object(obj) for obj in data_obj.parse_transports()]
        [gameMap.add_object(obj) for obj in data_obj.parse_bounties()]
        return gameMap
