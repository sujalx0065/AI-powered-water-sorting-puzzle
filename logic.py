from collections import deque
import copy

# AUTO DETECT CAPACITY

def get_capacity(state):
   
    return max(len(b) for b in state)

# GOAL CONDITION

def is_goal(state):

    CAPACITY = get_capacity(state)

    for bottle in state:

        # empty allowed
        if len(bottle) == 0:
            continue

        # must be full
        if len(bottle) != CAPACITY:
            return False

        # single colour only
        if len(set(bottle)) != 1:
            return False

    return True

# MOVE VALIDATION

def is_valid_move(state, src, dest):

    CAPACITY = get_capacity(state)

    if src == dest:
        return False

    source = state[src]
    target = state[dest]

    if len(source) == 0:
        return False

    if len(target) == CAPACITY:
        return False

    # colour mismatch
    if len(target) > 0 and source[-1] != target[-1]:
        return False

    return True

# POUR LOGIC

def pour(state, src, dest):

    CAPACITY = get_capacity(state)

    new_state = copy.deepcopy(state)

    source = new_state[src]
    target = new_state[dest]

    color = source[-1]

    # move same-colour block
    while source and source[-1] == color and len(target) < CAPACITY:
        target.append(source.pop())

    return new_state

# BFS AI SOLVER

def state_to_tuple(state):
    return tuple(tuple(b) for b in state)


def get_moves(state):

    moves = []
    n = len(state)

    for i in range(n):
        for j in range(n):
            if is_valid_move(state, i, j):
                moves.append((i, j))

    return moves


def solve_bfs(initial):

    queue = deque()
    visited = set() #Visited avoids repeated states

    queue.append((initial, []))
    visited.add(state_to_tuple(initial))

    while queue:

        state, path = queue.popleft()

        if is_goal(state):
            return path

        for move in get_moves(state):

            new_state = pour(state, move[0], move[1])
            key = state_to_tuple(new_state)

            if key not in visited:
                visited.add(key)
                queue.append((new_state, path + [move]))

    return None
