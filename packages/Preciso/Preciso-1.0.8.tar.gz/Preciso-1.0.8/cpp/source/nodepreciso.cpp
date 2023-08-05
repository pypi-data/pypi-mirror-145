#include <iostream>
#include <vector>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include "math.h"
#include "string.h"
#include "nodepreciso.h"
#include "preciso.h"
#include "input.h"
#include "error.h"
#include "element.h"
#include "precipitate.h"
#include "temperature.h"
#include "matrix.h"
#include "constants.h"
#include "output.h"

/// \file nodepreciso.cpp
/// \brief Methods of the class NodePreciso

#define MIN(a,b) ((a) < (b) ? (a) : (b))
#define MAX(a,b) ((a) > (b) ? (a) : (b))

using namespace std;

NodePreciso::NodePreciso()
{
    numberOfNodes=1; numberOfConnections=0; currentTime=0.;           dt=0;
    nodeShift=0;     reduceDT=0.5;          coeffCFLcondition=1;      nodeSmallestTimeStep=1e-9;
    reduced=false;   notVerboseBool=false;
    //To load the last distribution for each nodes and run only the mechanical part of preciso
    onlyMechanicComputation=false;
    hardeningComputation=false;
    mechanicalHardeningCoupling=false;
    mechanicalSemiHardeningCoupling=false;
    reasonTimeStepRejected="";
}
NodePreciso::~NodePreciso() {}

