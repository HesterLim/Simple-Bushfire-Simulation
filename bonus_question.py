# Sample Solution 

from collections import defaultdict
from hidden import check_ignition, update_state, run_model

# valid wind directions
w_dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', None]

def test_burn(f_grid, h_grid, i_threshold, town_cell):
    '''
    Run all possible prescribed burns on a landscape containing a town,
    returning a dictionary of valid prescribed burn cells, together with the 
    fuel load following that burn.
    '''
    grid_size = len(f_grid)
    town_i, town_j = town_cell
    
    # maps valid prescribed burn cells to the subsequent fuel load matrix.
    valid_burns = {}

    # test prescribed burn from each valid starting cell
    for i in range(grid_size):
        for j in range(grid_size):
            cur_seed = (i, j)
            # skip town cell, and cells with zero fuel load
            if cur_seed == town_cell or f_grid[i][j] == 0:
                continue
                
            # test prescribed burn
            new_f_grid, burnt = run_model(f_grid, h_grid, 
                                          i_threshold * 2, None, [cur_seed])
            # if town did not catch fire, add seed to valid burn cell dictionary
            if new_f_grid[town_i][town_j] == f_grid[town_i][town_j]:
                valid_burns[(cur_seed)] = new_f_grid
            
    return valid_burns

def test_fire(f_grid, h_grid, i_threshold, town_cell):
    '''
    evaluate all possible bushfires (each starting cell, except town, and 
    each wind direction), returning the proportion of scenarios in which
    the town was burnt
    '''
    grid_size = len(f_grid)
    town_i, town_j = town_cell
    
    # store True if town burnt, otherwise False
    town_burnt = []
    
    # test each starting cell
    for i in range(grid_size):
        for j in range(grid_size):
            # skip town cell, and cells with zero fuel load
            if (i, j) == town_cell or f_grid[i][j] == 0:
                continue
                
            # test each wind direction
            for cur_w_dir in w_dirs:
                new_f_grid, burnt = run_model(f_grid, h_grid, 
                                              i_threshold, cur_w_dir, [(i, j)])
                # keep track of whether town was burnt
                town_burnt.append(new_f_grid[town_i][town_j] 
                                  < f_grid[town_i][town_j])

    if town_burnt:
        return sum(town_burnt) / len(town_burnt)
    else:
        return 0


def plan_burn(f_grid, h_grid, i_threshold, town_cell):
    '''
    determine the optimal cells in which to conduct a prescribed burn in order
    to reduce the probability of a future bushfire burning the town cell.
    '''
    # determine valid burn cells
    valid_burns = test_burn(f_grid, h_grid, i_threshold, town_cell)
    
    # build dictionary mapping burn scores to burn seeds
    burn_scores = defaultdict(list)

    # calculate burn score for each valid burn cell
    for cur_seed, cur_f_grid in valid_burns.items():
        cur_burnt = test_fire(cur_f_grid, h_grid, i_threshold, town_cell)
        burn_scores[cur_burnt].append(cur_seed)
        
    # sort burn scores, sort seeds for each burn score, 
    # and return list of optimal burn seeds
    if burn_scores:
        return [sorted(burn_scores[k]) for k in sorted(burn_scores)][0]
    else:
        return []


