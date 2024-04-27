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

FPS = 30

# Формируем URL запрос к MapsAPI
url = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}" \
      f"&z={zoom}&l=map"

response = requests.get(url)
# Грузим нашу картинку
map_image = pygame.image.load(BytesIO(response.content))

# Создаем окно Pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Большая задача по Maps API. Часть №3")

# Отображаем карту в окне
screen.blit(map_image, (0, 0))
pygame.display.flip()

clock = pygame.time.Clock()

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
                    # Формируем новый URL запрос
                    url = f"https://static-maps.yandex.ru/1.x/" \
                          f"?ll={longitude},{latitude}&z={zoom}&l=map"
                response = requests.get(url)
                # Грузим обновленную картинку
                map_image = pygame.image.load(BytesIO(response.content))
                # Отображаем обновленную карту в окне
                screen.blit(map_image, (0, 0))
                pygame.display.flip()
            elif event.key == pygame.K_PAGEDOWN:
                # Уменьшаем масштаб
                if zoom > MIN_ZOOM:
                    zoom -= 1
                    # Формируем новый URL запрос
                    url = f"https://static-maps.yandex.ru/1.x/" \
                          f"?ll={longitude},{latitude}&z={zoom}&l=map"
                response = requests.get(url)
                # Грузим обновленную картинку
                map_image = pygame.image.load(BytesIO(response.content))
                # Отображаем обновленную карту в окне
                screen.blit(map_image, (0, 0))
                pygame.display.flip()
            elif event.key == pygame.K_UP:
                # Перемещаем карту вверх
                if latitude < 90 - LATITUDE_STEP:
                    latitude += LATITUDE_STEP
                    # Формируем новый URL запрос
                    url = f"https://static-maps.yandex.ru/1.x/" \
                          f"?ll={longitude},{latitude}&z={zoom}&l=map"
                response = requests.get(url)
                # Грузим обновленную картинку
                map_image = pygame.image.load(BytesIO(response.content))
                # Отображаем обновленную карту в окне
                screen.blit(map_image, (0, 0))
                pygame.display.flip()
            elif event.key == pygame.K_DOWN:
                # Перемещаем карту вниз
                if latitude > -90 + LATITUDE_STEP:
                    latitude -= LATITUDE_STEP
                    # Формируем новый URL запрос
                    url = f"https://static-maps.yandex.ru/1.x/" \
                          f"?ll={longitude},{latitude}&z={zoom}&l=map"
                response = requests.get(url)
                # Грузим обновленную картинку
                map_image = pygame.image.load(BytesIO(response.content))
                # Отображаем обновленную карту в окне
                screen.blit(map_image, (0, 0))
                pygame.display.flip()
            elif event.key == pygame.K_LEFT:
                # Перемещаем карту влево
                if longitude > -180 + LONGITUDE_STEP:
                    longitude -= LONGITUDE_STEP
                    # Формируем новый URL запрос
                    url = f"https://static-maps.yandex.ru/1.x/" \
                          f"?ll={longitude},{latitude}&z={zoom}&l=map"
                response = requests.get(url)
                # Грузим обновленную картинку
                map_image = pygame.image.load(BytesIO(response.content))
                # Отображаем обновленную карту в окне
                screen.blit(map_image, (0, 0))
                pygame.display.flip()
            elif event.key == pygame.K_RIGHT:
                # Перемещаем карту вправо
                if longitude < 180 - LONGITUDE_STEP:
                    longitude += LONGITUDE_STEP
                    # Формируем новый URL запрос
                    url = f"https://static-maps.yandex.ru/1.x/" \
                          f"?ll={longitude},{latitude}&z={zoom}&l=map"
                response = requests.get(url)
                # Грузим обновленную картинку
                map_image = pygame.image.load(BytesIO(response.content))
                # Отображаем обновленную карту в окне
                screen.blit(map_image, (0, 0))
                pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
