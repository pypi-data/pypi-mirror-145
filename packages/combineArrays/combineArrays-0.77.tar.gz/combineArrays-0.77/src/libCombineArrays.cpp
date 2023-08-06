//
//  main.cpp
//  libCombineArrays
//
//  Created by Norbert Henseler on 31/3/22.
//

#include <iostream>
#include <math.h>
using namespace std;


extern "C"
{
    /*
     * Replicate the array n_times and return an array which shape is (length_ary * n_times)
     * Example:
     * a_lat_b = [4, 5]
     * result = replicate_array(a_lat_b,3) -> result = [4, 5, 4, 5, 4, 5]
     * Input parameters:
     *   double pa[] :  array to be replicated
     *   int length_a: length of array
     *   int n       : num replications
     * Output parameters:
     *   double py[]   : replicated array of length n_times * length_array
     */
    int replicate_arrays( double *pa, double *py, int length_a, int n)
    {
        for( int j = 0; j < n; j++){
            std::copy( pa, pa + length_a, py + j * length_a);
        }
       return 0; 
    }
    
    /*
     * Calculate Euclidean distance
     */
    inline double euclidian_distance(double x1, double y1, double x2, double y2)
    {
        return( sqrt( pow(x1 - x2, 2) + pow(y1 - y2, 2)));
    }

    /*
     * given the coordinates of n_users and n_beams. Calculate the euclidean distance between all the users to all beams
     * inputs:
     *   a_x_u, a_y_u (float arrays of length U)
     *   b_x, b_y (float arrays of length B)
     *   U, B - integers, calculated in the python wrapper
     * output:
     *   distances - array float of size U*B of pairwise distances arranged as
     *   [d_u1b1, d_u1b2,    d_u2b1, d_u2b2,    d_u3b1, d_u3b2].
     */
    int calc_distance( double *pa_x_u, double *pa_y_u, double *pb_x, double *pb_y, double *pdist, int num_u, int num_b)
    {
        for( int u = 0; u < num_u; u++){
            for( int b = 0; b < num_b; b++){
                pdist[u * num_b + b] = euclidian_distance( pa_x_u[u], pa_y_u[u], pb_x[b], pb_y[b]);
            }
        }
        return 0;
    }

  
    /*
     * function centroids. Similar to combineArrays def centroid_aux( a_demand, ov_allocation_u_b ,  a_coordinate_u) returns array coo_b
     * demand: doubles length U
     * allocation double or int length U*B
     * coordinate double length U
     * coo_b : doubles, length B
     *
     * formula/code:
     * for(b=0;b<B;b++){
     *    coo_b[b]=0;
     *    double C=0;
     *    for(u=0;u<U;u++){
     *      coo_b[b] +=coordinate[u]*allocation[u*B+b]* demand[u];
     *      C+=demand[u]*allocation[u*B+b];
     *    }
     *    if (fabs(C)>1e-10 )  coo_b[b] /=C; else coo_b[b]=0;
     * }
     */
    int centroid_aux( double* pa_demand, double *pov_allocation_u_b, double *pa_coordinate_u, double *pcoo_b, int num_u, int num_b)
    {
        for( int b = 0; b < num_b; b++){
            pcoo_b[b] = 0;
            double C = 0;
            for( int u = 0; u < num_u; u++){
                pcoo_b[b] += pa_coordinate_u[u] * pov_allocation_u_b[u * num_b + b] * pa_demand[u];
                C += pa_demand[u] * pov_allocation_u_b[u * num_b + b];
            }
            if (fabs(C)>1e-10 ){
                pcoo_b[b] /= C;
            } else {
                pcoo_b[b] = 0;
            }
         }
         return 0;
    }
}

/*
int main(int argc, const char * argv[]) {
    
    // test replicate_arrays()
    // expected result: 4, 5, 6, 4, 5, 6, 4, 5, 6,
    double a[] = {4,5,6};
    int length_a = 3;
    int n = 3;
    double y[length_a * n];
    replicate_arrays( a, y, length_a, n);
    cout << "- test replicate_arrays()\n";
    for( int i = 0; i < length_a * n; i++){
        cout << y[i] << ", ";
    }
    cout << "\n\n";
    
    // test calc_distance()
    // expected result: 0.5662, 2.46048, 0.16181, 2.26403,
    const int num_u = 2;
    const int num_b = 2;
    double a_x_u[num_u] = {-38.4, -38.2};
    double a_y_u[num_u] = {140.7, 141.4};
    double b_x[num_b] = {-38.2444, -35.9639};
    double b_y[num_b] = {141.2444, 141.0455};
    
    double dist[num_u * num_b];
    calc_distance( a_x_u, a_y_u, b_x, b_y, dist, num_u, num_b);
    cout << "- test calc_distance()\n";
    for( int i = 0; i < num_u * num_b; i++){
        cout << dist[i] << ", ";
    }
    cout << "\n\n";
    
    // test centroid_aux()
    // expected result: -36.1923, -38,
    const int num__u = 3;
    const int num__b = 2;
    double  a_demand[num__u] = {1.1, 2.1, 3.1};
    double ov_allocation_u_b[num__u * num__b] = {0, 1, 1, 0, 1, 0};
    double a_coordinate_u[num__u] = { -38, -35, -37};
    double coo_b[num__b];
    centroid_aux( a_demand, ov_allocation_u_b, a_coordinate_u, coo_b, num__u, num__b);
    cout << "- test centroid_aux()\n";
    for( int i = 0; i < num__b; i++){
        cout << coo_b[i] << ", ";
    }
    cout << "\n\n";

    return 0;
}
*/