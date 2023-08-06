# Funtions to combine NumPy arrays in C++ 
import numpy as np
import types
from _wowa import ffi, lib
# from cffi import FFI
# ffi = FFI()


# Callback funtion when no sorting is needed when used in the tree
# Input parameters:
#   double x[]: array of size n
#   double w[]: array of size n
# Output parameters:
#   double y: sum of x[i] * w[i]
@ffi.def_extern()
def py_owa( n, x, w):
    # Call C++ function
    return lib.OWA( n, x, w)
    

# Function F is the symmetric base aggregator.
# Input parameters:
#   double x[] = inputs
#   double p[] = array of weights of inputs x[],
#   double w[] = array of weights for OWA, 
#   n = the dimension of x, p, w.
#   the weights must add to one and be non-negative.
#   double(*cb)(int, double[],double[]) = callback function 
#   L = number of binary tree levels. Run time = O[(n-1)L] 
# Output parameters:
#    y = weightedf
def weightedf( x, p, w, cb, L):
    try:
        # check for size
        if not( x.size == p.size == w.size): raise ValueError( "arrays must have same size")
        # check type of function
        if not( isinstance(cb, types.FunctionType)): raise ValueError( "no callback function")

        # check types of arrays
        if x.dtype != "float64": x = x.astype(float)
        if p.dtype != "float64": p = p.astype(float)
        if w.dtype != "float64": w = w.astype(float)
    
        # Use CFFI type conversion
        px = ffi.cast( "double *", x.ctypes.data)
        pp = ffi.cast( "double *", p.ctypes.data)
        pw = ffi.cast( "double *", w.ctypes.data)

        # Call C++ function
        y = lib.weightedf( px, pp, pw, x.size, lib.py_owa, L)
        return y

    except ValueError:
        raise
