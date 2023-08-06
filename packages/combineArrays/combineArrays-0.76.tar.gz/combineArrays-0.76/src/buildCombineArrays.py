from cffi import FFI
import os

ffibuilder = FFI()
PATH = os.path.dirname(__file__)

ffibuilder.cdef("""
    int replicate_arrays( double *pa, double *py, int length_a, int n);
    int calc_distance( double *pa_x_u, double *pa_y_u, double *pb_x, double *pb_y, double *pdist, int num_u, int num_b);
    int centroid_aux( double* pa_demand, double *pov_allocation_u_b, double *pa_coordinate_u, double *pcoo_b, int num_u, int num_b);
    """, override=True)

ffibuilder.set_source("_libCombineArrays", r"""
    #include "libCombineArrays.h"
""",
    sources=[os.path.join(PATH, "libCombineArrays.cpp")],
    include_dirs=[PATH]
    )


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
