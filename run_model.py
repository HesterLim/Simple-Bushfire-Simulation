from reference import check_ignition

# Add functions that carry out a single step of the mode;
# determining the new burning state and fuel load at time t + 1
def b_state_fuel(ij_list, cell_burnt_dict, cell_burnt, b_grid, f_grid, h_grid,
                 i_threshold, w_direction, burn_seeds):
    """ Update all the burning states of the cell & fuel load for t + 1 and 
        also check if it will ignite to prepare for updating the 
        burning states of cell & fuel load of the cell for t + 2 onwards"""
    
    # Loop through all the coordinates and determine the new burning state
    # and fuel load
    for coordinates in ij_list:
        i = coordinates[0]
        j = coordinates[1]
        
        # Get the original f_grid before looping for comparison later 
        # To compare whether the f_grid has changed value 
        original_f_grid = f_grid[i][j]
        
        # Check for each coordinates whether it will ignite
        result = check_ignition(b_grid, f_grid, h_grid, i_threshold, 
                                w_direction, i, j)
        
        # For burning cells that are still burning and fuel load more than 0
        # - 1 its value. AND if the burning cell is still burning and no more
        # fuel load then burning cell should stop burning
        if b_grid[i][j] is True and f_grid[i][j] > 0:
            f_grid[i][j] -= 1
        elif b_grid[i][j] is True and f_grid[i][j] == 0:
            b_grid[i][j] = False
        
  
        
        # If the cell ignites and has a fuel load of more than 0
        # then we will set the burning cell to burn for t + 1
        # and if the cell ignites but no more fuel load, the burning cell 
        # should not burn anymore
        
        # If the cell fails to ignite and the fuel_load values change which 
        # means the burning cell is still burning
        if result is True:
            # if the cell has not be burned before then add it as burned cell
            if cell_burnt_dict[(i, j)] is False and b_grid[i][j] is False:
                    cell_burnt += 1
                    cell_burnt_dict[(i, j)] = True
            if f_grid[i][j] > 0:
                b_grid[i][j] = True
            elif f_grid[i][j] == 0:
                b_grid[i][j] = False
                
        elif result is False:
            if original_f_grid != f_grid[i][j] and f_grid[i][j] > 0:
                b_grid[i][j] = True
                

    return f_grid, cell_burnt, b_grid



def run_model(f_grid, h_grid, i_threshold, w_direction, burn_seeds):

    # Get a list of all the possible coordinates
    ij_list = []
    for i in range(len(f_grid)):
        for j in range(len(f_grid[i])):
            ij = i, j
            ij = tuple(ij)
            ij_list.append(ij)
    # print(ij_list)
                
    # Make a grid of burning state of each cell based on boolean values
    # Make a dict of each coordinates of cell_burnt assigned to a value so that
    # u dont -= 1 mutliple times when going through each loop
    cell_burnt = 0
    b_grid = []
    cell_burnt_dict = {}
    cell_burnt = 0
    total_no_coordinates = 0
    for row_num in range(len(f_grid)):
        b_grid_list = []
        for column_num in range(len(f_grid[row_num])):
            total_no_coordinates += 1
            i = row_num
            j = column_num
            if (i, j) in burn_seeds and f_grid[i][j] > 0:
                b_grid_list.append(True)
                
                cell_burnt_dict[(i, j)] = True
                cell_burnt += 1
            else:
                b_grid_list.append(False)
                
                cell_burnt_dict[(i, j)] = False
        b_grid.append(b_grid_list)
    
    # print('Cell_burnt before entering the function: ' + str(cell_burnt))
    # print('Total number of coordinates: ' + str(total_no_coordinates))
    
    # If one of the burning cells still burning then continue loop till
    # all the cells stop burning
    still_burning = True
    while still_burning is True:
        result = b_state_fuel(ij_list, cell_burnt_dict, cell_burnt, b_grid,
                              f_grid, h_grid, i_threshold, 
                              w_direction, burn_seeds)
        cell_burnt = result[1]
        b_grid = result[2]
        
        count = 0
        
        # If all burning cells are not burning then stop the loop
        for row_num in range(len(b_grid)):
            for column_num in range(len(b_grid[row_num])):
                i = row_num
                j = column_num
                if b_grid[i][j] is False:
                    count += 1
                    if count == total_no_coordinates:
                        still_burning = False
                    else:
                        still_burning = True
        # print(result[0],result[1])     
        
    return result[0], result[1]