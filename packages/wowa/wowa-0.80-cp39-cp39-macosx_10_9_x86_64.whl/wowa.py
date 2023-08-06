# Funtions to combine NumPy arrays in C++ 
import numpy as np
import types
from _wowa import ffi, lib

CB = None
# Callback funtion when no sorting is needed when used in the tree
# Input parameters:
#   n: size of arrays
#   double x[]: array of size n
#   double w[]: array of size n
# Output parameters:
#   double y: sum of x[i] * w[i]
@ffi.def_extern()
def py_WAM( n, x, w):
    # print( "py_WAM")
    # Call C++ function
    return lib.OWA( n, x, w)

# Callback funtion 
@ffi.def_extern()
def py_OWA( n, x, w):
    # print( "py_OWA")
    return lib.OWASorted( n, x, w)

# Callback funtion 
@ffi.def_extern()
def py_user_defined_for_WOWATree( n, x, w):
    # print( "py_user_defined_for_")
    # User defined python function
    return CB( n, x, w)


# Callback funtion 
@ffi.def_extern()
def py_user_defined_for_WAn(  x, w):
    # print( "py_user_defined")
    # User defined python function
    return CB( x, w)

# Retrieve C callback function based on Python callback function
def get_c_callback_function( py_cb): 
    try:
        # check if this is a function function
        if not( isinstance( py_cb, types.FunctionType)): raise ValueError( "no callback function")

        # Check if Python callback function is one of the pre-defined callbacks
        if( py_cb == py_OWA): p_c_cb = lib.py_OWA
        elif( py_cb == py_WAM): p_c_cb = lib.py_WAM
        elif( py_cb == py_user_defined_for_WOWATree): p_c_cb = lib.py_user_defined_for_WOWATree
        elif( py_cb == py_user_defined_for_WAn): p_c_cb = lib.py_user_defined_for_WAn
        else: raise ValueError( "undefined callback function")

        return p_c_cb
    except ValueError:
        raise



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
def WowaTree( x, p, w, cb, L):
    try:
        global CB
        if (cb != None) and (cb != py_OWA) and (cb != py_WAM): 
            CB = cb
            cb = py_user_defined_for_WOWATree

        # check for size
        if not( x.size == p.size == w.size): raise ValueError( "arrays must have same size")

        # check types of arrays
        if x.dtype != "float64": x = x.astype(float)
        if p.dtype != "float64": p = p.astype(float)
        if w.dtype != "float64": w = w.astype(float)
    
        # Use CFFI type conversion
        px = ffi.cast( "double *", x.ctypes.data)
        pp = ffi.cast( "double *", p.ctypes.data)
        pw = ffi.cast( "double *", w.ctypes.data)

        # Retrieve C callback function
        p_c_cb =  get_c_callback_function( cb) 

        # Call C++ function
        y = lib.weightedf( px, pp, pw, x.size, p_c_cb, L)
        return y

    except ValueError:
        raise

# Function F is        
# Input parameters:
# Output parameters:
#    y = double
def WAn( x, w, L, F):
    try:
        global CB
        if (F != None) and (F != py_OWA) and (F != py_WAM): 
            CB = F
            F = py_user_defined_for_WAn
        # check for size
        if not( x.size == w.size): raise ValueError( "arrays must have same size")
        
        # check types of arrays
        if x.dtype != "float64": x = x.astype(float)
        if w.dtype != "float64": w = w.astype(float)
    
        # Use CFFI type conversion
        px = ffi.cast( "double *", x.ctypes.data)
        pw = ffi.cast( "double *", w.ctypes.data)

        # Retrieve C callback function
        p_c_cb =  get_c_callback_function( F) 

        # Call C++ function
        # double WAn(double * x, double * w, int n, int L, double(*F)( double, double))
        y = lib.WAn( px, pw, x.size, L, p_c_cb)
        return y

    except ValueError:
        raise


# Function F is        
# Input parameters:
# Output parameters:
#    temp[] = working memory, keeps the spline knots and coefficients for later use in weightedOWAQuantifier
#    should be at least 12(n+1) in length and the memory should be allocated by the calling program
#     T  = the number of knots in the monotone spline
# Return values:
#    temp[]
def weightedOWAQuantifierBuild( p, w, T):
    try:
        # check for size
        if not( p.size == w.size): raise ValueError( "arrays must have same size")
        # check types of arrays
        if p.dtype != "float64": p = p.astype(float)
        if w.dtype != "float64": w = w.astype(float)
        if T.dtype != "intc": T = T.astype(int)
    

        # Use CFFI type conversion
        pp = ffi.cast( "double *", p.ctypes.data)
        pw = ffi.cast( "double *", w.ctypes.data)
        pT = ffi.cast("int *", T.ctypes.data)

        # init result array for spline knots and coefficients 
        n = p.size
        temp = np.zeros( (12 * n) + 1 )
        ptemp = ffi.cast( "double *", temp.ctypes.data)

        # Call C++ function
        # void weightedOWAQuantifierBuild( double p[], double w[], int n, double temp[], int *T)
        lib.weightedOWAQuantifierBuild( pp, pw, n, ptemp, pT)
        return temp

    except ValueError:
        raise



# Function F is        
# Input parameters:
# Output parameters:
#    y = double
def weightedOWAQuantifier( x, p, w, temp, T):
    try:
        # check for size
        if not( x.size == p.size == w.size): raise ValueError( "arrays must have same size")
        if x.dtype != "float64": x = x.astype(float)
        if p.dtype != "float64": p = p.astype(float)
        if w.dtype != "float64": w = w.astype(float)

        # Use CFFI type conversion
        px = ffi.cast( "double *", x.ctypes.data)
        pp = ffi.cast( "double *", p.ctypes.data)
        pw = ffi.cast( "double *", w.ctypes.data)
        ptemp = ffi.cast( "double *", temp.ctypes.data)

        n = x.size;
        if ( temp.size != ( 12 * n) + 1): raise ValueError( "wrong size for array of spline nots")

        # Call C++ function
        # double weightedOWAQuantifier(double x[], double p[], double w[], int n, double temp[], int T)
        y = lib.weightedOWAQuantifier( px, pp, pw, n, ptemp, T)
        return y

    except ValueError:
        raise


# Function F is        
# Input parameters:
# Output parameters:
#    y = double
def ImplicitWOWA( x, p, w,):
    try:
        # check for size
        if not( x.size == p.size == w.size): raise ValueError( "arrays must have same size")
        # check types of arrays
        if x.dtype != "float64": x = x.astype(float)
        if p.dtype != "float64": p = p.astype(float)
        if w.dtype != "float64": w = w.astype(float)
    
        # Use CFFI type conversion
        px = ffi.cast( "double *", x.ctypes.data)
        pp = ffi.cast( "double *", p.ctypes.data)
        pw = ffi.cast( "double *", w.ctypes.data)

        # Call C++ function
        # double ImplicitWOWA(double x[], double p[], double w[], int n )
        y = lib.ImplicitWOWA( px, pp, pw, x.size )
        return y

    except ValueError:
        raise



