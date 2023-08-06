# Funtions to combine NumPy arrays in C++ 
import numpy as np
from _libCombineArrays import lib
from cffi import FFI
ffi = FFI()



# Replicate the array n_times and return an array which shape is (length_ary * n_times)
# Example:
# a_lat_b = [4, 5]
# result = replicate_array(a_lat_b,3) -> result = [4, 5, 4, 5, 4, 5]
# Input parameters:
#    double pa[] :  array to be replicated
#    int n       : num replications
#  Output parameters:
#    double py[]   : replicated array of length n_times * length_array
def replicate_arrays( a, n):
    # init result array
    y = np.zeros( n * a.size)
    # check types of arrays
    if a.dtype != "float64": a = a.astype(float)
    if y.dtype != "float64": y = y.astype(float)
    
    # Use CFFI type conversion
    pa = ffi.cast( "double *", a.ctypes.data)
    py = ffi.cast( "double *", y.ctypes.data)

    # Call C++ function
    result = lib.replicate_arrays( pa, py, a.size, n)

    return y



# given the coordinates of n_users and n_beams. Calculate the euclidean distance between all the users to all beams
# inputs:
#   a_x_u, a_y_u (float arrays of length U)
#   b_x, b_y (float arrays of length B)
#   U, B - integers, calculated in the python wrapper
# output:
#   distances - array float of size U*B of pairwise distances arranged as
#   [d_u1b1, d_u1b2,    d_u2b1, d_u2b2,    d_u3b1, d_u3b2].
def calc_distance( a_x_u, a_y_u, b_x, b_y):
    # init result array
    dist = np.zeros( a_x_u.size * b_x.size)
    # check types of arrays
    if a_x_u.dtype != "float64": a_x_u = a_x_u.astype(float)
    if a_y_u.dtype != "float64": a_y_u = a_y_u.astype(float)
    if b_x.dtype != "float64": b_x = b_x.astype(float)
    if b_y.dtype != "float64": b_y = b_y.astype(float)
    
    # Use CFFI type conversion
    pa_x_u = ffi.cast( "double *", a_x_u.ctypes.data)
    pa_y_u = ffi.cast( "double *", a_y_u.ctypes.data)
    pb_x = ffi.cast( "double *", b_x.ctypes.data)
    pb_y = ffi.cast( "double *", b_y.ctypes.data)
    pdist = ffi.cast( "double *", dist.ctypes.data)

    # Call C++ function
    result = lib.calc_distance( pa_x_u, pa_y_u, pb_x, pb_y, pdist, a_x_u.size, b_x.size)

    return dist



# function centroids. Similar to combineArrays def centroid_aux( a_demand, ov_allocation_u_b ,  a_coordinate_u) returns array coo_b
# demand: doubles length U
# allocation double or int length U*B
# coordinate double length U
# coo_b : doubles, length B
def centroid_aux( a_demand, ov_allocation_u_b, a_coordinate_u):
    # init result array
    num_b = int( ov_allocation_u_b.size / a_demand.size)
    coo_b = np.zeros( num_b)
    # check types of arrays
    if a_demand.dtype != "float64": a_demand = a_demand.astype(float)
    if ov_allocation_u_b.dtype != "float64": ov_allocation_u_b = ov_allocation_u_b.astype(float)
    if a_coordinate_u.dtype != "float64": a_coordinate_u = a_coordinate_u.astype(float)
    if coo_b.dtype != "float64": coo_b = coo_b.astype(float)
    
    # Use CFFI type conversion
    pa_demand = ffi.cast( "double *", a_demand.ctypes.data)
    pov_allocation_u_b = ffi.cast( "double *", ov_allocation_u_b.ctypes.data)
    pa_coordinate_u = ffi.cast( "double *", a_coordinate_u.ctypes.data)
    pcoo_b = ffi.cast( "double *", coo_b.ctypes.data)

    # Call C++ function
    result = lib.centroid_aux( pa_demand, pov_allocation_u_b, pa_coordinate_u, pcoo_b, a_demand.size, coo_b.size)

    return coo_b
