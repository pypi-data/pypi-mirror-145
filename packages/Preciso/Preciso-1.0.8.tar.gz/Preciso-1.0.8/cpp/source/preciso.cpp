/// \file preciso.cpp
/// \brief Methods of the class Preciso
#include <iostream>
#include <fstream>  //For file read/write options
#include <vector>
#include <sstream>
#include <stdio.h>
#include <stdlib.h> //for atof, atoi, strtod
#include <math.h>
#include "string.h"
#include "preciso.h"
#include "input.h"
#include "error.h"
#include "element.h"
#include "precipitate.h"
#include "temperature.h"
#include "matrix.h"
#include "constants.h"
#include "output.h"

using namespace std;

Preciso::Preciso()
{
    //The following default values should not be modified without discussion with all developpers.
    //------------mechanical-------------
    leaveMechaDomain=false;
    currentMechanicTimeIndex=1;
    uncoupledMecaResults.clear();
    //---------precipitation---------------
    leaveDomain=false;
    Precipitates.clear(); Elements.clear();       currentTime=0;
    Criterion.clear();    currentTimeIndex=1;
    volume=1;             nodeIndex=0;            xPos=yPos=zPos=0;
    //---------generalities---------------
    firstTime=0.;

    //----------------- Options default value --------------------------
    solvePrecipitation=true;       increaseDT=1.1;             initialDT=1e-6;
    dt=0.;
    maxCriterionIncrease=0.01;     timeStepManagement=3;       smallestTimeStep=1e-9;
    notVerboseBool=false;
    mechanicalModelActivated=false;
    noVatSS=false;
    //The following default values should not be modified without discussion with all developpers.
    onlyMechanicComputation=false;
    hardeningComputation=false;
    mechanicalHardeningCoupling=false;
    mechanicalSemiHardeningCoupling=false;
    //The following default values should not be modified without discussion with all developpers.
    simplifiedMassBalance=true;
    //The following default values should not be modified without discussion with all developpers.
    criterion=1; //1->Rstar,2->solContent
}

Preciso::~Preciso() {}

void Preciso::Initialize(string const& _filename)  //Initialisation of the object
{
    //conserve this order!
    InitializeMatrixAndElementsAndGeneral(_filename);
    InitializePrecipitates(_filename);
    InitializeTemperature(_filename);
    InitializeDistribution(_filename);
    InitializeOutputsData(_filename);
    InitializeOptions(_filename);
    InitializeThermodynamicData();

    //after preciso initialization we have mechanical part
    InitializeMechanical(_filename);
}

void Preciso::InitializeMatrixAndElementsAndGeneral(string const& _filename)
{
    char* endCharact=NULL;
    //Keyword starting the lines in the data file
    string keyword;
    //Matrix of lines containing the keyword. /!\ lines is erased at the beginning of each call of LinesStartingWithKeyword
    vector<vector<string> > lines;

    //--------------------VERBOSE MODE--------------------
    //Read if the optionnal booleen "notVerboseBool" exist (default false)
    keyword="notVerbose";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("notVerbose defined twice.");}
    else if (lines.size()==1) {notVerboseBool=true;}
    else {notVerboseBool=false;}
    lines.clear();

    //--------------------CRITERION CHOICE--------------------
    keyword="criterion";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("criterion defined twice.");}
    if (lines.size()==1) {
        if (lines[0].size()!=2) {error.Fatal("criterion must have 1 argument.");}
        if (lines[0][1]=="Rstar" || lines[0][1]=="rstar" || lines[0][1]=="rStar") {
            criterion=1;
            cout << "criterion is:" << lines[0][1] << endl;        }
        else if (lines[0][1]=="solContent" || lines[0][1]=="solcontent") {
            criterion=2;
            cout << "criterion is:" << lines[0][1] << endl;}
        else {error.Fatal("This criterion is not active");}
    }
    lines.clear();

    //--------------------MATRIX DATA--------------------
    keyword="matrix";
    input.LinesStartingWithKeyword(_filename,keyword,lines,false);

    if (lines.size()>1) {error.Fatal("More than one matrix information given");}

    //Checking the number of input arguments for the matrix
    ostringstream convertedString;
    convertedString << lines[0].size()-1;
    if (lines[0].size()-1!=4) {error.Fatal("matrix command needs 4 arguments and " + convertedString.str() + " were given.");}

    //Adding the matrix information to the instance matrix
    matrix.DefineMatrix(lines[0]);

    //Read the optional choice of VatSS management
    keyword="noVatSS";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("noVatSS defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1>1) {error.Warning("No arguments necessary for noVatSS, extra arguments are neglected.");}
        matrix.setVatSSbool(false);
        if (notVerboseBool==false) {cout << "No computation of VatSS the choice is always VatSS=VatM" << endl ;}
    }
    lines.clear();

    if (notVerboseBool==false) {cout << "Matrix: OK" << endl;}
    //--------------------ELEMENT DATA-------------------------
    keyword="element";
    input.LinesStartingWithKeyword(_filename,keyword,lines,false);
    if (notVerboseBool==false) {cout << lines.size() << " elements defined in the data file." << endl;}

    for (size_t i=0;i<lines.size();i++)    {
        //Checking the number of input arguments for the element
        ostringstream convertedString1, convertedString2;
        convertedString1 << lines[i].size()-1;
        convertedString2 << lines[i][1];
        if (lines[i].size()-1!=5) error.Fatal("element command needs 5 arguments and " + convertedString1.str() + " were given for element " + convertedString2.str());

        //Adding the element information to the vector element
        Element localElement(lines[i],i);
        Elements.push_back(localElement);
        if (notVerboseBool==false) {cout << "Element " << Elements[i].GetName() << ": OK" << endl;}
    }

    //Adding the matrix to the list of elements
    vector<string> virtualLineMatrixAsElement;
    virtualLineMatrixAsElement.clear();
    virtualLineMatrixAsElement.push_back("element");
    virtualLineMatrixAsElement.push_back(matrix.GetName());
    double contentWtPctMatrix=100.0;
    for (size_t i=0;i<Elements.size();i++) contentWtPctMatrix-=Elements[i].GetContentWtPc();
    ostringstream convertedString2;
    convertedString2 << contentWtPctMatrix;
    virtualLineMatrixAsElement.push_back(convertedString2.str());
    convertedString2.str("");
    convertedString2 << matrix.GetMolarMass();
    virtualLineMatrixAsElement.push_back(convertedString2.str());
    virtualLineMatrixAsElement.push_back("0");
    virtualLineMatrixAsElement.push_back("0");
    Element matrixAsElement(virtualLineMatrixAsElement,Elements.size());
    Elements.push_back(matrixAsElement);
    if (notVerboseBool==false) {cout << "Matrix added to list of Elements" << endl;}

    //Check that no element has been defined twice
    for (size_t i=0;i<Elements.size()-1;i++)    {
        string testedElement1=Elements[i].GetName();
        for (size_t j=i+1;j<Elements.size();j++)        {
            string testedElement2=Elements[j].GetName();
            if (testedElement1==testedElement2) error.Fatal("element " + testedElement1 + " defined twice.");
        }
    }

    //Read the optional choice of mass balance type
    keyword="improvedMassBalance";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("improvedMassBalance defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1>1) {error.Warning("No arguements necessary for improvedMassBalance, extra arguments are neglected.");}
        for (size_t i=0;i<Elements.size();i++) {Elements[i].SetImprovedMassBalance();}
        if (notVerboseBool==false) {cout << "Use of improved mass balance." << endl ;}
        simplifiedMassBalance=false;
    }
    lines.clear();

    //Read the optional value of inflateDiffusionCoeff (default value 1)
    keyword="inflateDiffusionCoeff";
    bool elementNotFound;
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>Elements.size()) {error.Fatal("nb of inflateDiffusionCoeff cannot be greather than nbOfElement.");}
    for (size_t i=0;i<lines.size();i++)    {
        if (lines[i].size()>0) {
            elementNotFound=true;
            ostringstream convertedString2;
            convertedString2 << lines[i][1];
            if (lines[i].size()-1>2) {error.Warning("Too many arguments defined for inflateDiffusionCoeff (element "+convertedString2.str()+" only the 2 first are taken into account.");}
            for (size_t j=0;j<Elements.size();j++) {
                if(lines[i][1]==Elements[j].GetName()) {
                    elementNotFound=false;
                    Elements[j].SetInflateDiffusionCoeff(strtod(lines[i][2].c_str(),&endCharact));
                }
            }
            if (elementNotFound) {error.Fatal("inflateDiffusionCoeff: this element "+convertedString2.str()+" was not found");}
            if (notVerboseBool==false) {cout << "inflateDiffusionCoeff changed to: " << lines[i][2] <<  " for element " << lines[i][1] << endl ;}
        }
    }
    lines.clear();
}