void NodePreciso::Initialize(int const& argc, const char *argv[])
{
    string filename;
    char* endCharact = NULL;
    // Read the input file name and check if the number of input arguments is correct
    filename=input.FileName(argc,argv);
    // Write the parameters in the log file
    WriteParameterLog();
    //--------------------NOT VERBOSE --------------------
    //Keyword starting input file lines
    string keyword;
    //Matrix of lines containing the keyword. /!\ lines is erased at the beginning of each call of LinesStartingWithKeyword
    vector<vector<string> > lines;
    //Read if the optionnal booleen "notVerboseBool" exist (default false)
    keyword="notVerbose";
    input.LinesStartingWithKeyword(filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("notVerbose defined twice.");}
    else if (lines.size()==1) {notVerboseBool=true;}
    else {notVerboseBool=false;}
    //-----------------------------------------------------------------------
    //Initialize the reference PreciSo object, initial mass balance and time initialization are done.
    preciso.Initialize(filename);
    InitializeNumberOfNodes(filename);
    //If there is only one node, no need to read further information
    if (numberOfNodes==1) {
        InitializeNodes(filename,true);
        InitializeOnlyMechanicOption(filename);
        //update mechanical boolcoupling in nodePreciSo to now the kind of time step management
        mechanicalHardeningCoupling=Node[0].mechanicalHardeningCoupling;
        mechanicalSemiHardeningCoupling=Node[0].mechanicalSemiHardeningCoupling;
        hardeningComputation=Node[0].hardeningComputation;
        //first mechanical Computation to update all variables
        Node[0].mechanicalComputation(true,false,0,preciso.matrix, preciso.Elements, preciso.Precipitates, Node[0].temperature.GetTemperature(Node[0].currentTime));
        //write outputs
        Node[0].WriteInitialOutputs();
        //write mechanical hardening results
        Node[0].WriteMechanicalHardeningResults(true,false);
        //check nodeProperties
        vector<vector<string> > lines;
        input.LinesStartingWithKeyword(filename,"nodeProperty",lines,true);
        size_t nbNodeProperties=lines.size();
        if(nbNodeProperties!=0) {error.Fatal("With 1node you cannot have node property!");}
        return;
    }
    InitializeNodes(filename,false);
    InitializeConnectivities(filename);
    InitializeNodeProperties(filename);
    InitializeOnlyMechanicOption(filename);
    //-----------------------------------------------------------------------
    //Read the optional value of reduceDT (default value 0.5)
    keyword="reduceDT";
    input.LinesStartingWithKeyword(filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("reduceDT defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for reduceDT.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for reduceDT, only the first is taken into account.");}
        reduceDT=strtod(lines[0][1].c_str(),&endCharact);
        if ((reduceDT>=1.0)||(reduceDT<=0)) {error.Fatal("Incorrect value for reduceDT (must be ]0;1[)");}
        if (notVerboseBool==false) {cout << "reduceDT changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();
    
    //Read the optional value of coeffCFLcondition (default value 1)
    keyword="coeffCFLcondition";
    input.LinesStartingWithKeyword(filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("coeffCFLcondition defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for coeffCFLcondition.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for coeffCFLcondition, only the first is taken into account.");}
        coeffCFLcondition=strtod(lines[0][1].c_str(),&endCharact);
        if (coeffCFLcondition<=0) {error.Fatal("Incorrect value for 'coeffCFLcondition' (must be>0)");}
        if (notVerboseBool==false) {cout << "coeffCFLcondition changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();
    
    //Read the optional value of nodeSmallestTimeStep (default value 1e-9)
    keyword="smallestTimeStep";
    input.LinesStartingWithKeyword(filename,keyword,lines,true);
    if (lines.size()>1) error.Fatal("smallestTimeStep defined twice.");
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for smallestTimeStep.");}
        if (lines[0].size()-1>1) error.Warning("Too many arguments defined for smallestTimeStep, only the first is taken into account.");
        nodeSmallestTimeStep=strtod(lines[0][1].c_str(),&endCharact);
        if (notVerboseBool==false) {cout << "smallestTimeStep changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();
    
    //Read the optional value of unstationnaryNucleation (default value false)
    //useful here because if node property is on precipitate it erase the previous value
    //of 'unstationnaryNucleation' in each precipitate
    keyword="unstationnaryNucleation";
    input.LinesStartingWithKeyword(filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("unstationnaryNucleation defined twice.");}
    if (lines.size()>0) {
        error.Warning("'unstationnaryNucleation' changed to true in nodePreciSo");
        size_t nbPrecipit=0;
        for (size_t i=0;i<Node.size();i++) {
            nbPrecipit=Node[i].Precipitates.size();
            for (size_t p=0;p<nbPrecipit;p++) {Node[i].Precipitates[p].SetUnstationnaryNucleation(true);}
        }
    }
    lines.clear();
    
    //1°) Write the initial thermodynamics outputs for the nodes
    //2°) update the mechanical hardening bool
    //we have the same state of coupling for all nodes
    hardeningComputation=Node[0].hardeningComputation;
    mechanicalHardeningCoupling=Node[0].mechanicalHardeningCoupling;
    mechanicalSemiHardeningCoupling=Node[0].mechanicalSemiHardeningCoupling;
    for (size_t i=0;i<Node.size();i++) {
        Node[i].mechanicalComputation(true,false,0,preciso.matrix, preciso.Elements, preciso.Precipitates, Node[i].temperature.GetTemperature(Node[i].currentTime));
        Node[i].WriteInitialOutputs();
        Node[i].WriteMechanicalHardeningResults(true,false);
    }
    
    if (mechanicalHardeningCoupling==true && mechanicalSemiHardeningCoupling==true) {
        error.Fatal("You cannot have both 'mechanicalHardeningCoupling' and 'mechanicalSemiHardeningCoupling' (nodePreciSo class)");
    }
}

void NodePreciso::InitializeNumberOfNodes(string const& _filename)
{
    char* endCharact = NULL;
    //Keyword starting input file lines
    string keyword;
    //Matrix of lines containing the keyword. /!\ lines is erased at the beginning of each call of LinesStartingWithKeyword
    vector<vector<string> > lines;
    //--------------------NUMBER OF NODES-------------------
    keyword="nodes";
    input.LinesStartingWithKeyword(_filename,keyword,lines,false);
    
    if (lines.size()>1) {error.Fatal("number of nodes defined more than once.");}
    
    //Checking the number of input arguments
    ostringstream convertedString;
    convertedString << lines[0].size()-1;
    if (lines[0].size()-1!=1) {error.Fatal("nodes command needs 1 argument and " + convertedString.str() + " were given.");}
    
    //Adding the information to the instance
    numberOfNodes=strtod(lines[0][1].c_str(),&endCharact);
    
    if (numberOfNodes==1)  {if (notVerboseBool==false) {cout << numberOfNodes <<" node in NodePreciSo: OK" << endl;}}
    else {if (notVerboseBool==false) {cout << numberOfNodes <<" nodes in NodePreciSo: OK" << endl;}}
    
    // Create numberOfNodes copies of preciso
    Node.assign(numberOfNodes,preciso);
}

void NodePreciso::InitializeNodes(string const& _filename,bool onlyOneNode)
{
    char* endCharact = NULL;
    //Keyword starting the lines in the data file
    string keyword;
    //Matrix of lines containing the keyword. /!\ lines is erased at the beginning of each call of LinesStartingWithKeyword
    vector<vector<string> > lines;
    keyword="node";
    if (onlyOneNode)
    {
        input.LinesStartingWithKeyword(_filename,keyword,lines,true);
        if (lines.size()>0) {
            if (lines.size()!=numberOfNodes)    {
                ostringstream convertedString1, convertedString2;
                convertedString1 << lines.size();
                convertedString2 << numberOfNodes;
                error.Fatal("the number of described nodes (" + convertedString1.str() + ") does not match the indicated number of nodes (" + convertedString2.str() + ").");
                if (lines[0].size()-1!=5) {error.Fatal("node command needs 5 arguments and " + convertedString1.str() + " were given for node " + convertedString2.str());}
            }
            Node[0].setVolume(strtod(lines[0][5].c_str(),&endCharact));
            Node[0].InitializeThermodynamicData();
        }
    }
    else {
        input.LinesStartingWithKeyword(_filename,keyword,lines,false);
        if (lines.size()!=numberOfNodes)    {
            ostringstream convertedString1, convertedString2;
            convertedString1 << lines.size();
            convertedString2 << numberOfNodes;
            error.Fatal("the number of described nodes (" + convertedString1.str() + ") does not match the indicated number of nodes (" + convertedString2.str() + ").");
        }
        
        //If the first node number is not 0
        if (strtod(lines[0][1].c_str(),&endCharact)!=0)    {
            error.Warning("first node number is not 0, the nodes number are shifted.");
            nodeShift=strtod(lines[0][1].c_str(),&endCharact);
        }
        
        vector<bool> DefinedNodes;
        for (size_t i=0;i<numberOfNodes;i++) {DefinedNodes.push_back(false);}
        
        for (size_t i=0;i<lines.size();i++)    {
            //Checking the number of input arguments
            ostringstream convertedString1, convertedString2;
            convertedString1 << lines[i].size()-1;
            convertedString2 << i;
            if (lines[i].size()-1!=5) {error.Fatal("node command needs 5 arguments and " + convertedString1.str() + " were given for node " + convertedString2.str());}
            
            int nodeIndex=strtod(lines[i][1].c_str(),&endCharact)-nodeShift;
            
            if (DefinedNodes[nodeIndex])        {
                ostringstream convertedString3;
                convertedString3 << nodeIndex;
                error.Fatal("node " + convertedString3.str() + " defined twice.");
            }
            if (nodeIndex<0) {error.Fatal("negative node index. An incorrect shift due to the index of the first described node might be the reason.");}
            if (nodeIndex>=signed(numberOfNodes)) {error.Fatal("node number too high. An incorrect shift due to the index of the first described node might be the reason.");}
            //Adding the information to the instance
            Node[nodeIndex].setNodeIndex(nodeIndex);
            Node[nodeIndex].setXPos(strtod(lines[i][2].c_str(),&endCharact));
            Node[nodeIndex].setYPos(strtod(lines[i][3].c_str(),&endCharact));
            Node[nodeIndex].setZPos(strtod(lines[i][4].c_str(),&endCharact));
            Node[nodeIndex].setVolume(strtod(lines[i][5].c_str(),&endCharact));
            DefinedNodes[nodeIndex]=true;
            if (notVerboseBool==false) {cout << "Node " << nodeIndex << " in NodePreciSo: OK" << endl;}
        }
        // Initialize time step
        dt=Node[0].initialDT;
        
        // The smallest time step of each preciso must be the same than 'nodeSmallestTimeStep'
        for (size_t i=0;i<numberOfNodes;i++) {Node[i].setSmallestTimeStep(nodeSmallestTimeStep);}
    }
}

void NodePreciso::InitializeConnectivities(string const& _filename)
{
    char* endCharact = NULL;
    //Keyword starting the lines in the data file
    string keyword;
    //Matrix of lines containing the keyword. /!\ lines is erased at the beginning of each call of LinesStartingWithKeyword
    vector<vector<string> > lines;
    //--------------------CONNECTIVITIES DATA----------------------
    keyword="connect";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    
    numberOfConnections=lines.size();
    if (notVerboseBool==false) {cout << lines.size() <<" connections" << endl;}
    
    for (size_t i=0;i<lines.size();i++)    {
        //Checking the number of input arguments
        ostringstream convertedString1, convertedString2;
        convertedString1 << lines[i].size()-1;
        convertedString2 << i;
        if (lines[i].size()-1!=3) {error.Fatal("connect command needs 3 arguments and " + convertedString1.str() + " were given for the " + convertedString2.str() + "th connection.");}
        
        vector<int> tempConnection;
        //Nodes of the connection, in the increasing order and shift the connections numbers by nodeShift
        //if the nodes described in the input file don't start with 0
        if (strtod(lines[i][1].c_str(),&endCharact)<strtod(lines[i][2].c_str(),&endCharact))        {
            tempConnection.push_back(atoi(lines[i][1].c_str())-nodeShift);
            tempConnection.push_back(atoi(lines[i][2].c_str())-nodeShift);        }
        else        {
            tempConnection.push_back(atoi(lines[i][2].c_str())-nodeShift);
            tempConnection.push_back(atoi(lines[i][1].c_str())-nodeShift);
        }
        Connection.push_back(tempConnection);
        //Check that the connections are correctly defined:
        if ((tempConnection[0]<0)||(tempConnection[1]>=signed(numberOfNodes))) {error.Fatal("incorrect node number in connection " + convertedString2.str() );}
        
        //Surface of the connection
        Surface.push_back(atof(lines[i][3].c_str()));
        if (notVerboseBool==false) {cout << "Connection " << i << " in NodePreciSo: OK" << endl;}
    }
    //Check that no connection is defined twice
    if (Connection.size()>1) {
        for (size_t i=0;i<Connection.size()-1;i++)    {
            for (size_t j=i+1;j<Connection.size();j++)        {
                ostringstream convertedString1, convertedString2;
                convertedString1 << Connection[i][0];
                convertedString2 << Connection[i][1];
                if ((Connection[i][0]==Connection[j][0]) && (Connection[i][1]==Connection[j][1])) {error.Fatal("Connection defined twice "+convertedString1.str()+" "+convertedString2.str());}
                if ((Connection[i][0]==Connection[j][1]) && (Connection[i][1]==Connection[j][0])) {error.Fatal("Connection defined twice "+convertedString1.str()+" "+convertedString2.str());}
            }
        }
    }
    //--------------------VERIFICATION OF DISTANCE FOR EACH CONNECTIONS--------------------
    int node0=0,node1=0;
    double distanceNodes=0.0,xPos0=0.,xPos1=0.,yPos0=0.,yPos1=0.,zPos0=0.,zPos1=0.;
    for (size_t i=0;i<numberOfConnections;i++) {
        node0=Connection[i][0]; node1=Connection[i][1];
        xPos0=Node[node0].xPos; xPos1=Node[node1].xPos;
        yPos0=Node[node0].yPos; yPos1=Node[node1].yPos;
        zPos0=Node[node0].zPos; zPos1=Node[node1].zPos;
        distanceNodes=sqrt((xPos1-xPos0)*(xPos1-xPos0)+(yPos1-yPos0)*(yPos1-yPos0)+(zPos1-zPos0)*(zPos1-zPos0));
        if (distanceNodes==0)        {
            ostringstream convertedString1,convertedString2;
            convertedString1 << node0; convertedString2 << node1;
            error.Fatal("If you have connections, distance between nodes (here "+convertedString1.str()+" and "+convertedString2.str()+") can't be NULL");
        }
    }
}

void NodePreciso::InitializeNodeProperties(string const& _filename)
{
    char* endCharact = NULL;
    //-----------LOAD ALL INITIAL NAMES OF PRECIPITATES (useful for precipitate's nodeProperty treatment -------------
    size_t nbPrecipit=Node[0].Precipitates.size();
    vector<string> namesPrecipit;
    for (size_t p=0;p<nbPrecipit;p++) {namesPrecipit.push_back(Node[0].Precipitates[p].GetName());}
    
    //--------------------GENERALITIES--------------------
    //Keyword starting input file lines
    string keyword;
    //Matrix of lines containing the keyword. /!\ lines is erased at the beginning of each call of LinesStartingWithKeyword
    vector<vector<string> > lines;
    
    
    //--------------------NODE PROPERTIES--------------------
    keyword="nodeProperty";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    //Group the node properties for each node
    vector<vector<string> > strainLoadLines,parametersForHardeningLines,youngLines,poissonLines,boostPrecipitateDiffusionLines;
    vector<vector<string> > matrixLines,elementsLines,precipitatesLines,temperatureLines,initialDistribLines,noPrecipitationLines;
    vector<vector<unsigned int> > numberOfChangedProperties;
    vector<unsigned int> tempVector;
    tempVector.assign(11,0);
    numberOfChangedProperties.assign(numberOfNodes,tempVector);
    //to save first and final node number of the range
    size_t nbOfNodeHere=0,nodeBegin=0,nodeEnd=0,nbMatrix=1;
    
    for (size_t i=0;i<lines.size();i++)    {
        ostringstream convertedString1,convertedString2;
        nodeBegin=atoi(lines[i][1].c_str())-nodeShift;
        nodeEnd=atoi(lines[i][2].c_str())-nodeShift;
        nbOfNodeHere=fabs(nodeEnd-nodeBegin)+1;
        
        if (nodeBegin<0 || nodeBegin>=size_t(numberOfNodes)) {error.Fatal("Incorrect first node number in node property.");}
        if (nodeEnd<0 || nodeEnd>=size_t(numberOfNodes)) {error.Fatal("Incorrect second node number in node property.");}
        if (nodeEnd<nodeBegin) {error.Fatal("Second nodeNumber must be greater than the first.");}
        if (lines[i].size()<4) {error.Fatal("For nodeProperty we must have at least 3 arguments");}
        
        if (lines[i][3]=="matrix")        {
            error.Fatal("In InitializeNodeProperties : we desactived this option and different matrix is commented in diffusion");
            //Checking the number of input arguments for the matrix
            convertedString1 << lines[i].size()-4;
            if (lines[i].size()-4!=1) {error.Fatal("Matrix command needs 1 arguments: 'fileOfNewMatrix', here " + convertedString1.str() + " arguments for nodes " + lines[i][1] +" : "+lines[i][2]);}
            matrixLines.push_back(lines[i]);
            for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
                convertedString2 << k;
                numberOfChangedProperties[k][0]++;
                if (numberOfChangedProperties[k][0]>1) {error.Fatal("Matrix redefined twice for node "+convertedString2.str());}
            }
        }
        else if (lines[i][3]=="element")        {
            //Checking the number of input arguments for the element
            convertedString1 << lines[i].size()-4;
            if (lines[i].size()-4!=5) {error.Fatal("Element command needs 5 arguments and " + convertedString1.str() + " were given for nodes " + lines[i][1] +" : "+lines[i][2]);}
            elementsLines.push_back(lines[i]);
            for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
                convertedString2 << k;
                numberOfChangedProperties[k][1]++;
                if (numberOfChangedProperties[k][1]>(preciso.Elements.size()-nbMatrix)) {error.Fatal("Two many elements (re)defined for node "+convertedString2.str());}
            }
        }
        else if (lines[i][3]=="precipitate")        {
            //Checking the number of input arguments for the precipitate and that the name of new precipitate is different
            if (lines[i].size()<13) {error.Fatal("insufficient number of arguments for precipitates for nodes " +lines[i][1]+" : "+lines[i][2]);}
            for (size_t p=0;p<nbPrecipit;p++) {
                if (namesPrecipit[p]==lines[i][4]){error.Warning("If we change precipitate (for nodes "+lines[i][1]+" : "+lines[i][2]+") we must load an initial distribution to don't lose the current!");}
            }
            precipitatesLines.push_back(lines[i]);
            for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
                convertedString2 << k;
                numberOfChangedProperties[k][2]++;
                if (!Node[k].solvePrecipitation) {error.Fatal("Can't define a new precipitation property if 'noPrecipitation' is actived for this node : "+convertedString2.str());}
                if (numberOfChangedProperties[k][2]>preciso.Precipitates.size()) {error.Fatal("Two many precipitates (re)defined for node " +convertedString2.str());}
            }
        }
        else if (lines[i][3]=="temperatureProfile")        {
            //Checking the number of input arguments for the temperature
            if ((lines[i].size()-4)%2!=0) {error.Fatal("Incorrect number of arguments for temperature at nodes "+lines[i][1]+" : "+lines[i][2]);}
            /// \warning We must keep these two conditions otherwise we can have false results without any error (in particular case)!!!
            
            if (fabs(strtod(lines[i][4].c_str(),&endCharact)-preciso.temperature.GetAndCheckInitialTime())>NUMERICLIMITDOUBLE) {
                if (numberOfConnections>0) {error.Fatal("nodeProperty: initial time must be same as time[0] in temperatureProfil for nodes " + lines[i][1] +" : "+lines[i][2]);}
                else {error.Warning("Here 'numberOfConnections<=0' and we have warning nodeProperty: initial time is not same as time[0] in temperatureProfil for nodes " + lines[i][1] +" : "+lines[i][2]);}
            }
            if (fabs(strtod(lines[i][lines[i].size()-2].c_str(),&endCharact)-preciso.temperature.GetTotalTime())>NUMERICLIMITDOUBLE) {
                if (numberOfConnections>0) {error.Fatal("nodeProperty: final time must be same as time[end] in temperatureProfil for nodes " + lines[i][1] +" : "+lines[i][2]);}
                else {error.Warning("Here 'numberOfConnections<=0' and we have warning nodeProperty: final time is not same as time[end] in temperatureProfil for nodes " + lines[i][1] +" : "+lines[i][2]);}
            }
            temperatureLines.push_back(lines[i]);
            for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
                convertedString2 << k;
                numberOfChangedProperties[k][3]++;
                if (numberOfChangedProperties[k][3]>1) {error.Fatal("'temperatureProfile' redefined twice for node "+convertedString2.str());}
            }
        }
        else if (lines[i][3]=="initialDistrib")        {
            //Checking the number of input arguments for the initialDistrib
            if ((lines[i].size()-4<2)||((lines[i].size()-4)%2!=0)) {error.Fatal("Incorrect number of arguments for 'initialDistrib' at nodes "+lines[i][1]+" : "+lines[i][2]);}
            initialDistribLines.push_back(lines[i]);
            for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
                convertedString2 << k;
                numberOfChangedProperties[k][4]++;
                if (numberOfChangedProperties[k][4]>1) {error.Fatal("'InitialDistrib' redefined twice node "+convertedString2.str());}
            }
        }
        else if (lines[i][3]=="noPrecipitation")        {
            if (lines[i].size()!=4) {error.Fatal("Incorrect number of arguments for noPrecipitation");}
            noPrecipitationLines.push_back(lines[i]);
            for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
                convertedString2 << k;
                numberOfChangedProperties[k][5]++;
            }
        }
        else if (lines[i][3]=="strainLoad")        {
            //Checking the number of input arguments for the strainLoad
            if (lines[i].size()-4!=2) {error.Fatal("Incorrect number of arguments for 'strainLoad' at nodes "+lines[i][1]+" : "+lines[i][2]);}
            strainLoadLines.push_back(lines[i]);
            for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
                convertedString2 << k;
                numberOfChangedProperties[k][6]++;
                if (numberOfChangedProperties[k][6]>1) {error.Fatal("'strainLoad' redefined twice node "+convertedString2.str());}
            }
        }
        else if (lines[i][3]=="parametersForHardening")        {
            parametersForHardeningLines.push_back(lines[i]);
            for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
                convertedString2 << k;
                numberOfChangedProperties[k][7]++;
                if (numberOfChangedProperties[k][7]>1) {error.Fatal("'parametersForHardeningLines' redefined twice node "+convertedString2.str());}
            }
        }
        else if (lines[i][3]=="young")        {
            youngLines.push_back(lines[i]);
            for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
                convertedString2 << k;
                numberOfChangedProperties[k][8]++;
                if (numberOfChangedProperties[k][8]>1) {error.Fatal("'youngLines' redefined twice node "+convertedString2.str());}
            }
        }
        else if (lines[i][3]=="poisson")        {
            poissonLines.push_back(lines[i]);
            for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
                convertedString2 << k;
                numberOfChangedProperties[k][9]++;
                if (numberOfChangedProperties[k][9]>1) {error.Fatal("'poissonLines' redefined twice node "+convertedString2.str());}
            }
        }
        else if (lines[i][3]=="boostPrecipitateDiffusion")        {
            //Checking the number of input arguments for the boostPrecipitateDiffusion
            convertedString1 << lines[i].size()-4;
            if (lines[i].size()-4!=2) {error.Fatal("boostPrecipitateDiffusion command needs 2 arguments and " + convertedString1.str() + " were given for nodes " + lines[i][1] +" : "+lines[i][2]);}
            boostPrecipitateDiffusionLines.push_back(lines[i]);
            for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
                convertedString2 << k;
                numberOfChangedProperties[k][10]++;
            }
        }
        else {error.Fatal("incorrect keyword for node property.");}
    }
    vector<string> tempLine;
    /// \warning Keep this order,there is a logical (example:udpate initialDistrib after precipitation,cancel precipitation even if we have previously a modification)
    /// \warning If we change a precipitate or a matrix it cancel its associed initialDistrib. So, we have to add a nodeProperty to reload an initialDistrib
    //Change the matrix
    string initialMatrixName=Node[0].matrix.GetName();
    for (size_t i=0;i<matrixLines.size();i++)    {
        ostringstream convertedString1,convertedString2;
        //read associed elements, precipitates and matrix
        string matrixInputFile=matrixLines[i][4];
        //for considered nodes we will erase Matrix and associed element, precipitates
        nodeBegin=atoi(matrixLines[i][1].c_str())-nodeShift; convertedString1<<nodeBegin;
        nodeEnd=atoi(matrixLines[i][2].c_str())-nodeShift;   convertedString2<<nodeEnd;
        nbOfNodeHere=fabs(nodeEnd-nodeBegin)+1;
        bool firstCallHere=true;
        for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
            Node[k].ChangeMatrixAndAssiocedElemPreci(firstCallHere,matrixInputFile,nodeBegin,nodeBegin+nbOfNodeHere-1);
            firstCallHere=false;
        }
        if (notVerboseBool==false) {
            cout << "Matrix " << initialMatrixName << " and associed elements-precipitates redefined with file '" \
            << matrixInputFile <<"' in PreciSo nodes " << convertedString1.str() << " : " << convertedString2.str() << endl;
        }
    }
    //Change the elements
    for (size_t i=0;i<elementsLines.size();i++)    {
        ostringstream convertedString1,convertedString2;
        //we erase the string "nodeProperty" and associed nodes and we send to the usual function
        tempLine.clear();
        for (size_t j=3;j<elementsLines[i].size();j++) {tempLine.push_back(elementsLines[i][j]);}
        nodeBegin=atoi(elementsLines[i][1].c_str())-nodeShift; convertedString1<<nodeBegin;
        nodeEnd=atoi(elementsLines[i][2].c_str())-nodeShift;   convertedString2<<nodeEnd;
        nbOfNodeHere=fabs(nodeEnd-nodeBegin)+1;
        for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {Node[k].ChangeElement(tempLine);}
        if (notVerboseBool==false)
        {
            cout << "Element " << elementsLines[i][4].c_str() << " redefined in PreciSo nodes " << convertedString1.str() \
            << " : " << convertedString2.str() << endl;
        }
    }
    //Change the precipitates
    for (size_t i=0;i<precipitatesLines.size();i++)    {
        ostringstream convertedString1,convertedString2;
        //we erase the string "nodeProperty" and associed nodes and we send to the usual function
        tempLine.clear();
        for (size_t j=3;j<precipitatesLines[i].size();j++) {tempLine.push_back(precipitatesLines[i][j]);}
        nodeBegin=atoi(precipitatesLines[i][1].c_str())-nodeShift; convertedString1<<nodeBegin;
        nodeEnd=atoi(precipitatesLines[i][2].c_str())-nodeShift;   convertedString2<<nodeBegin;
        nbOfNodeHere=fabs(nodeEnd-nodeBegin)+1;
        for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
            Node[k].ChangePrecipitate(tempLine);
        }
        if (notVerboseBool==false) {
            cout << "Precipitates " << precipitatesLines[i][4].c_str() << " redefined in PreciSo nodes " << convertedString1.str() \
            << " : " << convertedString2.str() << endl;
        }
    }
    //Change the initialDistrib
    for (size_t i=0;i<initialDistribLines.size();i++)    {
        tempLine.clear();
        ostringstream convertedString1,convertedString2;
        //we erase the string "nodeProperty" and associed nodes and we send to the usual function
        for (size_t j=3;j<initialDistribLines[i].size();j++) {tempLine.push_back(initialDistribLines[i][j]);}
        nodeBegin=atoi(initialDistribLines[i][1].c_str())-nodeShift; convertedString1<<nodeBegin;
        nodeEnd=atoi(initialDistribLines[i][2].c_str())-nodeShift;   convertedString2<<nodeEnd;
        nbOfNodeHere=fabs(nodeEnd-nodeBegin)+1;
        for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {Node[k].LoadInitialDistrib(tempLine);}
        if (notVerboseBool==false) {
            cout << "initialDistribLines redefined in PreciSo nodes " << convertedString1.str() \
            << " : " << convertedString2.str() << endl;
        }
    }
    //Define the nodes at which no precipitation occurs
    for (size_t i=0;i<noPrecipitationLines.size();i++)    {
        ostringstream convertedString1,convertedString2;
        nodeBegin=atoi(noPrecipitationLines[i][1].c_str())-nodeShift; convertedString1<<nodeBegin;
        nodeEnd=atoi(noPrecipitationLines[i][2].c_str())-nodeShift;   convertedString2<<nodeEnd;
        nbOfNodeHere=fabs(nodeEnd-nodeBegin)+1;
        for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {Node[k].solvePrecipitation=false;Node[k].Precipitates.clear();}
        error.Warning("No precipitation at nodes "+convertedString1.str()+" : "+convertedString2.str());
    }
    //Change the temperatures
    for (size_t i=0;i<temperatureLines.size();i++)    {
        tempLine.clear();
        ostringstream convertedString1,convertedString2;
        //we erase the string "nodeProperty" and associed nodes and we send to the usual function
        for (size_t j=3;j<temperatureLines[i].size();j++) {tempLine.push_back(temperatureLines[i][j]);}
        nodeBegin=atoi(temperatureLines[i][1].c_str())-nodeShift; convertedString1<<nodeBegin;
        nodeEnd=atoi(temperatureLines[i][2].c_str())-nodeShift;   convertedString2<<nodeEnd;
        nbOfNodeHere=fabs(nodeEnd-nodeBegin)+1;
        for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
            Node[k].temperature.DefineTemperature(tempLine);
            Node[k].firstTime=Node[k].temperature.GetInitialTime();
        }
        if (notVerboseBool==false) {
            cout << "Temperature profile redefined for nodes " << convertedString1.str() \
            << " : " << convertedString2.str() << endl ;
        }
    }
    //Change 'strainLoad'
    for (size_t i=0;i<strainLoadLines.size();i++)    {
        ostringstream convertedString1,convertedString2;
        //we erase the string "nodeProperty" and associed nodes and we send to the usual function
        nodeBegin=atoi(strainLoadLines[i][1].c_str())-nodeShift; convertedString1<<nodeBegin;
        nodeEnd=atoi(strainLoadLines[i][2].c_str())-nodeShift;   convertedString2<<nodeEnd;
        nbOfNodeHere=fabs(nodeEnd-nodeBegin)+1;
        for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
            Node[k].mechanical.loadStrainLoading(strainLoadLines[i][4],strainLoadLines[i][5]);
        }
        if (notVerboseBool==false) {
            cout << "'strainLoad' for nodes " << convertedString1.str() << " : " << convertedString2.str() << endl ;
        }
    }
    //Change 'parametersForHardeningLines'
    for (size_t i=0;i<parametersForHardeningLines.size();i++)    {
        tempLine.clear();
        for (size_t j=3;j<parametersForHardeningLines[i].size();j++) {tempLine.push_back(parametersForHardeningLines[i][j]);}
        ostringstream convertedString1,convertedString2;
        //we erase the string "nodeProperty" and associed nodes and we send to the usual function
        nodeBegin=atoi(parametersForHardeningLines[i][1].c_str())-nodeShift; convertedString1<<nodeBegin;
        nodeEnd=atoi(parametersForHardeningLines[i][2].c_str())-nodeShift;   convertedString2<<nodeEnd;
        nbOfNodeHere=fabs(nodeEnd-nodeBegin)+1;
        //we keep on
        for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
            Node[k].mechanical.DefineCoefficientsForHardeningModel(tempLine);
        }
        if (notVerboseBool==false) {
            cout << "'parametersForHardening' for nodes " << convertedString1.str() << " : " << convertedString2.str() << endl ;
        }
    }
    //Change 'young'
    for (size_t i=0;i<youngLines.size();i++)    {
        tempLine.clear();
        for (size_t j=3;j<youngLines[i].size();j++) {tempLine.push_back(youngLines[i][j]);}
        ostringstream convertedString1,convertedString2;
        //we erase the string "nodeProperty" and associed nodes and we send to the usual function
        nodeBegin=atoi(youngLines[i][1].c_str())-nodeShift; convertedString1<<nodeBegin;
        nodeEnd=atoi(youngLines[i][2].c_str())-nodeShift;   convertedString2<<nodeEnd;
        nbOfNodeHere=fabs(nodeEnd-nodeBegin)+1;
        //we keep on
        for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
            if ((tempLine.size()-1)%2!=0) {error.Fatal("Nodes "+convertedString1.str()+" : "+convertedString2.str()+"-you must have for each temperature a young modulus (pair arguments)");}
            Node[k].mechanical.DefineYoungModulus(tempLine);
        }
        if (notVerboseBool==false) {
            cout << "'young' for nodes " << convertedString1.str() << " : " << convertedString2.str() << endl ;
        }
    }
    //Change 'poisson'
    for (size_t i=0;i<poissonLines.size();i++)    {
        tempLine.clear();
        for (size_t j=3;j<poissonLines[i].size();j++) {tempLine.push_back(poissonLines[i][j]);}
        ostringstream convertedString1,convertedString2;
        //we erase the string "nodeProperty" and associed nodes and we send to the usual function
        nodeBegin=atoi(poissonLines[i][1].c_str())-nodeShift; convertedString1<<nodeBegin;
        nodeEnd=atoi(poissonLines[i][2].c_str())-nodeShift;   convertedString2<<nodeEnd;
        nbOfNodeHere=fabs(nodeEnd-nodeBegin)+1;
        //we keep on
        for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
            if ((tempLine.size()-1)%2!=0) {error.Fatal("Nodes "+convertedString1.str()+" : "+convertedString2.str()+"-you must have for each temperature a young modulus (pair arguments)");}
            Node[k].mechanical.DefinePoissonCoeff(tempLine);
        }
        if (notVerboseBool==false) {
            cout << "'poisson' for nodes " << convertedString1.str() << " : " << convertedString2.str() << endl ;
        }
    }
    //Change the boostPrecipitateDiffusion
    for (size_t i=0;i<boostPrecipitateDiffusionLines.size();i++)    {
        ostringstream convertedString1,convertedString2;
        //we erase the string "nodeProperty" and associed nodes and we send to the usual function
        tempLine.clear();
        for (size_t j=3;j<boostPrecipitateDiffusionLines[i].size();j++) {tempLine.push_back(boostPrecipitateDiffusionLines[i][j]);}
        nodeBegin=atoi(boostPrecipitateDiffusionLines[i][1].c_str())-nodeShift; convertedString1<<nodeBegin;
        nodeEnd=atoi(boostPrecipitateDiffusionLines[i][2].c_str())-nodeShift;   convertedString2<<nodeEnd;
        nbOfNodeHere=fabs(nodeEnd-nodeBegin)+1;
        for (size_t k=nodeBegin;k<nodeBegin+nbOfNodeHere;k++) {
            Node[k].ChangeBoostPrecipitateDiffusion(tempLine);
        }
        if (notVerboseBool==false)
        {
            cout << "boostPrecipitateDiffusionLines " << boostPrecipitateDiffusionLines[i][4].c_str() << " redefined in PreciSo nodes " << convertedString1.str() \
            << " : " << convertedString2.str() << endl;
        }
    }
    //Reinitialize the thermodynamic data for the PreciSo that where changed
    for (size_t i=0;i<numberOfChangedProperties.size();i++)    {
        if ((numberOfChangedProperties[i][0]!=0)|| (numberOfChangedProperties[i][1]!=0) || \
            (numberOfChangedProperties[i][2]!=0) ||(numberOfChangedProperties[i][3]!=0)|| \
            (numberOfChangedProperties[i][4]!=0)|| (numberOfChangedProperties[i][5]!=0) || \
            (numberOfChangedProperties[i][6]!=0) || (numberOfChangedProperties[i][7]!=0) || \
            (numberOfChangedProperties[i][8]!=0) || (numberOfChangedProperties[i][9]!=0) || \
            (numberOfChangedProperties[i][10]!=0)
            )  {
            Node[i].InitializeThermodynamicData();
            Node[i].checkVectorOfHardeningCoupling();
        }
    }
}

