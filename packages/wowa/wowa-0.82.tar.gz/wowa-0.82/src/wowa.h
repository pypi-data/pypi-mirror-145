#ifndef _WOWA
#define _WOWA

// Callbacks
extern double OWASorted(int n, double x[],double w[]); // Pyhthon:OWA
extern double OWA(int n, double x[],double w[]); //Python: WAM


// WOWA functions
extern double weightedf(double x[], double p[], double w[], int n, double(*F)(int, double[],double[]), int L); //Python: WOWATree
extern double WAn(double * x, double * w, int n, int L, double(*F)( double, double)); //Python: WAn
extern void weightedOWAQuantifierBuild( double p[], double w[], int n, double temp[], int *T); // Python: weightedOWAQuantifierBuild
extern double weightedOWAQuantifier(double x[], double p[], double w[], int n, double temp[], int T); // Python: weightedOWAQuantifier
extern double ImplicitWOWA(double x[], double p[], double w[], int n ); // Python: ImplicitWOWA

#endif