#ifndef _LIB_COMBINE_ARRAYS
#define _LIB_COMBINE_ARRAYS

extern int replicate_arrays( double *pa, double *py, int length_a, int n);
extern int calc_distance( double *pa_x_u, double *pa_y_u, double *pb_x, double *pb_y, double *pdist, int num_u, int num_b);
extern int centroid_aux( double* pa_demand, double *pov_allocation_u_b, double *pa_coordinate_u, double *pcoo_b, int num_u, int num_b);

#endif