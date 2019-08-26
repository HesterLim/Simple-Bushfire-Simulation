# Sample Solution 1
# ignition factors
UPHILL = 2
DOWNHILL = 0.5

def check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, i, j):
    # False if no fuel at (i, j) or (i, j) already burning
    if b_grid[i][j] or not f_grid[i][j]:
        return False
    
    # neighbouring cells
    n_list = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    # supplement neighbour list based on wind direction
    if w_direction == 'N':
        n_list += [(-2, -1), (-2, 0), (-2, 1)]
    elif w_direction == 'NE':
        n_list += [(-2, 1), (-2, 2), (-1, 2)]
    elif w_direction == 'E':
        n_list += [(-1, 2), (0, 2), (1, 2)]
    elif w_direction == 'SE':
        n_list += [(1, 2), (2, 2), (2, 1)]   
    elif w_direction == 'S':
        n_list += [(2, 1), (2, 0), (2, -1)]
    elif w_direction == 'SW':
        n_list += [(2, -1), (2, -2), (1, -2)]  
    elif w_direction == 'W':
        n_list += [(-1, -2), (0, -2), (1, -2)]  
    elif w_direction == 'NW':
        n_list += [(-1, -2), (-2, -2), (-2, -1)]   
    else:
        pass  # no (valid) wind direction
    
    # get size
    grid_size = len(b_grid)
    
    # calculate ignition factor 
    i_factor = 0
    for (d_i, d_j) in n_list:
        # check neighbour is on the grid
        if not (0 <= i + d_i < grid_size and 0 <= j + d_j < grid_size):
            continue
        # fire spreading uphill
        if h_grid[i + d_i][j + d_j] < h_grid[i][j]:
            i_factor += UPHILL * b_grid[i + d_i][j + d_j]
        # fire spreading downhill
        elif h_grid[i + d_i][j + d_j] > h_grid[i][j]:
            i_factor += DOWNHILL * b_grid[i + d_i][j + d_j]
        # fire spreading on level
        else:
            i_factor += b_grid[i + d_i][j + d_j]

    return i_factor >= i_threshold

# Sample Solution 2

WIND_DIRECTION_DELTAS = {
    'N': [(-2, -1), (-2, 0), (-2, 1)],
    'NE': [(-2, 1), (-2, 2), (-1, 2)],
    'E': [(-1, 2), (0, 2), (1, 2)],
    'SE': [(1, 2), (2, 2), (2, 1)],
    'S': [(2, 1), (2, 0), (2, -1)],
    'SW': [(1, -2), (2, -2), (2, -1)],
    'W': [(-1, -2), (0, -2), (1, -2)],
    'NW': [(-2, -1), (-2, -2), (-1, -2)],
    None: [],

}

MOVE_DELTAS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1),
]

# ignition factors
UPHILL = 2.0
LEVEL = 1.0
DOWNHILL = 0.5

def check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, i, j):
    # If the cell is currently burning, bail.
    if b_grid[i][j]:
        return False
      
    # If the cell has no fuel, bail.
    if f_grid[i][j] == 0:
        return False

    # Work out the cells we need to check relative to the given cell.
    deltas = list(MOVE_DELTAS)
    if w_direction != '0':
        deltas += WIND_DIRECTION_DELTAS[w_direction]
    
    # Compute the ignition factor.
    i_factor = 0.0
    size = len(b_grid)
    for di, dj in deltas:
        # Compute the i, j value of the new cell.
        ni, nj = i + di, j + dj

        # Ensure that new cell is on the grid and that it's currently burning.
        if ni < 0 or ni >= size or nj < 0 or nj >= size:
            continue
        elif not b_grid[ni][nj]:
            continue
        
        # Account for the height differential between cells.
        dh = h_grid[ni][nj] - h_grid[i][j]
        if dh == 0:
            i_factor += LEVEL
        elif dh < 0:
            i_factor += UPHILL
        else:
            i_factor += DOWNHILL
    
    return i_factor >= i_threshold