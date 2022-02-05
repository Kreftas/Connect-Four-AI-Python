import numpy as np
import random
import math
from ai import evaluation as e
from ai.settings import depth, num_children, pruning


# T----------------------------------------------------------------------------------------------------------------- #
def run(game_state, player):
    state = invert_state(game_state, player)
    root = Bonsai_Leaf(state)
    max_eval = minimax(root, depth, -math.inf, math.inf, True)
    return choose_child(root, max_eval, state)


def invert_state(state, player):
    if player != 1:
        s = state
        s = np.where(s == 1, 3, s)
        s = np.where(s == -1, 1, s)
        s = np.where(s == 3, -1, s)
        return s
    else:
        return state


def choose_child(root, max_eval, state):
    children_alive = av_moves(state)
    num = 0
    possibles = []
    for child in root.children:
        if num in children_alive:
            if child.score == max_eval:
                possibles.append(num)
        num += 1
    rand = random.randint(0, len(possibles) - 1)
    return possibles[rand]


def av_moves(state):
    children_alive = []
    for x in range(len(state[0])):
        if state[0][x] == 0:
            children_alive.append(x)
    return children_alive


# T----------------------------------------------------------------------------------------------------------------- #
def minimax(leaf, depth, alpha, beta, maximizing_player):
    player = [1, -1][maximizing_player]
    if depth == 0:
        leaf.score = e.evaluate_state(leaf.state, player)
        return leaf.score
    elif e.game_over(leaf.state):
        leaf.score = e.evaluate_game_over(player, depth)
        return leaf.score

    if maximizing_player:
        max_eval = -math.inf
        for child in create_children(leaf, 1):
            evaluation = minimax(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, evaluation)
            if max_eval > beta and pruning:
                break
            alpha = max(alpha, max_eval)
        leaf.score = max_eval
        return max_eval

    else:
        min_eval = math.inf
        for child in create_children(leaf, -1):
            evaluation = minimax(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, evaluation)
            if min_eval < alpha and pruning:
                break
            beta = min(beta, min_eval)
        leaf.score = min_eval
        return min_eval


def create_children(child, turn):
    new_children = []
    for x in range(num_children - 1, -1, -1):
        new_state = create_child_state(child, x, turn)
        new_children.append(Bonsai_Leaf(new_state))
    child.children = new_children
    return new_children


def create_child_state(child, x, turn):
    new_state = child.state.copy()
    testing = True
    index = new_state.size - 1 - x
    while testing:
        if new_state.item(index) != 0:
            index += -num_children
            if index < 0:
                testing = False
        else:
            new_state.put(index, turn)
            testing = False
    return new_state


# T----------------------------------------------------------------------------------------------------------------- #
class Bonsai_Leaf:
    score: int = 0
    children = []

    def __init__(self, state):
        self.state = state
        self.score = 0

    def add_children(self, children):
        self.children = children

    def __repr__(self):
        return str(self.score)


# T----------------------------------------------------------------------------------------------------------------- #