void Preciso::InitializePrecipitates(string const& _filename)
{
    char* endCharact = NULL;
    //Keyword starting the lines in the data file
    string keyword;
    //Matrix of lines containing the keyword. /!\ lines is erased at the beginning of each call of LinesStartingWithKeyword
    vector<vector<string> > lines;

    //See if the precipitation is calculated for this preciso
    keyword="noPrecipitation";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    ostringstream convertedString1;
    convertedString1<<nodeIndex;
    if (lines.size()>0) {
        solvePrecipitation=false;
        error.Warning("'noPrecitation' by default in input file");
    }
    lines.clear();

    if (solvePrecipitation) {
        //--------------------PRECIPITATES DATA---------------------
        keyword="precipitate";
        input.LinesStartingWithKeyword(_filename,keyword,lines,false);
        if (notVerboseBool==false) {cout << lines.size() << " precipitate(s) defined in the data file." << endl;}

        for (size_t i=0;i<lines.size();i++)    {
            //Checking the number of input arguments for the precipitate
            ostringstream convertedString1, convertedString2;
            convertedString1 << lines[i].size()-1;
            convertedString2 << lines[i][1];
            if (lines[i].size()<10) {error.Fatal("Insufficient number of arguments for precipitate " + convertedString2.str());}

            //Adding the element information to the vector element
            Precipitate localPrecipitate(Elements);
            localPrecipitate.DefinePrecipitate(lines[i]);
            Precipitates.push_back(localPrecipitate);
            if (notVerboseBool==false) {cout << "Precipitate " << Precipitates[i].GetName() << ": OK" << endl;}
        }

        //Check that no precipitate has been defined twice
        for (size_t i=0;i<Precipitates.size()-1;i++)    {
            string testedPrecipitate1=Precipitates[i].GetName();
            for (size_t j=i+1;j<Precipitates.size();j++)        {
                string testedPrecipitate2=Precipitates[j].GetName();
                if (testedPrecipitate1==testedPrecipitate2) {error.Fatal("precipitate " + Precipitates[i].GetName() + " defined twice.");}
            }
        }
    }

    //Read the optional value of the Brent Dichotomy algorithm tolerance (default value 1e-9)
    keyword="tol_Brent_Dicho";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("BrentDichoTolerance defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for BrentDichoTolerance.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for BrentDichoTolerance, only the first is taken into account.");}
        for (size_t i=0;i<Precipitates.size();i++) {Precipitates[i].SetBrentDichoAlgorithmTolerance(strtod(lines[0][1].c_str(),&endCharact));}
        if (notVerboseBool==false) {cout << "Brent or dichotomy tolerance changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();

    //Read the optional value of the Newton raphson algorithm tolerance (default value 100)
    keyword="tol_divideResidu_NR";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("NRtolerance defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for NRtolerance.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for NRtolerance, only the first is taken into account.");}
        for (size_t i=0;i<Precipitates.size();i++) {Precipitates[i].SetNewtonRaphsonAlgorithmTolerance(strtod(lines[0][1].c_str(),&endCharact));}
        if (notVerboseBool==false) {cout << "NewtonRaphson algorithm tolerance changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();

    //Read the optional value of the Newton raphson algorithm maximum count (default value 1000)
    keyword="NR_maximumCount";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("NR_maximumCount defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for NR_maximumCount.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for NR_maximumCount, only the first is taken into account.");}
        for (size_t i=0;i<Precipitates.size();i++) {Precipitates[i].SetNRmaximumCount(strtod(lines[0][1].c_str(),&endCharact));}
        if (notVerboseBool==false) {cout << "NewtonRaphson maximumCount changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();

    //Read the optional value "nonLinearAlgorithm" to choice algo (default value NR)
    keyword="nonLinearAlgorithm";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("nonLinearAlgorithm defined twice.");}
    if (lines.size()>0) {
        double choiceAlgo=0;
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for nonLinearAlgorithm.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for nonLinearAlgorithm, only the first is taken into account.");}
        if (lines[0][1]!="NR" && lines[0][1]!="CNR" && lines[0][1]!="dicho" && lines[0][1]!="brent") {
            error.Fatal("This choice for nonLinearAlgorithm is not recognized");        }
        else {
            if (lines[0][1]=="NR") {choiceAlgo=1;}
            else if (lines[0][1]=="CNR") {choiceAlgo=2;}
            else if (lines[0][1]=="brent") {choiceAlgo=3;}
            else if (lines[0][1]=="dicho") {choiceAlgo=4;}
            else {error.Fatal("Unrecognized error in reading of 'nonLinearAlgorithm'");}
        }
        for (size_t i=0;i<Precipitates.size();i++) {Precipitates[i].SetNonLinearAlgorithm(choiceAlgo);}
        if (notVerboseBool==false) {cout << "nonLinearAlgorithm changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();

    //Read the optional value of diffusionCoefficientRatio (default value 1.0e4)
    keyword="diffusionCoefficientRatio";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) error.Fatal("diffusionCoefficientRatio defined twice.");
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for diffusionCoefficientRatio.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for diffusionCoefficientRatio, only the first is taken into account.");}
        for (size_t i=0;i<Precipitates.size();i++) {Precipitates[i].SetDiffusionCoefficientRatio(strtod(lines[0][1].c_str(),&endCharact));}
        if (notVerboseBool==false) {cout << "diffusionCoefficientRatio changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();

    //Read the optionnal booster for growth
    keyword="boostPrecipitateDiffusion";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0) {
      if (lines.size()!=Precipitates.size()) {error.Fatal("nb of 'boostPrecipitateDiffusion' must be equal to the nb of precipitates");}
      else {
        for (size_t i=0;i<Precipitates.size();i++) {
          string testedPrecipitate1=Precipitates[i].GetName();
          for (size_t j=0;j<lines.size();j++) {
            if (lines[j].size()-1<2) {error.Fatal("Too low nb of arguments defined for boostPrecipitateDiffusion (2 required).");}
            if (lines[j].size()-1>2) {error.Fatal("Too many arguments defined for boostPrecipitateDiffusion (2 required).");}
            string testedPrecipitate2=lines[j][1];
              if (testedPrecipitate1==testedPrecipitate2) {
                Precipitates[i].SetBoostPrecipitateDiffusion(strtod(lines[j][2].c_str(),&endCharact));
              }
                if (notVerboseBool==false) {cout << "boostPrecipitateDiffusion changed to: " << lines[j][2] << " for " << lines[j][1] << endl ;}
              }
          }
        }
      }
    lines.clear();

    //Read the optional value of targetClassNumber (default value 250)
    keyword="targetClassNumber";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("targetClassNumber defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for targetClassNumber.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for targetClassNumber, only the first is taken into account.");}
        for (size_t i=0;i<Precipitates.size();i++) {Precipitates[i].SetTargetClassNumber(strtoul(lines[0][1].c_str(),NULL,0));}
        if (notVerboseBool==false) {cout << "targetClassNumber changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();

    //Read the optional value of limitOfpreciInClassForDissolution (default value 0.)
    keyword="limitOfpreciInClassForDissolution";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("limitOfpreciInClassForDissolution defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1<1) error.Fatal("Too low nb of arguments defined for limitOfpreciInClassForDissolution.");
        if (lines[0].size()-1>1) error.Warning("Too many arguments defined for limitOfpreciInClassForDissolution, only the first is taken into account.");
        for (size_t i=0;i<Precipitates.size();i++) {Precipitates[i].SetLimitOfpreciInClassForDissolution(strtod(lines[0][1].c_str(),NULL));}
        if (notVerboseBool==false) {cout << "limitOfpreciInClassForDissolution changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();

    //Read the optional value of changeNumberInClass (default value 0.01)
    keyword="changeNumberInClass";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) error.Fatal("changeNumberInClass defined twice.");
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for changeNumberInClass.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for changeNumberInClass, only the first is taken into account.");}
        if ((strtod(lines[0][1].c_str(),&endCharact)>1)||(strtod(lines[0][1].c_str(),&endCharact)<=0)) error.Warning("Incorrect value for changeNumberInClass (must be ]0;1])");
        for (size_t i=0;i<Precipitates.size();i++) {Precipitates[i].SetChangeNumberInClass(strtod(lines[0][1].c_str(),&endCharact));}
        if (notVerboseBool==false) {cout << "changeNumberInClass changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();

    //Read the optional value of unstationnaryNucleation (default value false)
    keyword="unstationnaryNucleation";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("unstationnaryNucleation defined twice.");}
    if (lines.size()>0) {
        for (size_t i=0;i<Precipitates.size();i++) {
            Precipitates[i].SetUnstationnaryNucleation(true);
        }
        error.Warning("unstationnaryNucleation changed to: true");
    }
    lines.clear();

    //Read the optional value of classManagementType (default value "lin")
    keyword="classManagementType";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("classManagementType defined twice.");}
    if (lines.size()>0) {
        double classManagementIndex=0.;
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for classManagementType.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for classManagementType, only the first is taken into account.");}
        if ((lines[0][1]!="quad")&&((lines[0][1]!="lin"))&&((lines[0][1]!="distrib"))&&((lines[0][1]!="old"))&&((lines[0][1]!="no"))&&((lines[0][1]!="oldWithLess"))) error.Fatal("Incorrect value for classManagementType (must be quad, lin, distrib, old or no)");
        else {
            //if (lines[0][1]=="quad") {classManagementIndex=5;}
            //else if (lines[0][1]=="lin") {classManagementIndex=3;}
            //else if (lines[0][1]=="distrib") {classManagementIndex=4;}
            //else if (lines[0][1]=="old") {classManagementIndex=2;}
            //else if (lines[0][1]=="no") {classManagementIndex=1;}
            //else if (lines[0][1]=="oldWithLess") {classManagementIndex=6;}
            //else {error.Fatal("Unrecongnized type in 'classManagementType' choice");}
            if (lines[0][1]=="no") {classManagementIndex=1;}
            else if (lines[0][1]=="old") {classManagementIndex=2;}
            else if (lines[0][1]=="lin") {classManagementIndex=3;}
            else if (lines[0][1]=="distrib") {classManagementIndex=4;}
            //else if (lines[0][1]=="quad") {classManagementIndex=5;}   //quad not correctly implemented
            else if (lines[0][1]=="oldWithLess") {classManagementIndex=6;}
            else {error.Fatal("Unrecongnized type in 'classManagementType' choice");}
        }
        for (size_t i=0;i<Precipitates.size();i++) {Precipitates[i].SetClassManagementType(classManagementIndex);}
        if (notVerboseBool==false) {cout << "classManagementType changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();

    //Read the optional value of minDissolutionLimit (default value 1e-10)
    keyword="minDissolutionLimit";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("minDissolutionLimit defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for minDissolutionLimit.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for minDissolutionLimit, only the first is taken into account.");}
        for (size_t i=0;i<Precipitates.size();i++) {Precipitates[i].SetMinDissolutionLimit(strtod(lines[0][1].c_str(),&endCharact));}
        if (notVerboseBool==false) {cout << "minDissolutionLimit changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();

    //Read the optional value of maxDissolutionLimit (default value 2e-10)
    keyword="maxDissolutionLimit";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("maxDissolutionLimit defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for maxDissolutionLimit.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for maxDissolutionLimit, only the first is taken into account.");}
        for (size_t i=0;i<Precipitates.size();i++) {Precipitates[i].SetMaxDissolutionLimit(strtod(lines[0][1].c_str(),&endCharact));}
        if (notVerboseBool==false) {cout << "maxDissolutionLimit changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();
    
}

void Preciso::InitializeTemperature(string const& _filename)
{
    //Keyword starting the lines in the data file
    string keyword;
    //Matrix of lines containing the keyword. /!\ lines is erased at the beginning of each call of LinesStartingWithKeyword
    vector<vector<string> > lines;

    //--------------------TEMPERATURE DATA--------------------
    keyword="temperatureProfile";
    input.LinesStartingWithKeyword(_filename,keyword,lines,false);

    if (lines.size()>1)           {error.Fatal("More than one reference temperature profile given");}
    if ((lines[0].size()-1)%2!=0) {error.Fatal("incorrect number of arguments for temperature profile.");}
    if ((lines[0].size()-1)<4) {error.Fatal("you must have at least 4 arguments for temperature profile.");}

    //Adding the temperature information to the instance temperature
    temperature.DefineTemperature(lines[0]);
    firstTime=temperature.GetInitialTime();

    if (notVerboseBool==false) {cout << "Temperature profile: OK" << endl;}
}

void Preciso::InitializeDistribution(string const& _filename)
{
    string keyword;
    vector<vector<string> > lines;
    //--------------------INITIAL DISTRIBUTION-----------------
    keyword="initialDistrib";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);

    if (lines.size()==0) {error.Warning("no initial distribution by default in inputFile");}
    else    {
        //first verification of inputFile
        if (lines.size()>1)                         {error.Fatal("More than one initial distribution is given");}
        size_t nbOfArguments=lines[0].size()-1;
        if (nbOfArguments%2!=0)                     {error.Fatal("We must have pair number of arguments for initial distribution.");}
        if (nbOfArguments/2.0!=Precipitates.size()) {error.Fatal("Nb of arguments/2 for initialDistrib must be equal to nb of precipitates");}

        LoadInitialDistrib(lines[0]);
        if (notVerboseBool==false) {cout << "Initial distribution: OK" << endl;}
    }
}

void Preciso::LoadInitialDistrib(vector<string> &_lines)
{
    char* endCharact = NULL;
    string dump;
    vector<string> arg;
    //Test names and we define distributions
    bool testName;
    double buffer=0.;
    string nameInitialDistrib;
    size_t nbOfArguments=_lines.size()-1;
    for (size_t j=0;j<Precipitates.size();j++)    {
        //Each precipitates must have its distribution, if yes we save the associated filename
        testName=false; nameInitialDistrib="";
        for (size_t i=1;i<nbOfArguments+1;i=i+2) {
            if (_lines[i]==Precipitates[j].GetName()) {testName=true; nameInitialDistrib=_lines[i+1];}
        }
        if (testName==false) {error.Fatal("Each precipitates must have its distribution.");}

        //we count the nb of filled _lines
        ifstream datafile(nameInitialDistrib.c_str(), ios::in); if (!datafile) error.Fatal("File "+ nameInitialDistrib +" not found");
        size_t nbOf_lines1=0;
        while (!datafile.eof())    {
            getline(datafile,dump); arg.clear(); input.Parse(dump,arg);
            if (arg.size()!=0) {nbOf_lines1=nbOf_lines1+1;}
        }
        datafile.close();

        //With this second reading we save the last Radius & last Number
        datafile.open(nameInitialDistrib.c_str(), ios::in); if (!datafile) error.Fatal("File "+ nameInitialDistrib +" not found");
        size_t nbOf_lines2=0;
        vector<double> initialInputRadius; initialInputRadius.clear();
        vector<double> initialInputNumber; initialInputNumber.clear();
        while (!datafile.eof())    {
            getline(datafile,dump); arg.clear(); input.Parse(dump,arg);
            if (arg.size()!=0) nbOf_lines2=nbOf_lines2+1;
            //NbOfLine1=density NbOfLine1-1=number NbOfLine1-2=number
            if (nbOf_lines2==nbOf_lines1-2)             {
                for (size_t p=1;p<arg.size();p++) {
                    buffer=strtod(arg[p].c_str(),&endCharact);
                    //f!=f false only for NaN (IEEE), isinf(n) return true is "n" is infinite
                    if (isnan(buffer) || isinf(buffer)) {error.Fatal("In initial distrib there is a nan or inf or radius < 0");}
                    //else if(buffer<NUMERICLIMITDOUBLE) {error.Warning("In initial distrib a class with a radius=0 is not taken into account");}
                    else {initialInputRadius.push_back(buffer);}
                }
            }
            if (nbOf_lines2==nbOf_lines1-1) {
                for (size_t p=1;p<arg.size();p++) {
                    buffer=strtod(arg[p].c_str(),&endCharact);
                    //f!=f false only for NaN (IEEE), isinf(n) return true is "n" is infinite
                    if (isnan(buffer) || isinf(buffer)) {error.Fatal("In initial distrib there is a nan or inf or number < 0");}
                    //else if(buffer<NUMERICLIMITDOUBLE) {error.Warning("In initial distrib a class with a number=0 is not taken into account");}
                    else {initialInputNumber.push_back(buffer);}
                }
            }
        }
        if (initialInputRadius.size()!=initialInputNumber.size()) {
            error.Fatal("File "+ nameInitialDistrib +" Number and Radius must have the same size");}
        
        // Check if empty number AND empty radius
        for(size_t i=0;i<initialInputRadius.size();i++)
            if((initialInputNumber[i]==0)&&(initialInputRadius[i]==0)){
                initialInputNumber.erase(initialInputNumber.begin()+i);
                initialInputRadius.erase(initialInputRadius.begin()+i);
        }
        
        datafile.close();

        //Define for each precipitates its initial distribution
        Precipitates[j].DefineInitialDistribution(initialInputRadius,initialInputNumber);
    }
}


void Preciso::InitializeOutputsData(string const& _filename)
{
    char* endCharact = NULL;
    //Keyword starting the lines in the data file
    string keyword;
    //Matrix of lines containing the keyword. /!\ lines is erased at the beginning of each call of LinesStartingWithKeyword
    vector<vector<string> > lines;

    //--------------------OUTPUTS DATA------------------------
    keyword="savethermodynamics";
    input.LinesStartingWithKeyword(_filename,keyword,lines,false);
    if (lines.size()>1) {error.Fatal("More than one savethermodynamics command");}
    //Checking the number of input arguments for savethermodynamics
    if ((lines[0].size()-1)!=2) {error.Fatal("incorrect number of arguments for savethermodynamics.");}
    //Adding the information to the instance output
    output.DefineThermoOutputs(lines[0]);
    if (notVerboseBool==false) {cout << "Saving thermodynamics options: OK" << endl;}

    keyword="savedistribution";
    input.LinesStartingWithKeyword(_filename,keyword,lines,false);
    if (lines.size()>1) {error.Fatal("More than one savedistribution command");}
    if ((lines[0].size()-1)!=2) {error.Fatal("incorrect number of arguments for savedistribution.");}
    output.DefineDistributionOutputs(lines[0]);
    if (notVerboseBool==false) {cout << "Saving distributions options: OK" << endl;}

    keyword="plot_distrib";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0){
        if (lines.size()>1) {error.Fatal("More than one plot_distrib command");}
        if ((lines[0].size()-1)<3) {error.Fatal("incorrect number of arguments for plot_distrib.");}
        output.SetNodeToPlotDistrib(lines[0][1]); //nodeThatWeWantToPlot
        output.DefinePlotDistributionOutputs(lines[0], Precipitates);
        if (notVerboseBool==false) {cout << "Plot distribution options: OK" << endl;}
    }

    keyword="plot_thermo";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0){
        if (lines.size()>1) {error.Fatal("More than one plot_thermo command");}
        if ((lines[0].size()-1)<3) {error.Fatal("incorrect number of arguments for plot_thermo.");}
        output.SetNodeToPlotThermo(lines[0][1]); //nodeThatWeWantToPlot
        output.DefinePlotThermoOutputs(lines[0], Precipitates);
        if (notVerboseBool==false) {cout << "Plot thermodynamics options: OK" << endl;}
    }

    keyword="plot_final";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0){
        if (lines.size()>1) {error.Fatal("More than one plot_final command");}
        if ((lines[0].size()-1)<2) {error.Fatal("incorrect number of arguments for plot_final.");}
        output.SetNodeToPlotFinal(lines[0][1]); //nodeThatWeWantToPlot
        output.DefinePlotFinalOutputs(lines[0], Precipitates);
        if (notVerboseBool==false) {cout << "Plot final output options: OK" << endl;}
    }

    //Read the optional value of outputPrecision (default value 1e-15 because is the precision is low wa can have "inf" density for initial distributions)
    keyword="outputPrecision";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("outputPrecision defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for outputPrecision.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for outputPrecision, only the first is taken into account.");}
        output.SetOutputPrecision(strtod(lines[0][1].c_str(),&endCharact));
        if (notVerboseBool==false) {cout << "outputPrecision changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();


    //if we choose 'heavyOuputs' we write the content in wt% and other auxiliary data in results
    keyword="heavyOuputs";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("'heavyOuputs' defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()!=1) {error.Fatal("heavyOuputs don't need arguments");}
        output.SetHeavyOuputs(true);
        if (notVerboseBool==false) {cout << "heavyOuputs changed to 'true'" << endl ;}
    }
    lines.clear();

}

