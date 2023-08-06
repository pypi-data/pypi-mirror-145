#ifndef _WOWA
#define _WOWA

extern double OWA(int n, double x[],double w[]);
extern double weightedf(double x[], double p[], double w[], int n, double(*F)(int, double[],double[]), int L);

#endif