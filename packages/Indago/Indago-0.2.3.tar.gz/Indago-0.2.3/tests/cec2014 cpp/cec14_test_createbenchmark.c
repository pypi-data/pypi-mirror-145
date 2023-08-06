/* Standard PSO version 2006

Motivation
Quite often some authors say they compare their PSO versions
to the "standard one" ... which is never the same!
So the idea is to define a real standard at least for one year, validated by some
researchers of the field, in particular James Kennedy and Maurice Clerc.
This PSO version does not intend to be the best one on the market (in particular there is
no adaptation of the swarm size nor of the coefficients) but simply very near of the
original version (1995) with just a few improvements based on some recent works.

So referring to "standard PSO 2006" would mean exactly this version with the default values
detailed below as,for example, referring to "standard PSO 2006 (w=0.8)" would mean almost
this version but with a non standard first cognitive/confidence coefficient.

Parameters
S := swarm size
K := maximum number of particles _informed_ by a given one
T := topology of the information links
w := first cognitive/confidence coefficient
c := second cognitive/confidence coefficient
R := random distribution of c
B := rule "to keep the particle in the box"

Equations
For each particle and each dimension
v(t+1) = w*v(t) + R(c)*(p(t)-x(t)) + R(c)*(g(t)-x(t))
x(t+1) = x(t) + v(t+1)
where
v(t) := velocity at time t
x(t) := position at time t
p(t) := best previous position of the particle
g(t) := best previous position of the informants of the particle

Default values
S = 10+2*sqrt(D) where D is the dimension of the search space
K = 3
T := randomly modified after each step if there has been no improvement
w = 1/(2*ln(2))
c = 0.5 + ln(2)
R = U(0..c), i.e. uniform distribution on [0, c]
B := set the position to the min. (max.) value and the velocity to zero

About information links topology
A lot of works have been done about this topic. The main result is there is no
"best" topology. Hence the random approach used here. Note that is does not mean that
each particle is informed by K ones: the number of particles that informs a given one
may be any value between 1 (for each particle informs itself) and S.

About initialisation
Initial positions are chosen at random inside the search space (which is
supposed to be a hyperparallelepid, and even often a hypercube), according to an uniform
distribution. This is not the best way, but the one of the original PSO.

Each initial velocity is simply defined as the difference of two random
positions. It is simple, and needs no additional parameter.
However, again, it is not the best approach. The resulting distribution is not even
uniform, as for any method that uses an uniform distribution independently for each
component. The mathematically correct approach needs to use an uniform
distribution inside a hypersphere. It is not that difficult, and indeed used in some PSO
versions, but quite different from the original one.

Some results with the standard values
You may want to recode this program in another language. Also you may want to modify it
for your own purposes. Here are some results on classical test functions to help you to
check your code.
Dimension D=30
Acceptable error eps=0
Objective value f_min=0
Number of runs n_exec_max=50
Number of evaluations for each run eval_max=30000

Problem                            Mean best value    Standard deviation
Parabola/Sphere on [-100, 100]^D        0                  0
Griewank on [-600, 600]^D               0.018              0.024
Rosenbrock/Banana on [-30, 30]^D       50.16              36.9
Rastrigin on [-5.12, 5.12]^D           48.35              14.43
Ackley on [-32, 32]^D                   1.12               0.85

Last updates
2006-02-27 Fixed a bug about minimal best value over several runs
2006-02-16 Fixed a bug (S_max for P, V, X, instead of D_max), thanks to Manfred Stickel
2006-02-16 replaced k by i x by xs (in perf()), because of possible confusion with K and X
2006-02-13  added De Jong's f4
*/


//#include "stdio.h"
#include "math.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
//#include <ctime>
#include "cec14_test_func.cpp"

#define	D_max 100  // Max number of dimensions of the search space
#define	S_max 200 // Max swarm size
#define R_max 2000 // Max number of runs


struct position
{
    int size;
    double x[D_max];
    double f;
};

// CEC2014 stuff
void cec14_test_func(double *, double *, int, int, int);
void init_test_func(int,int);
double *OShift,*M,*y,*z,*x_bound;
int ini_flag=0,n_flag,func_flag,*SS;


// Sub-programs
double alea( double a, double b );
int alea_integer( int a, int b );
double perf(int s, int function, int dim); // Fitness evaluation

#define X_SAMPLE_SIZE 10

// Global variables
int best; // Best of the best position (rank in the swarm)
int D; // Search space dimension
//double E; // exp(1). Useful for some test functions
double f_min; // Objective(s) to reach
double pi; // Useful for some test functions
//struct velocity V[S_max]; // Velocities
struct position X[X_SAMPLE_SIZE]; // Positions
double xmin[D_max], xmax[D_max]; // Intervals defining the search space