void Preciso::InitializeOptions(string const& _filename)
{
    char* endCharact = NULL;
    //Keyword starting the lines in the data file
    string keyword;
    //Matrix of lines containing the keyword. /!\ lines is erased at the beginning of each call of LinesStartingWithKeyword
    vector<vector<string> > lines;

    //Read the optional value of increaseDT (default value 1.1)
    keyword="increaseDT";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("increaseDT defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for increaseDT.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for increaseDT, only the first is taken into account.");}
        if (strtod(lines[0][1].c_str(),&endCharact)<1.0) {error.Fatal("Incorrect value for increaseDT (must be >=1)");}
        increaseDT=strtod(lines[0][1].c_str(),&endCharact);
        if (notVerboseBool==false) {cout << "increaseDT changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();

    //Read the optional value of initialDT (default value 1e-6)
    keyword="initialDT";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("initialDT defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for initialDT.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for initialDT, only the first is taken into account.");}
        initialDT=strtod(lines[0][1].c_str(),&endCharact);
        if (notVerboseBool==false) {cout << "initialDT changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();

    //Read the optional value of maxCriterionIncrease (default value 0.01)
    keyword="maxCriterionIncrease";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("maxCriterionIncrease defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for maxCriterionIncrease.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for maxCriterionIncrease, only the first is taken into account.");}
        maxCriterionIncrease=strtod(lines[0][1].c_str(),&endCharact);
        if (notVerboseBool==false) {cout << "maxCriterionIncrease changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();

    //Read the optional value of timeStepManagement (default value 3)
    keyword="timeStepManagement";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) {error.Fatal("timeStepManagement defined twice.");}
    if (lines.size()>0) {
        if (lines[0].size()-1<1) {error.Fatal("Too low nb of arguments defined for timeStepManagement.");}
        if (lines[0].size()-1>1) {error.Warning("Too many arguments defined for timeStepManagement, only the first is taken into account.");}
        if ((strtod(lines[0][1].c_str(),&endCharact)!=1)&&((strtod(lines[0][1].c_str(),&endCharact)!=3))) {error.Fatal("Incorrect value for timeStepManagement (must be 1 or 3)");}
        timeStepManagement=atoi(lines[0][1].c_str());
        if (notVerboseBool==false) {cout << "timeStepManagement changed to: " << lines[0][1] << endl ;}
    }
    lines.clear();
}

