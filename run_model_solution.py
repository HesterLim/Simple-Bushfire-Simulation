# Sample Solution 1

from reference import check_ignition
#
#   def update_state(b_grid, f_grid, h_grid, i_threshold, w_direction) returns a 
#
def update_state(b_grid, f_grid, h_grid, i_threshold, w_direction):
    # create matrices to store next state
    b_grid_next = [[x for x in y] for y in b_grid]
    f_grid_next = [[x for x in y] for y in f_grid]
    ignitions = 0
    grid_size = len(b_grid)
    # update each cell in turn
    for i in range(grid_size):
        for j in range(grid_size):
            # handle fuel depletion
            if b_grid[i][j]:
                f_grid_next[i][j] -= 1
                # extinguish fire at (i, j) if fuel depleted
                if f_grid_next[i][j] == 0:
                    b_grid_next[i][j] = False
            # check for new ignitions
            else:
                new_ignition = check_ignition(b_grid, f_grid, h_grid, 
                                              i_threshold, w_direction, i, j)
                if new_ignition:
                    ignitions += 1
                    b_grid_next[i][j] = True
    return b_grid_next, f_grid_next, ignitions

def burning(b_grid):
    # check if any cells are burning
    r = [any(x) for x in b_grid]
    return any(r)

def run_model(f_grid, h_grid, i_threshold, w_direction, seed_cells):
    grid_size = len(f_grid)
    # initialise burn grid
    b_grid = [[False for _ in range(grid_size)] for _ in range(grid_size)]
    burnt_cells = 0
    for i, j in set(seed_cells):
        if f_grid[i][j] > 0:
            b_grid[i][j] = 1
            burnt_cells += 1
    # repeat updates while there is still fire present
    while burning(b_grid):
        b_grid, f_grid, ignitions = update_state(b_grid, f_grid, h_grid, i_threshold, w_direction)
        burnt_cells += ignitions
    return f_grid, burnt_cells

# Sample Solution 2

import copy
import itertools

from reference import check_ignition


def run_model(f_grid, h_grid, i_threshold, w_direction, burn_seeds):
    size = len(f_grid)
    
    # Keep a set of all (i, j) pairs that have been burnt by fire.
    burnt = set()

    # Compute the initial burn grid.
    b_grid = [[False] * size for _ in range(size)]
    for i, j in burn_seeds:
        b_grid[i][j] = True
        burnt.add((i, j))
    
    # Run the simulation while at least one cell is burning.
    while any(itertools.chain.from_iterable(b_grid)):
        new_b_grid = copy.deepcopy(b_grid)
        new_f_grid = copy.deepcopy(f_grid)
        
        # Work out what new cell should ignite.
        for i in range(size):
            for j in range(size):
                if check_ignition(b_grid, f_grid, h_grid,
                                  i_threshold, w_direction, i, j):
                    new_b_grid[i][j] = True
                    burnt.add((i, j))

        # Decrease fuel for all currently burning cells.
        for i in range(size):
            for j in range(size):
                if b_grid[i][j]:
                    new_f_grid[i][j] -= 1
                    if new_f_grid[i][j] == 0:
                        new_b_grid[i][j] = False
        
        # Update our burn state for the next iteration.
        b_grid = new_b_grid
        f_grid = new_f_grid

    return (f_grid, len(burnt))
    