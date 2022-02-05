import random
import sys
import pygame
from pygame.locals import *
import numpy as np
from ai import evaluation as e
from ai import bonsai as b
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RESOLUTION_SCALE = 3  # 1 - 4
WINDOW_SIZE = (480 * RESOLUTION_SCALE, 300 * RESOLUTION_SCALE)

main_screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
pygame.display.set_caption("Connect four")
clock = pygame.time.Clock()

board = pygame.image.load('assets/ConnectFourBoard.png')
red = pygame.image.load('assets/marker_red_cropped.png')
yellow = pygame.image.load('assets/marker_yellow_cropped.png')
numbers = pygame.image.load('assets/board_numbers.png')

BOARD_OFFSET_X = 200
BOARD_OFFSET_Y = 50

TILE_OFFSET_X = 45
TILE_OFFSET_Y = 27

TILE_MOVE_X = 120
TILE_MOVE_Y = 114


def current_milli_time():
    return round(time.time() * 1000)


def update_state(state, move, turn):
    new_state = state
    testing = True
    worked = False
    index = new_state.size - 1 - (6 - move)
    while testing:
        if new_state.item(index) != 0:
            index += -7
            if index < 0:
                testing = False
        else:
            new_state.put(index, turn)
            worked = True
            testing = False
    return new_state, worked


def render(state):
    if state is None:
        return
    for x in range(7):
        for y in range(6):
            if state[y][x] == 1:
                put_tile(x, y, red)
            elif state[y][x] == -1:
                put_tile(x, y, yellow)


def put_tile(x, y, marker):
    pos_x = BOARD_OFFSET_X + TILE_OFFSET_X + (x * TILE_MOVE_X)
    pos_y = BOARD_OFFSET_Y + TILE_OFFSET_Y + (y * TILE_MOVE_Y)
    main_screen.blit(marker, (pos_x, pos_y))


def run():
    pygame.init()
    current_state = np.zeros((6, 7), dtype=int)
    game_over = False
    you_won = False

    # main_screen.blit(board, (BOARD_OFFSET_X, BOARD_OFFSET_Y))

    font = pygame.font.Font('freesansbold.ttf', 32)
    sub_font = pygame.font.Font('freesansbold.ttf', 20)

    your_turn = random.randint(0, 1)
    if your_turn:
        text = font.render('Your Turn', True, WHITE)
        subtext = sub_font.render('Press 0 - 6 to play', True, WHITE)
        played_text = sub_font.render(' ', True, WHITE)
    else:
        text = font.render('Opponent Turn', True, WHITE)
        subtext = sub_font.render('Waiting for Ai', True, WHITE)
        played_text = sub_font.render(' ', True, WHITE)

    while True:

        if not your_turn and not game_over:
            # T AI MOVE

            t1 = current_milli_time()
            move = b.run(current_state, -1)
            t2 = current_milli_time()
            print(f'Time = {t2 - t1}')

            current_state, valid = update_state(current_state, move, -1)
            text = font.render('Your Turn', True, WHITE)
            subtext = sub_font.render('Press 0 - 6 to play', True, WHITE)
            played_text = sub_font.render(f'AI played : {move}', True, WHITE)
            your_turn = True

        if e.game_over(current_state):
            game_over = True

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and your_turn:
                move = 10
                if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                    move = 0
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    move = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    move = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    move = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    move = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    move = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    move = 6

                if move != 10:
                    # T Student move
                    current_state, valid = update_state(current_state, move, 1)
                    if valid:
                        text = font.render('Opponent Turn', True, WHITE)
                        subtext = sub_font.render('Waiting for Ai', True, WHITE)
                        played_text = sub_font.render(f'You played : {move}', True, WHITE)
                        your_turn = False
                    else:
                        text = font.render('Invalid move', True, WHITE)
                        subtext = sub_font.render('Press 0 - 6 to play', True, WHITE)

                if e.game_over(current_state):
                    game_over = True
                    you_won = True

        if game_over:
            text = font.render('Game over', True, WHITE)
            if you_won:
                subtext = sub_font.render('You won', True, WHITE)
            else:
                subtext = sub_font.render('AI won', True, WHITE)
            played_text = sub_font.render('', True, WHITE)

        main_screen.fill((0, 0, 0, 0))
        main_screen.blit(board, (BOARD_OFFSET_X, BOARD_OFFSET_Y))
        render(current_state)
        main_screen.blit(numbers, (BOARD_OFFSET_X, 750))
        main_screen.blit(text, (1160, 200))
        main_screen.blit(subtext, (1160, 250))
        main_screen.blit(played_text, (1160, 300))
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    run()
