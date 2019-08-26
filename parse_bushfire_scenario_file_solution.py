# Sample Solution 1
#
#   def parse_scenario(filename) returns a 
#
def parse_scenario(filename):
    # read file
    with open(filename) as f:
        # get size
        grid_size = int(f.readline())
        # get fuel load grid
        f_grid = []
        for i in range(grid_size):
            row = f.readline()
            f_grid.append([int(x) for x in row.strip().split(',')])
        # get height grid
        h_grid = []
        for i in range(grid_size):
            row = f.readline()
            h_grid.append([int(x) for x in row.strip().split(',')])
        # get ignition threshold
        i_threshold = int(f.readline())
        # get wind direction
        w_direction = f.readline().strip()
        if w_direction == 'None': 
            w_direction = None
        # get initial burning cells
        burn_seeds = []
        for row in f.readlines():
            x, y = [int(x) for x in row.strip().split(',')]
            burn_seeds.append((x, y))
    # validate values
    if i_threshold > 8 or i_threshold < 1:
        return None
    if w_direction not in ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'None']:
        return None
    for i, j in burn_seeds:
        if i > grid_size-1 or j > grid_size-1:
            return None
        if f_grid[i][j] < 1:
            return None
    return {'f_grid': f_grid, 'h_grid': h_grid,
        'i_threshold': i_threshold, 'w_direction': w_direction, 'burn_seeds': 
         burn_seeds}

# Smaple Solution 2

WIND_DIRECTIONS = {'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', None}


def is_valid(data):
    size = len(data['f_grid'])
    if data['i_threshold'] < 1 or data['i_threshold'] > 8:
        return False
    if data['w_direction'] not in WIND_DIRECTIONS:
        return False
    for r, c in data['burn_seeds']:
        if r < 0 or r >= size or c < 0 or c >= size:
            return False
        elif data['f_grid'][r][c] < 1:
            return False
    return True
  

def parse_scenario(filename):
    # Read the whole file.
    with open(filename) as f:
        lines = f.readlines()[::-1]

    # Extract the size of the grid.
    size = int(lines.pop())
    
    # Extract the initial fuel values for each cell in the grid.
    fuels = [list(map(int, lines.pop().split(','))) for r in range(size)]
    
    # Extract the height values for each cell in the grid.
    heights = [list(map(int, lines.pop().split(','))) for r in range(size)]
    
    # Extract the ignition threshold.
    ignition_threshold = int(lines.pop())
    
    # Extract the initial wind direction.
    wind_direction = lines.pop().strip()
    if wind_direction == 'None':
        wind_direction = None
    
    # Extract the grid locations for the cells that are initially burning.
    burning_cells = [tuple(map(int, line.split(','))) for line in lines[::-1]]
    
    # Validate the data and return appropriately.
    data = {
        'f_grid': fuels,
        'h_grid': heights,
        'i_threshold': ignition_threshold,
        'w_direction': wind_direction,
        'burn_seeds': burning_cells,
    }
    return data if is_valid(data) else None