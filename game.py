import pygame
import sys
import random
import json
# import time

clock = pygame.time.Clock()

W = 1500
H = 800

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('RAKBATTLESIMULATOR9999')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
background = pygame.image.load('images/ФОН.jpg').convert()
background = pygame.transform.scale(background, (W, H))
title = pygame.image.load('images/НАДПИСЬ RBs.png').convert_alpha()

hopping_size = 10
step_hopping_size = -5
font1 = pygame.font.Font(None, 74)
font = pygame.font.Font(None, 30)
select = ['', 'игра', 'настройки', 'выход', 'game_over']
select_type_games = ['', 'сюжет', 'бесконечный', 'дуэль']

hints = ['also try Zametki', 'also try SimpleDraw', 'some cheats: uuddLrLra1a2', 'a gde?', 'also try OГЭ по химии',
         'play PowerPoint', 'Ты сделал все уроки?', 'also try Яндекс Лицей', 'RAK', 'CANCER', 'Jq, yt nf hfcrkflrf',
         'MOM?', 'WE NEED 100$', 'Я сдам физику, честно', 'y = kx + b', 'Saratow2077', 'Roll D20', '3,14',
         'This sentence is a lie', 'Trust us', 'Wellcome to the underground', 'Hello World', 'Are you sure?', '(*)_(*)',
         'also try PyCharm', 'AAAAAAAAA', 'Plant B', 'bye', 'cake is a lie', 'spaceeeee...', 'also try Alt + f4',
         'power of 3 is Lr shot', 'I am the danger', 'yoyoyo 1483 to 3 to 6 to 9', 'Better call Soul']

hint = random.choice(hints)
cur_select = select[0]
cur_select_game = select_type_games[0]
move_selected = 0
move_selected_game = 0
selected_level = 0
last_moves = ['', '', '', '', '', '', '', '', '', '']
score_count = 0
wave = 10
old_wave = wave

with open('bd.json', 'r') as f:
    keybindings = json.load(f)


