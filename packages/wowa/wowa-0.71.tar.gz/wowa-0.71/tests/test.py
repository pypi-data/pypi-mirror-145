import numpy as np
import math
from wowa import py_owa
from wowa import weightedf

def print_test_result( res, exp_res):
    print( "result: ", res)
    
    if np.array_equal( res, exp_res):
        print( "pass")
    else:
        print( "fail")
    
# test weightedf
# preparing some test inputs
# dimension and the number of levels of the n-ary tree
n=4 
L=10 

x = np.array([0.3, 0.4, 0.8, 0.2])   # inputs
w = np.array([0.4, 0.35 ,0.2 ,0.05]) # OWA weights
p = np.array([0.3, 0.25, 0.3, 0.15]) # inputs weights

# calling the PnTA algorithm
y = weightedf( x, p, w, py_owa, L);
# expected result: 0.595603
exp_res = np.array([0.595603])
y = np.around( y, 6)
npy = np.array([y])
print_test_result( npy, exp_res)