// File(s)
//FILE * f_run;

// =================================================
int main ( int argc, char *argv[] )
{
    int iArg=1;
    int expectedArgument = 0;
    // 0 - option
    // 1 - test
    // 2 - dimensions
    // 3 - parameters
    // 4 - out
    //char* test = "";

    char* out = "out.txt";

    //FILE *fr;            /* declare the file pointer */

    //int p_func = -1;    // CEC function number (1, 2, ...30)
    //int p_dim = 0;
    float p_lb = -100.0;
    float p_ub = 100.0;


    //char line[80];



    //int function; // Code of the objective function

    //f_run = fopen( "f_run.txt", "w" );
    //E = exp( 1 );
    //pi = acos( -1 );

    //----------------------------------------------- PROBLEM
    //function = p_func; //Function code

    //int nIter = (int)( ceil( (double)p_maxeval / (double)p_swarmSize ) );
    //double* OUT =(double *)malloc(sizeof(double)  *  p_runs * nIter);
    // (x, f(x)) * 30 functions for each dim


    /*****

    double* OUT =(double *)malloc(sizeof(double) * (11 + 21 + 51 + 101) * 30);


    FILE *f = fopen(out, "a");
    if (f == NULL)
    {
        printf("Error opening file!\n");
        exit(1);
    }

    double fit;


    for (int dim = 10; dim<101; dim = dim*2)
    {

        for (int s = 0; s < X_SAMPLE_SIZE; s++)
        {
            // create vector x
            for ( int d = 0; d < dim; d++ )
            {
                X[s].x[d] = alea( p_lb, p_ub );
                fprintf(f, "%13.6e ", X[s].x[d]);
            }
            fprintf(f, "\n");
        }

        // evaluate all f(x)
        for (int s = 0; s < X_SAMPLE_SIZE; s++)
        {
            for (int fun = 1; fun < 31; fun++)
            {
                init_test_func(dim, fun);

                //X.size = dim;
                fit = perf(s, fun, dim);
                fprintf(f, "%13.6e ", fit);
            }
            fprintf(f, "\n");
        }

        // fix for 20*2 != 50
        if (dim == 20) dim = 25;

    }


    fclose(f);

    free(OUT);


    *******/

    int DIMS[] = {10, 20, 50, 100};

    for(int idim = 0; idim < 4; idim++)
    {
        int dim = DIMS[idim];

        // Read test samples
        char samples_filename[100];
        sprintf(samples_filename, "../cec2014_benchmark_data/samples_%dd.txt", dim);
        printf("samples file: %s\n", samples_filename);

        FILE *samples_file;
        samples_file = fopen(samples_filename, "r");
        for (int s = 0; s < X_SAMPLE_SIZE; s++)
        {
            for (int i = 0; i < dim; i++)
            {
                fscanf(samples_file, "%le", &(X[s].x[i]));
            }
            //for (int i = 0; i < dim; i++)
            //{
            //    printf("X[%d]: %e\n", i, X[s].x[i]);
            //}
        }
        fclose(samples_file);

        char results_filename[100];
        sprintf(results_filename, "../cec2014_benchmark_data/results_%dd.txt", dim);
        printf("results file: %s\n", results_filename);
        FILE *results_file = fopen(results_filename, "w");
        for(int fun = 1; fun < 31; fun++)
        {
            // Initialize test function
            init_test_func(dim, fun);

            // Evaluate
            for (int s = 0; s < X_SAMPLE_SIZE; s++)
            {
                double fit = perf(s, fun, dim);
                //printf("\n%dD F%d: %.10e ", dim, fun, fit);
                fprintf(results_file, "%.10e ", fit);
            }
            fprintf(results_file, "\n");
        }
        fclose(results_file);
    }

    return 0;
}

//===========================================================
double alea( double a, double b )
{ // random number (uniform distribution) in [a b]
    double r;
    r=(double)rand(); r=r/RAND_MAX;
    return a + r * ( b - a );
}

//===========================================================
int alea_integer( int a, int b )
{ // Integer random number in [a b]
    int ir;
    double r;
    r = alea( 0, 1 ); ir = ( int )( a + r * ( b + 1 - a ) );
    if ( ir > b ) ir = b;
    return ir;
}

//===========================================================
double perf( int s, int function, int dim )
{
    double fval;
    cec14_test_func(&(X[s].x), &fval, dim, 1, function);
    return fval - function*100;
}
