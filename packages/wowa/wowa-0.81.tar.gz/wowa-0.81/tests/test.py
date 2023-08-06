import numpy as np
import math
from wowa import py_WAM
from wowa import py_OWA
from wowa import WowaTree
from wowa import WAn
from wowa import weightedOWAQuantifier
from wowa import weightedOWAQuantifierBuild
from wowa import ImplicitWOWA 


def print_test_result( name, res, exp_res):
    print( "Scenario: ",  name)
    print( "result: ", res)
    
    if np.array_equal( res, exp_res):
        print( "pass")
    else:
        print( "fail")
    
#
# test WowaTree with pre-defined callback
#
scenario = "test WowaTree with pre-defined callback"
# preparing some test inputs
# dimension and the number of levels of the n-ary tree
n=4 
L=10 

x = np.array([0.3, 0.4, 0.8, 0.2])   # inputs
w = np.array([0.4, 0.35 ,0.2 ,0.05]) # OWA weights
p = np.array([0.3, 0.25, 0.3, 0.15]) # inputs weights

# calling the algorithm
y = WowaTree( x, p, w, py_WAM, L);
# expected result: 0.595603
exp_res = np.array([0.595603])
y = np.around( y, 6)
npy = np.array([y])
print_test_result( scenario, npy, exp_res)

#
# test WowaTree with user-defined callback
#
scenario = "test WowaTree with user-defined callback"

def my_callback1( n, x, w):
    # print( "my_callback1")
    z = 0.0
    for i in range( n): z += x[i] * w[i]
    return z

def my_callback2( n, x, w):
    # print( "my_callback2")
    z = 1.0
    for i in range( n): z += x[i] * w[i]
    return z


# calling the algorithm
y = WowaTree( x, p, w, my_callback1, L);
# expected result: 0.595603
exp_res = np.array([0.595603])
y = np.around( y, 6)
npy = np.array([y])
print_test_result( scenario, npy, exp_res)

# calling the algorithm again
scenario = "test WowaTree with different user-defined callback"
y = WowaTree( x, p, w, my_callback2, L);
# expected result: 2.453897
exp_res = np.array([2.453897])
y = np.around( y, 6)
npy = np.array([y])
print_test_result( scenario, npy, exp_res)

#
# Test WAn
#
def my_callback3(  x, w):
    z = ( x + w) / 2
    return z

x = np.array([0.3, 0.4, 0.8, 0.2])   # inputs
w = np.array([0.4, 0.35 ,0.2 ,0.05]) # OWA weights
L =10
scenario = "test WAn with user-defined callback"
y = WAn( x, w, L, my_callback3)
# expected result: 0.430078
exp_res = np.array([0.430078])
y = np.around( y, 6)
npy = np.array([y])
print_test_result( scenario, npy, exp_res)

#
# Test ImplicitWOWA
#
x = np.array([0.3, 0.4, 0.8, 0.2])   # inputs
p = np.array([0.3, 0.25, 0.3, 0.15]) # inputs weights
w = np.array([0.4, 0.35 ,0.2 ,0.05]) # OWA weights
scenario = "test ImplicitWOWA"
y = ImplicitWOWA( x, p, w,)
# expected result: 0.532743
exp_res = np.array([0.532743])
y = np.around( y, 6)
npy = np.array([y])
print_test_result( scenario, npy, exp_res)


#
# Test weightedOWAQuantifierBuild
#
p = np.array([0.3, 0.25, 0.3, 0.15]) # inputs weights
w = np.array([0.4, 0.35 ,0.2 ,0.05]) # OWA weights
T = np.zeros( 1, np.intc)
T[0] = p.size
# test weightedOWAQuantifierBuild and keep keeps the spline knots and coefficients
tspline = weightedOWAQuantifierBuild( p, w, T)
print( "Scenario: test weightedOWAQuantifierBuild\n", "spline knots and coefficients:\n", tspline)
#
# Test weightedOWAQuantifier
#
scenario = "test weightedOWAQuantifier using splile calculated with weightedOWAQuantifierBuild"
x = np.array([0.3, 0.4, 0.8, 0.2])   # inputs
y = weightedOWAQuantifier( x, p, w, tspline, T)
# expected result: 0.567287
exp_res = np.array([0.567287])
y = np.around( y, 6)
npy = np.array([y])
print_test_result( scenario, npy, exp_res)