void Preciso::InitializeThermodynamicData()
{
    for (size_t i=0;i<Elements.size();i++)    {
        //on fait premiere mise a jour pour que le solidSolContent soit mis à jour pour la ligne suivante qui a besoin de ceci pour VatSS
        Elements[i].Initialize(Elements, matrix, Precipitates,true);
    }
    //le solidSolContent est à jour donc on peut calculer VatSS et ensuite faire "vrai massBalance" i.e. qui prendre en compte VatSS
    //see document "massBalanceEtEquilibreFluxFINAL" for VatSS informations
    InitializeAtomicVolumeSS(matrix,Elements,true);
    // First mass balance, calculates the initial atomic fractions of each element
    for (size_t i=0;i<Elements.size();i++)    {
        //set mass balance is useful to check the initial distribution
        Elements[i].SetFirstMassBalance(true);
        Elements[i].Initialize(Elements, matrix, Precipitates,false);
        Elements[i].SetFirstMassBalance(false);
    }
    // Initialize the time, time step and rStar
    InitializeTime(temperature, Elements, Precipitates);
    InitializeAtomicVolumeSS(matrix,Elements,false);
}

void Preciso::InitializeMechanical(string const& _filename)
{
    /// \warning here all is optionnal: first aim of preciso isnot mechanical part ('if (lines.size()>0)')
    //Keyword starting the lines in the data file
    string keyword;
    //Matrix of lines containing the keyword. /!\ lines is erased at the beginning of each call of LinesStartingWithKeyword
    vector<vector<string> > lines;
    bool hardeningLoaded=false;

    //------------modelChoice (must be at the beginning)---------------
    keyword="mechanicModel";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0)    {
        if (lines.size()==1) {
            if (lines[0].size()>=2) {
                if (lines[0].size()>2) {
                    error.Warning("'mechanicModel' needs only one argument, extra arguments are neglected.");
                }
                mechanical.SetModel(atoi(lines[0][1].c_str()));
                mechanical.SetVerboseMode(notVerboseBool);
                mechanicalModelActivated=true;
            }
        }
        else {error.Fatal("More than one 'mechanicModel' information given");}
    }

    //-----------hardeningChoice (must be at the beginning)------------
    keyword="hardeningModel";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0)    {
        hardeningLoaded=true;
        if (lines.size()==1) {
            if (mechanicalModelActivated==false){error.Fatal("If you have 'hardeningModel' you must have 'mechanicModel'");}

            if (lines[0].size()>=2) {
                if (lines[0].size()>2) {error.Warning("'hardeningChoice' needs only one arguments, extra arguments are neglected.");}
                mechanical.SetHardeningModel(atoi(lines[0][1].c_str()));
                mechanical.SetActivedHardening(true);
                hardeningComputation=true;
            }
        }
        else {error.Fatal("More than one 'hardeningChoice' information given");}
    }

    //-----------parameters for the hardening model------------
    keyword="parametersForHardening";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0)    {
        if (hardeningComputation!=true) {error.Fatal("If the 'hardeningModel' is present you must have parameters of model 'parametersForHardening'");}
        if (lines.size()==1) {
            if (lines[0].size()>1) {mechanical.DefineCoefficientsForHardeningModel(lines[0]);}
            else {error.Fatal("Nb of arguments for 'parametersForHardening' must be bigger than 1");}
        }
        else {error.Fatal("More than one 'parametersForHardening' information given");}
    }

    //------SolidSolution constants---------
    keyword="SSconstant";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0)    {
        mechanical.DefineSScontribution(lines,Elements);
    }
    //------grainSize constants----------
    keyword="grainSize";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0)    {
        if (lines.size()>1) {error.Fatal("You can have only 1keyword 'grainSize' in input data");}
        if (lines[0].size()-1!=4) {error.Fatal("'grainSize' must have 4 arguments.");}
        //1st=grainSize in meters
        //2nd=initial nb of dislocation in grains
        //3nd=number of dislocation that sature grain
        else {mechanical.DefineGrainSize(lines[0]);}
    }
    //------young modulus----------
    keyword="young";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0) {
        if (lines.size()==1)    {
            if ((lines[0].size()-1)%2!=0) {error.Fatal("You must have for each temperature a young modulus (pair arguments)");}
            mechanical.DefineYoungModulus(lines[0]);
        }
        else {error.Fatal("You have one matrix so you must have only one Young modulus");}
    }
    //------poisson coefficient----------
    keyword="poisson";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0) {
        if (lines.size()==1)    {
            if ((lines[0].size()-1)%2!=0) {error.Fatal("You must have for each temperature a Poisson coeff (pair arguments)");}
            mechanical.DefinePoissonCoeff(lines[0]);
        }
        else {error.Fatal("You have one matrix so you must have only one Poisson coefficient");}
    }
    //------dislocations constants----------
    keyword="dislocations";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0)    {
        if (lines.size()>1) {error.Fatal("You can have only 1keyword 'dislocations' in input data");}
        if (lines[0].size()-1!=3) {error.Fatal("dislocations must have 3 arguments.");}
        else {mechanical.DefineDislocationsConstants(lines[0]);}
    }
    //------cristallographic constants----------
    keyword="cristalloConstant";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0)    {
        if (lines.size()>1) {error.Fatal("You can have only 1keyword 'cristalloConstant' in input data");}
        if (lines[0].size()-1<4) {error.Fatal("'cristalloConstant' must have, at least 4 arguments.");}
        //1st=purYieldStress(lattice friction) 2nd=taylorsFactor 3rd=burgersNorm 4th=cristallographicStructure
        else {mechanical.DefineCristalloConstant(lines[0]);}
    }
    //! Precipitates must be loaded after dislocation constant
    //------Precipitates constants----------
    keyword="precipitateConstants";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0)    {
        mechanical.DefinePrecipitateConstants(lines,Precipitates);
    }
    //------------strainLoad-------------
    //! this loading must be after the loading of "hardeningComputation"
    keyword="strainLoad";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>0) {
        if (lines.size()==1)    {
            if (lines[0].size()==3) {mechanical.loadStrainLoading(lines[0][1],lines[0][2]);}
            else {error.Fatal("'strainLoad' must have 2arguments: 1)the name of the file 2) the extension");}
        }
        else {error.Fatal("you can have only one line 'strainLoad'");}
    }
    else {if(hardeningLoaded) {error.Fatal("If you have 'hardeningModel' you must have 'strainLoad' keyword");}}


    //------------choose coupling or not (must be after strainLoad)---------------
    keyword="couplingHardening";
    input.LinesStartingWithKeyword(_filename,keyword,lines,true);
    if (lines.size()>1) error.Fatal("couplingHardening defined twice.");
    if (lines.size()==1) {
        if(hardeningLoaded==false) {error.Fatal("If you have 'couplingHardening' you must have 'hardeningComputation'");}
        if (lines[0].size()!=2) {error.Fatal("You must have one argument for 'couplingHardening': strong or semi");}
        //-------------------------------
        if (lines[0][1]=="strong" || lines[0][1]=="Strong") {
            mechanicalHardeningCoupling=true;
            mechanical.SetMechanicalHardeningCoupling(mechanicalHardeningCoupling);
            if (notVerboseBool==false) {cout << "mechanicalHardeningCoupling is true" << endl ;}
            //if we have coupling we have to test first and last time
            checkVectorOfHardeningCoupling();
        }
        else if (lines[0][1]=="semi" || lines[0][1]=="Semi") {
            mechanicalSemiHardeningCoupling=true;
            mechanical.SetMechanicalSemiHardeningCoupling(mechanicalSemiHardeningCoupling);
            if (notVerboseBool==false) {cout << "mechanicalSemiHardeningCoupling is true" << endl ;}
            //if we have semi-coupling we have to test first and last time
            checkVectorOfHardeningCoupling();
        }
        else {error.Fatal("For 'couplingHardening' it is 'strong' or 'semi' for argument");}
    }
    lines.clear();

    //###########################################################
    //###--------------CHECK MODEL CONSISTENCY----------------###
    //###-------------AND DEFENITION OF OUTPUTS---------------###
    //###########################################################
    if (mechanicalModelActivated) {
        mechanical.CheckMechanicalModel();
        output.SetActivationOfMechanicalOutputs(true);
        output.SetMechanicalModelWritting(mechanical.GetModel());
        if (mechanicalHardeningCoupling==true && mechanicalSemiHardeningCoupling==true) {
            error.Fatal("You cannot have both 'mechanicalHardeningCoupling' and 'mechanicalSemiHardeningCoupling' (PreciSo class)");
        }
    }
    //###########################################################
    if (notVerboseBool==false) {cout << "Load mechanical data: OK" << endl;}
}


