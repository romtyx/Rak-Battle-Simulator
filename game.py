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
select = ['', 'игра', 'настройки', 'выход', 'game_over']
select_type_games = ['', 'сюжет', 'бесконечный', 'дуэль']

hints = ['also try Zametki', 'also try SimpleDraw', 'some cheats: uuddLrLra1a2', 'a gde?', 'also try OГЭ по химии',
         'play PowerPoint', 'Ты сделал все уроки?', 'also try Яндекс Лицей', 'RAK', 'CANCER', 'Jq, yt nf hfcrkflrf',
         'MOM?', 'WE NEED 100$', 'Я сдам физику, честно', 'y = kx + b', 'Saratow2077', 'Roll D20', '3,14',
         'This sentence is a lie', 'Trust us', 'Wellcome to the underground', 'Hello World', 'Are you sure?', '(*)_(*)',
         'also try PyCharm', 'AAAAAAAAA', 'Plant B', 'bye', 'cake is a lie', 'spaceeeee...', 'also try Alt + f4',
         'power of 3 is Lr shot']

hint = random.choice(hints)
cur_select = select[0]
cur_select_game = select_type_games[0]
move_selected = 0
move_selected_game = 0
last_moves = ['', '', '', '', '', '', '', '', '', '']
cheat_code = [119, 119, 115, 115, 97, 100, 97, 100, 113, 101]
triple_shot = [97, 100, 32]
infinity_count = 0
wave = 10
old_wave = wave


class MainRak(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/просто рак.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 3
        self.maxhp = 100
        self.hp = 100
        self.scale = 50
        self.up = pygame.K_w
        self.down = pygame.K_s
        self.left = pygame.K_a
        self.right = pygame.K_d
        self.shot = pygame.K_SPACE
        self.abikukles = pygame.K_e
        self.ulpotato = pygame.K_q
        self.reverse = False
        self.kd = pygame.time.get_ticks() + 500
        self.gif = pygame.time.get_ticks()
        self.cgif = 0

    def update(self):
        global infinity_count
        if self.hp <= 0:
            game_over(infinity_count)
        keys = pygame.key.get_pressed()
        if keys[self.up]:
            self.rect.y -= self.speed
        if keys[self.down]:
            self.rect.y += self.speed
        if keys[self.left]:
            self.rect.x -= self.speed
        if keys[self.right]:
            self.rect.x += self.speed
            # self.rect = self.image.get_rect(center=(self.x, self.y))
            # print(self.rect)
            # print(self.x, self.y)
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

        # bullets_hits = pygame.sprite.groupcollide(all_bullets, all_enemies, True, False)
        # bullets_hits_mask = pygame.sprite.collide_mask()

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
        global infinity_count
        self.rect.x += self.speedx
        self.rect.y += self.vy
        if self.rect.left > W or self.rect.right < 0 or self.rect.bottom < 0 or self.rect.top > H:
            self.kill()

        for e in all_enemies:
            if pygame.sprite.collide_mask(self, e):
                e.hp -= 5
                self.kill()
                if e.hp <= 0:
                    infinity_count += e.cost
                    print(infinity_count)
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
        self.hp = 10
        self.cur_hp = self.hp
        self.speed = 2

    def update(self):
        if self.rev == 0:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.rect.x > W + 500 or self.rect.x < -500:
            self.kill()


class Giant(MainEnemy):
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
        self.hp = 50
        self.speed = 1

    def update(self):
        if self.rev == 0:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.rect.x > W + 1000 or self.rect.x < -1000:
            self.kill()


def infinity_game():
    global wave, old_wave, infinity_count
    screen.fill(WHITE)
    screen.blit(background, (0, 0))

    screen.blit(rak.image, rak.rect)
    all_enemies.draw(screen)
    all_bullets.draw(screen)
    # я понял что рект это ТОЧНО верхний левый угол картинки
    pygame.draw.rect(screen, BLACK, (50, H - 80, 320, 70))
    pygame.draw.rect(screen, (200, 0, 0), (60, H - 70, 300, 50))
    pygame.draw.rect(screen, (0, 200, 40), (60, H - 70, 300 * rak.hp / rak.maxhp, 50))
    pygame.display.flip()

    timer = pygame.time.get_ticks()
    stop = random.randint(0, 500)
    r = random.randint(0, 100)
    if r < 5:
        a = Giant()
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


def show_menu():
    global hopping_size, step_hopping_size
    font2 = pygame.font.Font(None, hopping_size)
    screen.fill(WHITE)
    screen.blit(background, (0, 0))

    # title_text = font1.render('RAKBATTLESIMULATOR', True, BLACK)
    play_text = font1.render('Играть', True, BLACK)
    store_text = font1.render('Настройки', True, BLACK)
    quit_text = font1.render('Выход', True, BLACK)
    hopping_text = font2.render(hint, True, (255, 0, 0))
    rotated_text = pygame.transform.rotate(hopping_text, 20)
    selected = pygame.draw.rect(screen, (255, 0, 0), (600, 250 + 100 * move_selected, 10, 50))
    # screen.blit(title_text, (440, 50))
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
    screen.fill(WHITE)
    screen.blit(background, (0, 0))
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
    if cur_select == select[2]:
        pass


def game_over(score):
    global cur_select, cur_select_game
    cur_select = select[4]
    cur_select_game = select_type_games[0]
    screen.fill(BLACK)
    screen.blit(font1.render(f'Вы умерли, ваш счёт: {score}', True, (200, 10, 10)), (W // 2 - 350, H // 2 - 100))


def kombo_check():
    if last_moves == cheat_code:
        rak.hp += 10000
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


all_bullets = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
rak = MainRak()
FPS = 60
game = True

while game:
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
                        infinity_count = 0
                        wave = 10
                        rak.starting_game()

            if event.key == pygame.K_ESCAPE:
                rak.hp = 100
                hint = random.choice(hints)
                move_selected = 0
                cur_select = select[0]
                cur_select_game = select_type_games[0]
                all_bullets.empty()
                all_enemies.empty()

            for i in range(len(last_moves)):
                try:
                    last_moves[i] = last_moves[i + 1]
                except IndexError:
                    last_moves[-1] = event.key
            print(last_moves)
            kombo_check()
    if cur_select_game == select_type_games[2]:
        infinity_game()
    rak.update()
    all_bullets.update()
    all_enemies.update()
    pygame.display.flip()
    clock.tick(FPS)
