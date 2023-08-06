# combineArrays
This package provides Python CFFI bindings to combine NumPy arrays in C++. Functions are:
- replicate_arrays
- calc_distance
- centroid_aux

## Documentation
[User Manual](https://github.com/nhenseler/compareArrays/blob/main/docs/user%20manual.pdf)

## Installation
To install type:
```python
$ pip install combineArrays
```
## Usage of replicate_arrays( a, y, length_a, n)
```python
from combineArrays import replicate_arrays
```
### Parameters
#### Input parameters:
a: array to be replicated, float  
n:  num replications, int64
#### Output parameters:
y: replicated array of length n_times * length_array, float  

## Usage of calc_distance( a_x_u, a_y_u, b_x, b_y, dist, num_u, num_b)
```python
from combineArrays import calc_distance
```
### Parameters
#### Input parameters:
a_x_u, a_y_u: arrays of length num_u, float  
b_x, b_y: arrays of length num_b, float
#### Output parameters:
dist: array of size U*B of pairwise distances arranged as [d_u1b1, d_u1b2, d_u2b1, d_u2b2, d_u3b1, d_u3b2], float  

## Usage of centroid_aux( a_demand, ov_allocation_u_b, a_coordinate_u, coo_b)
```python
from combineArrays import centroid_aux
```
### Parameters
#### Input parameters:
demand: array of length num_u, float  
allocation: array of length num_u * num_b, float  
coordinate: array of length num_u, float  
#### Output parameters:
coo_b : array of length num_b, float  

## Test
To unit test type:
```python
$ test/test.py
```