void Preciso::ChangeMatrixAndAssiocedElemPreci(bool _firstCallHere,string _nameFile,size_t _nodeBegin,size_t _nodeEnd)
{
    char* endCharact = NULL;
    ostringstream nodeIndexINI, nodeIndexFIN;
    nodeIndexINI << _nodeBegin; nodeIndexFIN << _nodeEnd;
    vector<Element> ElementsCOPY; ElementsCOPY=Elements;
    Elements.clear();Precipitates.clear();
    size_t nbOfMatrix=1;
    vector<string> arg;
    vector<vector<string> > matrixLines, elementLines, precipitatesLines;
    string dump;
    /// \warning keep this order : matrix, elements, precipitates
    // -------- first reading : matrix data -----------
    ifstream matrixFile1(_nameFile.c_str(), ios::in);
    if (!matrixFile1) {error.Fatal("File "+ _nameFile +" not found");}
    while (!matrixFile1.eof())    {
        getline(matrixFile1,dump);
        arg.clear();
        input.Parse(dump,arg);
        if (arg.size()!=0 && arg[0]=="matrix") {matrixLines.push_back(arg);}
    }
    matrixFile1.close();
    //lot of verifications: for example we check that this new matrix is already defined in the initialDataBase
    if (matrixLines.size()!=1) {error.Fatal("We must have 1matrix in file '"+ _nameFile +"' that redifined matrix '"+matrix.GetName()+"'");}
    if (matrixLines[0].size()!=5) {error.Fatal("In file '"+_nameFile+"' matrix can have only 4arguments");}
    if (matrixLines[0][1]==matrix.GetName()) {error.Fatal("Our new matrix must be different as current");}
    bool matrixNOK=true;
    for (size_t p=0;p<ElementsCOPY.size();p++) {if (ElementsCOPY[p].GetName()==matrixLines[0][1]) {matrixNOK=false;}}
    if (matrixNOK) {error.Fatal("Our new matrix "+matrixLines[0][1]+" in '"+_nameFile+"' isn't defined in the initialDataBase");}
    matrix.SetName(matrixLines[0][1]);
    matrix.SetLatticeParameter(strtod(matrixLines[0][2].c_str(),&endCharact));
    matrix.SetAtomicVolume(strtod(matrixLines[0][3].c_str(),&endCharact));
    matrix.SetMolarMass(strtod(matrixLines[0][4].c_str(),&endCharact));
    // -------- second reading : element data --------------
    ifstream matrixFile2(_nameFile.c_str(), ios::in);
    if (!matrixFile2) {error.Fatal("File '"+ _nameFile +"' not found");}
    while (!matrixFile2.eof())    {
        getline(matrixFile2,dump);
        arg.clear();
        input.Parse(dump,arg);
        if (arg.size()!=0 && arg[0]=="element") {elementLines.push_back(arg);}
    }
    matrixFile2.close();
    if (elementLines.size()!=(ElementsCOPY.size()-nbOfMatrix)) {error.Fatal("In file '"+ _nameFile +"' we must have the same number of elements according to initial inputFile");}
    bool elementLost=true;
    //add new element in the vector Elements
    for (size_t p=0;p<elementLines.size();p++) {
        if (elementLines[p].size()!=6) {error.Fatal("In file '"+_nameFile+"' element '"+elementLines[p][1]+ "' can have only 5arguments");}
        elementLost=true;
        for (size_t m=0;m<ElementsCOPY.size();m++) {
            if(elementLines[p][1]==ElementsCOPY[m].GetName()) {
                Element localElement(elementLines[p],p);
                Elements.push_back(localElement);
                elementLost=false;
            }
        }
        if (elementLost) {error.Fatal("We haven't found this corresponding element '"+elementLines[p][1]+"' (compare 'input file' and '"+_nameFile+"')");}
    }
    // -------- we had the matrix at the end of the element vector-----------
    vector<string> virtualLineMatrixAsElement;virtualLineMatrixAsElement.clear();
    virtualLineMatrixAsElement.push_back("element");virtualLineMatrixAsElement.push_back(matrix.GetName());
    double contentWtPctMatrix=100.0;
    for (size_t i=0;i<Elements.size();i++) {contentWtPctMatrix-=Elements[i].GetContentWtPc();}
    ostringstream convertedString2;convertedString2 << contentWtPctMatrix;
    virtualLineMatrixAsElement.push_back(convertedString2.str());
    convertedString2.str("");convertedString2 << matrix.GetMolarMass();
    virtualLineMatrixAsElement.push_back(convertedString2.str());
    virtualLineMatrixAsElement.push_back("0");virtualLineMatrixAsElement.push_back("0");
    Element matrixAsElement(virtualLineMatrixAsElement,Elements.size());
    Elements.push_back(matrixAsElement);
    // -------- third reading : precipitates data -----------
    bool boolPrecipitationActived=true;
    ifstream matrixFile3(_nameFile.c_str(), ios::in);
    if (!matrixFile3) {error.Fatal("File "+ _nameFile +" not found");}
    while (!matrixFile3.eof())    {
        getline(matrixFile3,dump);
        arg.clear();
        input.Parse(dump,arg);
        if (arg.size()!=0 && arg[0]=="noPrecipitation") {boolPrecipitationActived=false;break;}
        if (arg.size()!=0 && arg[0]=="precipitate") {precipitatesLines.push_back(arg);}
    }
    matrixFile3.close();
    if (boolPrecipitationActived)  {
        for (size_t p=0;p<precipitatesLines.size();p++) {
            for (size_t k=0;k<precipitatesLines.size();k++) {
                if(p!=k) {if(precipitatesLines[p][1]==precipitatesLines[k][1]) {error.Fatal("In file '"+_nameFile+"' precipitate '"+precipitatesLines[p][1]+"' defined twice");}}
            }
        }
        for (size_t p=0;p<precipitatesLines.size();p++) {
            if (precipitatesLines[p].size()<10) {error.Fatal("In file '"+_nameFile+"' insufficient number of arguments for precipitate "+precipitatesLines[p][1]);}
            Precipitate localPrecipitate(Elements);
            localPrecipitate.DefinePrecipitate(precipitatesLines[p]);
            Precipitates.push_back(localPrecipitate);
        }
    }
    else {if (_firstCallHere){error.Warning("No precitation at nodes "+nodeIndexINI.str()+" : "+nodeIndexFIN.str());}}
}

