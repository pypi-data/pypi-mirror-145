#ifndef PRECISO_H
#define PRECISO_H

/// \file preciso.h
/// \brief Header of the class Preciso
#include <vector>
#include <string>
#include "input.h"
#include "error.h"
#include "precipitate.h"
#include "element.h"
#include "temperature.h"
#include "matrix.h"
#include "output.h"
#include "mechanical.h"

// /// \brief Forward declaration of class Input, necessary for the compilation
// class Input;

/// \brief Main class of PreciSo managing Nucleation, Growth and Dissolution
class Preciso
{
public:
    
    /// \brief Constructor of the class Preciso, initialises the vector of Elements and Precipitates.
    /// \callgraph
    Preciso();
    
    /// \brief Destructor of the class Preciso.
    /// \callgraph
    ~Preciso();
    
    /// \brief Initiliases the Preciso instance. calls the input.run to read the input data and initialise the objects.
    /// \return Nothing
    /// \param _fileName Path to the input file
    /// \callgraph
    void Initialize(std::string const& _fileName);

    /// \brief Initialize the matrix and elements data for this instance taking the data from the data file _filename
    /// The matrix needs to be defined to correctly defined the elements since the matrix is then included as an element in the element list.
    /// \callgraph
    void InitializeMatrixAndElementsAndGeneral(std::string const& _filename);

    /// \brief Initialize the precipitates data (including numerical options) for this instance taking the data from the data file _filename
    /// \callgraph
    void InitializePrecipitates(std::string const& _filename);

    /// \brief Initialize the temperature data for this instance taking the data from the data file _filename
    /// \callgraph
    void InitializeTemperature(std::string const& _filename);

    /// \brief Initialize the distribution data for this instance taking the data from the data file _filename
    /// \callgraph
    void InitializeDistribution(std::string const& _filename);

    /// \brief To load an initial distribution for this node (cf. nodeproperties from NodePreciso)
    /// \callgraph
    void LoadInitialDistrib(std::vector<std::string> &_lines);

    /// \brief Initialize the outputs data for this instance taking the data from the data file _filename (keywords defined in the routine)
    /// \callgraph
    void InitializeOutputsData(std::string const& _filename);

    /// \brief Initialize the options from the data file that are linked to the preciSo object
    /// \callgraph
    void InitializeOptions(std::string const& _filename);

    /// \brief Initialize the mechanical part
    /// \callgraph
    void InitializeMechanical(std::string const& _filename);

    /// \brief Initialize the thermodynamic data for this preciso, when one or several parameters are changed
    /// A first mass balance is done and InitializeTime is called.
    /// \callgraph
    void InitializeThermodynamicData();

    /// \brief Change matrix properties (and associed elements/precipitates) from NodePreciso. The matrix contents is then recalculated.
    /// \callgraph
    void ChangeMatrixAndAssiocedElemPreci(bool _firstCallHere,std::string _nameFile,size_t _nodeBegin,size_t _nodeEnd);

    /// \brief Change one element properties from NodePreciso. The matrix contents is recalculated.
    /// \callgraph
    void ChangeElement(std::vector<std::string> const& _line);

    /// \brief Change one precipitate family properties from NodePreciso.
    /// \callgraph
    void ChangePrecipitate(std::vector<std::string>& _line);

    /// \brief Change boostPrecipitateDiffusion for one precipitate from NodePreciso.
    /// \callgraph
    void ChangeBoostPrecipitateDiffusion(std::vector<std::string>& _line);

    /// \brief Initialize the time, timestep and initial value of rstar to check the validity of the time step
    /// \return Nothing
    void InitializeTime(Temperature const&,std::vector<Element> const&,std::vector<Precipitate>&);

    /// \brief Initialize after all element initialization we initialize atomicVolumeSS for each PreciSo
    /// \return Nothing
    void InitializeAtomicVolumeSS(Matrix & _matrix,std::vector<Element> const& _Elements,bool _firstCall);

    /// \brief To have the 'SmallestTimeStep' equal to 'NodeSmallestTimeStep'
    /// \return Nothing
    void setSmallestTimeStep(double);

    /// \todo Comment this procedure
    /// \return Boolean stating if the timestep is valid or not
    bool validTimeStep(std::vector<Element> const&,std::vector<Precipitate>&, double const&,unsigned int const&,std::string&);
    
    /// \brief Calculation new criterion (either rStar or solConcent) for timestep validation
    /// \return Nothing
    void PreNuclGrowthDiss(Matrix&, std::vector<Element>&,std::vector<Precipitate>&, double const&);
    
    /// \todo Comment this procedure
    /// \return new timestep
    double PostNuclGrowthDiss(Matrix &, std::vector<Element>&,std::vector<Precipitate>&, double const&, unsigned int const&,bool&);

