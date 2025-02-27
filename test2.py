import pygame
import json

# Загрузка данных из JSON файла
with open('bd.json', 'r') as f:
    controls = json.load(f)

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
FONT_SIZE = 30

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Настройка экрана и шрифта
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Настройки")
font = pygame.font.Font(None, FONT_SIZE)


def settings_menu():
    running = True
    selected_index = 0
    keys_to_change = list(controls.keys())

    while running:
        screen.fill(WHITE)

        # Отображение заголовка
        title_surface = font.render("Настройки", True, (0, 0, 0))
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 50))

        # Отображение списка действий и кнопок
        for index, action in enumerate(keys_to_change):
            button_text = f"{action}: {controls[action]}"
            text_surface = font.render(button_text, True, (0, 0, 0))
            screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 100 + index * (FONT_SIZE + 10)))

            # Отображение красного прямоугольника для выделения выбранного действия
            if index == selected_index:
                pygame.draw.rect(screen, RED,
                                 (WIDTH // 2 - text_surface.get_width() // 2 - 10,
                                  100 + index * (FONT_SIZE + 10) - 5,
                                  text_surface.get_width() + 20,
                                  FONT_SIZE + 10),
                                 border_radius=5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index -= 1
                    if selected_index < 0:
                        selected_index = len(keys_to_change) - 1

                elif event.key == pygame.K_DOWN:
                    selected_index += 1
                    if selected_index >= len(keys_to_change):
                        selected_index = 0

                elif event.key == pygame.K_SPACE:
                    action_to_change = keys_to_change[selected_index]
                    controls[action_to_change] = "***"

                    waiting_for_key = True

                    while waiting_for_key:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                waiting_for_key = False

                            if event.type == pygame.KEYDOWN:
                                new_key_name = pygame.key.name(event.key)
                                controls[action_to_change] = new_key_name
                                waiting_for_key = False

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    # Сохранение изменений в JSON файл перед выходом из меню настроек
    with open('bd.json', 'w') as f:
        json.dump(controls, f)


# Запуск меню настроек
settings_menu()

pygame.quit()