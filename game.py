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
select = ['', 'игра', 'магазин', 'выход']
hints = ['also try Zametki', 'also try SimpleDraw', 'some cheats: uuddLrLra1a2', 'a gde?', 'also try OГЭ по химии',
         'play PowerPoint', 'Ты сделал все уроки?', 'also try Яндекс Лицей', 'RAK', 'CANCER', 'Jq, yt nf hfcrkflrf',
         'MOM?', 'WE NEED 100$', 'Я сдам физику, честно', 'y = kx + b', 'Saratow2077', 'Roll D20', '3,14',
         'This sentence is a lie', 'Trust us', 'Wellcome to the underground', 'Hello World', 'Are you sure?', '(*)_(*)',
         'also try PyCharm']
hint = random.choice(hints)
cur_select = select[0]
move_selected = 0
last_moves = ['', '', '', '', '', '', '', '', '', '']
cheat_code = [119, 119, 115, 115, 97, 100, 97, 100, 113, 101]


def show_menu():
    global hopping_size, step_hopping_size
    font2 = pygame.font.Font(None, hopping_size)
    screen.fill(WHITE)
    title_text = font1.render('Главное Меню', True, BLACK)
    play_text = font1.render('Играть', True, BLACK)
    store_text = font1.render('Бесконечный режим', True, BLACK)
    quit_text = font1.render('Выход', True, BLACK)
    hopping_text = font2.render(hint, True, (0, 0, 255))
    rotated_text = pygame.transform.rotate(hopping_text, 20)
    selected = pygame.draw.rect(screen, (255, 0, 0), (600, 250 + 100 * move_selected, 10, 50))
    screen.blit(title_text, (570, 50))
    screen.blit(play_text, (650, 250))
    screen.blit(store_text, (650, 350))
    screen.blit(quit_text, (650, 450))
    screen.blit(rotated_text, (900 - hopping_size * len(hint) * 0.01, 90 - hopping_size * len(hint) * 0.05))
    hopping_size = int((step_hopping_size ** 2) // 1) + 30
    step_hopping_size += 0.07
    if step_hopping_size // 1 >= 5:
        step_hopping_size = -5
    pygame.display.flip()

# def infinite_game():
#     screen.blit()


def menu_loop():
    if cur_select == select[0]:
        show_menu()
    if cur_select == select[-1]:
        print('Пока, спасибо что играли')
        pygame.quit()
        sys.exit()
    if cur_select == select[2]:
        # infinite_game()
        pass


FPS = 60
game = True

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if cur_select == select[0]:
                if event.key == pygame.K_DOWN:
                    move_selected = (move_selected + 1) % (len(select) - 1)
                if event.key == pygame.K_UP:
                    move_selected = (move_selected - 1) % (len(select) - 1)
                if event.key == pygame.K_SPACE:
                    cur_select = select[move_selected + 1]
                    print(cur_select)
            if event.key == pygame.K_ESCAPE:
                hint = random.choice(hints)
                move_selected = 0
                cur_select = select[0]
            for i in range(len(last_moves)):
                try:
                    last_moves[i] = last_moves[i + 1]
                except IndexError:
                    last_moves[-1] = event.key
            print(last_moves)
            if last_moves == cheat_code:
                print('ax ty....')
    menu_loop()
    clock.tick(FPS)
