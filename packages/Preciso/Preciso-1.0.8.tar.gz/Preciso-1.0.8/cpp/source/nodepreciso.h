#ifndef PreciSo_3_nodepreciso_h
#define PreciSo_3_nodepreciso_h

/// \file preciso.h
/// \brief Header of the class Preciso
#include <vector>
#include <string>
#include "input.h"
#include "error.h"
#include "temperature.h"
#include "matrix.h"
#include "output.h"
#include "preciso.h"


/// \brief Class that manages the multi-node version of PreciSo
class NodePreciso
{
public:
    
    /// \brief Constructor of the class NodePreciso, initialises number of nodes and connections.
    /// \callgraph
    NodePreciso();

    /// \brief Destructor of the class NodePreciso, no specific effect.
    /// \callgraph
    ~NodePreciso();
    
    /// \brief Initiliases the Preciso instance. Checks the number of input arguments to the programm and calls the input.run to read the input data and initialise the objects.
    /// argv must constain the keywords -path and -file followed by their respectives values.
    /// \return Nothing
    /// \param argc Number of executable input arguments
    /// \param argv Table of pointers to the input arguments
    /// \callgraph
    void Initialize(int const& argc, const char *argv[]);

    /// \brief Initialize the number of nodes and allocates the Node table taking the data from the data file _filename
    /// \callgraph
    void InitializeNumberOfNodes(std::string const& _filename);

    /// \brief Sets the properties of each node taking the data from the data file _filename
    /// \callgraph
    void InitializeNodes(std::string const& _filename,bool onlyOneNode);

    /// \brief Creates the tables of connectivities and surfaces taking the data from the data file _filename
    /// \callgraph
    void InitializeConnectivities(std::string const& _filename);

    /// \brief Changes the properties of each node compared to the reference preciso taking the data from the data file _filename.
    /// Reinitiliazes the data of the node when necessary.
    /// \callgraph
    void InitializeNodeProperties(std::string const& _filename);

    /// \brief Load all the precipitations data and desactive PreciSo computation, only mechanic
    /// \callgraph
    void InitializeOnlyMechanicOption(std::string const& _filename);

    /// \brief Write the parameters (constants.h file) in the log file
    /// \return Nothing
    /// \callgraph
    void WriteParameterLog();
    
    /// \brief Runs the classical version of PreciSo with only 1 node
    /// \return Nothing
    /// \callgraph
    /// \callergraph
    void Run();

    /// \brief Computation of mean Vat
    /// \return Nothing
    /// \callgraph
    /// \callergraph
    double meanVatNodeI(std::vector<Preciso> &,size_t const);

private:
    /// \brief Preciso instance of this node 
    Preciso preciso; 
    
    /// \brief Vector containing all instances of Preciso
    std::vector<Preciso> Node;
    
    /// \brief criterion for timeStep, deltaX for each element must not excess 1% due to diffusion
    double coeffCFLcondition;

    /// \brief number of nodes, i.e. number of instances of Preciso that will run simultaneously
    size_t numberOfNodes;
    
    /// \brief number of connections
    size_t numberOfConnections;
    
    /// \brief Error instance of this Preciso
    Error error;
    
    /// \brief Current time values in s
    double currentTime;
    
    /// \brief Time step in s
    double dt;

    /// \brief Coefficient for decreasing the time step when too large (by default 0.5)
    double reduceDT;

    /// \brief 
    Input input;

    /// \brief To load the last distribution for each nodes and run only the mechanical part of preciso
    bool onlyMechanicComputation;

    /// \brief To have or not a hardening computation
    bool hardeningComputation;

    /// \brief To have or not a hardening computation during precipitation
    bool mechanicalHardeningCoupling;

    /// \brief To have semi-coupling for hardening computation during precipitation
    bool mechanicalSemiHardeningCoupling;

    /// \brief leaving a domain or not
    bool reduced;

    /// \brief To desactivate comments
    bool notVerboseBool;

    /// \brief Shif of the nodes number if the nodes described in the input file don't start from 0.
    int nodeShift;
    
    /// \brief Connectivity table: array containing indexes of connected nodes
    std::vector<std::vector<int> > Connection;
    
    /// \brief Surface of each connection in m^2
    std::vector<double> Surface;

    /// \brief Smallest acceptable timestep is same as preciso.cpp smallestTimeStep (by default 1e-9)
    double nodeSmallestTimeStep;
    
    /// \brief Manage the fluxes between neighbouring nodes
    /// \return false if flux management leads to negative concentration
    /// \callgraph
    /// \callergraph
    bool validFluxManagement(std::vector<Preciso>&,std::vector<std::vector<Element> >&,std::vector<Matrix>&,std::vector<std::vector<Precipitate> >&,std::vector<double >&,std::string&);
    
    /// \brief String in which the reason why the time step is rejected is given
    std::string reasonTimeStepRejected;

};


#endif
