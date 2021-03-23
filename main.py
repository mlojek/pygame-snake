import pygame
from random import randint

pygame.init()
pygame.font.init()

window = pygame.display.set_mode((600, 600))
pixel_font = pygame.font.Font('pixel_font.ttf', 50)
clock = pygame.time.Clock()
memory = open('high_score.txt', 'r')

snake = [[2, 2]]
length = 4
direction = 'd'
apple = [17, 17]

try:
    high_score = memory.readline()
    memory.close()
    high_score_int = int(high_score)
except ValueError:
    high_score = '0'
    high_score_int = 0


BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 255)
WHITE = (255, 255, 255)


def move(keys_pressed):
    global direction

    if(keys_pressed[pygame.K_w]) and not direction == 'd':
        direction = 'u'
    if(keys_pressed[pygame.K_s]) and not direction == 'u':
        direction = 'd'
    if(keys_pressed[pygame.K_a]) and not direction == 'r':
        direction = 'l'
    if(keys_pressed[pygame.K_d]) and not direction == 'l':
        direction = 'r'

    if direction == 'd':
        head = [snake[-1][0], (snake[-1][1] + 1) % 20]
    if direction == 'u':
        head = [snake[-1][0], (snake[-1][1] - 1) % 20]
    if direction == 'l':
        head = [(snake[-1][0] - 1) % 20, snake[-1][1]]
    if direction == 'r':
        head = [(snake[-1][0] + 1) % 20, snake[-1][1]]

    snake.append(head)

    if len(snake) > length:
        snake.pop(0)


def draw_snake(window, color):
    for element in snake:
        rect = pygame.Rect(element[0] * 30, element[1] * 30, 30, 30)
        pygame.draw.rect(window, color, rect)


def draw_apple(window, color):
    rect = pygame.Rect(apple[0] * 30, apple[1] * 30, 30, 30)
    pygame.draw.rect(window, color, rect)


def colission():
    for i in range(len(snake)):
        for j in range(i+1, len(snake)):
            if snake[i][0] == snake[j][0] and snake[i][1] == snake[j][1]:
                return True
    return False


def eat():
    global length
    if snake[-1] == apple:
        new_apple()
        length += 1


def new_apple():
    global apple
    while apple in snake:
        apple = [randint(0, 19), randint(0, 19)]


def main_menu():
    title = pixel_font.render('Pygame snake', True, WHITE, BLACK)
    title_rect = title.get_rect()
    title_rect.center = (300, 150)

    hs_txt = pixel_font.render('High score: ' + high_score, True, WHITE, BLACK)
    hs_rect = hs_txt.get_rect()
    hs_rect.center = (300, 200)

    play_text = pixel_font.render('PLAY!', True, WHITE, BLACK)
    play = play_text.get_rect()
    play.center = (300, 450)

    window.fill(BLACK)
    window.blit(title, title_rect)
    window.blit(hs_txt, hs_rect)
    window.blit(play_text, play)
    pygame.display.update()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if play.collidepoint(mouse_pos):
                    return


def pause_menu():
    pause = pixel_font.render('PAUSE MENU', True, WHITE, BLACK)
    pause_rect = pause.get_rect()
    pause_rect.center = (300, 150)

    score = pixel_font.render('Score: ' + str(length), True, WHITE, BLACK)
    score_rect = score.get_rect()
    score_rect.center = (300, 200)

    play = pixel_font.render('PLAY!', True, WHITE, BLACK)
    play_rect = play.get_rect()
    play_rect.center = (300, 450)

    window.fill(BLACK)
    window.blit(pause, pause_rect)
    window.blit(score, score_rect)
    window.blit(play, play_rect)
    pygame.display.update()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    return


def save_score():
    if length > high_score_int:
        save = open('high_score.txt', 'w')
        save.write(str(length))
        save.close()


def game():
    while True:
        run = True
        while run:
            clock.tick(length / 4 + 2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.set_caption(f'SNAKE    Score: {length}')
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_ESCAPE]:
                break

            move(keys_pressed)
            eat()
            if colission():
                return

            window.fill((0, 0, 0))
            draw_snake(window, WHITE)
            draw_apple(window, RED)
            pygame.display.update()
        pause_menu()


def game_over():
    save_score()
    window.fill((255, 255, 255))
    draw_snake(window, BLACK)
    draw_apple(window, BLUE)
    pygame.display.update()
    pygame.display.set_caption(f'GAME OVER    Score: {length}')

    pause = pixel_font.render('GAME OVER', True, WHITE, BLACK)
    pause_rect = pause.get_rect()
    pause_rect.center = (300, 150)

    score = pixel_font.render('Score: ' + str(length), True, WHITE, BLACK)
    score_rect = score.get_rect()
    score_rect.center = (300, 200)

    play = pixel_font.render('PLAY AGAIN!', True, WHITE, BLACK)
    play_rect = play.get_rect()
    play_rect.center = (300, 350)

    menu = pixel_font.render('MAIN MENU', True, WHITE, BLACK)
    menu_rect = menu.get_rect()
    menu_rect.center = (300, 400)

    window.blit(pause, pause_rect)
    window.blit(score, score_rect)
    window.blit(play, play_rect)
    window.blit(menu, menu_rect)
    pygame.display.update()
    
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    return True
                elif menu_rect.collidepoint(mouse_pos):
                    return False


def main():
    while True:
        main_menu()
        while True:
            game()
            if not game_over():
                break


if __name__ == "__main__":
    main()
