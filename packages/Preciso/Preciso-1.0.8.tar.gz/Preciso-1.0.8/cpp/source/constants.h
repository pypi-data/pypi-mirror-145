#ifndef CONSTANTS_H
#define CONSTANTS_H
#include <limits>

/// \file constants.h
/// \brief Header for constant of the program

/// \param NUMERICLIMITDOUBLE precisionLimit for test with double (http://www.cplusplus.com/reference/limits/numeric_limits/)
#define NUMERICLIMITDOUBLE numeric_limits<double>::epsilon()

/// \param RGAZCONSTANT Gaz constant in J/mol/K
#define RGAZCONSTANT 8.314

/// \param KB Boltzmann constant in J/K
#define KB 1.38e-23

/// \param LIVEGNUPLOTTERMINAL set terminal for gnuplot
/// "x11 enhanced color" on mac ; "windows enhanced color" on windows
//#define LIVEGNUPLOTTERMINAL "x11 enhanced color";
#define LIVEGNUPLOTTERMINAL "x11 enhanced";
//#define LIVEGNUPLOTTERMINAL "windows enhanced color";

/// \param GNUPLOTTERMINAL set terminal for gnuplot
#define FINALGNUPLOTTERMINAL "postscript enhanced color";

/// \param GNUPLOTPATH set terminal for gnuplot
/// "/opt/local/bin/gnuplot" on mac or "/usr/local/bin/gnuplot"; "gnuplot" on windows if gnuplot path correctly defined
//for windows 7, just '#define GNUPLOTPATH "gnuplot"' seams not good
#define GNUPLOTPATH "/opt/local/bin/gnuplot";
//#define GNUPLOTPATH "/usr/local/bin/gnuplot";
//#define GNUPLOTPATH "gnuplot";

//sometimes on windows, it seems that gnuplot does not work.
//But if we run gnuplot with the console when the computer is just started
//it seems works all times after this manipulation

#endif // CONSTANTS_H
