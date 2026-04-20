import numpy as np
import sys
sys.setrecursionlimit(30000)
def main():
    PLAYER = 'X' # CPU
    game = [
        ['_', 'O', '_'],
        ['O', '_', '_'],
        ['O', '_', 'X']
    ]
    lookup_table = {
        'X': 1,
        'O': -1,
    }
    # create state from game, with "_" as 0
    # and "X" as 1, "O" as -1
    state = [[lookup_table.get(col, 0) for col in row] for row in game]
    state = np.asarray(state, dtype=np.int8)
    data = []
    indices = np.where(state == 0) # find empty cells
    for row, col in zip(indices[0], indices[1]):
        state[row, col] = lookup_table[PLAYER]
        state_value = intermittent_state(state, -lookup_table[PLAYER])
        state[row, col] = 0 # reset the cell to empty
        data.append([(int(row), int(col)), state_value])
    for (row, col), val in data:
        print(f"Move at ({row}, {col}) → Score: {val}")
def intermittent_state(state, player=1):
    state = np.asarray(state, dtype=np.int8)
    indices = np.where(state == 0) # find empty cells
    no_move_remaining = indices[0].size == 0 # indices == [[], []]
    if no_move_remaining:
        return state_check(state)
    else:
        all_moves = [] 
        for row, col in zip(indices[0], indices[1]):
            state[row, col] = player
            all_moves.append(intermittent_state(state, -player))
            state[row, col] = 0 # reset the cell to empty
        return max(all_moves) if player == 1 else min(all_moves)
        
        
def state_check(state, print_result=False):
    arr = np.asarray(state, dtype=np.int8)
    column_check_ones = np.any(np.all(np.equal(arr, 1), axis=0))
    column_check_zeros = np.any(np.all(np.equal(arr, -1), axis=0))
    row_check_ones = np.any(np.all(np.equal(arr, 1), axis=1))
    row_check_zeros = np.any(np.all(np.equal(arr, -1), axis=1))
    principle_diag = np.diagonal(arr)
    secondary_diag = np.diagonal(np.fliplr(arr))
    diag_ones = np.all(principle_diag == 1) | np.all(secondary_diag == 1)
    diag_zeros = np.all(principle_diag == -1) | np.all(secondary_diag == -1)
    if print_result == True:
        if row_check_zeros:
            print("Zero Won in row match")
        elif row_check_ones:
            print("One Won in row match")
        elif column_check_zeros:
            print("Zero Won in column match")
        elif column_check_ones:
            print("One Won in column match")
        elif diag_zeros:
            print("Zero Won in diagonal")
        elif diag_ones:
            print("One Won in diagonal")
    zero_won = row_check_zeros | column_check_zeros | diag_zeros
    one_won = row_check_ones | column_check_ones | diag_ones
    if zero_won and one_won:
        return 0    
    elif one_won:
        return 1
    elif zero_won: # there was no need for this condition but it is here for clarity
        return -1 
main()