void Preciso::ChangeElement(vector<string> const& _line)
{
    //Find the position in the vector Elements of the element to change
    int position=-1;
    for (size_t i=0;i<Elements.size();i++) if (_line[1]==Elements[i].GetName())    {
        position=i;
        //We can break the loop since it has already been check that no element was defined twice
        break;
    }
    if (position==-1) {error.Fatal("name of Element for current node not defined in elements list.");}

    //The former element is erased
    Elements.erase(Elements.begin()+position);

    //Define the new element
    Element localElement(_line,position);

    //Insert the new precipitate in the precipitate table
    Elements.insert(Elements.begin()+position,localElement);

    //Remove the matrix (last element) and re-add it to the list of elements
    if (Elements[Elements.size()-1].GetName()!=matrix.GetName()) {error.Fatal("Incorrect position of the matrix in the list of elements.");}
    Elements.pop_back();

    vector<string> virtualLineMatrixAsElement;
    virtualLineMatrixAsElement.clear();
    virtualLineMatrixAsElement.push_back("element");
    virtualLineMatrixAsElement.push_back(matrix.GetName());
    double contentWtPctMatrix=100.0;
    for (size_t i=0;i<Elements.size();i++) {contentWtPctMatrix-=Elements[i].GetContentWtPc();}
    ostringstream convertedString2;
    convertedString2 << contentWtPctMatrix;
    virtualLineMatrixAsElement.push_back(convertedString2.str());
    convertedString2.str("");
    convertedString2 << matrix.GetMolarMass();
    virtualLineMatrixAsElement.push_back(convertedString2.str());
    virtualLineMatrixAsElement.push_back("0");
    virtualLineMatrixAsElement.push_back("0");
    Element matrixAsElement(virtualLineMatrixAsElement,Elements.size());
    Elements.push_back(matrixAsElement);
}

void Preciso::ChangePrecipitate(vector<string>& _line)
{
    //Find the position in the vector Precipitates of the precipitate to change
    int position=-1;
    for (size_t i=0;i<Precipitates.size();i++) if (_line[1]==Precipitates[i].GetName())    {
        position=i;
        //We can break the loop since it has already been check that no precipitate was defined twice
        break;
    }
    if (position==-1) error.Fatal("name of Precipitate for current node not defined in precipitates list.");

    //The former precipitate is erased
    Precipitates.erase(Precipitates.begin()+position);
    //Define the new precipitate
    Precipitate localPrecipitate(Elements);
    localPrecipitate.DefinePrecipitate(_line);
    //Insert the new precipitate in the precipitate table
    Precipitates.insert(Precipitates.begin()+position,localPrecipitate);
}

void Preciso::ChangeBoostPrecipitateDiffusion(vector<string>& _line)
{
    char* endCharact = NULL;
    //Find the position in the vector Precipitates of the precipitate to change
    int position=-1;
    for (size_t i=0;i<Precipitates.size();i++) if (_line[1]==Precipitates[i].GetName())    {
        position=i;
        //We can break the loop since it has already been check that no precipitate was defined twice
        break;
    }
    if (position==-1) error.Fatal("name of Precipitate in boostPrecipitateDiffusion for current node not defined in precipitates list.");
    Precipitates[position].SetBoostPrecipitateDiffusion(strtod(_line[2].c_str(),&endCharact));
}

void Preciso::InitializeTime(Temperature const& _temperature,vector<Element> const& _Elements,vector<Precipitate> &_Precipitates)
{
    if (timeStepManagement==1) {
        if (_temperature.GetAndCheckInitialTime()==0) {error.Fatal("Initial time must be non 0 for version 1 time step management");}
        currentTime=_temperature.GetAndCheckInitialTime();
        dt=currentTime/10000.0;
        criterion=1;    }
    else if (timeStepManagement==3) {
        currentTime=_temperature.GetAndCheckInitialTime();
        dt=initialDT;    }
    else error.Fatal("Incorrect choice for time management");

    //check that the first increment of time don't goes behind the first boundary
    if (fabs(_temperature.GetTimeWithIndex(1)-_temperature.GetTimeWithIndex(0))<initialDT){
        error.Fatal("First time must be greather than initialDt to have good management of time's boundary");
    }

    currentTimeIndex=1;
    double initialTemperature=temperature.GetTemperature(_temperature.GetAndCheckInitialTime());

    //Clear Criterion for the case where this routine is called from a node for reinitialisation
    if(criterion==1)   {
        Criterion.clear();
        for (size_t i=0;i<_Precipitates.size();i++)    {
            _Precipitates[i].SuperSaturationCalculation(_Elements, initialTemperature);
            _Precipitates[i].DrivingForceCalculation(initialTemperature);
            _Precipitates[i].RStarCalculation(initialTemperature);
            Criterion.push_back(_Precipitates[i].GetRStar());
        }
    }
    else if (criterion==2) {
        Criterion.clear();
        for (size_t i=0;i<_Elements.size();i++)    {
            Criterion.push_back(_Elements[i].GetSolidSolContent());
        }
    }
    else {error.Fatal("Incorrect kind of criterion");}
}

