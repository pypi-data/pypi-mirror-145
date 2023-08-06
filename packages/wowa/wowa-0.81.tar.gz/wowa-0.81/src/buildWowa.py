from cffi import FFI
import os

ffibuilder = FFI()
PATH = os.path.dirname(__file__)

ffibuilder.cdef(r"""
    extern "Python" double(py_OWA)(int, double *, double *);
    extern "Python" double(py_WAM)(int, double *, double *);
    extern "Python" double(py_user_defined_for_WOWATree)(int, double *, double *);
    extern "Python" double(py_user_defined_for_WAn)( double, double);

    double OWASorted(int n, double x[],double w[]);
    double OWA(int n, double x[],double w[]);

    double WAn(double * x, double * w, int n, int L, double(*F)( double, double));
    double weightedf(double x[], double p[], double w[], int n, double(*F)(int, double[],double[]), int L);
    void weightedOWAQuantifierBuild( double p[], double w[], int n, double temp[], int *T);
    double weightedOWAQuantifier(double x[], double p[], double w[], int n, double temp[], int T);
    double ImplicitWOWA(double x[], double p[], double w[], int n );
    """, override=True)

ffibuilder.set_source("_wowa", r"""
    #include "wowa.h"
    """,
    sources=[os.path.join(PATH, "wowa.cpp")],
    include_dirs=[PATH]
    )


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
