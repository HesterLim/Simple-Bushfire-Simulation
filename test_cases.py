from testcase_tournament import test_fn as test_run_model

# Write your test cases here

# Evaluated by running it on several known incorrect implementations, return an
# incorrect final state of the landscape and/or number of cells burnt

# Check when all the values are at base case
test_run_model([[[0, 0,0], [0, 0,0], [0,0,0]], [[1,1, 1], [1,1,1],[1,1,1]], 2, 
                None, [(0, 0)]],[[[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0])

# Check when i_threshold = 3 and all the fuel_load is 2
test_run_model([[[2, 2,2 ], [2, 2,2], [2,2,2]], [[1,1, 1], [1,1,1],[1,1,1]], 3
                , None, [(0, 0)]], [[[0, 2, 2], [2, 2, 2], [2, 2, 2]], 1])

# Check when there is a direction and a higher height
test_run_model([[[2,3,1], [4, 5,6], [3,2,3]], [[2,2, 5], [2,1,3],[2,3,4]], 2, 
                'N', [(0, 1),(1,2)]], [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], 9])

# Check when all surrounding has no fuel load
test_run_model([[[3, 0, 2], [0, 0, 2], [3, 2, 3]], [[2, 2, 2], [2, 2, 2],
                                                    [2, 2, 2]], 1, None, 
                [(0, 0)]], [[[0, 0, 2], [0, 0, 2], [3, 2, 3]], 1])

# Check when the burn_seeds is an empty list
test_run_model([[[2, 2], [2, 2]], [[1, 1], [1, 1]], 1, 'N', []], 
               [[[2, 2], [2, 2]], 0])

# Check when i_threshold is at its maximum which is 8
test_run_model([[[8, 3,3], [3, 3,8], [3,3,3]], [[2,2, 2], [2,2,2],[2,2,2]], 8, 
                None, [(0, 0),(1,2)]],[[[0, 3, 3], [3, 3, 0], [3, 3, 3]], 2])

# Check when h_grid is higher than burning cell and has a direction of North
test_run_model([[[1, 1,1], [1, 2,1], [1,1,1]], [[2,2, 2], [2,1,2],[2,2,2]], 2,
                'N', [(1, 1)]],[[[0, 0, 0], [0, 0, 0], [0, 0, 0]], 9])

# Check when h_grid is lower than burning cell's height and has no direction
test_run_model([[[1, 1,1], [1, 2,1], [1,1,1]], [[1,1, 1], [1,2,1],[1,1,1]], 2, 
                None, [(1, 1)]],[[[1, 1, 1], [1, 0, 1], [1, 1, 1]], 1])


    