class MainRak(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # with open('bd.json', 'r') as f:
        #     keybindings = json.load(f)
        print(keybindings)
        print(keybindings.keys())
        self.up = getattr(pygame, f"K_{keybindings['up']}")
        self.down = getattr(pygame, f"K_{keybindings['down']}")
        self.left = getattr(pygame, f"K_{keybindings['left']}")
        self.right = getattr(pygame, f"K_{keybindings['right']}")
        self.shot = getattr(pygame, f"K_{keybindings['shot']}")
        self.abikukles = getattr(pygame, f"K_{keybindings['abikukles']}")
        self.ulpotato = getattr(pygame, f"K_{keybindings['ulpotato']}")
        self.image = pygame.image.load("images/просто рак.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 3
        self.maxhp = 100
        self.hp = 100
        self.scale = 50
        # self.up = pygame.K_w
        # self.down = pygame.K_s
        # self.left = pygame.K_a
        # self.right = pygame.K_d
        # self.shot = pygame.K_SPACE
        # self.abikukles = pygame.K_e
        # self.ulpotato = pygame.K_q
        self.reverse = False
        self.kd = pygame.time.get_ticks() + 500
        self.gif = pygame.time.get_ticks()
        self.cgif = 0

    def keys_update(self):
        self.up = getattr(pygame, f"K_{keybindings['up']}")
        self.down = getattr(pygame, f"K_{keybindings['down']}")
        self.left = getattr(pygame, f"K_{keybindings['left']}")
        self.right = getattr(pygame, f"K_{keybindings['right']}")
        self.shot = getattr(pygame, f"K_{keybindings['shot']}")
        self.abikukles = getattr(pygame, f"K_{keybindings['abikukles']}")
        self.ulpotato = getattr(pygame, f"K_{keybindings['ulpotato']}")

    def update(self):
        global score_count
        if self.hp <= 0:
            game_over()
        keys = pygame.key.get_pressed()
        if keys[self.up]:
            self.rect.y -= self.speed
        if keys[self.down]:
            self.rect.y += self.speed
        if keys[self.left]:
            self.rect.x -= self.speed
        if keys[self.right]:
            self.rect.x += self.speed
        if self.rect.y >= H - 150:
            self.rect.y = H - 150
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.x >= W - 150:
            self.rect.x = W - 150
        if self.rect.x <= 0:
            self.rect.x = 0

        if self.rect.x > 675:
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.reverse = True
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.image = self.original_image
            self.reverse = False
            self.mask = pygame.mask.from_surface(self.image)

        if cur_select_game != select_type_games[0] and keys[self.shot] and self.kd < pygame.time.get_ticks():
            self.kd = pygame.time.get_ticks() + 500
            self.shoot()

        for e in all_enemies:
            if pygame.sprite.collide_mask(self, e):
                self.hp -= e.hp
                print('hp:', self.hp)
                e.kill()

    def starting_game(self):
        self.rect.x = 650
        self.rect.y = 300
        self.hp = 100

    def shoot(self, vy=0):
        if self.reverse:
            bullet = Bullet(self.rect.x, self.rect.y + 75, -1, vy)
        else:
            bullet = Bullet(self.rect.x + 150, self.rect.y + 75, 1, vy)
        all_bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, rev, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/пуля просто рак.png").convert_alpha()
        scale = pygame.transform.scale(self.image, (100, 50))
        self.image = scale
        if rev == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.speedx = 15 * rev
        else:
            self.speedx = 15
        self.rect = self.image.get_rect(center=(x, y))
        self.pseudo_rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.damage = 5
        self.vy = vy

    def update(self):
        global score_count
        self.rect.x += self.speedx
        self.rect.y += self.vy
        if self.rect.left > W or self.rect.right < 0 or self.rect.bottom < 0 or self.rect.top > H:
            self.kill()

        for e in all_enemies:
            if pygame.sprite.collide_mask(self, e):
                e.hp -= 5
                self.kill()
                if e.hp <= 0:
                    score_count += e.cost
                    print(score_count)
                    e.kill()


class MainEnemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rev = random.randint(0, 1)
        # self.rev = 0
        self.cost = 1
        self.image = pygame.image.load("images/рыба(она просто есть).png").convert_alpha()
        scale = pygame.transform.scale(self.image, (200, 150))
        self.image = scale
        if self.rev == 1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = (W + 650) * self.rev - 400
        self.rect.y = random.randint(0, H - 150)
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = 20
        self.speedx = 2

    def update(self):
        if self.rev == 0:
            self.rect.x += self.speedx
        else:
            self.rect.x -= self.speedx

        if self.rect.x > W + 500 or self.rect.x < -500:
            self.kill()


class GiantEnemy(MainEnemy):
    def __init__(self):
        super().__init__()
        self.cost = 20
        self.image = pygame.image.load("images/рыба(она просто есть).png").convert_alpha()
        scale = pygame.transform.scale(self.image, (800, H - 50))
        self.image = scale
        if self.rev == 1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = (W + 950) * self.rev - 850
        self.rect.y = 5
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = 55
        self.speed = 1

    def update(self):
        if self.rev == 0:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.rect.x > W + 1000 or self.rect.x < -1000:
            self.kill()


class KrabEnemy(MainEnemy):
    def __init__(self):
        super().__init__()
        self.rev = random.choice([0, 1])
        self.cost = 5
        self.image = pygame.image.load("images/быстрый краб.png").convert_alpha()
        scale = pygame.transform.scale(self.image, (200, 150))
        self.image = scale
        self.rect = self.image.get_rect()
        self.rect.x = (W + 650) * self.rev - 400
        self.rect.y = random.randint(0, H - 150)
        self.mask = pygame.mask.from_surface(self.image)
        self.speedx = 7
        self.speedy = 0
        self.time = pygame.time.get_ticks()

    def update(self):
        if self.time + 700 < pygame.time.get_ticks():
            self.speedx = random.randint(-1, 3)
            self.speedy = random.randint(-2, 2)
            self.time = pygame.time.get_ticks()
        if self.rev == 0:
            self.rect.x += self.speedx
        else:
            self.rect.x -= self.speedx
        self.rect.y += self.speedy

        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > H - 150:
            self.rect.y = H - 150

        if self.rect.x > W + 500 or self.rect.x < -500:
            self.kill()


def infinity_game():
    global wave, old_wave, score_count

    timer = pygame.time.get_ticks()
    stop = random.randint(0, 500)
    r = random.randint(0, 100)
    if r < 5:
        a = GiantEnemy()
    elif r < 45:
        a = KrabEnemy()
    else:
        a = MainEnemy()
    if timer + stop < pygame.time.get_ticks():
        print(wave, 1)
        enemy = a
        cost = enemy.cost
        if wave - cost >= 0:
            wave -= cost
            all_enemies.add(enemy)
            timer = pygame.time.get_ticks()
            stop = random.randint(0, 500)
        print(wave, 2)
    if wave <= 0:
        timer = pygame.time.get_ticks() + 1000
        old_wave *= 4
        wave = old_wave
    pygame.display.flip()


level_info = {1: {'chance': [[100, 1]], 'cost': 30, 'min': 10}, 2: {'chance': [[95, 1], [5, 20]], 'cost': 60, 'min': 25},
              3: {'chance': [[100, 5], [75, 5], [5, 20]], 'cost': 130, 'min': 50}}
level_copy = level_info


def levels(lvl):
    global level_copy, score_count
    timer = pygame.time.get_ticks()
    stop = random.randint(0, 700)
    r = random.randint(1, 100)
    a = 1
    for i in level_copy[lvl]['chance']:
        if r <= i[0]:
            a = i[1]
    if a == 1:
        enemy = MainEnemy()
    elif a == 20:
        enemy = GiantEnemy()
    elif a == 5:
        enemy = KrabEnemy()
    if timer + stop < pygame.time.get_ticks():
        if level_copy[lvl]['cost'] - a >= 0:
            level_copy[lvl]['cost'] -= a
            all_enemies.add(enemy)
            timer = pygame.time.get_ticks()
            stop = random.randint(0, 700)

    if level_copy[lvl]['cost'] <= 0 and not all_enemies:
        if score_count >= level_copy[lvl]['min']:
            game_over()
        else:
            rak.hp = 0
            rak.hp -= 100000000
            game_over()


def level_select():
    global selected_level
    title_text = font1.render('Выбор уровня:', True, BLACK)
    lvl1 = font1.render('1', True, BLACK)
    lvl2 = font1.render('2', True, BLACK)
    lvl3 = font1.render('3', True, BLACK)
    sp = []
    for i in range(3):
        sp.append(pygame.Rect(450 + 200 * i, 250, 180, 180))
        pygame.draw.rect(screen, (140, 100, 0), sp[i])
    screen.blit(title_text, (570, 50))
    screen.blit(lvl1, (530, 300))
    screen.blit(lvl2, (730, 300))
    screen.blit(lvl3, (930, 300))
    for i in sp:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if i.collidepoint(mouse_pos):
                selected_level = sp.index(i) + 1
                print(selected_level)
    pygame.display.flip()


def show_menu():
    global hopping_size, step_hopping_size
    font2 = pygame.font.Font(None, hopping_size)

    play_text = font1.render('Играть', True, BLACK)
    store_text = font1.render('Настройки', True, BLACK)
    quit_text = font1.render('Выход', True, BLACK)
    hopping_text = font2.render(hint, True, (255, 0, 0))
    rotated_text = pygame.transform.rotate(hopping_text, 20)
    selected = pygame.draw.rect(screen, (255, 0, 0), (600, 250 + 100 * move_selected, 10, 50))
    screen.blit(title, (400, 40))
    screen.blit(play_text, (650, 250))
    screen.blit(store_text, (650, 350))
    screen.blit(quit_text, (650, 450))
    screen.blit(rotated_text, (1000 - hopping_size * len(hint) * 0.01, 140 - hopping_size * len(hint) * 0.05))
    hopping_size = int((step_hopping_size ** 2) // 1) + 30
    step_hopping_size += 0.07
    if step_hopping_size // 1 >= 5:
        step_hopping_size = -5
    pygame.display.flip()


def select_game():
    title_text = font1.render('Режимы игры', True, BLACK)
    suj_text = font1.render('Сюжетный', True, BLACK)
    infi_text = font1.render('БЕСКОНЕЧНЫЙ!', True, BLACK)
    pvp_text = font1.render('Дуэль', True, BLACK)
    selected = pygame.draw.rect(screen, (255, 0, 0), (600, 250 + 100 * move_selected_game, 10, 50))
    screen.blit(title_text, (570, 50))
    screen.blit(suj_text, (650, 250))
    screen.blit(infi_text, (650, 350))
    screen.blit(pvp_text, (650, 450))
    pygame.display.flip()


def menu_loop():
    if cur_select == select[0]:
        show_menu()
    if cur_select == select[3]:
        print('Пока, спасибо что играли')
        pygame.quit()
        sys.exit()
    if cur_select == select[1]:
        if cur_select_game == '':
            select_game()
        if cur_select_game == 'сюжет':
            if selected_level == 0:
                level_select()
    if cur_select == select[2]:
        settings_menu()
    if cur_select == select[4]:
        game_over()


def game_over():
    global cur_select, cur_select_game, selected_level, score_count
    cur_select = select[4]
    cur_select_game = select_type_games[0]
    selected_level = 0
    screen.fill(BLACK)
    if rak.hp > 0:
        text = 'Вы выйграли! Ваш счёт:'
    else:
        text = 'Вы проиграли, ваш счёт:'
    screen.blit(font1.render(f'{text} {score_count}', True, (200, 10, 10)), (W // 2 - 350, H // 2 - 100))
    pygame.display.flip()


def kombo_check():
    cheat_code = [rak.up, rak.up, rak.down, rak.down, rak.left, rak.right, rak.left, rak.right, rak.ulpotato, rak.abikukles]
    triple_shot = [rak.left, rak.right, rak.shoot()]
    if last_moves == cheat_code:
        rak.hp += 500
        for i in range(10):
            rak.shoot(vy=5)
            rak.shoot(vy=4)
            rak.shoot(vy=3)
            rak.shoot(vy=2)
            rak.shoot(vy=1)
            rak.shoot(vy=-1)
            rak.shoot(vy=-2)
            rak.shoot(vy=-3)
            rak.shoot(vy=-4)
            rak.shoot(vy=-5)
        print('YOU CHEATER!!!')
    if last_moves[-3:] == triple_shot and rak.kd + 200 < pygame.time.get_ticks():
        rak.shoot(vy=4)
        rak.shoot(vy=-4)


def settings_menu():
    global hint, move_selected, cur_select, cur_select_game
    running = True
    selected_index = 0
    keys_to_change = list(keybindings.keys())

    while running:
        screen.blit(background, (0, 0))
        title_surface = font.render("Настройки", True, (0, 0, 0))
        screen.blit(title_surface, (W // 2 - title_surface.get_width() // 2, 50))

        # Отображение списка действий и кнопок
        for index, action in enumerate(keys_to_change):
            button_text = f"{action}: {keybindings[action]}"
            text_surface = font.render(button_text, True, (0, 0, 0))
            screen.blit(text_surface,
                        (W // 2 - 70,
                         100 + index * (30 + 10)))

            # Отображение красного прямоугольника слева от текста для выделения выбранного действия
            if index == selected_index:
                pygame.draw.rect(screen, (255, 0, 0),
                                 (W // 2 - 120,
                                  100 + index * 40 - 10,
                                  20,
                                  30 + 10),
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

                elif event.key == pygame.K_ESCAPE:
                    hint = random.choice(hints)
                    move_selected = 0
                    cur_select = select[0]
                    cur_select_game = select_type_games[0]
                    running = False

                elif event.key == pygame.K_SPACE:  # Кнопка подтверждения для переназначения
                    action_to_change = keys_to_change[selected_index]
                    keybindings[action_to_change] = "***"  # Заменяем на "***"

                    waiting_for_key = True

                    while waiting_for_key:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                waiting_for_key = False

                            if event.type == pygame.KEYDOWN:
                                new_key_name = pygame.key.name(event.key)
                                if event.key == pygame.K_SPACE:
                                    new_key_name = new_key_name.upper()
                                keybindings[action_to_change] = new_key_name  # Назначаем новую кнопку
                                waiting_for_key = False

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    with open('bd.json', 'w') as f:
        json.dump(keybindings, f)
    rak.keys_update()
    # Сохранение изменений в JSON файл перед выходом из меню настроек


all_bullets = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
rak = MainRak()
FPS = 60
game = True

while game:
    screen.blit(background, (0, 0))
    menu_loop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if cur_select_game == '':
                if cur_select == select[0]:
                    if event.key == pygame.K_DOWN:
                        move_selected = (move_selected + 1) % (len(select) - 2)
                    if event.key == pygame.K_UP:
                        move_selected = (move_selected - 1) % (len(select) - 2)
                    if event.key == pygame.K_SPACE:
                        cur_select = select[move_selected + 1]
                        print(cur_select)

                elif cur_select == select[1]:
                    if event.key == pygame.K_DOWN:
                        move_selected_game = (move_selected_game + 1) % (len(select_type_games) - 1)
                    if event.key == pygame.K_UP:
                        move_selected_game = (move_selected_game - 1) % (len(select_type_games) - 1)
                    if event.key == pygame.K_SPACE:
                        cur_select_game = select_type_games[move_selected_game + 1]
                        print(cur_select_game)
                        print(cur_select_game == select_type_games[2])
                        score_count = 0
                        wave = 10
                        rak.starting_game()

            if event.key == pygame.K_ESCAPE:
                rak.hp = 100
                hint = random.choice(hints)
                move_selected = 0
                cur_select = select[0]
                cur_select_game = select_type_games[0]
                selected_level = 0
                level_copy = level_info
                all_bullets.empty()
                all_enemies.empty()

            for i in range(len(last_moves)):
                try:
                    last_moves[i] = last_moves[i + 1]
                except IndexError:
                    last_moves[-1] = event.key
            kombo_check()

    if cur_select_game == select_type_games[2]:
        screen.blit(rak.image, rak.rect)
        all_enemies.draw(screen)
        all_bullets.draw(screen)
        pygame.draw.rect(screen, BLACK, (50, H - 80, 320, 70))
        pygame.draw.rect(screen, (200, 0, 0), (60, H - 70, 300, 50))
        pygame.draw.rect(screen, (0, 200, 40), (60, H - 70, 300 * rak.hp / rak.maxhp, 50))
        infinity_game()

    if cur_select_game == select_type_games[1] and selected_level != 0:
        screen.blit(rak.image, rak.rect)
        all_enemies.draw(screen)
        all_bullets.draw(screen)
        pygame.draw.rect(screen, BLACK, (50, H - 80, 320, 70))
        pygame.draw.rect(screen, (200, 0, 0), (60, H - 70, 300, 50))
        pygame.draw.rect(screen, (0, 200, 40), (60, H - 70, 300 * rak.hp / rak.maxhp, 50))
        levels(selected_level)

    rak.update()
    all_bullets.update()
    all_enemies.update()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
