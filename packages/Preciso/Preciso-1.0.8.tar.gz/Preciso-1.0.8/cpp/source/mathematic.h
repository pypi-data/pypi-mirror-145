#ifndef MATHEMATIC_H
#define MATHEMATIC_H

/// \file mathematic.h
/// \brief Header of the class Mathematic
#include "error.h"
#include "element.h"
#include "matrix.h"
#include <string>
#include <vector>
#include <math.h>

/// \brief Forward declaration of class Element, necessary for the compilation (Element needs Mathematics and vice-versa)
class Element;

struct complexe
{
    double re;
    double im;
};
/// \brief Mathematical constants, algorithms and solvers
class Mathematic
{
public:
    /// \brief Constructor of the class Mathematic, initializing all values to zero.
    /// \callgraph
    Mathematic();
    /// \brief Destructor of the class Mathematic, no specific effect.
    /// \callgraph
    ~Mathematic();
    /// \brief Nothing up to now...
    /// \callgraph
    void Initialize();
    /// \brief To have the ordonnate corresponding to an abscisse according linear interpolation
    /// \callgraph
    double LinearInterpolation(double const&, double const&, double const&, double const&, double const&);
    /// \brief To have the ordonnate corresponding to an abscisse according quadratic interpolation
    /// \callgraph
    double LagrangeInterpolation(double const&, double const&, double const&, double const&, double const&, double const&, double const&);
    /// \brief To solve with efficiency a non linear equation between two bounds
    /// \callgraph
    double BrentAlgorithm(double,double,std::string,double const&,std::vector<double> const&,std::vector<std::vector<double> > const&);

    /// \brief To solve fast non linear equations
    // we want "tol_Brent_Dicho" tolerance but if this tolerance is done at the beginning
    //we keep initial residu divided by "tol_divideResidu_NR"
    double newtonRaphson(double,double,std::string,double const&,std::vector<double> const&,std::vector<std::vector<double> >const&);

    /// \brief Constrained newtonRaphson
    // we want "tol_Brent_Dicho" tolerance but if this tolerance is done at the beginning
    //we keep initial residu divided by "tol_divideResidu_NR"
    double constrainedNewtonRaphson(double,double,std::string,double const&,std::vector<double> const&,std::vector<std::vector<double> >const&);


    /// \brief To solve with efficiency a non linear equation between two bounds
    /// \callgraph
    double Dichotomy(double,double,std::string,double const&,std::vector<double> const&,std::vector<std::vector<double> >const&);

    /// \brief Fonction that is call by brent for general 2elements precipitation
    double Sphere2elem(double,std::vector<double> const&);

    /// \brief Fonction that is call by brent for general Nelements precipitation
    double SphereNelem(double,std::vector<double> const&,std::vector<std::vector<double> > const&);

    /// \brief Set the tolerance of Brent and Dichotomy algorithms (default 1e-9)
    void SetTolerance_Brent_Dicho(double const& _tolerance);

    /// \brief Set the tolerance of NewtonRaphson algorithms (default 10000)
    void SetTolerance_NewtonRaphson(double const& _tolerance);

    /// \brief Set the maxNbOfIterations of NewtonRaphson algorithms (default 1000)
    void SetNRmaximumCount(double const& _maxNbOfIterations);

    /// \brief to compute cubique racine
    double radcubic(double nb);

    /// \brief to compute polynome of first order
    int PolynomFirstDegree(double a,double b,complexe buffer[1]);

    /// \brief to compute polynome of 2nd order
    int polynomSecondDegree(double a,double b,double c,complexe buffer[2]);

    /// \brief to compute polynome of 3th order
    int polynomThirdDegree(double a,double b,double c,double d,complexe buffer[3]);

    /// \brief to compute polynome of 4th order
    int polynomFourthDegree(double a,double b,double c,double d,double e,complexe buffer[4]);

    /// \brief runge kutta 45 (didier's version validated with matlab)
    std::vector<std::vector<double> > rk45adaptive(double,std::vector<double> const&,std::vector<double> const&,int const&,std::vector<double> const&);

    /// \brief to define differential system for rk45adaptive
    std::vector<double> functionRk45(int const&,std::vector<double> const&,double const&,std::vector<double> const&,std::vector<double> const&);

private:
    /// \brief Error instance of this class
    Error error;

    /// \brief Tolerance for the convergence of the Brent or Dichotomy algorithms, (1e-9 by default)
    double tol_Brent_Dicho;

    /// \brief Tolerance for the convergence of the NR algorithms->initialResiduDivided by this value (100 by default) (if initial residu lower than 1e-9)
    double tol_divideResidu_NR;

    /// \brief Maximum count for Newton Raphson (1000 by default)
    double NRmaximumCount;



    
};

#endif // MATHEMATIC_H