void Preciso::InitializeAtomicVolumeSS(Matrix & _matrix,vector<Element> const& _Elements,bool _firstCall)
{
    if (timeStepManagement==3) {_matrix.SetAtomicVolumeSS(_Elements,_firstCall);}
    else {cout<<"If time step management is not 3 then VatSS=VatM"<<endl;}
}

void Preciso::setSmallestTimeStep(double _nodeSmallestTimeStep) {smallestTimeStep=_nodeSmallestTimeStep;}

bool Preciso::validTimeStep(vector<Element> const& _Elements,vector<Precipitate> &_Precipitates, double const& _currentTemperature,unsigned int const& _timeStep, string& _reasonTimeStepRejected)
{
    for (size_t i=0;i<_Elements.size();i++) {
        if ((_Elements[i].GetSolidSolContent()<0.0)||(_Elements[i].GetSolidSolContent()>1.0)){
            if (notVerboseBool==false) {cout << _Elements[i].GetName() << endl;}
            //Check if the time step is too small
            if (dt<smallestTimeStep) {
                error.Fatal("Smallest time step value reached with incorrect solid solution content values.");
            }
            _reasonTimeStepRejected="Element "+_Elements[i].GetName()+" has concentration <0 or >1";
            return false;
        }
        if (isnan(_Elements[i].GetSolidSolContent()) || isinf(_Elements[i].GetSolidSolContent())){
            if (notVerboseBool==false) {cout << _Elements[i].GetName() << endl;}
            error.Warning("GetSolidSolContent is nan or inf in valid time step");
            //Check if the time step is too small
            if (dt<smallestTimeStep) {
                error.Fatal("Smallest time step value reached with nan or inf solid solution.");
            }
            _reasonTimeStepRejected="Element "+_Elements[i].GetName()+" is nan of inf";
            return false;
        }
    }

    if (dt<smallestTimeStep) {
        ostringstream convertedString;
        convertedString << nodeIndex;
        error.Warning("Time step < lowerLimite. Node : " + convertedString.str());
        if(criterion==1)   {
            for (size_t i=0;i<_Precipitates.size();i++) {Criterion[i]=_Precipitates[i].GetRStar();}
        }
        else if (criterion==2) {
            for (size_t i=0;i<_Elements.size();i++) {Criterion[i]=_Elements[i].GetSolidSolContent();}
        }
        else {error.Fatal("Incorrect kind of criterion in 'validTimeSte[1]    double    0.0000070339023669811759p'");}
        return true;
    }
    double CriterionTest=0.,CriterionTestAbs=0.;
    if(criterion==1)   {
        for (size_t i=0;i<_Precipitates.size();i++) {
            if (_Precipitates[i].GetNumberOfClass()!=0)        {
                //rStar is updated (w/ the new volume fractions but the current temperature) the new volume fractions at the end of the current time step are calculated before the call of this routine
                _Precipitates[i].SuperSaturationCalculation(_Elements, _currentTemperature);
                _Precipitates[i].DrivingForceCalculation(_currentTemperature);
                _Precipitates[i].RStarCalculation(_currentTemperature);
                CriterionTest=fabs((Criterion[i]-_Precipitates[i].GetRStar())/Criterion[i]);
                //Force the validation of the time step if it's too small
                if (CriterionTest>maxCriterionIncrease) {
                    _reasonTimeStepRejected="criterion for time step validation (rStar) is not fulfilled";
                    return false;
                    
                }
            }
        }
    }
    else if (criterion==2) {
        for (size_t i=0;i<_Elements.size();i++) {
            //masseBalance was already called
            CriterionTest=fabs((Criterion[i]-_Elements[i].GetSolidSolContent())/Criterion[i]);
            CriterionTestAbs=fabs(Criterion[i]-_Elements[i].GetSolidSolContent());
            if (_timeStep!=1) {if (CriterionTest>maxCriterionIncrease) {
                _reasonTimeStepRejected="criterion for time step validation (solContent) is not fulfilled";
                return false;}
                
            }
            else if (CriterionTest>maxCriterionIncrease && CriterionTestAbs>1e-6) {
                _reasonTimeStepRejected="criterion for time step validation (solContent) is not fulfilled (first time step)";
                return false;}
        }
    }
    else {error.Fatal("Incorrect kind of criterion in 'validTimeStep'");}
    
    return true;
}

bool Preciso::ValidNuclGrowthDiss(Matrix& _Matrix, vector<Element>& _Elements,vector<Precipitate> &_Precipitates, double const& _currentTemperature,unsigned int const& _timeStep,string& _reasonTimeStepRejected)
{
    if (onlyMechanicComputation) {return true;}
    else   {
        for (size_t j=0;j<_Elements.size();j++) {
            _Elements[j].MassBalance(_Matrix,_Precipitates,_Elements);
        }
        
        for (size_t j=0;j<_Precipitates.size();j++) if(_Precipitates[j].IsDormant()==false)    {
            _Precipitates[j].Nucleation(_Elements,_Matrix,currentTime,dt,_currentTemperature,firstTime,timeStepManagement);
            _Precipitates[j].Growth(_Elements,_Matrix,dt,_currentTemperature);
            _Precipitates[j].Dissolution();
        }
        
        for (size_t j=0;j<_Elements.size();j++) {
            _Elements[j].MassBalance(_Matrix,_Precipitates,_Elements);
        }
        if (simplifiedMassBalance==false) {_Matrix.SetAtomicVolumeSS(_Elements,false);}

        return validTimeStep(_Elements,_Precipitates,_currentTemperature,_timeStep, _reasonTimeStepRejected);
    }
}

void Preciso::PreNuclGrowthDiss(Matrix& _Matrix, vector<Element>& _Elements,vector<Precipitate> &_Precipitates, double const& _currentTemperature)
{
    // Update the criterion for next timestep validation
    if (criterion==1) for (size_t i=0;i<_Precipitates.size();i++) {
        _Precipitates[i].SuperSaturationCalculation(_Elements, _currentTemperature);
        _Precipitates[i].DrivingForceCalculation(_currentTemperature);
        _Precipitates[i].RStarCalculation(_currentTemperature);
        Criterion[i]=_Precipitates[i].GetRStar();
    }
    else if (criterion==2) {for (size_t i=0;i<_Elements.size();i++) {
        Criterion[i]=_Elements[i].GetSolidSolContent();}
    }
    else {error.Fatal("Incorrect kind of criterion in 'validTimeStep'");}
}

