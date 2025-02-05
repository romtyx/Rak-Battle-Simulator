import pygame
import sys
import random
import time

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1500, 800))
pygame.display.set_caption('RAKBATTLESIMULATOR9999')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
background = ''

hopping_size = 10
step_hopping_size = -5
font1 = pygame.font.Font(None, 74)
select = ['', 'игра', 'настройки', 'выход']
select_type_games = ['', 'сюжет', 'бесконечный', 'дуэль']

hints = ['also try Zametki', 'also try SimpleDraw', 'some cheats: uuddLrLra1a2', 'a gde?', 'also try OГЭ по химии',
         'play PowerPoint', 'Ты сделал все уроки?', 'also try Яндекс Лицей', 'RAK', 'CANCER', 'Jq, yt nf hfcrkflrf',
         'MOM?', 'WE NEED 100$', 'Я сдам физику, честно', 'y = kx + b', 'Saratow2077', 'Roll D20', '3,14',
         'This sentence is a lie', 'Trust us', 'Wellcome to the underground', 'Hello World', 'Are you sure?', '(*)_(*)',
         'also try PyCharm', 'AAAAAAAAA', 'Plant B', 'bye', 'cake is a lie', 'spaceeeee...', 'also try Alt + f4']

hint = random.choice(hints)
cur_select = select[0]
cur_select_game = select_type_games[0]
move_selected = 0
move_selected_game = 0
last_moves = ['', '', '', '', '', '', '', '', '', '']
cheat_code = [119, 119, 115, 115, 97, 100, 97, 100, 113, 101]


class MainRak(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/просто рак.png").convert_alpha()
        scale = pygame.transform.scale(self.image, (150, 150))
        self.image = scale
        self.original_image = self.image
        # self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = 3
        self.x = 750
        self.y = 200
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
        self.kd = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.up]:
            self.y -= self.speed
        if keys[self.down]:
            self.y += self.speed
        if keys[self.left]:
            self.x -= self.speed
        if keys[self.right]:
            self.x += self.speed
            # self.rect = self.image.get_rect(center=(self.x, self.y))
            # print(self.rect)
            # print(self.x, self.y)
        if self.y >= 800:
            self.y = 800
        if self.y <= 0:
            self.y = 0
        if self.x >= 1500:
            self.x = 1500
        if self.x <= 0:
            self.x = 0

        if self.x > 675:
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.reverse = True
        else:
            self.image = self.original_image
            self.reverse = False

        if cur_select_game != select_type_games[0] and keys[self.shot] and self.kd + 500 < pygame.time.get_ticks():
            self.kd = pygame.time.get_ticks()
            self.shoot()

    def starting_game(self):
        self.x = 100
        self.y = 400

    def shoot(self):
        if self.reverse:
            bullet = Bullet(self.x, self.y + 75, -1)
        else:
            bullet = Bullet(self.x + 75, self.y + 75, 1)
        all_stars.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, rev):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/пуля просто рак.png").convert_alpha()
        scale = pygame.transform.scale(self.image, (100, 50))
        self.image = scale
        if rev == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        # self.speedx = 15 * rev
        self.speedx = 0
        self.rect = self.image.get_rect(center=(x, y))
        self.pseudo_rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > 1700:
            self.kill()
        screen.blit(self.image, self.rect)


def show_menu():
    global hopping_size, step_hopping_size
    font2 = pygame.font.Font(None, hopping_size)
    screen.fill(WHITE)
    title_text = font1.render('RAKBATTLESIMULATOR', True, BLACK)
    play_text = font1.render('Играть', True, BLACK)
    store_text = font1.render('Настройки', True, BLACK)
    quit_text = font1.render('Выход', True, BLACK)
    hopping_text = font2.render(hint, True, (0, 0, 255))
    rotated_text = pygame.transform.rotate(hopping_text, 20)
    selected = pygame.draw.rect(screen, (255, 0, 0), (600, 250 + 100 * move_selected, 10, 50))
    screen.blit(title_text, (440, 50))
    screen.blit(play_text, (650, 250))
    screen.blit(store_text, (650, 350))
    screen.blit(quit_text, (650, 450))
    screen.blit(rotated_text, (1000 - hopping_size * len(hint) * 0.01, 90 - hopping_size * len(hint) * 0.05))
    hopping_size = int((step_hopping_size ** 2) // 1) + 30
    step_hopping_size += 0.07
    if step_hopping_size // 1 >= 5:
        step_hopping_size = -5
    pygame.display.flip()


def select_game():
    screen.fill(WHITE)
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


def infinity_game():
    screen.fill(WHITE)
    screen.blit(rak.image, [rak.x, rak.y])
    pygame.display.flip()


all_stars = pygame.sprite.Group()
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
                        move_selected = (move_selected + 1) % (len(select) - 1)
                    if event.key == pygame.K_UP:
                        move_selected = (move_selected - 1) % (len(select) - 1)
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
                        rak.starting_game()

            if event.key == pygame.K_ESCAPE:
                hint = random.choice(hints)
                move_selected = 0
                cur_select = select[0]
                cur_select_game = select_type_games[0]

            for i in range(len(last_moves)):
                try:
                    last_moves[i] = last_moves[i + 1]
                except IndexError:
                    last_moves[-1] = event.key
            # print(last_moves)
            if last_moves == cheat_code:
                print('YOU CHEATER!!!')
    if cur_select_game == select_type_games[2]:
        infinity_game()
    rak.update()
    all_stars.update()
    pygame.display.flip()
    clock.tick(FPS)
