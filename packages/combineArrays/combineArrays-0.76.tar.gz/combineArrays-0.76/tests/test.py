import numpy as np
import math
from combineArrays import replicate_arrays
from combineArrays import calc_distance
from combineArrays import centroid_aux

def print_test_result( res, exp_res):
    print( "result: ", res)
    
    if np.array_equal( res, exp_res):
        print( "pass")
    else:
        print( "fail")
    

# test replicate_arrays()
# expected result: 4, 5, 6, 4, 5, 6, 4, 5, 6
a = np.array([4,5,6])
n = 3
# y = np.zeros( n * a.size)
print( "- test replicate_arrays()")
y = replicate_arrays( a, n)
exp_res = np.array([4, 5, 6, 4, 5, 6, 4, 5, 6])
print_test_result( y, exp_res)

# test clac_distance()
# expected result: 0.5662, 2.46048, 0.16181, 2.26403
a_x_u = np.array([-38.4, -38.2])
a_y_u = np.array([140.7, 141.4])
b_x = np.array([-38.2444, -35.9639])
b_y = np.array([141.2444, 141.0455])
# dist = np.zeros( a_x_u.size * b_x.size)
print("test clac_distance()")
dist = calc_distance( a_x_u, a_y_u, b_x, b_y)
exp_res = np.array([0.5662, 2.46048, 0.16181, 2.26403])
dist = np.around( dist, 5)
print_test_result( dist, exp_res)

# test centroid_aux()
# expected result: -36.1923, -38,
num_b = 2
# a_demand = np.array([1.1, 2.1, 3.1])
# ov_allocation_u_b = np.array([0, 1, 1, 0, 1, 0])
# a_coordinate_u = np.array([-38, -35, -37])
a_demand = np.array([1.0, 2.0, 3.0])
ov_allocation_u_b = np.array([0, 1, 1, 0, 1, 0])
a_coordinate_u = np.array([1.0, -1.0, 2.0])


# coo_b = np.zeros( num_b)
print( "test centroid_aux()")
coo_b = centroid_aux( a_demand, ov_allocation_u_b, a_coordinate_u)
# exp_res = np.array([-36.1923, -38])
exp_res = np.array([0.8, 1.0])
coo_b = np.around( coo_b, 4)
print_test_result( coo_b, exp_res)