double Preciso::PostNuclGrowthDiss(Matrix& _Matrix, vector<Element>& _Elements,vector<Precipitate> &_Precipitates, double const& _currentTemperature, unsigned int const& _timestep,bool &_reduced)
{
    for (size_t j=0;j<_Precipitates.size();j++) {_Precipitates[j].ClassManagement();}
    Precipitates=_Precipitates;
    Elements=_Elements;
    matrix=_Matrix;
    
    // Output in the output file and Time and time step increment
    // true version v3 : Update the next time before increasing the time step used for the next computation
    if (timeStepManagement==1)      {
        output.TimeStepOutput(mechanical,matrix,Elements,Precipitates,temperature,currentTimeIndex,currentTime,_currentTemperature,dt,_timestep,nodeIndex,false);
        dt*=increaseDT;  currentTime+=dt;
        if (leaveDomain==true && _reduced==false) {if (currentTimeIndex<temperature.GetNumberOfTime()-1) {currentTimeIndex++;}}
        if (leaveMechaDomain==true && _reduced==false && (mechanicalHardeningCoupling==1 || mechanicalSemiHardeningCoupling==1))      {
            //for last time we cannot go beyond the last index
            mechanicalComputation(false,true,currentMechanicTimeIndex,matrix,Elements,Precipitates,temperature.GetTemperature(currentTime));
            WriteMechanicalHardeningResults(false,false);
            if (currentMechanicTimeIndex<mechanical.GetNumberOfMechanicalTime()-1) {
                currentMechanicTimeIndex++;
            }
        }
        leaveDomain=false;
        leaveMechaDomain=false;
    }
    else if (timeStepManagement==3) {
        //output.TimeStepOutput(mechanical,matrix,Elements,Precipitates,temperature,currentTimeIndex,currentTime+dt,_currentTemperature,dt,_timestep,nodeIndex,false);
        output.TimeStepOutput(mechanical,matrix,Elements,Precipitates,temperature,currentTimeIndex,currentTime,_currentTemperature,dt,_timestep,nodeIndex,false);
        currentTime+=dt;
        //if(dt>1) dt=1;
        dt*=increaseDT;
        if (leaveDomain==true && _reduced==false) {if (currentTimeIndex<temperature.GetNumberOfTime()-1) {currentTimeIndex++;}}
        if (leaveMechaDomain==true && _reduced==false && (mechanicalHardeningCoupling==1 || mechanicalSemiHardeningCoupling==1))        {
            //for last time we cannot go beyond the last index
            mechanicalComputation(false,true,currentMechanicTimeIndex,matrix,Elements,Precipitates,temperature.GetTemperature(currentTime));
            WriteMechanicalHardeningResults(false,false);
            if (currentMechanicTimeIndex<mechanical.GetNumberOfMechanicalTime()-1) {
                currentMechanicTimeIndex++;
            }
        }
        leaveDomain=false;
        leaveMechaDomain=false;
    }

    //#################################################################
    //##### we check if we overcome a temperature of strain flag ######
    //#################################################################
    int temperatureFlagOvershoot=0,  mechanicalFlagOvershoot=0;
    double dt_temperatureChoice=0.,  dt_mechanicalChoice=0.;
    double timeFlag=temperature.GetTimeWithIndex(currentTimeIndex);

    //Check if we leave a temperature domain
    if (currentTime<timeFlag && currentTime+dt>timeFlag) {
        dt_temperatureChoice=timeFlag-currentTime;
        leaveDomain=true;
        temperatureFlagOvershoot=1;
    }

    // Check if we leave a mechanical time domaine for mechanical-precipitation problem
    if (mechanicalHardeningCoupling || mechanicalSemiHardeningCoupling) {
        timeFlag=mechanical.GetMechanicalTimeWithIndex(currentMechanicTimeIndex);
        if (currentTime<timeFlag && currentTime+dt>timeFlag) {
            dt_mechanicalChoice=timeFlag-currentTime;
            leaveMechaDomain=true;
            mechanicalFlagOvershoot=1;
        }
    }
    //#################################################################
    //#####   we choose dt if there is at least one overshoot    ######
    //#################################################################
    if (temperatureFlagOvershoot==1 && mechanicalFlagOvershoot==0)      {dt=dt_temperatureChoice;}
    else if (temperatureFlagOvershoot==0 && mechanicalFlagOvershoot==1) {dt=dt_mechanicalChoice;}
    else if (temperatureFlagOvershoot==1 && mechanicalFlagOvershoot==1) {
        if (dt_mechanicalChoice<dt_temperatureChoice) {
            dt=dt_mechanicalChoice;}
        else {dt=dt_temperatureChoice;}
    }
    else {dt=dt;}

    //#################################################################
    return dt;
}

void Preciso::setNodeIndex(size_t const& _index) {nodeIndex=_index;}

void Preciso::setXPos(double const& _xPos) {xPos=_xPos;}

void Preciso::setYPos(double const& _yPos) {yPos=_yPos;}

void Preciso::setZPos(double const& _zPos) {zPos=_zPos;}

void Preciso::setVolume(double const& _volume) {
    volume=_volume;
    for (size_t i=0;i<Precipitates.size();i++)        {
        Precipitates[i].SetVolumeNode(volume);
        matrix.SetVolumeNode(volume);
    }
}


double Preciso::getVolume() const {return volume;}

void Preciso::WriteInitialOutputs(){
    bool forceWriting=true;
    if (timeStepManagement==1)     {output.TimeStepOutput(mechanical,matrix,Elements,Precipitates,temperature,currentTimeIndex,currentTime,temperature.GetTemperature(temperature.GetAndCheckInitialTime()),0,0,nodeIndex,forceWriting);}
    else if (timeStepManagement==3){output.TimeStepOutput(mechanical,matrix,Elements,Precipitates,temperature,currentTimeIndex,currentTime,temperature.GetTemperature(temperature.GetAndCheckInitialTime()),0,0,nodeIndex,forceWriting);}

}

void Preciso::mechanicalComputation(bool initialisation,bool _semiCoupling,size_t _timeMechaIndex,Matrix const& _Matrix, vector<Element> const& _Elements,vector<Precipitate> const& _Precipitates,double const& _currentTemperature)
{
    if (mechanicalModelActivated)
    {
        //verification
        if (mechanicalHardeningCoupling && mechanicalSemiHardeningCoupling) {error.Fatal("You cannot have 'mechanicalHardeningCoupling' & 'mechanicalSemiHardeningCoupling'");}
        //########################################################
        //yield stress computation and computation of strong coupling if chosen
        //########################################################
        //-------------------update temperature in mechanical class-----------------------
        mechanical.SetTemperature(_currentTemperature);

        //--------------run model that compute precipitate contribution-------------------
        int activedMicrostructuralModel=mechanical.GetModel();

        if (activedMicrostructuralModel==1) {mechanical.ModelOne(_Matrix,_Elements,_Precipitates,currentTime,dt);}
        else if (activedMicrostructuralModel==0) {mechanical.ModelAlex(_Matrix,_Elements,_Precipitates,currentTime,dt);}
        else if (activedMicrostructuralModel==2) {mechanical.ModelTwo(_Matrix,_Elements,_Precipitates,currentTime,dt);}
        else if (activedMicrostructuralModel==3) {mechanical.ModelThree(_Matrix,_Elements,_Precipitates,currentTime,dt);}
        else if (activedMicrostructuralModel==4) {mechanical.ModelFour(_Matrix,_Elements,_Precipitates,currentTime,dt);}
        else if (activedMicrostructuralModel==5) {mechanical.ModelFisk(_Matrix,_Elements,_Precipitates,currentTime,dt);}
        else if (activedMicrostructuralModel==6) {mechanical.ModelAlexSphere(_Matrix,_Elements,_Precipitates,currentTime,dt);}
        else {
            ostringstream convertToString;
            convertToString << activedMicrostructuralModel;
            error.Fatal("In 'mechanicalComputation' model n°"+convertToString.str()+" is not defined");
        }
        if (_semiCoupling==false)   {
            //-----------------------coupled hardening is activated----------------------------
            if(mechanicalHardeningCoupling && initialisation==false) {
                mechanical.BehaviourCoupledIntegration(currentTime,dt);
            }
        }
        //########################################################
        //yield stress computated and here if semi coupling is chosen we compute it (cf. 'PostNuclGrowthDiss')
        //########################################################
        if (_semiCoupling && initialisation==false && mechanicalSemiHardeningCoupling) {
            mechanical.BehaviourSemiCoupledIntegration(_timeMechaIndex);
        }
    }
}

void Preciso::checkVectorOfHardeningCoupling()
{
    if (mechanicalHardeningCoupling || mechanicalSemiHardeningCoupling) {
        ostringstream convertToString1,convertToString2,convertToString3,convertToString4,convertToString5;
        convertToString1 << nodeIndex;                   convertToString2 << mechanical.GetEndMechanicalTime();
        convertToString3 << temperature.GetTotalTime();  convertToString4 << mechanical.GetFirstMechanicalTime();
        convertToString5 << temperature.GetAndCheckInitialTime();

        //
        if (mechanical.GetEndMechanicalTime()!=temperature.GetTotalTime()) {
            vector<string> nameAndExtension=mechanical.GetNameExtensionHardeningFile();
            error.Fatal("Node:"+convertToString1.str()+", File '"+nameAndExtension[0]+ \
                        "': If hardening/precipitation coupling is actived the finalMechanical time "+ \
                        convertToString2.str()+" must be the same than final 'temperatureProfile' time"+ \
                        convertToString3.str());
        }
        if (mechanical.GetFirstMechanicalTime()!=temperature.GetAndCheckInitialTime()) {
            vector<string> nameAndExtension=mechanical.GetNameExtensionHardeningFile();
            error.Fatal("Node:"+convertToString1.str()+", File '"+nameAndExtension[0]+ \
                        "': If hardening/precipitation coupling is actived the firstMechanical time "+ \
                        convertToString4.str()+" must be the same than first 'temperatureProfile' time"+ \
                        convertToString5.str());
        }
    }
}

void Preciso::WriteMechanicalHardeningResults(bool _initialCall,bool _uncoupledModel)
{
    if (hardeningComputation)
    {
        //##### if hardening coupling is activated #####
        if (mechanicalModelActivated && _uncoupledModel==false) {
            output.HardeningResults(_initialCall,false,currentTime,mechanical,nodeIndex,uncoupledMecaResults);
        }

        //##### if coupling is not activated #####
        if (mechanicalModelActivated && _uncoupledModel)         {
            uncoupledMecaResults.clear();
            output.HardeningResults(true,true,currentTime,mechanical,nodeIndex,uncoupledMecaResults);        //write title
            uncoupledMecaResults=mechanical.BehaviourUncoupledIntegration();                                              //solve mechanic
            output.HardeningResults(false,true,currentTime,mechanical,nodeIndex,uncoupledMecaResults);      //write all mechanical results
        }
    }
}
