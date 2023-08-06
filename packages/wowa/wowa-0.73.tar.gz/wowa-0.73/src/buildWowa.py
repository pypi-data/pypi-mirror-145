from cffi import FFI
import os

ffibuilder = FFI()
PATH = os.path.dirname(__file__)

ffibuilder.cdef(r"""
    extern "Python" double(py_owa)(int, double *, double *);
    double OWA(int n, double x[],double w[]);
    double weightedf(double x[], double p[], double w[], int n, double(*F)(int, double[],double[]), int L);
    """, override=True)

ffibuilder.set_source("_wowa", r"""
    #include "wowa.h"
    """,
    sources=[os.path.join(PATH, "wowa.cpp")],
    include_dirs=[PATH]
    )


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
