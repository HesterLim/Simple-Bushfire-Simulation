def check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, i, j):
    # TODO implement this function
    """ returns True if that cell will catch fire at time t + 1
        and False otherwise. """
    
    # Only cells that are located within the bounds of the land scape grid 
    # can contribute to a cell's ignition factore

    # initialise ignition_factor
    ignition_factor = 0
    
    # Find the coordinate of the cell that is burning
    burning_cells_list = []
    for burning_row_num in range(len(b_grid)):
        for burning_column_num in range(len(b_grid[burning_row_num])):
            if b_grid[burning_row_num][burning_column_num] is True:
                burning_cells = burning_row_num, burning_column_num
                burning_cells_list.append(burning_cells)
    
    # Find Cell i, j in f_grid's fuel_load
    fuel_i_j = f_grid[i][j]
    # print('fuel_i_j: ' + str(fuel_i_j))
    
    # List of all potential adjacent_cells to Cell i, j
    adjacent_cells = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), 
                      (i, j + 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]

    
    # Wind:
    # Carry burning that allows a fire to spread more rapidly in a particular 
    # direction, up to 3 additional cells are consider to be ajacent to cell 
    # for the purpose of calculatin its ignition factor
    
    # When considering the joint effects of height & wind, compare to heights 
    # of cells and each ots adjacent cells on a pairwise basis, disregarding 
    # the heights of any other surrounding ccells

    # Add additional adjacent cells based on direction given
    if w_direction == 'N':
        adjacent_cells.append((i - 2, j - 1))
        adjacent_cells.append((i - 2, j))
        adjacent_cells.append((i -2, j + 1))
    elif w_direction == 'NW':
        adjacent_cells.append((i - 1, j - 2))
        adjacent_cells.append((i - 2, j - 2))
        adjacent_cells.append((i - 2, j - 1))
    elif w_direction == 'W':
        adjacent_cells.append((i, j - 2))
        adjacent_cells.append((i - 1, j - 2))
        adjacent_cells.append((i + 1, j - 2))
    elif w_direction == 'SW':
        adjacent_cells.append((i + 1, j - 2))
        adjacent_cells.append((i + 2, j - 2))
        adjacent_cells.append((i + 2, j - 1))
    elif w_direction == 'S':
        adjacent_cells.append((i + 2, j - 1))
        adjacent_cells.append((i + 2, j))
        adjacent_cells.append((i + 2, j + 1))
    elif w_direction == 'SE':
        adjacent_cells.append((i + 2, j + 1))
        adjacent_cells.append((i + 2, j + 2))
        adjacent_cells.append((i + 1, j + 2))
    elif w_direction == 'E':
        adjacent_cells.append((i + 1, j + 2))
        adjacent_cells.append((i, j + 2))
        adjacent_cells.append((i - 1, j + 2))
    elif w_direction == 'NE':
        adjacent_cells.append((i - 1, j + 2))
        adjacent_cells.append((i - 2, j + 2))
        adjacent_cells.append((i - 2, j + 1))
       
    adjacent_burning_cells = []

    for adjacent_burning in adjacent_cells:
        if adjacent_burning in burning_cells_list:
            adjacent_burning_cells.append(adjacent_burning)
   
    # Height:
    # If a cell has height greter than that if adjacent burning cell, 
    # that cell will contribute twice as much to the ignition factor


    # Find the height of the burning cells
    height_ij = h_grid[i][j]
    for h_row_num in range(len(h_grid)):
        for h_column_num in range(len(h_grid[h_row_num])):
            h_cell = (h_row_num, h_column_num)
            if h_cell in adjacent_burning_cells:
                if height_ij > h_grid[h_row_num][h_column_num]:
                    ignition_factor +=  1 *  2
                elif height_ij < h_grid[h_row_num][h_column_num]:
                    ignition_factor += 1 / 2
                else:
                    ignition_factor += 1
                
    # a cell will catch fire if its ignition factor is greater than or equal to 
    # the ignition threshold. A cell must be currently not burning and have a 
    # fuel load greater than 0 (zero) in order to catch fire
    burn_cell = b_grid[i][j]
    if ignition_factor >= i_threshold and fuel_i_j > 0 and burn_cell is False:
        return True
    else:
        return False
            
    pass