    /// \todo Comment this procedure
    /// \return Boolean stating if the timestep is valid or not
    bool ValidNuclGrowthDiss(Matrix&, std::vector<Element>&,std::vector<Precipitate> &, double const& ,unsigned int const&,std::string&);

    /// \brief Sets the node index of this instance
    /// \param _index Index of the node
    /// \return Nothing
    void setNodeIndex(size_t const& _index);

    /// \brief Sets the x position of this instance
    /// \param _xPos X position of the node in m
    /// \return Nothing
    void setXPos(double const& _xPos);

    /// \brief Sets the y position of this instance
    /// \param _yPos Y position of the node in m
    /// \return Nothing
    void setYPos(double const& _yPos);

    /// \brief Sets the z position of this instance
    /// \param _zPos Z position of the node in m
    /// \return Nothing
    void setZPos(double const& _zPos);

    /// \brief Sets the volume of this instance
    /// \param _volume Volume of the node in m^3
    /// \return Nothing
    void setVolume(double const& _volume);
    double getVolume() const;

    /// \brief Write the initial values of thermodynamic outputs
    void WriteInitialOutputs();

    /// \brief Run mechanical computation
    void mechanicalComputation(bool,bool,size_t,Matrix const&, std::vector<Element> const&,std::vector<Precipitate> const&,double const&);

    /// \brief If we have precipitation-hardening coupling we have to check vector
    void checkVectorOfHardeningCoupling();

    /// \brief To write mechanical hardening results
    void WriteMechanicalHardeningResults(bool,bool);

private:

    /// \brief Input instance of this Preciso
    Input input;
    /// \brief Output instance of this Preciso
    Output output;
    /// \brief Error instance of this Preciso
    Error error;
    /// \brief Temperature instance of this Preciso
    Temperature temperature;
    /// \brief Matrix instance of this Preciso
    Matrix matrix;
    /// \brief Mechanical instance of this Preciso
    Mechanical mechanical;
    /// \brief Vector of the Precipitate instances of this Preciso
    std::vector<Precipitate> Precipitates;
    /// \brief Vector to the Element instances of this Preciso
    std::vector<Element> Elements;
    /// \brief Successive time values in s
    double currentTime;
    /// \brief Time step in s
    double dt;
    /// \brief in m
    std::vector<double> Criterion;
    /// \brief Next time index in the table of time/temperature
    size_t currentTimeIndex;
    /// \brief Next time index in the table of time/temperature
    size_t currentMechanicTimeIndex;
    /// \brief Node index of this Preciso
    size_t nodeIndex;
    /// \brief Position X of this instance of Preciso
    double xPos;
    /// \brief Position Y of this instance of Preciso
    double yPos;
    /// \brief Position Z of this instance of Preciso
    double zPos;
    /// \brief Volume of this instance of Preciso
    double volume;
    /// \brief First time of this PreciSo (useful for example in nucleation)
    double firstTime;
    /// \brief Indicates if the precipitation is calculated for this instance
    bool solvePrecipitation;
    /// \brief To desactivate comments
    bool notVerboseBool;
    /// \brief Coefficient for increasing the time step at each step (by default 1.1)
    double increaseDT;
    /// \brief Initial time step in s (by default 1e-6)
    double initialDT;
    /// \brief Maximum increase of rStar for the time step validation (by default 0.01)
    double maxCriterionIncrease;
    /// \brief 1 for PreciSo v1 version, 3 for PreciSo "v3" version (by default 3)
    int timeStepManagement;
    /// \brief Smallest acceptable timestep (by default 1e-9)
    double smallestTimeStep;
    /// \brief Leaving a domain or not
    bool leaveDomain;
    /// \brief Leaving a mechanical domain or not
    bool leaveMechaDomain;
    /// \brief To choice the kind of criterion
    int criterion;
    /// \brief To active mechanical model
    bool mechanicalModelActivated;
    /// \brief No precipitate or diffusion computation
    bool onlyMechanicComputation;
    /// \brief if we want a 'hardeningModel' computation
    bool hardeningComputation;
    /// \brief If we want to compute hardening during treatment
    bool mechanicalHardeningCoupling;
    /// \brief If we want to compute hardening during treatment but with semi-hardening coupling
    bool mechanicalSemiHardeningCoupling;
    /// \brief Bool to know which mass balance we have
    bool simplifiedMassBalance;
    /// \brief If we have to solve an uncoupled mechanical problem
    std::vector<std::vector<double> > uncoupledMecaResults;
    /// \brief
    bool noVatSS;

    friend class NodePreciso;
};


#endif // PRECISO_H
