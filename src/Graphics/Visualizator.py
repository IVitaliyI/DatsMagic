import pygame
import sys
import time
from DataClasses.Anomaly import Anomaly
from DataClasses.Gold import Gold
from DataClasses.Carpet_airplane import OurCarpetAirplane, EnemyCarpetAirplane
from DataClasses.Map import Map
from Parser.Parser import Parser

class Visualizator:
    def __init__(self, window_size=(900, 900), update_time=2, scale=0.05):
        self.window_size = window_size
        self.update_time = update_time
        self.scale = scale
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('Визуализация координат')

    def visualize_objects(self, objects: Map):
        #while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or event.type == pygame.KEYDOWN):
                    pygame.quit()
                    sys.exit()
            self.screen.fill((0, 0, 0))
            for coords, obj in objects.objects.items():
                scaled_coords = (int(coords[0] * self.scale), int(coords[1] * self.scale))
                if isinstance(obj, Anomaly):
                    color = (255, 255, 255)
                    pygame.draw.circle(self.screen, color, scaled_coords, 1)
                    pygame.draw.circle(self.screen, color, scaled_coords, 200*self.scale, 1)
                elif isinstance(obj, OurCarpetAirplane):
                    color = (0, 255, 0)
                    pygame.draw.circle(self.screen, color, scaled_coords, 1)
                elif isinstance(obj, EnemyCarpetAirplane):
                    color = (255, 0, 0)
                    pygame.draw.circle(self.screen, color, scaled_coords, 1)
                elif isinstance(obj, Gold):
                    color = (255, 215, 0)
                    pygame.draw.circle(self.screen, color, scaled_coords, 1)
                    pygame.draw.circle(self.screen, color, scaled_coords, 5*self.scale, 1)  # Окружность радиусом 5 клеток
            pygame.display.flip()
            #time.sleep(self.update_time)
    
    @staticmethod
    def generate_game_state(data_obj: Parser) -> Map:
        CONSTANTS = data_obj.parse_constants()
        gameMap = Map(CONSTANTS.mapSizeX, CONSTANTS.mapSizeY)
        [gameMap.add_object(obj) for obj in data_obj.parse_anomalies()]
        [gameMap.add_object(obj) for obj in data_obj.parse_enemies()]
        [gameMap.add_object(obj) for obj in data_obj.parse_transports()]
        [gameMap.add_object(obj) for obj in data_obj.parse_bounties()]
        return gameMap
