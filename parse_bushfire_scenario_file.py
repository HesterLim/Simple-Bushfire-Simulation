def parse_scenario(filename):
    # TODO implement this function
    """ parses a file with the structure described below, validates the 
    contents and returns either a dictionary containing all values required 
    to specify a model scenario if the contents are valid, or None if any of 
    the contents are invalid."""
    
    import csv

    file_object = open(filename)
    reader = csv.reader(file_object)
    
    data = list(reader)
    len_of_file = len(data)
    
    # Initialise a dictionary
    result = {}
    
    # Specify the width and height (M) of the square landscape grid
    # Check M is a positive integer
    if int(data[0][0]) > 0:
        m = int(data[0][0])
    else:
        return None
    
    # Check the dimensions of the f_grid are a positive integer
    # & Each row has a length = M
    for row_grid in range(1, m + 1):
        for i_f_load in data[row_grid]:
            if int(i_f_load) >= 0 and len(data[row_grid]) == m:
                pass
            else: 
                return None
    
    # Once checked, put into f_grid and into dict
    f_grid = []
    for row_grid in range(1, m + 1):
        inside_f_grid = []
        for i_f_load in data[row_grid]:
            inside_f_grid.append(int(i_f_load))
        f_grid.append(inside_f_grid)
    result['f_grid'] = f_grid
    
    # Check the dimensions of h_grid are a positive integer
    # & Each row has a length = M
    for row_grid in range(m + 1, m * 2 + 1):
        for height in data[row_grid]:
            if int(height) >= 0 and len(data[row_grid]) == m:
                pass
            else:
                return None
            
    # Once checked, put into h_grid
    h_grid = []
    for row_grid in range(m + 1, m * 2 + 1):
        inside_h_grid = []
        for height in data[row_grid]:
            inside_h_grid.append(int(height))
        h_grid.append(inside_h_grid)
    result['h_grid'] = h_grid
    
    count_i_threshold = m * 2 + 1
    # Check the ignition threshold is a positive integer, not greater than 8
    if 0 < int(data[count_i_threshold][0]) <= 8:
        result['i_threshold'] = int(data[count_i_threshold][0])
    else:
        return None
    
    # Check the wind direction is valid and the wind direction is None if there
    # is no wind
    count_w_direction = count_i_threshold + 1
    wind_directions = ['SW', 'S', 'SE', 'E', 'NE', 'N', 'NW', 'W']
    if data[count_w_direction][0] == 'None':
        result['w_direction'] = None
    elif data[count_w_direction][0].upper() in wind_directions:
        result['w_direction'] = data[count_w_direction][0].upper()
    else:
        return None
    
    # Check the coordinates of the burning cells:
    # (a) located on the landscape
    # (b) have non-zero intial fuel load
    
    # (a) By checking that the coordinate is a positive integer and less 
    # than M. And also the length of a row should be 2
    count_burn_seeds = count_w_direction + 1
    for row_grid in range(count_burn_seeds, len_of_file):
        for cell in data[row_grid]:
            if 0 <= int(cell) < m:
                pass
            else:
                return None
    
    # (b) By checking the values in f_grid is bigger than 0
    check_burn_seeds = []
    for row_grid in range(count_burn_seeds, len_of_file):
        check_inside_burn_seeds = []
        for f_load in data[row_grid]:
            check_inside_burn_seeds.append(int(f_load))
        check_burn_seeds.append(tuple(check_inside_burn_seeds))
     
    for f_load in range(len(check_burn_seeds)):
        i = check_burn_seeds[f_load][0]
        j = check_burn_seeds[f_load][1]
        if result['f_grid'][i][j] > 0:
            pass
        else: 
            return None
                
    # Once checked put it into the dict
    burn_seeds = []
    for row_grid in range(count_burn_seeds, len_of_file):
        inside_burn_seeds = []
        for cell in data[row_grid]:
            inside_burn_seeds.append(int(cell))
        burn_seeds.append(tuple(inside_burn_seeds))
    result['burn_seeds'] = burn_seeds
        
    return result