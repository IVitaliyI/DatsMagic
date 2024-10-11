import pygame
import random
import time

# Константы
WIDTH, HEIGHT = 900, 900
CELL_SIZE = 3  # Размер ячейки в пикселях
FPS = 30  # Частота обновления

# Цвета
EMPTY_COLOR = (0, 0, 0)  # Черный для пустоты
ALLY_COLOR = (0, 255, 0)  # Зеленый для союзника
ENEMY_COLOR = (255, 0, 0)  # Красный для врага
ANOMALY_COLOR = (255, 255, 0)  # Желтый для аномалии

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Array Visualization")
clock = pygame.time.Clock()


def generate_random_array():
    """Генерация случайного массива 900x900."""
    return [[random.choice(['empty', 'ally', 'enemy', 'anomaly']) for _ in range(900)] for _ in range(900)]


def draw_array(array):
    """Отрисовка массива на экране."""
    for y in range(len(array)):
        for x in range(len(array[y])):
            cell = array[y][x]
            if cell == 'empty':
                color = EMPTY_COLOR
            elif cell == 'ally':
                color = ALLY_COLOR
            elif cell == 'enemy':
                color = ENEMY_COLOR
            elif cell == 'anomaly':
                color = ANOMALY_COLOR

            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def print_map():
    running = True
    array = generate_random_array()  # Начальный массив

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Очистка экрана
        draw_array(array)  # Отрисовка массива

        pygame.display.flip()  # Обновление экрана
        clock.tick(FPS)  # Установка частоты кадров

        # Обновление массива каждые 2 секунды
        time.sleep(2)
        array = generate_random_array()

    pygame.quit()

