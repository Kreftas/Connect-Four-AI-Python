from ai.settings import num_children, height_map
import numpy as np

horizontal = 7
vertical = 1
diagonal1 = 6
diagonal2 = 8
all_directions = [7, 1, 6, 8]


# T----------------------------------------------------------------------------------------------------------------- #
def evaluate_state(state, player):
    flipped_state = np.fliplr(state)
    sum_score = 0

    for h in range(height_map - 1, -1, -1):
        sum_score += calc_score(player, state[h])

    for h in range(num_children):
        sum_score += calc_score(player, state[:, h])

    for h in range(-2, 4):
        sum_score += calc_score(player, state.diagonal(h))
        sum_score += calc_score(player, flipped_state.diagonal(h))

    return int(sum_score)


def calc_score(player, state_slice):
    score = 0
    if player in state_slice:
        for x in range(len(state_slice) - 3):
            block = state_slice[x:x + 4]
            if (player * -1) not in block and player in block:
                result = np.sum(block == player)
                if result != 1:
                    score += pow(result, result)
    return score


# T----------------------------------------------------------------------------------------------------------------- #
def evaluate_game_over(player, depth):
    return (depth + 1) * 1000 * player


def game_over(state):
    return connected_four_check(state, 1) or connected_four_check(state, -1)


def connected_four_check(state, player):
    bitstring = to_bitstring_state(state, player)
    for direction in all_directions:
        map_check = bitstring & (bitstring >> direction)
        if map_check & (map_check >> (direction * 2)):
            return True
    return False


def to_bitstring_state(state, player):
    r = num_children - 1
    position = ''
    for j in range(r, -1, -1):
        position += '0'
        for i in range(0, r):
            position += ['0', '1'][state[i, j] == player]
    return int(position, 2)


# T----------------------------------------------------------------------------------------------------------------- #