void NodePreciso::InitializeOnlyMechanicOption(string const& _filename)
{
    //-----------LOAD ALL INITIAL NAMES OF PRECIPITATES (useful for precipitate's nodeProperty treatment -------------
    size_t nbPrecipit=Node[0].Precipitates.size();
    vector<string> namesPrecipit;
    for (size_t p=0;p<nbPrecipit;p++) {namesPrecipit.push_back(Node[0].Precipitates[p].GetName());}
    
    //--------------------only mechanic treatment--------------------
    //Keyword starting input file lines
    string keyword,nameOfDitributionFile;
    //Matrix of lines containing the keyword. /!\ lines is erased at the beginning of each call of LinesStartingWithKeyword
    vector<vector<string> > lines; lines.clear();
    vector<string> linesTemp,tempLine; linesTemp.clear(),tempLine.clear();
    keyword="onlyMechanic";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0) {onlyMechanicComputation=true;}
    if (onlyMechanicComputation)
    {
        //---------------------- load name of distrib file --------------------
        keyword="savedistribution";
        input.LinesStartingWithKeyword(_filename,keyword,lines,false);
        if (lines.size()>1) {error.Fatal("In 'onlyMechanicComputation' more than one savedistribution command");}
        if ((lines[0].size()-1)!=2) {error.Fatal("In 'onlyMechanicComputation' incorrect number of arguments for savedistribution.");}
        nameOfDitributionFile=lines[0][1];
        
        //-------------- Here we generate a matrix of line property as we can find in input file ----------
        //the file that is used for initial distrib is the last result
        lines.clear();
        for (size_t i=0;i<numberOfNodes;i++) {
            ostringstream convertedString1;
            convertedString1 << i;
            linesTemp.clear();
            linesTemp.push_back("nodeProperty");
            linesTemp.push_back(convertedString1.str());
            linesTemp.push_back(convertedString1.str());
            linesTemp.push_back("initialDistrib");
            for (size_t j=0;j<nbPrecipit;j++) {
                //concatenate the name of Precipitate
                linesTemp.push_back(namesPrecipit[j]);
                //concatenate the name of file for precipitate "j" and node "i"
                linesTemp.push_back(nameOfDitributionFile+namesPrecipit[j]+"_"+convertedString1.str()+".dat");
            }
            lines.push_back(linesTemp);
            Node[i].onlyMechanicComputation=true;
        }
        
        error.Warning("If you use 'onlyMechanic' precipitation and diffusion are not computed");
        
        //------------check initialDistrib lines----------------
        for (size_t i=0;i<lines.size();i++)    {
            //check number of arguments
            if (lines[i][3]=="initialDistrib") {if ((lines[i].size()-4<2)||((lines[i].size()-4)%2!=0)) {error.Fatal("Incorrect number of arguments in 'onlyMechanicComputation' "+lines[i][1]+" : "+lines[i][2]);}}
            else {
                ostringstream convertedString2;
                convertedString2 << i;
                error.Fatal("In 'onlyMechanicComputation' the argument n°3 must be 'InitialDistrib' for node "+convertedString2.str());
            }
            //keep only the usefull argument and call 'LoadInitialDistrib'
            tempLine.clear();
            for (size_t j=3;j<lines[i].size();j++) {tempLine.push_back(lines[i][j]);}
            
            //load previous results
            Node[i].LoadInitialDistrib(tempLine);
        }
        //-------------------------------------------------------
    }
}

