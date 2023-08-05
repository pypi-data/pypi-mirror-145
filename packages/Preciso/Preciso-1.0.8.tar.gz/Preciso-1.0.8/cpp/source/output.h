#ifndef OUTPUT_H
#define OUTPUT_H

/// \file output.h
/// \brief Header of the class Output
#include <string>
#include <vector>
#include "error.h"
#include "precipitate.h"
#include "element.h"
#include "temperature.h"
#include "matrix.h"
#include "mechanical.h"


/// \brief Output routines
/// \todo Optimize the outputs that take more than 90% of the execution time
class Output
{
public:
    
    Output();
    
    ~Output();
    
    /// \brief To Set the index for the node that we want to plot
    void SetNodeToPlotDistrib(std::string const&);
    void SetNodeToPlotThermo(std::string const&);
    void SetNodeToPlotFinal(std::string const&);

    /// \brief Define the name of the thermodynamic results output file and the iterations at which it should be written
    /// \param
    void DefineThermoOutputs(std::vector<std::string> const&);
    
    /// \brief Define the name of the distribution results files and the iterations at which it should be written
    void DefineDistributionOutputs(std::vector<std::string> const&);
    
    /// \brief Define the plot distribution ouputs and the iterations at which it should be written
    void DefinePlotDistributionOutputs(std::vector<std::string> const&,std::vector<Precipitate> const&);
    
    /// \brief Define the thermodynamical plot ouputs and the iterations at which it should be written
    void DefinePlotThermoOutputs(std::vector<std::string> const&,std::vector<Precipitate> const&);
    
    /// \brief Define the final thermodynamical plot ouputs
    void DefinePlotFinalOutputs(std::vector<std::string> const&,std::vector<Precipitate> const&);
    
    /// \todo Method that is call to write in a file at each steps
    void TimeStepOutput(Mechanical const&,Matrix const&,std::vector<Element> const&,std::vector<Precipitate> const&,Temperature const&,size_t const&,\
                        double const&, double const&, double const&, int const&,size_t const& nodeIndex, bool _forceWriting);
    
    /// \todo Method that allow to plot the last step
    void FinalOutputPlot(std::vector<Element> const&,std::vector<Precipitate> const&, double const&, double const&, double const&, int const&);
    
    /// \todo The writing thermo current step (function slave of 'TimeStepOutput')
    void TimeStepThermoResults(double const&, double const&, double const&,Matrix const&, std::vector<Element> const&, std::vector<Precipitate> const&,size_t const& nodeIndex);
    
    /// \todo The writing Mechanical current step (function slave of 'TimeStepOutput')
    void TimeStepMechanicalResults(double const&, double const&, double const&,Mechanical const&, std::vector<Element> const&, std::vector<Precipitate> const&,size_t const&);

    /// \todo Comment this procedure
    void TimeStepDistributionResults(double const&, double const&, std::vector<Precipitate> const&,size_t const& nodeIndex);

    /// \brief Sets the outputPrecision tolerance of outputs
    void SetOutputPrecision(double const &_tolerance);

    /// \brief To active or desactive the writing of mechanical outputs
    void SetActivationOfMechanicalOutputs(bool);

    /// \brief To set the model index
    void SetMechanicalModelWritting(int);

    /// \brief To choose or not heavy outputs
    void SetHeavyOuputs(bool);

    /// \brief To write hardening results
    void HardeningResults(bool,bool,double const&,Mechanical const&,size_t const&,std::vector<std::vector<double> > const&);
    
private:
    /// \brief Precision of numbers in outputs files
    int outputPrecision;
    /// \brief bool to check if it is the first call for outputs
    bool firstCallStepOutputs;
    /// \brief variable to know if the microstructural model is actived
    int activedMicrostructuralModel;
    /// \brief bool for mechanical outputs
    bool mechanicalOutputActived;
    /// \brief bool to check if it is the first call for distrib outputs
    bool firstCallDistrib;
    /// \brief bool to check if it is the first call for plot distrb
    bool firstCallPlotDistrib;
    /// \brief bool to check if it is the first call for plot thermo
    bool firstCallPlotThermo;
    /// \brief error object
    Error error;
    /// \brief to know the increment of saving
    int saveThermoEach;
    /// \brief to know the increment of saving for distrib
    int saveDistribEach;
    /// \brief to know the increment of ploting for dsitrib
    int plotDistribEach;
    /// \brief bool to know if ploting is activated
    bool plotThermo;
    /// \brief bool to know if ploting distrib is activated
    bool plotDistrib;
    /// \brief bool to know if final ploting is activated
    bool plotFinal;
    /// \brief to know the increment of ploting
    int plotThermoEach;
    /// \brief distrib that we have to plot
    std::vector<bool> DistribToPlot;
    /// \brief results that we have to plot
    std::vector<bool> ThermoToPlot;
    /// \brief final results that we have to plot
    std::vector<bool> FinalToPlot;
    /// \brief name of output file
    std::string thermoOutputFile;
    /// \brief name of output file for distrib
    std::string distribOutputFile;
    /// \brief To save thermo results only a defined time
    bool couplingThermoBool;
    /// \brief To save distrib results only a defined time
    bool couplingDistribBool;
    /// \brief Counter to know when we couple the number of thermoResults that are wrote
    size_t nbOfThermoResults;
    /// \brief Counter to know when we couple the number of thermoResults that are wrote
    size_t nbOfDistribResults;
    
    /// \brief Stream to communicate with GNUPLOT and plot precipitate size distributions
    FILE* gnuplotDistrib;
    /// \brief Stream to communicate with GNUPLOT and plot thermodynamical data
    FILE* gnuplotThermo;
    
    /// \todo Plot the precipitate size distibutions
    void PlotDistribution(double const&, double const&, std::vector<Precipitate> const&);
    
    /// \todo Plot thermodyamical data from the thermo file
    void PlotThermo(double const&, double const&, std::vector<Element> const&,std::vector<Precipitate> const&);
    
    /// \todo Plot thermodyamical data from the thermo file
    void GnuPlotThermo(double const&, double const&, std::vector<Element> const&,std::vector<Precipitate> const&);
    
    /// \brief index of the node that we want to plot for distrib
    unsigned int nodeToPlotDistrib;
    
    /// \brief index of the node that we want to plot
    unsigned int nodeToPlotThermo;
    
    /// \brief index of the node that we want to plot at the end
    unsigned int nodeToPlotFinal;

    /// \brief to active or not the full writing of results (necessary for sysweld coupling)
    bool heavyOuputs;
    
    
};

#endif // OUTPUT_H
