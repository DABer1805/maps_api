import pygame
import requests
from io import BytesIO

# Задаем координаты, масштаб и предельные значения карты
latitude = 55.75396
longitude = 37.620393
zoom = 10
MIN_ZOOM = 1
MAX_ZOOM = 19
LATITUDE_STEP = 0.05
LONGITUDE_STEP = 0.05
FPS = 60  # Частота кадров

UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3

# Слои карты
LAYERS = ["map", "sat", "sat,skl"]
current_layer = 0

# Формируем URL запрос к MapsAPI
url = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}" \
      f"&z={zoom}&l={LAYERS[current_layer]}"

response = requests.get(url)
# Грузим нашу картинку
map_image = pygame.image.load(BytesIO(response.content))

# Создаем окно Pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Большая задача по Maps API. Часть №4")

# Отображаем карту в окне
screen.blit(map_image, (0, 0))
pygame.display.flip()

clock = pygame.time.Clock()


def update_map(latitude, longitude, zoom, layer):
    # Формируем новый URL запрос
    url = f"https://static-maps.yandex.ru/1.x/" \
          f"?ll={longitude},{latitude}&z={zoom}&l=" \
          f"{LAYERS[layer]}"
    response = requests.get(url)
    # Грузим обновленную картинку
    map_image = pygame.image.load(BytesIO(response.content))
    # Отображаем обновленную карту в окне
    screen.blit(map_image, (0, 0))


def move_map(latitude, longitude, zoom, layer, direction):
    """ Перемещаем карту """
    if direction == UP:
        if not (latitude < 90 - LATITUDE_STEP):
            return latitude, longitude
        latitude += LATITUDE_STEP
    elif direction == DOWN:
        if not (latitude > -90 + LATITUDE_STEP):
            return latitude, longitude
        latitude -= LATITUDE_STEP
    elif direction == RIGHT:
        if not (longitude < 180 - LONGITUDE_STEP):
            return latitude, longitude
        longitude += LONGITUDE_STEP
    elif direction == LEFT:
        if not (longitude > -180 + LONGITUDE_STEP):
            return latitude, longitude
        longitude -= LONGITUDE_STEP
    update_map(latitude, longitude, zoom, layer)
    return latitude, longitude


def change_layer(latitude, longitude, zoom, layer):
    # Переключаем слой карты
    layer = (layer + 1) % len(LAYERS)
    # Формируем новый URL запрос
    update_map(latitude, longitude, zoom, layer)
    return layer


# Основной цикл приложения
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                # Увеличиваем масштаб
                if zoom < MAX_ZOOM:
                    zoom += 1
                    update_map(latitude, longitude, zoom, current_layer)
            elif event.key == pygame.K_PAGEDOWN:
                # Уменьшаем масштаб
                if zoom > MIN_ZOOM:
                    zoom -= 1
                    update_map(latitude, longitude, zoom, current_layer)
            elif event.key == pygame.K_UP:
                # Перемещаем центр карты вверх
                latitude, longitude = move_map(latitude, longitude,
                                               zoom, current_layer, UP)
            elif event.key == pygame.K_DOWN:
                # Перемещаем центр карты вниз
                latitude, longitude = move_map(latitude, longitude,
                                               zoom, current_layer, DOWN)
            elif event.key == pygame.K_LEFT:
                # Перемещаем карту влево
                latitude, longitude = move_map(latitude, longitude,
                                               zoom, current_layer, LEFT)
            elif event.key == pygame.K_RIGHT:
                # Перемещаем карту вправо
                latitude, longitude = move_map(latitude, longitude,
                                               zoom, current_layer, RIGHT)
            elif event.key == pygame.K_TAB:
                current_layer = change_layer(latitude, longitude, zoom,
                                             current_layer)

    # Ограничение частоты кадров
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