void NodePreciso::WriteParameterLog()
{
    /// \todo Modify the writing in the log that opens and closes the file at each time.
    ostringstream convertStr;
    error.Log("Constant parameters values");
    convertStr.str("");convertStr << NUMERICLIMITDOUBLE;      error.Log("Max precision for double: "+convertStr.str());
    convertStr.str("");convertStr << RGAZCONSTANT;            error.Log("Gas constant: "+convertStr.str());
    convertStr.str("");convertStr << KB;                      error.Log("Boltzman constant: "+convertStr.str());
}

//################################ MAIN LOOP ##########################################
void NodePreciso::Run()
{
    // Node #0 indicates the duration
    if (numberOfConnections==0)  {
        //All nodes are independant. Each node full computation is treated independantly to save time (the nodes don't have to adapt to the
        // other's times.
        for(size_t i=0;i<Node.size();i++)        {
            unsigned int timestep=1;
            unsigned int invalidTimesteps=0;
            vector<Precipitate> TempPrecipitates;
            vector<Element> TempElements;
            Matrix TempMatrix;
            double CurrentTemperature=0.;
            bool validTimeStep=true;
            double timeCurrent=0.;
            
            TempPrecipitates=preciso.Precipitates;
            TempElements=preciso.Elements;
            TempMatrix=preciso.matrix;
            dt=Node[i].dt;
            /// \warning If 'numberOfConnections==0' all nodes are independant, so we must considere each final time that is not necessary the same
            while (Node[i].currentTime<Node[i].temperature.GetTotalTime() && fabs(Node[i].currentTime-Node[i].temperature.GetTotalTime())>NUMERICLIMITDOUBLE)     {
                validTimeStep=true;
                //nucleation/growth/dissolution and associed verification
                TempPrecipitates.clear();  TempElements.clear();
                TempPrecipitates=Node[i].Precipitates;
                TempElements=Node[i].Elements;
                TempMatrix=Node[i].matrix;
                timeCurrent=Node[i].currentTime;
                CurrentTemperature=Node[i].temperature.GetTemperature(timeCurrent);
                
                //cout << "------------" << endl;
                //cout << i << endl;
                
                if (!Node[i].ValidNuclGrowthDiss(TempMatrix, TempElements,TempPrecipitates,CurrentTemperature,timestep,reasonTimeStepRejected)){
                    validTimeStep=false;
                    invalidTimesteps++;
                }
                // if the programm enters in a new temperature domain for a given node, ajust its dt to reach its domain limit and
                // adjust all other nodes' dt to the smallest dt.
                if (validTimeStep)   {
                    //the mecanical computation must be before 'PostNuclGrowthDiss'
                    Node[i].mechanicalComputation(false,false,0,TempMatrix, TempElements, TempPrecipitates, CurrentTemperature);
                    dt=Node[i].PostNuclGrowthDiss(TempMatrix, TempElements, TempPrecipitates,CurrentTemperature,timestep,reduced);
                    timestep++;
                    reduced=false;
                    if (notVerboseBool==false) {cout << "Simulation time " << Node[i].currentTime << endl;}                }
                else  {
                    dt*=reduceDT;
                    reduced=true;
                    if (notVerboseBool==false) {
                        cout << "Time step rejected by node " << i << " because " << reasonTimeStepRejected << endl;
                    }
                }
                Node[i].dt=dt;
            }
            // Save final distributions
            Node[i].output.TimeStepOutput(Node[i].mechanical, Node[i].matrix,Node[i].Elements, Node[i].Precipitates, Node[i].temperature,Node[i].currentTimeIndex, Node[i].currentTime, CurrentTemperature, Node[i].dt, timestep, Node[i].nodeIndex, true);
            
            if (notVerboseBool==false) {
                cout << "Computation ended for node " << i << endl;
                cout << "Time steps: " << timestep << endl;
                cout << "Rejected time steps: " << invalidTimesteps << endl;
            }
        }
    }
    else    {
        unsigned int timestep=1;
        unsigned int invalidTimesteps=0;
        vector<vector<Precipitate> > TempPrecipitates;
        vector<vector<Element> > TempElements;
        vector<Matrix> TempMatrix; //useful for flux management
        vector<double> CurrentTemperature;
        bool validTimeStep=true;
        double tempdt=0.,timeCurrent=0.;
        
        //Are these lines useful ?
        for(size_t i=0;i<Node.size();i++){
            TempPrecipitates.push_back(preciso.Precipitates);
            TempElements.push_back(preciso.Elements);
            TempMatrix.push_back(preciso.matrix);
            CurrentTemperature.push_back(0);
        }
        
        //Nodes have connections. The time are the same for each. Can take a longer time. Might be improved.
        /// \warning If 'numberOfConnections!=0' nodes are dependant-->final&initial times must be the same for each nodes so with check just PreciSo final Time!!!
        while (Node[0].currentTime<preciso.temperature.GetTotalTime() && fabs(Node[0].currentTime-preciso.temperature.GetTotalTime())>NUMERICLIMITDOUBLE)   {
            validTimeStep=true;
            size_t failingNodeIndex=0;
            for(size_t i=0;i<Node.size();i++){
                //nucleation/growth/dissolution and associed verification
                TempPrecipitates[i].clear();  TempElements[i].clear();
                TempPrecipitates[i]=Node[i].Precipitates;
                TempElements[i]=Node[i].Elements;
                TempMatrix[i]=Node[i].matrix;
                timeCurrent=Node[i].currentTime;
                CurrentTemperature[i]=Node[i].temperature.GetTemperature(timeCurrent);
                Node[i].PreNuclGrowthDiss(TempMatrix[i],TempElements[i],TempPrecipitates[i],CurrentTemperature[i]);
                if (!Node[i].ValidNuclGrowthDiss(TempMatrix[i], TempElements[i], TempPrecipitates[i], CurrentTemperature[i], timestep,reasonTimeStepRejected)){
                    validTimeStep=false;
                    failingNodeIndex=i;
                    invalidTimesteps++;
                    break;
                }
                
                //cout << "------------" << endl;
                //cout << i << endl;
                
            }
            if (validTimeStep) {
                if(Connection.size()>0) {
                    if (!validFluxManagement(Node,TempElements,TempMatrix,TempPrecipitates,CurrentTemperature,reasonTimeStepRejected)) {
                        validTimeStep=false;}
                }
            }
            // if the programm enters in a new temperature domain for a given node, ajust its dt to reach its domain limit and
            // adjust all other nodes' dt to the smallest dt.
            if (validTimeStep)   {
                dt=1e300;
                for(size_t i=0;i<Node.size();i++){
                    //the mecanical computation must be before 'PostNuclGrowthDiss'
                    Node[i].mechanicalComputation(false,false,0,TempMatrix[i], TempElements[i], TempPrecipitates[i],CurrentTemperature[i]);
                    tempdt=Node[i].PostNuclGrowthDiss(TempMatrix[i], TempElements[i], TempPrecipitates[i],CurrentTemperature[i],timestep,reduced);
                    if(tempdt<dt) {dt=tempdt;}
                }
                timestep++;
                reduced=false;
                if (notVerboseBool==false) {cout << "Simulation time " << timeCurrent << endl;}
                
            }
            else  {
                dt*=reduceDT;
                reduced=true;
                if (notVerboseBool==false)
                    cout << "Time step rejected by node " << failingNodeIndex << " because " << reasonTimeStepRejected << endl;
            }
            for(size_t i=0;i<Node.size();i++) Node[i].dt=dt;
        }
        // Save final distributions
        for(size_t i=0;i<Node.size();i++)
            Node[i].output.TimeStepOutput(Node[i].mechanical, Node[i].matrix,Node[i].Elements, Node[i].Precipitates, Node[i].temperature,Node[i].currentTimeIndex, Node[i].currentTime, CurrentTemperature[i], Node[i].dt, timestep, Node[i].nodeIndex, true);
        if (notVerboseBool==false && numberOfConnections!=0) {
            cout << "Time steps: " << timestep << endl;
            cout << "Rejected time steps: " << invalidTimesteps << endl;
        }
    }
    // ### mechanical post treatment ###
    if (hardeningComputation && mechanicalHardeningCoupling==false && mechanicalSemiHardeningCoupling==false) {
        for(size_t i=0;i<Node.size();i++) {Node[i].WriteMechanicalHardeningResults(false,true);}
    }
}
//#######################################################################################
bool NodePreciso::validFluxManagement(vector<Preciso> &_Node,vector<vector<Element> > &_TempElements,vector<Matrix> &_TempMatrix,vector<vector<Precipitate> > &_TempPrecipitates,vector<double > &_CurrentTemperature, string &_reasonTimeStepRejected)
{
    if (onlyMechanicComputation) {return true;}
    else {
        //if the solidSolContent or CFL stability condition are not good we will turn on false
        bool validation=true;
        //------------------------------------------------------------------------------------------
        // calculation of number of atomes and total number
        //------------------------------------------------------------------------------------------
        //initialization
        double inflateCoeff=0.;
        vector<double> newTotalNbOfAtoms;
        vector< vector<double> > newNbOfAtoms;
        size_t nbOfElement=_Node[0].Elements.size();
        string nameToCompare;
        //Boolean to check if diffusion effectively occured, if not the contents are not updated at the end of the routine and the mass balance is not computed.
        bool diffusionOccured=false;
        //computation of nbOfAtoms_i and totalNumberAtoms
        
        double meanVat=0.,volume=0.,X=0.,atomsI=0.;
        for (size_t i=0;i<_Node.size();i++){
            meanVat=meanVatNodeI(_Node,i);
            volume=_Node[i].volume;
            /// \warning  : dans le meanVat on a pas pris en compte le fait que des éléments intersticiles ont pu partir !!! car on a pas fait ça pour VatMatrice
            newTotalNbOfAtoms.push_back(volume/meanVat);
            //newTotalNbOfAtoms.push_back(volume/meanVat);
            newNbOfAtoms.push_back(vector<double>(0));
            atomsI=0.;
            for (size_t j=0;j<_TempElements[i].size()-1;j++){
                X=_TempElements[i][j].GetContentAtFrac();
                newNbOfAtoms[i].push_back(X/meanVat*volume);
                atomsI=atomsI+X/meanVat*volume;
            }
            newNbOfAtoms[i].push_back(newTotalNbOfAtoms[i]-atomsI);
        }
        
        //------------------------------------------------------------------------------------------
        // diffusion treatment
        //-------------------------------------------------------------------------------------------
        // initializations before diffusion
        /// \warning The matrix have the last index in the element array
        size_t indexOfMatrixElement=nbOfElement-1;
        double X0=0,X1=0,C0=0,C1=0,xPos0=0,xPos1=0,yPos0=0,yPos1=0,zPos0=0,zPos1=0,V0=0,V1=0;
        double distanceNodes=0,T0=0,T1=0,D0=0,D1=0,D=0,diffusedAtoms=0,atomicVolumSS0=0.,atomicVolumSS1=0.;
        int node0=0,node1=0;
        //------ loop on all connections to calculate number of diffused atomes ------
        for (size_t n=0;n<numberOfConnections;n++) {
            //index node 0 and node 1 of connection "i"
            node0=Connection[n][0];
            node1=Connection[n][1];
            atomicVolumSS0=_TempMatrix[node0].GetAtomicVolumeSS();
            atomicVolumSS1=_TempMatrix[node1].GetAtomicVolumeSS();
            //------ loop on all elements to calculate number of their diffused atomes ------
            /// \warning we considere diffusion for matrix index but its diffusion is always null because coeff diffusion =0 (because can be useful for mutimatrix)
            for (size_t i=0;i<nbOfElement;i++) {
                //we convert solidSolContent to concentration (atoms/m3)
                X0=_TempElements[node0][i].GetSolidSolContent();
                X1=_TempElements[node1][i].GetSolidSolContent();
                C0=X0/atomicVolumSS0;
                C1=X1/atomicVolumSS1;
                //we compute de distance between node 0 and node 1 for connection "i"
                xPos0=Node[node0].xPos; xPos1=Node[node1].xPos;
                yPos0=Node[node0].yPos; yPos1=Node[node1].yPos;
                zPos0=Node[node0].zPos; zPos1=Node[node1].zPos;
                distanceNodes=sqrt((xPos1-xPos0)*(xPos1-xPos0)+(yPos1-yPos0)*(yPos1-yPos0)+(zPos1-zPos0)*(zPos1-zPos0));
                //we compute the diffusion coefficient of each node to choice the lower because it monitor diffusion
                T0=_CurrentTemperature[node0];
                T1=_CurrentTemperature[node1];
                /// \warning  : if we inflate diffusion coeff for "phomenologic precipitation approch" we don't have to inflate diffusion coeff for flux because flux is not phenomenologic
                inflateCoeff=_TempElements[node0][i].GetInflateDiffusionCoeff();
                D0=_TempElements[node0][i].GetDiffusionCoefficient(T0)*(1/inflateCoeff);
                D1=_TempElements[node1][i].GetDiffusionCoefficient(T1)*(1/inflateCoeff);
                D=MIN(D0,D1);
                
                //compute Nb of atomes that goes from node 0 to 1 & update nbOfAtoms"j" of each nodes
                diffusedAtoms=-D*((C1-C0)/distanceNodes)*Surface[n]*dt;
                V1=_Node[node1].volume;
                V0=_Node[node0].volume;
                if (fabs(diffusedAtoms)>NUMERICLIMITDOUBLE)                {
                    //If diffusion occurs, check that concentrations
                    if (((C0>C1)&&(C0-diffusedAtoms/V0<C1+diffusedAtoms/V1))
                        ||((C0<C1)&&(C0-diffusedAtoms/V0>C1+diffusedAtoms/V1))){
                    //if (C0-diffusedAtoms/V0<C1+diffusedAtoms/V1){
                        diffusedAtoms=(C0-C1)/(1.0/V1+1.0/V0);
                        if ((dt>nodeSmallestTimeStep)
                            &&((fabs(diffusedAtoms)/newNbOfAtoms[node0][i]>0.01)
                               ||(fabs(diffusedAtoms)/newNbOfAtoms[node1][i]>0.01))) {
                            validation=false;
                            break;}
                        else {
                            error.Warning("For flux : Time step too large but forcing it anyway.");
                        }
                    }
                }
                
                newNbOfAtoms[node0][i]-=diffusedAtoms;
                newNbOfAtoms[node1][i]+=diffusedAtoms;
                
                if((newNbOfAtoms[node0][i]<0)||(newNbOfAtoms[node1][i]<0)){
                    diffusedAtoms=diffusedAtoms;
                }
                
                //------ compensation or note by one of the matrix ------
                //for interstitial elements=> diffusion without compensation of matrix. (So Total Nb of atoms is not conserved)

                nameToCompare=_TempElements[node0][i].GetName();
                if (nameToCompare=="C" || nameToCompare=="N" || nameToCompare=="H"){
                    newTotalNbOfAtoms[node0]-=diffusedAtoms;
                    newTotalNbOfAtoms[node1]+=diffusedAtoms;                }
                else {
                    newNbOfAtoms[node0][indexOfMatrixElement]+=diffusedAtoms;
                    newNbOfAtoms[node1][indexOfMatrixElement]-=diffusedAtoms;
                }
                
                if (fabs(diffusedAtoms)>NUMERICLIMITDOUBLE) {diffusionOccured=true;}
                
            }
        }
        //------------------------------------------------------------------------------------------
        //now all new number of atoms are know, so we can update the "contentAtFrac"
        //------------------------------------------------------------------------------------------
        if (diffusionOccured)        {
            //The content in at frac and mass balance are made only if diffusion occured since it necessarly introduce a numerical error
            double contentAtFrac=0.;
            for (size_t n=0;n<_Node.size();n++){
                if(!validation) {
                    break;}
                for (size_t i=0;i<_TempElements[n].size();i++){
                    contentAtFrac=newNbOfAtoms[n][i]/newTotalNbOfAtoms[n];
                    if (contentAtFrac<0||contentAtFrac>1) {
                        validation=false;
                        _reasonTimeStepRejected="contentAtFrac <0 or >1 after diffusion between nodes occured";
                        break;
                    }
                    _TempElements[n][i].SetContentAtFrac(contentAtFrac);
                }
            }
            //------------------------------------------------------------------------------------------
            // Mass Balance : we MUST run massBalance for each nodes to have a correct future nucleation
            //------------------------------------------------------------------------------------------
            for (size_t n=0;n<_Node.size();n++){
                if(!validation) {
                    break;}
                for (size_t i=0;i<_TempElements[n].size();i++){
                    _TempElements[n][i].MassBalance(_TempMatrix[n],_TempPrecipitates[n],_TempElements[n]);
                }
                if (_Node[n].noVatSS==false) {_TempMatrix[n].SetAtomicVolumeSS(_TempElements[n],false);}
            }
        }
        
        return validation;
    }
}

double NodePreciso::meanVatNodeI(vector<Preciso> &_Node,size_t const _nodeIndex)
{
    /// \warning  : dans le meanVat on a pas pris en compte le fait que des éléments intersticiles ont pu partir !!! car on a pas fait ça pour VatMatrice
    //meanVat is the mean atomic vomule of node "i" by taking into account the precipitates
    double sumFvPrecipitatesNodeI=0.,sumFvByVatPrecipitatesNodeI=0., fvJ=0.;
    size_t nbOfPrecipitatesNodeI=_Node[_nodeIndex].Precipitates.size();
    for (size_t i=0;i<nbOfPrecipitatesNodeI;i++)    {
        fvJ=_Node[_nodeIndex].Precipitates[i].VolumeFraction();
        sumFvPrecipitatesNodeI=sumFvPrecipitatesNodeI+fvJ;
        sumFvByVatPrecipitatesNodeI=sumFvByVatPrecipitatesNodeI+(fvJ/_Node[_nodeIndex].Precipitates[i].GetAtomicVolume());
    }
    double VatSS=_Node[_nodeIndex].matrix.GetAtomicVolumeSS();
    return 1.0/((1-sumFvPrecipitatesNodeI)/VatSS+sumFvByVatPrecipitatesNodeI);
}
