/// \file mechanical.cpp
/// \brief Methods of the class Mechanical
#include <iostream>
#include "error.h"
#include <fstream>  //For file read/write options
#include "mechanical.h"
#include <string.h> //to use strncmp
#include "mathematic.h"
#include "constants.h"
#include "element.h"
#include "precipitate.h"
#include "matrix.h"
#include <stdlib.h> //for atof, atoi, strtod
#include <string>
#include <vector>
#include <math.h>
#include <sstream>

using namespace std;

Mechanical::Mechanical() {
    //YIELD STRESS MODELING:   1=didier's PhD model 2=...Etc
    activedMicrostructuralModel=1;
    //! HARDENING MODELING COUPLED WITH METALLURGICAl YIELD STRESS:
    //1=isotropLinearHardening___NoTemperature //2=kinematicLinearHardening___NoTemperature //3=mixteLinearHardening___NoTemperature
    //4=isotropVoce___NoTemperature            //5=kinematicAmstrongFred___NoTemperature    //6=kinematicAmstrongFredWithGammaEvolution___NoTemperature
    //7=mixteVoceAmstrongFred___NoTemperature  //8=mixteVoceAmstrongFredWithGammaEvolution___NoTemperature
    //! KME model with sigma0 yield stress:
    //9=iso without sigmaSS et sigmaP          //10=iso with sigmaSS et sigmaP
    
    hardeningModelChosen=1;
    //COUPLING OR NOT:
    mechanicalHardeningCoupling=false;
    mechanicalSemiHardeningCoupling=false;
    //-----------generalities-------------
    notVerboseBool=false;    hardeningComputation=false;
    timeMechanicalSize=0;
    //----------- temperature-strainRate-------------
    currentTemperature=0.;    strainRate=0.;
    //----------- strain time surve ---------------
    StainMechanic.clear();    TimeMechanic.clear();
    nameOfHardeningFile="";   hardeningFileExtension="";
    //----------- SScontribution ---------------
    SSconstant.clear();          SSunit.clear();
    //----------- Graincontribution ---------------
    K_HP=0;
    //---------- precipitateConstants --------------
    transitionRadius.clear();    PathStructure.clear(); //can be regularPath=1,triangularPath=2...etc
    nbOfPrecipitates=0; //defined in 'DefinePrecipitateConstants'
    shearConstantStrength.clear();
    //--------- DislocationsConstants ----------
    initialDislocDensity=0.;            dislocStrength=0.;
    tensionLineConstant=0.;             dislocDensity=0;
    //----------- CristalloConstant ------------
    initialYield=0.;                    burgersNorm=0.;
    taylorFactor=3.06;                  structure=1; //1=cfc
    stringStructure="cfc";              powSum=2.0;
    //----------- Young modulus ------------
    TemperatureYoung.clear();           Young.clear();
    sizeYoung=0.;                       currentYoung=0.;
    //----------- Poisson coeff ------------
    TemperaturePoisson.clear();         Poisson.clear();
    sizePoisson=0.;                     currentPoisson=0.;
    //-------- various other variables -----
    currentShearModulus=0.;
    //-------- booleen to check model ----------
    SScontributionLoaded=false;         PrecipitateConstantsLoaded=false;
    DislocationsConstantsLoaded=false;  CristalloConstantLoaded=false;
    YoungModulusLoaded=false;           PoissonCoeffLoaded=false;
    grainSizeLoaded=false;
    //----------- sigma contribution ------------
    sigmaSS=0.;          dsigmaSS=0.;
    sigmaDislo=0.;       dsigmaDislo=0.;
    sigmaPreci=0.;       dsigmaPreci=0.;
    sigmaPreciI.clear(); dsigmaPreciI.clear();
    sigmaPreciIsh.clear(); sigmaGrain=0.;
    sigmaPreciIbp.clear(); dsigmaGrain=0.;
    sigmaFlowMicro=0.;   dsigmaFlowMicro=0.;
    // ################## CHOICE FOR HARENING LAW ########################
    //--------------GENERALITIES-------------------
    //initialPlasticStrain
    currentStrain=0.;
    epsP=0.;          epsP_initial=0.;
    epsPcum=0.;       epsPcum_initial=0.;
    //hardening values various model
    R=0.;  R_initial=0.;  X=0.;  X_initial=0.;
    //sigma
    stressMechanic=0.;     stressMechanic_initial=0.;
    //physics
    Zdislo=0.;       ZdisloPPT=0.;
    nG=0.;           nG_star=0.;
    nPPT.clear();    nPPT_star.clear();
    n_ppt=0;
    X_G=0;           Xppt=0.; //normaly must be a vector
    //metallurgical by-passed constants for physical model
    omegaEshelby.clear();
    YoungModulusPreci.clear();
    PoissonCoeffPreci.clear();
    fv_bp.clear();               dfv_bp.clear();
    meanR_bp.clear();            dmeanR_bp.clear();
    meanT_bp.clear();            dmeanT_bp.clear();
    meanL_bp.clear();            dmeanL_bp.clear();
    Ntot_bp.clear();             dNtot_bp.clear();
    distanceBetweenPPT.clear();  ddistanceBetweenPPT.clear();
    grainSize=0;        dgrainsize=0.;
    phiPPT.clear();
    //ici on detail la distance entre les divers type de PPT
    ddistancePPTsh.clear();
    distancePPTsh.clear();
    ddistancePPTbp.clear();
    distancePPTbp.clear();
    ddistancePPTall.clear();
    distancePPTall.clear();
    //------------semiphenomenological didier's model 6061----
    K_kin=0.;      K_iso=0.;                               //constants model 1,2 ou/et 3
    c_kin=0;       gamma_kin=0;    b_iso=0;    Rinf_iso=0; //constants model 4,5,8 et/ou 7
    gamma0_kin=0.; gammaK_kin=0.;  gammaInf_kin=0.;        //constants model 6 et/ou
    
    //------------physical didier's model----
    //equal to k2 if no precipitate influence on isotropHardening
    k1=0.;         k2_0=0.;          k2_P=0.;  //constants model 9 à 16
    lambdaG=0.;    k2=0.;            k3=0.;
    disableK2modif=false; //if 'disableK2modif' is true k2=k2_0
    disableRhoPPTcouplingBool=false;
    //------------------model with reversibility---------
    activeSSreversibility=false;
    activeDreversibility=false;
    activeHreversibility=false;
    activePreversibility=false;
    //####################################################################
}
Mechanical::~Mechanical() {}

double Mechanical::GetMechanicalTimeWithIndex(size_t const & _index) const
{
    if (_index>timeMechanicalSize-1) {
        ostringstream convertToString1,convertToString2;
        convertToString1 << _index;
        convertToString2 << TimeMechanic[_index-1];
        error.Fatal("Time index '"+convertToString1.str()+"' just after the time'" \
                    +convertToString2.str()+"' is out of range for 'GetMechanicalTimeWithIndex'");
    }
    return TimeMechanic[_index];
}

double Mechanical::GetStrainWithIndex(size_t const& _indexTime) const
{
    if (_indexTime>timeMechanicalSize-1) {error.Fatal("Strain index out of range in 'GetStrainWithIndex'");}
    if (_indexTime<0) {error.Fatal("Strain index cannot be negative in 'GetStrainWithIndex'");}
    return StainMechanic[_indexTime];
}

double Mechanical::GetStrain(double const& _time) const
{
    double timeI=0.;
    if ((_time<TimeMechanic[0])||(_time>TimeMechanic[timeMechanicalSize-1])) {
        error.Fatal("time out of range for 'strain'");
        return -1;    }
    else  {
        //the last member is timeMechanicalSize-1 but here we test timeMechanicalSize with < :(strictly less)
        //be carful for the linear interpolation we must don't enumerate the last indice because i+1 will be faulse
        for (size_t i=0;i<timeMechanicalSize;i++) {
            timeI=TimeMechanic[i];
            if (_time==timeI) {return StainMechanic[i];}
            else {
                if ((_time>timeI)&&(_time<TimeMechanic[i+1])&&(i!=timeMechanicalSize-1))            {
                    return StainMechanic[i]+((StainMechanic[i+1]-StainMechanic[i])/(TimeMechanic[i+1]-timeI))*(_time-timeI);
                }
            }
        }
    }
    error.Fatal("Bad interpolation in GetStrain");
    return -1;
}

size_t Mechanical::GetNumberOfMechanicalTime() const {return timeMechanicalSize;}

vector<string> Mechanical::GetNameExtensionHardeningFile() const
{
    vector<string> nameAndExtension; nameAndExtension.clear();
    nameAndExtension.push_back(nameOfHardeningFile);
    nameAndExtension.push_back(hardeningFileExtension);
    
    return nameAndExtension;
}

double Mechanical::GetIsotropHardening() const {return R;}

double Mechanical::GetKinematicHardening_phenomeno() const {return X;}

double Mechanical::GetEndMechanicalTime() const {return TimeMechanic[timeMechanicalSize-1];}

double Mechanical::GetCurrentStrain() const {return currentStrain;}

double Mechanical::GetCurrentStressMechanic() const {return stressMechanic;}

double Mechanical::GetFirstMechanicalTime() const {return TimeMechanic[0];}

void Mechanical::SetVerboseMode(bool _verboseBool) {notVerboseBool=_verboseBool;}

void Mechanical::SetMechanicalHardeningCoupling(bool _mechanicalHardeningCoupling) {mechanicalHardeningCoupling=_mechanicalHardeningCoupling;}

void Mechanical::SetMechanicalSemiHardeningCoupling(bool _mechanicalSemiHardeningCoupling) {mechanicalSemiHardeningCoupling=_mechanicalSemiHardeningCoupling;}

bool Mechanical::GetMechanicalHardeningCoupling() const {return mechanicalHardeningCoupling;}

bool Mechanical::GetMechanicalSemiHardeningCoupling() const {return mechanicalSemiHardeningCoupling;}

void Mechanical::SetModel(int _modelChoice) {activedMicrostructuralModel=_modelChoice;}

void Mechanical::SetTemperature(double _currentTemperature) {currentTemperature=_currentTemperature;}

void Mechanical::SetHardeningModel(int _hardeningModelChoice) {hardeningModelChosen=_hardeningModelChoice;}

int Mechanical::GetHardeningModel() const {return hardeningModelChosen;}

void Mechanical::SetActivedHardening(bool _activeBool) {hardeningComputation=_activeBool;}

void Mechanical::SetInitialHardeningValues()
{
    if (hardeningComputation)  {
        //------------semiphenomenological didier's model 6061----
        if (hardeningModelChosen>=1 && hardeningModelChosen<=8) {
            epsP=epsP_initial;                      epsPcum=epsPcum_initial;
            R=R_initial;                            X=X_initial;
            stressMechanic=stressMechanic_initial;
        }
        //------------Physical didier's model 6061----
        else if(hardeningModelChosen>=9 && hardeningModelChosen<=16) {
            epsP=epsP_initial; epsPcum=epsPcum_initial;
            R=R_initial;       stressMechanic=stressMechanic_initial;
        }
        else {error.Fatal("This hardening model is not implemented in 'SetInitialHardeningValues'");}
    }
    else {error.Fatal("Hardening computation is not activated in function 'SetInitialHardeningValues'");}
}

void Mechanical::loadStrainLoading(string const& _nameOfFile,string const& _extensionOfFile)
{
    //------------------------------------
    //we read this file for hardening and fill the vectors 'TimeMechanic' & 'StainMechanic'
    if (hardeningComputation) {
        //initialization
        char* endCharact = NULL;
        string dump;
        vector<string> arg;
        nameOfHardeningFile=_nameOfFile;
        hardeningFileExtension=_extensionOfFile;
        TimeMechanic.clear();
        StainMechanic.clear();
        string nameWithExtension=nameOfHardeningFile+hardeningFileExtension;
        
        //we load the file
        ifstream datafile(nameWithExtension.c_str(), ios::in);
        if (!datafile) {error.Fatal("File '"+ _nameOfFile +"' not found for the command 'strainLoad'");}
        //we check in first line the name of column
        getline(datafile,dump); arg.clear(); Parse(dump,arg);
        if(arg.size()<1) {error.Fatal("The file '"+_nameOfFile+"' must have in first line the legend");}
        
        //we check only the 3 first charactere
        if (strncmp(arg[0].c_str(),"tim",3)!=0 && strncmp(arg[0].c_str(),"tem",3)!=0 )  {error.Fatal("The first column of '"+_nameOfFile+"' must be 'time' or 'temps' (begin by 'temp' or 'tim')");}
        if (strncmp(arg[1].c_str(),"eps",3)!=0 && strncmp(arg[1].c_str(),"def",3)!=0 && strncmp(arg[1].c_str(),"strain",3)!=0 )  {error.Fatal("The second column of '"+_nameOfFile+"' must begin by 'temp' or 'tim' or must be 'strain'");}
        
        while (!datafile.eof())    {
            //we read the file and fill vectors timeMechanical and strainLoad
            getline(datafile,dump); arg.clear(); Parse(dump,arg);
            if (arg.size()>=2) {
                //we just take into account the 2 first column
                TimeMechanic.push_back(strtod(arg[0].c_str(),&endCharact));
                StainMechanic.push_back(strtod(arg[1].c_str(),&endCharact));
            }
        }
        datafile.close();
    }
    else {error.Fatal("If the 'hardeningModelChosen' have not been chosen we can't have the keyword 'strainLoad'");}
    
    timeMechanicalSize=TimeMechanic.size();
    currentStrain=StainMechanic[0];
    SetInitialHardeningValues();
}

void Mechanical::DefineSScontribution(vector<vector<string> > _InputLines,vector<Element> const& _Elements)
{
    size_t NbOfLines=_InputLines.size(),indexJ=0;
    char* endCharact = NULL;
    //1st=nameOfElement
    //2nd=unit
    //3rd=constantValue
    for (size_t i=0;i<_InputLines.size();i++) {
        if (_InputLines[i].size()-1!=3) {error.Fatal("SSconstant "+_InputLines[i][1]+" must have three arguments.");}
    }
    //check names/unit of described SScontribution element and fill associed vectors
    string nameOfElement="";
    int findName=0;
    int numberOfSScontribution=0;
    for (size_t i=0;i<_Elements.size();i++)    {
        nameOfElement=_Elements[i].GetName();
        findName=0;
        for (size_t j=0;j<NbOfLines;j++) {
            if (nameOfElement==_InputLines[j][1]) {
                numberOfSScontribution=numberOfSScontribution+1;
                findName=1;
                indexJ=j;
                if (notVerboseBool==false) {cout << "Mechanical model: element "+nameOfElement+" taken into account in SScontribution" << endl;}
                if (_InputLines[j][2]!="MPa_Wpct" && _InputLines[j][2]!="MPa_Xat" && _InputLines[j][2]!="Pa_Wpct" && _InputLines[j][2]!="Pa_Xat") {
                    error.Fatal("This unit for "+nameOfElement+" is not known in SScontribution");}
            }
        }
        if (findName==1) {
            SSconstant.push_back(strtod(_InputLines[indexJ][3].c_str(),&endCharact));
            SSunit.push_back(_InputLines[indexJ][2]);        }
        else {SSconstant.push_back(0.);SSunit.push_back("");}
    }
    if (notVerboseBool==false) {cout <<"The number of SS contributions is: " << numberOfSScontribution << endl;}
    SScontributionLoaded=true;
}

void Mechanical::DefinePrecipitateConstants(vector<vector<string> > _InputLines,vector<Precipitate> const& _Precipitates)
{
    nbOfPrecipitates=_Precipitates.size();
    
    if(CristalloConstantLoaded==false || YoungModulusLoaded==false || PoissonCoeffLoaded==false) {
        error.Fatal("'CristalloConstant, YoungModulusLoaded, PoissonCoeffLoaded' must be loaded before 'PrecipitateConstants' (because of taylor's fator using here)");
    }
    
    for (size_t i=0;i<nbOfPrecipitates;i++)    {
        if(_Precipitates[i].GetShapeIndex()!=2 && hardeningModelChosen>=9 && hardeningModelChosen<=16) {
            error.Fatal("Only rods now if physical hardening is chosen");}
    }
    
    size_t NbOfLines=_InputLines.size(),indexJ=0;
    ostringstream convertedStringStr;
    char* endCharact = NULL;
    //1st=nameOfPrecipitate  //2nd=shearConstantStrength  //3st=path structure
    //4nd=YoungModulusPreci  //5nd=PoissonCoeffPreci //6nd=PoissonCoeffPreci
    //7nd=initial number of boucles arrounf precipitate (usefull only for physical hardening)
    for (size_t i=0;i<_InputLines.size();i++) {
        convertedStringStr << _InputLines[i][1];
        if (_InputLines[i].size()-1!=9) {error.Fatal("precipitateConstants # "+convertedStringStr.str()+" must have 9 arguments.");}
    }
    //--- check if one precipitate definied twice ---
    int nameFound=0;
    string nameOfPrecipitate="";
    for (size_t i=0;i<nbOfPrecipitates;i++)    {
        nameFound=0;
        nameOfPrecipitate=_Precipitates[i].GetName();
        for (size_t j=0;j<_InputLines.size();j++) {if (nameOfPrecipitate==_InputLines[j][1]) {nameFound=nameFound+1;}}
        convertedStringStr << nameOfPrecipitate;
        if (nameFound>1) {error.Fatal("Precipitate "+convertedStringStr.str()+" defined twice in 'precipitateConstants'");}
        if (nameFound==0) {error.Fatal("Precipitate "+convertedStringStr.str()+" not defined in 'precipitateConstants'");}
    }
    //----- fill vectors 'transition radius', 'sigmaPreciI' & 'kindOfPath' ----
    nameOfPrecipitate="";
    int findName=0;
    for (size_t i=0;i<nbOfPrecipitates;i++)    {
        sigmaPreciI.push_back(0.); dsigmaPreciI.push_back(0.);        dfv_bp.push_back(0.);
        sigmaPreciIsh.push_back(0.);
        sigmaPreciIbp.push_back(0.);
        fv_bp.push_back(0.);       meanR_bp.push_back(0.);            dmeanR_bp.push_back(0.);
        meanT_bp.push_back(0.);    dmeanT_bp.push_back(0.);           Ntot_bp.push_back(0.);
        meanL_bp.push_back(0.);    dmeanL_bp.push_back(0.);
        dNtot_bp.push_back(0.);    distanceBetweenPPT.push_back(0.);  ddistanceBetweenPPT.push_back(0.);
        ddistancePPTsh.push_back(0.);
        distancePPTsh.push_back(0.);
        ddistancePPTbp.push_back(0.);
        distancePPTbp.push_back(0.);
        ddistancePPTall.push_back(0.);
        distancePPTall.push_back(0.);
        nameOfPrecipitate=_Precipitates[i].GetName();
        findName=0;
        for (size_t j=0;j<NbOfLines;j++) {
            if (nameOfPrecipitate==_InputLines[j][1]) {
                findName=1;
                indexJ=j;
                if (notVerboseBool==false) {cout << "Mechanical model: precipitate "+nameOfPrecipitate+" taken into account in 'precipitateConstants'" << endl;}
            }
        }
        if (findName==1) {
            //transition radius
            transitionRadius.push_back(strtod(_InputLines[indexJ][2].c_str(),&endCharact));
            //read path structure
            if (_InputLines[indexJ][3]=="regularPath" || _InputLines[indexJ][3]=="regular")            {PathStructure.push_back(1);}
            else if (_InputLines[indexJ][3]=="triangularPath" || _InputLines[indexJ][3]=="triangular") {PathStructure.push_back(2);}
            else {error.Fatal("This precipitate path is not defined in 'DefinePrecipitateConstants'");}
            //
            //error.Fatal("shearConstantStrength added from ABalan phD code, check mechanical program execution");
            // MODIF DB&MP(08/2017): on passe le paramtre k rajoutŽ par AB ˆ la fin pour raison de back-compatibilitŽ
            YoungModulusPreci.push_back(strtod(_InputLines[indexJ][4].c_str(),&endCharact));
            
            PoissonCoeffPreci.push_back(strtod(_InputLines[indexJ][5].c_str(),&endCharact));
            ShearModulusPreci.push_back(YoungModulusPreci[i]/(2*(1+PoissonCoeffPreci[i])));
            nPPT.push_back(strtod(_InputLines[indexJ][6].c_str(),&endCharact));
            nPPT_star.push_back(strtod(_InputLines[indexJ][7].c_str(),&endCharact));
            phiPPT.push_back(strtod(_InputLines[indexJ][8].c_str(),&endCharact));
            shearConstantStrength.push_back(strtod(_InputLines[indexJ][9].c_str(),&endCharact));
        }
        else {error.Fatal("Precipitate "+_InputLines[indexJ][1]+" not found in 'precipitateConstants' command");}
        //-----------------------------------------
        //       define Eshelby "stress factor"
        //       (useful for physical hardening)
        //-----------------------------------------
        
        n_ppt=nPPT[0]; //this scalaire is used because in physical hardening we assumed only one precipitate
        
        currentShearModulus=currentYoung/(2*(1+currentPoisson));
        
        if (_Precipitates[i].GetShapeIndex()==1) {
            omegaEshelby.push_back((7-5*currentPoisson)/(15-15*currentPoisson));
            double tempNumerator1=currentShearModulus*omegaEshelby[i]*ShearModulusPreci[i]*burgersNorm;
            double tempDenominator1=ShearModulusPreci[i]-omegaEshelby[i]*(ShearModulusPreci[i]-currentShearModulus);
            factorKineticContribution.push_back(taylorFactor*tempNumerator1/tempDenominator1);
        }
        else if (_Precipitates[i].GetShapeIndex()==2) { //Rod
            //aspect ratio is the length divided by the radius in PreciSo !!!
            double k=_Precipitates[i].GetAspectRatio()/2;
            double numeratorPart1=acosh(k)*(k*k*k*(1+currentPoisson)+k*(2-currentPoisson));
            double numeratorPart2=sqrt(k*k-1)*(k*k*k*k*(1-currentPoisson)+k*k*(currentPoisson-4));
            double denominator=(2-2*currentPoisson)*pow((k*k-1),5./2.);
            omegaEshelby.push_back((numeratorPart1+numeratorPart2)/denominator);
            double tempNumerator2=sqrt(3.0)*currentShearModulus*omegaEshelby[i]*ShearModulusPreci[i]*burgersNorm;
            double tempDenominator2=ShearModulusPreci[i]-omegaEshelby[i]*(ShearModulusPreci[i]-currentShearModulus);
            factorKineticContribution.push_back(taylorFactor*tempNumerator2/tempDenominator2);
        }
        else if (_Precipitates[i].GetShapeIndex()==6) { // RodFunction
            //aspect ratio is the length divided by the radius in PreciSo !!!
            double k=_Precipitates[i].AspectRatioFromRodFunction(_Precipitates[i].MeanRadius())/2;
            double numeratorPart1=acosh(k)*(k*k*k*(1+currentPoisson)+k*(2-currentPoisson));
            double numeratorPart2=sqrt(k*k-1)*(k*k*k*k*(1-currentPoisson)+k*k*(currentPoisson-4));
            double denominator=(2-2*currentPoisson)*pow((k*k-1),5./2.);
            omegaEshelby.push_back((numeratorPart1+numeratorPart2)/denominator);
            double tempNumerator2=sqrt(3.0)*currentShearModulus*omegaEshelby[i]*ShearModulusPreci[i]*burgersNorm;
            double tempDenominator2=ShearModulusPreci[i]-omegaEshelby[i]*(ShearModulusPreci[i]-currentShearModulus);
            factorKineticContribution.push_back(taylorFactor*tempNumerator2/tempDenominator2);
        }
        else if (_Precipitates[i].GetShapeIndex()==4) {
            //aspect ratio is the diameter divided by the height in PreciSo !!!
            double k=_Precipitates[i].GetAspectRatio()/2;
            double numeratorPart1=acosh(k)*(k*k*k*(1+currentPoisson)+k*(2-currentPoisson));
            double numeratorPart2=sqrt(k*k-1)*(k*k*k*k*(1-currentPoisson)+k*k*(currentPoisson-4));
            double denominator=(2-2*currentPoisson)*pow((k*k-1),5./2.);
            omegaEshelby.push_back((numeratorPart1+numeratorPart2)/denominator);
            double tempNumerator2=sqrt(3.0)*currentShearModulus*omegaEshelby[i]*ShearModulusPreci[i]*burgersNorm;
            double tempDenominator2=ShearModulusPreci[i]-omegaEshelby[i]*(ShearModulusPreci[i]-currentShearModulus);
            factorKineticContribution.push_back(taylorFactor*tempNumerator2/tempDenominator2);
        }
        else {error.Fatal("'omegaEshelby' is just implemented for rods and sphere");}
        
    }
    //-----------------------------------------
    PrecipitateConstantsLoaded=true;
}

void Mechanical::DefineDislocationsConstants(vector<string> _InputLine)
{
    char* endCharact = NULL;
    //1st=dislocationDensity    //2nd=strenghtConstant
    //3rd=tensionLineConstant
    initialDislocDensity=strtod(_InputLine[1].c_str(),&endCharact);
    dislocStrength=strtod(_InputLine[2].c_str(),&endCharact);
    tensionLineConstant=strtod(_InputLine[3].c_str(),&endCharact);
    dislocDensity=initialDislocDensity;
    DislocationsConstantsLoaded=true;
}

void Mechanical::DefineGrainSize(vector<string> _InputLine)
{
    char* endCharact = NULL;
    //1st=grainSize in meters
    //2nd=number of dislocations at grain boundaries
    //3nd=saturation of dislocations at grains
    //4nd=Hall Petch constant
    grainSize=strtod(_InputLine[1].c_str(),&endCharact);
    nG=strtod(_InputLine[2].c_str(),&endCharact);
    nG_star=strtod(_InputLine[3].c_str(),&endCharact);
    K_HP=strtod(_InputLine[4].c_str(),&endCharact);
    grainSizeLoaded=true;
}

void Mechanical::DefineCristalloConstant(vector<string> _InputLine)
{
    char* endCharact = NULL;
    //1st=purYieldStress(lattice friction)
    //2nd=taylorsFactor
    //3rd=burgersNorm
    //4th=structureCristallo
    //5nd=coefficient pour sommation contribution
    initialYield=strtod(_InputLine[1].c_str(),&endCharact);
    taylorFactor=strtod(_InputLine[2].c_str(),&endCharact);
    burgersNorm=strtod(_InputLine[3].c_str(),&endCharact);
    if (_InputLine[4]=="cfc") {structure=1;stringStructure="cfc";}
    else {error.Fatal("In mechanical part 'DefineCristalloConstant' only 'cfc' structure is possible");}
    if (_InputLine.size()-1>4)  {
        powSum=strtod(_InputLine[5].c_str(),&endCharact);
    }
    CristalloConstantLoaded=true;
}

void Mechanical::DefineCoefficientsForHardeningModel(vector<string> _InputLine)
{
    double disableK2modifInput,disableRhoPPTcoupling;
    char* endCharact = NULL;
    if (hardeningModelChosen==1) {
        if (_InputLine.size()-1!=1) {error.Fatal("For hardening model 1, the number of parameters for 'parametersForHardening' must be 1");}
        K_iso=strtod(_InputLine[1].c_str(),&endCharact);//unit [Pa]
    }
    else if (hardeningModelChosen==2) {
        if (_InputLine.size()-1!=1) {error.Fatal("For hardening model 2, the number of parameters for 'parametersForHardening' must be 1");}
        K_kin=strtod(_InputLine[1].c_str(),&endCharact);//unit [Pa]
    }
    else if (hardeningModelChosen==3) {
        if (_InputLine.size()-1!=2) {error.Fatal("For hardening model 3, the number of parameters for 'parametersForHardening' must be 2");}
        K_iso=strtod(_InputLine[1].c_str(),&endCharact);//unit [Pa]
        K_kin=strtod(_InputLine[2].c_str(),&endCharact);//unit [Pa]
    }
    else if (hardeningModelChosen==4) {
        if (_InputLine.size()-1!=2) {error.Fatal("For hardening model 4, the number of parameters for 'parametersForHardening' must be 2");}
        Rinf_iso=strtod(_InputLine[1].c_str(),&endCharact);//unit [Pa]
        b_iso=strtod(_InputLine[2].c_str(),&endCharact);//[no unit]
        
    }
    else if (hardeningModelChosen==5) {
        if (_InputLine.size()-1!=2) {error.Fatal("For hardening model 5, the number of parameters for 'parametersForHardening' must be 2");}
        c_kin=strtod(_InputLine[1].c_str(),&endCharact);//unit [Pa]
        gamma_kin=strtod(_InputLine[2].c_str(),&endCharact);//[no unit]
    }
    else if (hardeningModelChosen==6) {
        if (_InputLine.size()-1!=4) {error.Fatal("For hardening model 6, the number of parameters for 'parametersForHardening' must be 4");}
        c_kin=strtod(_InputLine[1].c_str(),&endCharact);//unit [Pa]
        gamma0_kin=strtod(_InputLine[2].c_str(),&endCharact);
        gammaInf_kin=strtod(_InputLine[3].c_str(),&endCharact);
        gammaK_kin=strtod(_InputLine[4].c_str(),&endCharact);
    }
    else if (hardeningModelChosen==7) {
        if (_InputLine.size()-1!=4) {error.Fatal("For hardening model 7, the number of parameters for 'parametersForHardening' must be 4");}
        c_kin=strtod(_InputLine[1].c_str(),&endCharact);//unit [Pa]
        gamma_kin=strtod(_InputLine[2].c_str(),&endCharact);//[no unit]
        Rinf_iso=strtod(_InputLine[3].c_str(),&endCharact);//unit [Pa]
        b_iso=strtod(_InputLine[4].c_str(),&endCharact);//[no unit]
        
    }
    else if (hardeningModelChosen==8) {
        if (_InputLine.size()-1!=6) {error.Fatal("For hardening model 8, the number of parameters for 'parametersForHardening' must be 6");}
        c_kin=strtod(_InputLine[1].c_str(),&endCharact);//unit [Pa]
        gamma0_kin=strtod(_InputLine[2].c_str(),&endCharact);
        gammaInf_kin=strtod(_InputLine[3].c_str(),&endCharact);
        gammaK_kin=strtod(_InputLine[4].c_str(),&endCharact);
        Rinf_iso=strtod(_InputLine[5].c_str(),&endCharact);//unit [Pa]
        b_iso=strtod(_InputLine[6].c_str(),&endCharact);//[no unit]
        
    }
    else if (hardeningModelChosen==9 || hardeningModelChosen==10) {
        if (_InputLine.size()-1!=2) {error.Fatal("For hardening model 9 or 10, the number of parameters for 'parametersForHardening' must be 2");}
        k1=strtod(_InputLine[1].c_str(),&endCharact);//unit
        k2=strtod(_InputLine[2].c_str(),&endCharact);
    }
    else if (hardeningModelChosen==11 || hardeningModelChosen==12) {
        if (_InputLine.size()-1!=4) {error.Fatal("For hardening model 11 or 12, the number of parameters for 'parametersForHardening' must be 4");}
        k1=strtod(_InputLine[1].c_str(),&endCharact);//
        k2=strtod(_InputLine[2].c_str(),&endCharact);
        k3=strtod(_InputLine[3].c_str(),&endCharact);
        lambdaG=strtod(_InputLine[4].c_str(),&endCharact);
    }
    else if (hardeningModelChosen==13 || hardeningModelChosen==14) {
        if (_InputLine.size()-1!=5) {error.Fatal("For hardening model 13 or 14, the number of parameters for 'parametersForHardening' must be 5");}
        k1=strtod(_InputLine[1].c_str(),&endCharact);//
        k2_0=strtod(_InputLine[2].c_str(),&endCharact);
        k2_P=strtod(_InputLine[3].c_str(),&endCharact);
        disableK2modifInput=strtod(_InputLine[4].c_str(),&endCharact);
        if(disableK2modifInput==0) {disableK2modif=true;}
        disableRhoPPTcoupling=strtod(_InputLine[5].c_str(),&endCharact);
        if(disableRhoPPTcoupling==0) {disableRhoPPTcouplingBool=true;}
    }
    else if (hardeningModelChosen==15) {
        if (_InputLine.size()-1!=7) {error.Fatal("For hardening model 15, the number of parameters for 'parametersForHardening' must be 7");}
        k1=strtod(_InputLine[1].c_str(),&endCharact);//
        k2_0=strtod(_InputLine[2].c_str(),&endCharact);
        k2_P=strtod(_InputLine[3].c_str(),&endCharact);
        disableK2modifInput=strtod(_InputLine[4].c_str(),&endCharact);
        if(disableK2modifInput==0) {disableK2modif=true;}
        k3=strtod(_InputLine[5].c_str(),&endCharact);
        lambdaG=strtod(_InputLine[6].c_str(),&endCharact);
        disableRhoPPTcoupling=strtod(_InputLine[7].c_str(),&endCharact);
        if(disableRhoPPTcoupling==0) {disableRhoPPTcouplingBool=true;}
    }
    else if (hardeningModelChosen==16) {
        if (_InputLine.size()-1!=9) {error.Fatal("For hardening model 16, the number of parameters for 'parametersForHardening' must be 9");}
        k1=strtod(_InputLine[1].c_str(),&endCharact);
        k2_0=strtod(_InputLine[2].c_str(),&endCharact);
        k2_P=strtod(_InputLine[3].c_str(),&endCharact);
        k3=strtod(_InputLine[4].c_str(),&endCharact);
        lambdaG=strtod(_InputLine[5].c_str(),&endCharact);
        //options pour activer les irreversibilites
        double SSreversibility=strtod(_InputLine[6].c_str(),&endCharact);
        if(SSreversibility==0) {activeSSreversibility=false;} else{activeSSreversibility=true;}
        double Dreversibility=strtod(_InputLine[7].c_str(),&endCharact);
        if(Dreversibility==0) {activeDreversibility=false;} else{activeDreversibility=true;}
        double Greversibility=strtod(_InputLine[8].c_str(),&endCharact);
        if(Greversibility==0) {activeHreversibility=false;} else{activeHreversibility=true;}
        double Preversibility=strtod(_InputLine[9].c_str(),&endCharact);
        if(Preversibility==0) {activePreversibility=false;} else{activePreversibility=true;}
    }
    else {error.Fatal("This 'hardeningModelChosen' is not implemented in 'DefineCoefficientsForHardeningModel'");}
}

void Mechanical::DefineYoungModulus(vector<string> _arg)
{
    char* endCharact = NULL;
    TemperatureYoung.clear();   Young.clear();
    //check is temperature increase
    for (size_t i=1;i<_arg.size()-2;i+=2){if(strtod(_arg[i+2].c_str(),&endCharact)<=strtod(_arg[i].c_str(),&endCharact)) {error.Fatal("Temperature value for Young modulus definition must be increasing");}}
    //add values in 'TemperatureYoung' and 'Young'
    for (size_t i=1;i<_arg.size();i+=2)    {
        TemperatureYoung.push_back((strtod(_arg[i].c_str(),&endCharact)));
        if ((strtod(_arg[i].c_str(),&endCharact))<0.) error.Fatal("Invalid temperature for temperature-YoungModulus history (<0)");
        Young.push_back((strtod(_arg[i+1].c_str(),&endCharact)));
        if ((strtod(_arg[i+1].c_str(),&endCharact))<0.) error.Fatal("Invalid YoungModulus for temperature-YoungModulus history (<0)");
    }
    sizeYoung=TemperatureYoung.size();
    
    if (sizeYoung==1) {error.Warning("If you have only one couple temperature-Young modulus, Young modulus is independant of temperature");}
    currentYoung=Young[0];
    
    YoungModulusLoaded=true;
}

void Mechanical::DefinePoissonCoeff(vector<string> _arg)
{
    char* endCharact = NULL;
    TemperaturePoisson.clear();   Poisson.clear();
    //check is temperature increase
    for (size_t i=1;i<_arg.size()-2;i+=2){if(strtod(_arg[i+2].c_str(),&endCharact)<=strtod(_arg[i].c_str(),&endCharact)) {error.Fatal("Temperature value for Poisson coeff definition must be increasing");}}
    //add values in 'TemperaturePoisson' and 'Poisson'
    for (size_t i=1;i<_arg.size();i+=2)    {
        TemperaturePoisson.push_back((strtod(_arg[i].c_str(),&endCharact)));
        if ((strtod(_arg[i].c_str(),&endCharact))<0.) error.Fatal("Invalid temperature for temperature-PoissonCoeff history (<0)");
        Poisson.push_back((strtod(_arg[i+1].c_str(),&endCharact)));
        if ((strtod(_arg[i+1].c_str(),&endCharact))<0.) error.Fatal("Invalid PoissonCoeff for temperature-PoissonCoeff history (<0)");
    }
    sizePoisson=TemperaturePoisson.size();
    
    if (sizePoisson==1) {error.Warning("If you have only one couple temperature-Poisson coeff, Poisson coeff is independant of temperature");}
    currentPoisson=Poisson[0];
    
    PoissonCoeffLoaded=true;
}

void Mechanical::CheckMechanicalModel()
{
    ostringstream convertedString;
    convertedString << activedMicrostructuralModel;
    if (activedMicrostructuralModel>=0 && activedMicrostructuralModel<=6)    {
        if (SScontributionLoaded==false)       {error.Fatal("for Model #"+convertedString.str()+": SSconstant must be Loaded");}
        if (PrecipitateConstantsLoaded==false)     {error.Fatal("for Model #"+convertedString.str()+": transRadius must be Loaded");}
        if (DislocationsConstantsLoaded==false){error.Fatal("for Model #"+convertedString.str()+": dislocations must be Loaded");}
        if (CristalloConstantLoaded==false)    {error.Fatal("for Model #"+convertedString.str()+": cristalloConstant must be Loaded");}
        if (YoungModulusLoaded==false)         {error.Fatal("for Model #"+convertedString.str()+": Young modulus must be Loaded");}
        if (PoissonCoeffLoaded==false)         {error.Fatal("for Model #"+convertedString.str()+": Poisson coeff must be Loaded");}
    }
    else {error.Fatal("The actived mechanical model # "+convertedString.str()+" is not implemented");}
}

int Mechanical::GetModel() const {return activedMicrostructuralModel;}

double Mechanical::GetYoung() const
{
    //if we have just one value forPoisson we get it
    if (sizeYoung==1) {return currentYoung;}
    //if we have temperature out of bounds we keep value of bounds
    else if (currentTemperature<TemperatureYoung[0]) {return Young[0];}
    else if (currentTemperature>TemperatureYoung[sizeYoung-1]) {return Young[sizeYoung-1];}
    //if we have temperature etween bounds we do a linear interpolation
    else  {
        double TemperatureYoungI=0.;
        for (size_t i=0;i<sizeYoung;i++) {
            TemperatureYoungI=TemperatureYoung[i];
            if (currentTemperature==TemperatureYoungI) {return Young[i];}
            else {
                if ((currentTemperature>TemperatureYoungI)&&(currentTemperature<TemperatureYoung[i+1])&&(i!=sizeYoung-1))            {
                    return Young[i]+((Young[i+1]-Young[i])/(TemperatureYoung[i+1]-TemperatureYoungI))*(currentTemperature-TemperatureYoungI);
                }
            }
        }
    }
    error.Fatal("Bad interpolation in GetYoung");
    return -1;
}

double Mechanical::GetPoisson() const
{
    //if we have just one value forPoisson we get it
    if (sizePoisson==1) {return currentPoisson;}
    //if we have temperature out of bounds we keep value of bounds
    else if (currentTemperature<TemperaturePoisson[0]) {return Poisson[0];}
    else if (currentTemperature>TemperaturePoisson[sizePoisson-1]) {return Poisson[sizePoisson-1];}
    //if we have temperature etween bounds we do a linear interpolation
    else  {
        double TemperaturePoissonI=0.;
        for (size_t i=0;i<sizePoisson;i++) {
            TemperaturePoissonI=TemperaturePoisson[i];
            if (currentTemperature==TemperaturePoissonI) {return Poisson[i];}
            else {
                if ((currentTemperature>TemperaturePoissonI)&&(currentTemperature<TemperaturePoisson[i+1])&&(i!=sizePoisson-1))            {
                    return Poisson[i]+((Poisson[i+1]-Poisson[i])/(TemperaturePoisson[i+1]-TemperaturePoissonI))*(currentTemperature-TemperaturePoissonI);
                }
            }
        }
    }
    error.Fatal("Bad interpolation in GetPoisson");
    return -1;
}

double Mechanical::GetSSconstantI(size_t const& _indexElem) const {return SSconstant[_indexElem];}

string Mechanical::GetSSunitI(size_t const& _indexElem) const {return SSunit[_indexElem];}

double Mechanical::GetTransitionRadiusI(size_t const& _indexPrecipitate) const {return transitionRadius[_indexPrecipitate];}

double Mechanical::GetshearConstantStrength(size_t const& _indexPrecipitate) const {return shearConstantStrength[_indexPrecipitate];}

double Mechanical::GetInitialYield() const {return initialYield;}

double Mechanical::GetSigmaSS() const {return sigmaSS;}

double Mechanical::GetSigmaGrain() const {return sigmaGrain;}

double Mechanical::GetDsigmaSS() const {return dsigmaSS;}

double Mechanical::GetSigmaDislo() const {return sigmaDislo;}

double Mechanical::GetDsigmaDislo() const {return dsigmaDislo;}

double Mechanical::GetSigmaPreci() const {return sigmaPreci;}

double Mechanical::GetDsigmaPreci() const {return dsigmaPreci;}

double Mechanical::GetSigmaPreciI(size_t _i) const {return sigmaPreciI[_i];}

double Mechanical::GetSigmaPreciIsh(size_t _i) const {return sigmaPreciIsh[_i];}

double Mechanical::GetSigmaPreciIbp(size_t _i) const {return sigmaPreciIbp[_i];}

double Mechanical::GetDsigmaPreciI(size_t _i) const {return dsigmaPreciI[_i];}

double Mechanical::GetsigmaFlowMicro() const {return sigmaFlowMicro;}

double Mechanical::GetDsigmaFlowMicro() const {return dsigmaFlowMicro;}

int Mechanical::GetIndexStructure() const {return structure;}

string Mechanical::GetNameStructure() const {return stringStructure;}

double Mechanical::Get_epsP() const {return epsP;}

double Mechanical::Get_epsPcum() const {return epsPcum;}

double Mechanical::Get_dislo() const {return Zdislo/burgersNorm;}

double Mechanical::Get_disloPPT() const {return ZdisloPPT/burgersNorm;}

double Mechanical::Get_nG() const {return nG;}

double Mechanical::Get_X_G() const {return X_G;}

double Mechanical::Get_n_ppt() const {return n_ppt;}

double Mechanical::Get_Xppt() const {return Xppt;}

double Mechanical::ComputeDisloContributionModel1()
{
    return taylorFactor*dislocStrength*currentShearModulus*burgersNorm*sqrt(dislocDensity);
}

double Mechanical::ComputeSScontributionModel1(vector<Element> const& _Elements)
{
    double sigmaSSTemp=0.;
    for (size_t i=0;i<_Elements.size();i++)    {
        if (fabs(SSconstant[i]>NUMERICLIMITDOUBLE)) {
            if (SSunit[i]=="MPa_Wpct")     {sigmaSSTemp=sigmaSSTemp+(SSconstant[i]*1e6)*pow(_Elements[i].SolidSolContentWtPercent(_Elements),2./3.);}
            else if (SSunit[i]=="MPa_Xat") {sigmaSSTemp=sigmaSSTemp+(SSconstant[i]*1e6)*pow(_Elements[i].GetSolidSolContent(),2./3.);}
            else if (SSunit[i]=="Pa_Wpct") {sigmaSSTemp=sigmaSSTemp+SSconstant[i]*pow(_Elements[i].SolidSolContentWtPercent(_Elements),2./3.);}
            else if (SSunit[i]=="Pa_Xat")  {sigmaSSTemp=sigmaSSTemp+SSconstant[i]*pow(_Elements[i].GetSolidSolContent(),2./3.);}
            else {error.Fatal("This unit "+SSunit[i]+" for SScontribution doesn't exist");}
        }
    }
    return sigmaSSTemp;
    
}


double Mechanical::ComputeSScontributionModelAlex(vector<Element> const& _Elements)
{
    double sigmaSSTemp=0.;
    double SolidSolContentTot=0.;
    int SSunitOk=1;
    int SSconstantOk=1;
    string SSunitTot;
    double SSconstantTot=0.;
    for (size_t i=0;i<_Elements.size();i++)    {
        if (i==0) {SSunitTot=SSunit[i]; SSconstantTot=SSconstant[i];}
        else if (SSunit[i]!=SSunitTot) {
            if (SSunit[i]!="") {SSunitOk=0;}} // ne sert à rien
        else if (SSconstant[i]!=SSconstantTot) {SSconstantOk=0;} // ne sert à rien
    }
    
    if (SSunitOk==1 && SSconstantOk==1) {
        for (size_t i=0;i<_Elements.size();i++)    {
            if (fabs(SSconstant[i]>NUMERICLIMITDOUBLE)) {
                if (SSunitTot=="MPa_Wpct"||SSunitTot=="Pa_Wpct")    {SolidSolContentTot= SolidSolContentTot+_Elements[i].SolidSolContentWtPercent(_Elements);}
                else if (SSunitTot=="MPa_Xat"||SSunitTot=="Pa_Xat") {SolidSolContentTot+=_Elements[i].GetSolidSolContent();}
                else {error.Fatal("This unit doesn't exist for SScontribution ");}
            }
        }
        if (SSunitTot=="MPa_Wpct")     {sigmaSSTemp=(SSconstantTot*1e6)*pow(SolidSolContentTot,2./3.);}
        else if (SSunitTot=="MPa_Xat") {sigmaSSTemp=(SSconstantTot*1e6)*pow(SolidSolContentTot,2./3.);}
        else if (SSunitTot=="Pa_Wpct") {sigmaSSTemp=SSconstantTot*pow(SolidSolContentTot,2./3.);}
        else if (SSunitTot=="Pa_Xat")  {sigmaSSTemp=SSconstantTot*pow(SolidSolContentTot,2./3.);}
    }
    else {error.Fatal("All units and SSconstants must be the same");}
    return sigmaSSTemp;
}

double Mechanical::ComputeSScontributionModelAlex_sqrt(vector<Element> const& _Elements)
{
    double sigmaSSTemp=0.;
    for (size_t i=0;i<_Elements.size();i++)    {
        if (fabs(SSconstant[i]>NUMERICLIMITDOUBLE)) {
            if (SSunit[i]=="MPa_Wpct")     {sigmaSSTemp=sigmaSSTemp+(SSconstant[i]*1e6)*pow(_Elements[i].SolidSolContentWtPercent(_Elements),1./2.);}
            else if (SSunit[i]=="MPa_Xat") {sigmaSSTemp=sigmaSSTemp+(SSconstant[i]*1e6)*pow(_Elements[i].GetSolidSolContent(),1./2.);}
            else if (SSunit[i]=="Pa_Wpct") {sigmaSSTemp=sigmaSSTemp+SSconstant[i]*pow(_Elements[i].SolidSolContentWtPercent(_Elements),1./2.);}
            else if (SSunit[i]=="Pa_Xat")  {sigmaSSTemp=sigmaSSTemp+SSconstant[i]*pow(_Elements[i].GetSolidSolContent(),1./2.);}
            else {error.Fatal("This unit "+SSunit[i]+" for SScontribution doesn't exist");}
        }
    }
    return sigmaSSTemp;
    
}

void Mechanical::ModelAlex(Matrix const& _matrix,vector<Element> const& _Elements,vector<Precipitate> const& _Precipitates,double _currentTime,double _dt)
{
    if(structure!=1) {error.Fatal("In model n°0 just 'cfc' structure is considered");}
    //###################################################################
    //###                      (Alex's model)                       ###
    //###################################################################
    
    //------------------- load constant ---------------------
    currentYoung=GetYoung();
    currentPoisson=GetPoisson();
    currentShearModulus=currentYoung/(2*(1+currentPoisson));
    //----------- compute SS & dislo contributions  ---------
    double sigmaDisloTemp=ComputeDisloContributionModel1();
    double sigmaSSTemp=ComputeSScontributionModelAlex_sqrt(_Elements);
    
    //-------------- precipitate contribution --------------
    //initialization
    double sigmaGrainTemp=0.;
    double sigmaPreciTemp=0.,sigmaBp=0.,sigmaSh=0.,sigmaTempI=0.;
    //**MP**error.Fatal("Line below to check, in ABalan PhD work, this value is not set to 0.");
    // checked by DB & MP
    //double shearConstantStrength=0.;
    double qj=0.,Nj=0.,Rj=0.,Tj=0.;
    
    double TjNj_bp=0.,RjNj_bp=0.,Nj_bp=0.,RjNj_sh=0.,NjRjsqrtqj_sh=0.,Nj_sh=0.;
    double F_bp=0.,F_sh=0.;
    double fv_bp_temp=0., distanceBetweenPPT_temp=0.,meanR_bp_temp=0.,meanT_bp_temp=0.,distanceBetweenPPT_bp=0.,distanceBetweenPPT_sh=0.,meanR_sh_temp=0.,meanT_sh_temp=0.;
    vector<double> sigmaPreciItemp;sigmaPreciItemp.clear();
    int yesShear=0;
    
    //tension line
    double tensionLine=tensionLineConstant*currentShearModulus*burgersNorm*burgersNorm;
    //-------------- initialisation for precipitate constants ---------------
    //stress contribution for each precipitates
    for (size_t i=0;i<_Precipitates.size();i++)    {
        //----------------------------------------
        if (_Precipitates[i].GetShapeIndex()!=4) {error.Fatal("Mechanical model Alex is just implemented for plates");}
        //----------------------------------------
        yesShear=0;
        
        //read transition radius and compute shearConstantStrength
        // If a null value of k is in input, k is calculated via the critical radius
        if (shearConstantStrength[i]==0){
        shearConstantStrength[i]=sqrt(_Precipitates[i].AspectRatioFromCylinderFunction(transitionRadius[i])*sqrt(2.0/3.0))/transitionRadius[i]*2*tensionLineConstant*burgersNorm;
            // shearConstantStrength=2*tensionLineConstant*burgersNorm/transitionRadius[i];
            //shearConstantStrength=2./3.*M_PI*pow(2./3.,1./4.)*0.0286/2.2;
            // shearConstantStrength=0.034; // d'après SUN 93
        }
        
        if (PathStructure[i]==2) //triangularPath
        {
            sigmaBp=0.; sigmaSh=0.; TjNj_bp=0.; RjNj_bp=0.; Nj=0.; Rj=0.; Tj=0.; RjNj_sh=0.; Nj_sh=0.;
            fv_bp_temp=0.; meanR_bp_temp=0.; meanT_bp_temp=0.; Nj_bp=0.; qj=0.; NjRjsqrtqj_sh=0.;
            
            qj=_Precipitates[i].AspectRatioFromCylinderFunction(_Precipitates[i].MeanRadius());
            
            for (size_t j=0;j<_Precipitates[i].GetNumberOfClass();j++)    {
                Nj=_Precipitates[i].GetNumber(j);
                Rj=_Precipitates[i].GetRadius(j);
                //qj=_Precipitates[i].AspectRatioFromCylinderFunction(Rj); // from AB PhD
                
                Tj=2*Rj/qj;
                if (Rj>=transitionRadius[i]) {
                    //bypassing
                    RjNj_bp+=Rj*Nj;
                    TjNj_bp+=Tj*Nj;
                    fv_bp_temp+=Rj*Rj*Tj*Nj;
                    Nj_bp+=Nj;
                }
                else {
                    //shearing
                    RjNj_sh+=Rj*Nj;
                    NjRjsqrtqj_sh+=Nj*Rj/sqrt(qj);
                    Nj_sh+=Nj;
                    yesShear=1; }
            }
            //compute some microstructural data
            //bypassing
            fv_bp_temp*=M_PI; // pourquoi enlever 2/3 à aspect ratio pour Didier ???
            
            if(Nj_bp==0) {
                meanR_bp_temp=0.;
                meanT_bp_temp=0.;
                distanceBetweenPPT_temp=1e300; // regarder à quoi ça sert!
                distanceBetweenPPT_bp=1e300;
            }
            else {
                meanR_bp_temp=RjNj_bp/Nj_bp;
                meanT_bp_temp=TjNj_bp/Nj_bp;
                //distanceBetweenPPT-->necessaire si l'on a une loi de Kock Mecking type Aude Simar.
                //distanceBetweenPPT_temp=sqrt(3/4*sqrt(2.0)*RjNj_bp)-M_PI/4*meanR_bp_temp-sqrt(2.0)*meanT_bp_temp; // (regarder à quoi ça sert!)
                distanceBetweenPPT_bp=sqrt(3.0/(4.0*sqrt(2.0)*RjNj_bp))-M_PI/4*meanR_bp_temp-1.5/sqrt(2.0)*meanT_bp_temp;
                // distanceBetweenPPT_bp=sqrt(3.0/(4.0*sqrt(2.0)*RjNj_bp))-M_PI/4*meanR_bp_temp-sqrt(2.0)*meanT_bp_temp; // AB
                F_bp=2*tensionLineConstant*currentShearModulus*burgersNorm*burgersNorm;
            }
            //shearing
            if(Nj_sh==0) {
                meanR_sh_temp=0.;
                meanT_sh_temp=0.;
                distanceBetweenPPT_sh=1e300;
            }
            else {
                //                meanR_sh_temp=RjNj_sh/Nj_sh;
                //                meanT_sh_temp=TjNj_sh/Nj_sh;
                F_sh=shearConstantStrength[i]*currentShearModulus*burgersNorm*sqrt(sqrt(1.5))*NjRjsqrtqj_sh/Nj_sh;
                //distanceBetweenPPT_sh=sqrt(sqrt(1.5)*tensionLine/F_sh/RjNj_sh); // true expression (identical to paper)
                
                // CORRECTED
                distanceBetweenPPT_sh=sqrt(4*tensionLine/(sqrt(3.0)*F_sh))*sqrt(3/(4*sqrt(2.0)*RjNj_sh)); // deleted the second *3 on Feb. 10th 2021 (now in agreement with AB paper and PrecipitateStrenghtening.pdf)
                
                //F_sh=shearConstantStrength[i]*currentShearModulus*burgersNorm*sqrt(sqrt(3.0)/2*sqrt(2.0))*NjsqrtRjTj_sh/Nj_sh;
                //distanceBetweenPPT_sh=sqrt(4*tensionLine/(sqrt(3.0)*F_sh))*sqrt(3/(4*sqrt(2.0)*RjNj_sh));
                
                //F_sh=shearConstantStrength[i]*currentShearModulus*burgersNorm*sqrt(sqrt(3.0)/(sqrt(2.0)))*NjsqrtRjTj_sh/Nj_sh;
                ////  F_sh=1.5*shearConstantStrength[i]*currentShearModulus*burgersNorm*sqrt(sqrt(3.0)/(sqrt(2.0)))*NjsqrtRjTj_sh/Nj_sh; // Fsh avec le coef mutiplicatif pour que ça colle bien
                ////  F_sh=shearConstantStrength[i]*currentShearModulus*burgersNorm*sqrt(sqrt(3.0)/sqrt(2.0))*NjTj_sh/Nj_sh; // Fsh avec la formulation de Oblak 74 Coherency
                
                //distanceBetweenPPT_sh=sqrt(4*tensionLine/(sqrt(3.0)*F_sh))*sqrt(3/(4*sqrt(2.0)*RjNj_sh)*3);
                //// distanceBetweenPPT_sh=sqrt(3.*sqrt(3.)*tensionLine/(8.*sqrt(2.)*F_sh))*1./sqrt(RjNj_sh);
            }
            //compute sigmaBp and sigmaSh for this precipitate (triangular path)
            sigmaBp=taylorFactor/burgersNorm*F_bp/distanceBetweenPPT_bp;
            if (yesShear==1) {
                sigmaSh=taylorFactor*F_sh/burgersNorm/distanceBetweenPPT_sh;
            }
        }
        else {error.Fatal("Just 'triangularPath' is implemented in mechanical model n°1");}
        
        //computation of sigmaPreciI and total "sigmaPrecipitates (that is the quadratic sum of each precipitates contribution)
        sigmaTempI=sqrt(sigmaSh*sigmaSh+sigmaBp*sigmaBp);
        
        
        if(fabs(sigmaSh-sigmaBp)/(sigmaSh+sigmaBp)*2<0.01)
        {
            double ratio=F_sh/F_bp;
            ratio=ratio*2/2;
        }
        //sigmaTempI=pow( pow(sigmaSh,2.) + pow(sigmaBp,2.),1./2.);
        sigmaPreciItemp.push_back(sigmaTempI);
        sigmaPreciTemp=sigmaPreciTemp+sigmaTempI*sigmaTempI;
        
        //update attribut of class for precipitates
        dsigmaPreciI[i]=(sigmaTempI-sigmaPreciI[i])/_dt;
        sigmaPreciI[i]=sigmaTempI;
        sigmaPreciIsh[i]=sigmaSh;
        sigmaPreciIbp[i]=sigmaBp;
        
        //
        dfv_bp[i]=(fv_bp_temp-fv_bp[i])/_dt;
        fv_bp[i]=fv_bp_temp;
        dmeanR_bp[i]=(meanR_bp_temp-meanR_bp[i])/_dt;
        meanR_bp[i]=meanR_bp_temp;
        dmeanT_bp[i]=(meanT_bp_temp-meanT_bp[i])/_dt;
        meanT_bp[i]=meanT_bp_temp;
        dNtot_bp[i]=(Nj_bp-Ntot_bp[i])/_dt;
        Ntot_bp[i]=Nj_bp;
        ddistanceBetweenPPT[i]=(distanceBetweenPPT_temp-distanceBetweenPPT[i])/_dt;
        distanceBetweenPPT[i]=distanceBetweenPPT_temp;
    }
    sigmaPreciTemp=sqrt(sigmaPreciTemp);
    
    //-------------------- Grain contribution ---------------------
    sigmaGrainTemp=K_HP*pow(grainSize,-0.5);
    
    //-------------------- final stress ---------------------
    double sigmaFlowMicroTemp=initialYield+sigmaGrainTemp+sigmaSSTemp+sqrt(sigmaDisloTemp*sigmaDisloTemp+sigmaPreciTemp*sigmaPreciTemp);
    
    
    //#######################################################
    //###        update all global stress variables       ###
    //#######################################################
    dsigmaDislo=(sigmaDisloTemp-sigmaDislo)/_dt;     dsigmaSS=(sigmaSSTemp-sigmaSS)/_dt;
    dsigmaPreci=(sigmaPreciTemp-sigmaPreci)/_dt;     dsigmaFlowMicro=(sigmaFlowMicroTemp-sigmaFlowMicro)/_dt;
    sigmaDislo=sigmaDisloTemp;                       sigmaSS=sigmaSSTemp;
    sigmaPreci=sigmaPreciTemp;                       sigmaFlowMicro=sigmaFlowMicroTemp;
    sigmaGrain=sigmaGrainTemp;
    //#######################################################
}

void Mechanical::ModelFisk(Matrix const& _matrix,vector<Element> const& _Elements,vector<Precipitate> const& _Precipitates,double _currentTime,double _dt)
{
    if(structure!=1) {error.Fatal("In model n°1 just 'cfc' structure is considered");}
    //###################################################################
    //###                      (Fisk's model - 2014)                       ###
    //###################################################################
    
    //------------------- load constant ---------------------
    currentYoung=GetYoung();
    currentPoisson=GetPoisson();
    currentShearModulus=currentYoung/(2*(1+currentPoisson));
    
    //----------- compute SS & dislo contributions  ---------
    double sigmaDisloTemp=ComputeDisloContributionModel1();
    double sigmaSSTemp=ComputeSScontributionModelAlex_sqrt(_Elements);
    
    //-------------- precipitate contribution --------------
    //initialization
    vector<double> sigmaPreciItemp;sigmaPreciItemp.clear();
    //initialization
    double sigmaGrainTemp=0.;
    double sigmaPreciTemp=0.,sigmaBp=0.,sigmaSh=0.,sigmaTempI=0.,shearConstantStrength=0.;
    double Nj=0.,Rj=0.,Tj=0.,meanR=0.,fv=0.,tempAspectRatio=0.,sumNj=0.;
    
    double Nj_bp=0.;
    double fv_bp_temp=0., distanceBetweenPPT_temp=0.,meanR_bp_temp=0.,meanT_bp_temp=0.;
    
    //stress contribution for each precipitates
    for (size_t i=0;i<_Precipitates.size();i++)    {
        //----------------------------------------
        if (_Precipitates[i].GetShapeIndex()!=4) {error.Fatal("Mechanical model n°5 is just implemented for plates");}
        //----------------------------------------
        //read transition radius and compute shearConstantStrength
        meanR=_Precipitates[i].MeanRadius();
        fv=_Precipitates[i].VolumeFraction();
        shearConstantStrength=2*tensionLineConstant*burgersNorm/transitionRadius[i]; // Kc
        Nj=0.,Rj=0.,sumNj=0.;
        
        if (PathStructure[i]==2) //triangularPath
        {
            Nj_bp=0.;sigmaBp=0.;sigmaSh=0.;tempAspectRatio=0.;Tj=0.;
            
            for (size_t j=0;j<_Precipitates[i].GetNumberOfClass();j++)    {
                Nj=_Precipitates[i].GetNumber(j);
                Rj=_Precipitates[i].GetRadius(j);
                tempAspectRatio=_Precipitates[i].AspectRatioFromCylinderFunction(Rj);
                Tj=2*Rj/tempAspectRatio;
                sumNj=sumNj+Nj;
                if (Rj>=transitionRadius[i]) {
                    //bypassing
                    Nj_bp+=Nj;
                    fv_bp_temp+=Rj*Rj*Tj*Nj;
                }
            }
            fv_bp_temp*=M_PI;
            sigmaBp=sqrt(6/M_PI)*tensionLineConstant*taylorFactor*currentShearModulus*burgersNorm*sqrt(fv)/meanR;
            sigmaSh=sqrt(3/(2*M_PI))*shearConstantStrength*taylorFactor*currentShearModulus*sqrt(fv);
            
            //computation of sigmaPreciI and total "sigmaPrecipitates (that is the quadratic sum of each precipitates contribution)
            sigmaTempI=fv_bp_temp/fv*sigmaBp+(1-fv_bp_temp/fv)*sigmaSh;
            sigmaPreciItemp.push_back(sigmaTempI);
            sigmaPreciTemp=sigmaPreciTemp+sigmaTempI*sigmaTempI;
        }
        
        //update attribut of class for precipitates
        dsigmaPreciI[i]=(sigmaTempI-sigmaPreciI[i])/_dt;
        sigmaPreciI[i]=sigmaTempI;
        sigmaPreciIsh[i]=sigmaSh;
        sigmaPreciIbp[i]=sigmaBp;
        
        //
        dfv_bp[i]=(fv_bp_temp-fv_bp[i])/_dt;
        fv_bp[i]=fv_bp_temp;
        dmeanR_bp[i]=(meanR_bp_temp-meanR_bp[i])/_dt;
        meanR_bp[i]=meanR_bp_temp;
        dmeanT_bp[i]=(meanT_bp_temp-meanT_bp[i])/_dt;
        meanT_bp[i]=meanT_bp_temp;
        dNtot_bp[i]=(Nj_bp-Ntot_bp[i])/_dt;
        Ntot_bp[i]=Nj_bp;
        ddistanceBetweenPPT[i]=(distanceBetweenPPT_temp-distanceBetweenPPT[i])/_dt;
        distanceBetweenPPT[i]=distanceBetweenPPT_temp;
    }
    
    sigmaPreciTemp=sqrt(sigmaPreciTemp);
    
    //-------------------- Grain contribution ---------------------
    sigmaGrainTemp=K_HP*pow(grainSize,-0.5);
    
    //-------------------- final stress ---------------------
    double sigmaFlowMicroTemp=initialYield+sigmaGrainTemp+sigmaSSTemp+sqrt(sigmaDisloTemp*sigmaDisloTemp+sigmaPreciTemp*sigmaPreciTemp);
    
    
    //#######################################################
    //###        update all global stress variables       ###
    //#######################################################
    dsigmaDislo=(sigmaDisloTemp-sigmaDislo)/_dt;     dsigmaSS=(sigmaSSTemp-sigmaSS)/_dt;
    dsigmaPreci=(sigmaPreciTemp-sigmaPreci)/_dt;     dsigmaFlowMicro=(sigmaFlowMicroTemp-sigmaFlowMicro)/_dt;
    sigmaDislo=sigmaDisloTemp;                       sigmaSS=sigmaSSTemp;
    sigmaPreci=sigmaPreciTemp;                       sigmaFlowMicro=sigmaFlowMicroTemp;
    sigmaGrain=sigmaGrainTemp;
    //#######################################################
    
}

void Mechanical::ModelAlexSphere(Matrix const& _matrix,vector<Element> const& _Elements,vector<Precipitate> const& _Precipitates,double _currentTime,double _dt)
{
    if(structure!=1) {error.Fatal("In model n°6 just 'cfc' structure is considered");}
    //###################################################################
    //###                      (AlexModel for spheres - 2014)         ###
    //###################################################################
    
    //------------------- load constant ---------------------
    currentYoung=GetYoung();
    currentPoisson=GetPoisson();
    currentShearModulus=currentYoung/(2*(1+currentPoisson));
    //----------- compute SS & dislo contributions  ---------
    double sigmaDisloTemp=ComputeDisloContributionModel1();
    double sigmaSSTemp=ComputeSScontributionModelAlex_sqrt(_Elements);
    
    //-------------- precipitate contribution --------------
    //initialization
    double sigmaGrainTemp=0.;
    double sigmaPreciTemp=0.,sigmaBp=0.,sigmaSh=0.,sigmaTempI=0.,shearConstantStrength=0.;
    double tempAspectRatio=0.,Nj=0.,Rj=0.,Tj=0.;
    
    double TjNj_bp=0.,RjNj_bp=0.,Nj_bp=0.,RjNj_sh=0.,NjsqrtRjTj_sh=0.,Nj_sh=0.;
    double F_bp=0.,F_sh=0.;
    double fv_bp_temp=0., distanceBetweenPPT_temp=0.,meanR_bp_temp=0.,meanT_bp_temp=0.,distanceBetweenPPT_bp=0.,distanceBetweenPPT_sh=0.,meanR_sh_temp=0.,meanT_sh_temp=0.;
    vector<double> sigmaPreciItemp;sigmaPreciItemp.clear();
    int yesShear=0;
    
    //tension line
    double tensionLine=tensionLineConstant*currentShearModulus*burgersNorm*burgersNorm;
    //-------------- initialisation for precipitate constants ---------------
    //stress contribution for each precipitates
    for (size_t i=0;i<_Precipitates.size();i++)    {
        //----------------------------------------
        if (_Precipitates[i].GetShapeIndex()!=1) {error.Fatal("Mechanical model AlexModel for spheres is just implemented for spheres");}
        //----------------------------------------
        yesShear=0;
        //read transition radius and compute shearConstantStrength
        shearConstantStrength=2*tensionLineConstant*burgersNorm/transitionRadius[i];
        // shearConstantStrength=sqrt(_Precipitates[i].AspectRatioFromCylinderFunction(transitionRadius[i]))/transitionRadius[i]*2*tensionLineConstant*burgersNorm*pow(2./3.,1./4.);
        
        if (PathStructure[i]==2) //triangularPath
        {
            sigmaBp=0.,sigmaSh=0.,TjNj_bp=0.,RjNj_bp=0.,Nj=0.,Rj=0.,Tj=0.; RjNj_sh=0.; Nj_sh=0.;
            fv_bp_temp=0.; meanR_bp_temp=0.; meanT_bp_temp=0.; Nj_bp=0.; tempAspectRatio=0.; NjsqrtRjTj_sh=0.;
            
            for (size_t j=0;j<_Precipitates[i].GetNumberOfClass();j++)    {
                Nj=_Precipitates[i].GetNumber(j);
                Rj=_Precipitates[i].GetRadius(j);
                
                
                if (Rj>=transitionRadius[i]) {
                    //bypassing
                    RjNj_bp=RjNj_bp+Rj*Nj;
                    fv_bp_temp+=Rj*Rj*Rj*Nj;
                    Nj_bp+=Nj;
                }
                else {
                    //shearing
                    RjNj_sh=RjNj_sh+Rj*Nj;
                    Nj_sh+=Nj;
                    yesShear=1; }
            }
            //compute some microstructural data
            //bypassing
            fv_bp_temp*=4/3*M_PI; // pourquoi enlever 2/3 à aspect ratio pour Didier ???
            if(Nj_bp==0) {
                meanR_bp_temp=0.;
                meanT_bp_temp=0.;
                distanceBetweenPPT_temp=1e300; // regarder à quoi ça sert!
                distanceBetweenPPT_bp=1e300;
            }
            else {
                meanR_bp_temp=RjNj_bp/Nj_bp;
                
                //distanceBetweenPPT-->necessaire si l'on a une loi de Kock Mecking type Aude Simar.
                distanceBetweenPPT_temp=sqrt(sqrt(3.0)/(4*RjNj_bp))-M_PI/4*meanR_bp_temp; // (regarder à quoi ça sert!)
                distanceBetweenPPT_bp=sqrt(sqrt(3.0)/(4*RjNj_bp))-M_PI/4*meanR_bp_temp;
                F_bp=2*tensionLineConstant*currentShearModulus*burgersNorm*burgersNorm;
            }
            //shearing
            if(Nj_sh==0) {
                meanR_sh_temp=0.;
                meanT_sh_temp=0.;
                distanceBetweenPPT_sh=1e300;
            }
            else {
                meanR_sh_temp=RjNj_sh/Nj_sh;
                
                F_sh=shearConstantStrength*currentShearModulus*burgersNorm*meanR_sh_temp;
                // distanceBetweenPPT_sh=sqrt(4*tensionLine/(sqrt(3.0)*F_sh))*sqrt(3/(4*sqrt(2.0)*RjNj_sh));
                distanceBetweenPPT_sh=sqrt(3.*tensionLine/(8.*F_sh))*1./sqrt(RjNj_sh);
            }
            //compute sigmaBp and sigmaSh for this precipitate (triangular path)
            sigmaBp=taylorFactor/burgersNorm*F_bp/distanceBetweenPPT_bp;
            if (yesShear==1) {
                sigmaSh=taylorFactor/burgersNorm*F_sh/distanceBetweenPPT_sh;
            }
        }
        else {error.Fatal("Just 'triangularPath' is implemented in mechanical model n°1");}
        
        //computation of sigmaPreciI and total "sigmaPrecipitates (that is the quadratic sum of each precipitates contribution)
        //sigmaTempI=sqrt(sigmaSh*sigmaSh+sigmaBp*sigmaBp);
        sigmaTempI=pow( pow(sigmaSh,2.) + pow(sigmaBp,2.),1./2.);
        sigmaPreciItemp.push_back(sigmaTempI);
        sigmaPreciTemp=sigmaPreciTemp+sigmaTempI*sigmaTempI;
        
        //update attribut of class for precipitates
        dsigmaPreciI[i]=(sigmaTempI-sigmaPreciI[i])/_dt;
        sigmaPreciI[i]=sigmaTempI;
        sigmaPreciIsh[i]=sigmaSh;
        sigmaPreciIbp[i]=sigmaBp;
        
        //
        dfv_bp[i]=(fv_bp_temp-fv_bp[i])/_dt;
        fv_bp[i]=fv_bp_temp;
        dmeanR_bp[i]=(meanR_bp_temp-meanR_bp[i])/_dt;
        meanR_bp[i]=meanR_bp_temp;
        dmeanT_bp[i]=(meanT_bp_temp-meanT_bp[i])/_dt;
        meanT_bp[i]=meanT_bp_temp;
        dNtot_bp[i]=(Nj_bp-Ntot_bp[i])/_dt;
        Ntot_bp[i]=Nj_bp;
        ddistanceBetweenPPT[i]=(distanceBetweenPPT_temp-distanceBetweenPPT[i])/_dt;
        distanceBetweenPPT[i]=distanceBetweenPPT_temp;
    }
    sigmaPreciTemp=sqrt(sigmaPreciTemp);
    
    //-------------------- Grain contribution ---------------------
    sigmaGrainTemp=K_HP*pow(grainSize,-0.5);
    
    //-------------------- final stress ---------------------
    double sigmaFlowMicroTemp=initialYield+sigmaGrainTemp+sigmaSSTemp+sqrt(sigmaDisloTemp*sigmaDisloTemp+sigmaPreciTemp*sigmaPreciTemp);
    
    
    //#######################################################
    //###        update all global stress variables       ###
    //#######################################################
    dsigmaDislo=(sigmaDisloTemp-sigmaDislo)/_dt;     dsigmaSS=(sigmaSSTemp-sigmaSS)/_dt;
    dsigmaPreci=(sigmaPreciTemp-sigmaPreci)/_dt;     dsigmaFlowMicro=(sigmaFlowMicroTemp-sigmaFlowMicro)/_dt;
    sigmaDislo=sigmaDisloTemp;                       sigmaSS=sigmaSSTemp;
    sigmaPreci=sigmaPreciTemp;                       sigmaFlowMicro=sigmaFlowMicroTemp;
    sigmaGrain=sigmaGrainTemp;
    //#######################################################
    
}


void Mechanical::ModelOne(Matrix const& _matrix,vector<Element> const& _Elements,vector<Precipitate> const& _Precipitates,double _currentTime,double _dt)
{
    if(structure!=1) {error.Fatal("In model 1 just 'cfc' structure is considered");}
    //###################################################################
    //###                      (didier's model)                       ###
    //###################################################################
    
    //------------------- load constant ---------------------
    currentYoung=GetYoung();
    currentPoisson=GetPoisson();
    currentShearModulus=currentYoung/(2*(1+currentPoisson));
    //----------- compute SS & dislo contributions  ---------
    double sigmaDisloTemp=ComputeDisloContributionModel1();
    double sigmaSSTemp=ComputeSScontributionModel1(_Elements);
    
    //-------------- precipitate contribution --------------
    //initialization
    double sigmaPreciTemp=0.,sigmaBp=0.,sigmaSh=0.,LjNj_bp=0.,LjNj_sh=0.,RjNj=0.,sumNj=0.;
    double aspectRatio=0.,Nj=0.,Rj=0.,Lj=0.,sigmaTempI=0.;//,shearConstantStrength=0.;
    double fv_bp_temp=0., meanR_bp_temp=0., meanL_BP_temp=0., Nj_bp, Nj_sh, distanceBetweenPPT_temp=0.;
    double distancePPTsh_temp=1e300,distancePPTbp_temp=1e300,distancePPTall_temp=1e300;
    
    vector<double> sigmaPreciItemp;sigmaPreciItemp.clear();
    int yesShear=0,yesByPass=0;
    
    //tension line
    double tensionLine=tensionLineConstant*currentShearModulus*burgersNorm*burgersNorm;
    //-------------- initialisation for precipitate constants ---------------
    //stress contribution for each precipitates
    for (size_t i=0;i<_Precipitates.size();i++)    {
        //----------------------------------------
        if((_Precipitates[i].GetShapeIndex()!=2)&&(_Precipitates[i].GetShapeIndex()!=6)) {error.Fatal("Mechanical model 1 is just implemented for 'Rod' and 'RodFuction'");}
        //----------------------------------------
        yesShear=0;yesByPass=0;
        //read transition radius and compute shearConstantStrength
        // If a null value of k is in input, k is calculated via the critical radius
        if (shearConstantStrength[i]==0){
            shearConstantStrength[i]=2*tensionLineConstant*burgersNorm/transitionRadius[i]/sqrt(sqrt(3.0));
        //shearConstantStrength[i]=sqrt(_Precipitates[i].AspectRatioFromCylinderFunction(transitionRadius[i])*sqrt(2.0/3.0))/transitionRadius[i]*2*tensionLineConstant*burgersNorm;
            // shearConstantStrength=2*tensionLineConstant*burgersNorm/transitionRadius[i];
            //shearConstantStrength=2./3.*M_PI*pow(2./3.,1./4.)*0.0286/2.2;
            // shearConstantStrength=0.034; // d'après SUN 93
        }
        //read transition radius and compute shearConstantStrength
        //shearConstantStrength=2*tensionLineConstant*burgersNorm/transitionRadius[i];
        
        if (PathStructure[i]==2) //triangularPath
        {
            if (_Precipitates[i].GetShapeIndex()==2) // rod
            {
                aspectRatio=_Precipitates[i].GetAspectRatio();
            }
            else if (_Precipitates[i].GetShapeIndex()==6) // rodFunction
            {
                aspectRatio=_Precipitates[i].AspectRatioFromRodFunction(_Precipitates[i].MeanRadius());
            }
            else
            {
                error.Fatal("In modelOne; only 'rod' and 'rodFuntion' are implemented"); // error
            }
            
            sigmaBp=0.,sigmaSh=0.,LjNj_bp=0.,LjNj_sh=0.,RjNj=0.,sumNj=0.,Nj=0.,Rj=0.,Lj=0.;
            fv_bp_temp=0.; meanR_bp_temp=0.; meanL_BP_temp=0.; Nj_bp=0.; Nj_sh=0.;
            for (size_t j=0;j<_Precipitates[i].GetNumberOfClass();j++)    {
                Nj=_Precipitates[i].GetNumber(j);
                Rj=_Precipitates[i].GetRadius(j);
                Lj=Rj*aspectRatio;
                if (Rj>=transitionRadius[i]) {
                    //by passing
                    LjNj_bp+=Lj*Nj;
                    fv_bp_temp+=Rj*Rj*Rj*Nj;
                    meanR_bp_temp+=Rj*Nj;
                    meanL_BP_temp+=Lj*Nj;
                    Nj_bp+=Nj;
                    yesByPass=1;
                }
                else {
                    //shearing
                    LjNj_sh=LjNj_sh+Lj*Nj;
                    RjNj=RjNj+Rj*Nj;
                    sumNj=sumNj+Nj;
                    Nj_sh+=Nj;
                    yesShear=1; }
            }
            //compute some microstructural data
            fv_bp_temp*=(aspectRatio-2.0/3.0)*M_PI;
            if(Nj_bp==0) {
                meanR_bp_temp=0.;
                meanL_BP_temp=0.;
                distanceBetweenPPT_temp=1e300;
                distancePPTbp_temp=1e300;
            }
            else {
                meanR_bp_temp=meanR_bp_temp/Nj_bp;
                meanL_BP_temp=meanL_BP_temp/Nj_bp;
                distanceBetweenPPT_temp=sqrt(2/LjNj_bp);
                distancePPTbp_temp=sqrt(2/LjNj_bp);
            }
            if(Nj_sh==0) {
                distancePPTsh_temp=1e300;
            }
            else {
                distancePPTsh_temp=sqrt(2/LjNj_sh);
            }
            //calcul de la distance (geometrique!) totale
            if (yesShear==0) {distancePPTall_temp=distancePPTbp_temp;}
            else if (yesByPass==0) {distancePPTall_temp=distancePPTsh_temp;}
            else {distancePPTall_temp=(distancePPTbp_temp*Nj_bp+distancePPTsh_temp*Nj_sh)/(Nj_sh+Nj_bp);}
            
            //compute sigmaBp and sigmaSh for this precipitate (triangular path)
            sigmaBp=taylorFactor*sqrt(2.0)*tensionLineConstant*currentShearModulus*burgersNorm*sqrt(LjNj_bp);
            if (yesShear==1) {
                sigmaSh=taylorFactor*sqrt((burgersNorm*LjNj_sh)/(2*sqrt(3.0)*tensionLine))*pow(shearConstantStrength[i]*currentShearModulus*RjNj/sumNj,1.5);
                sigmaSh=pow(3,1.0/8.0)*taylorFactor*currentShearModulus*sqrt(LjNj_sh/(2*tensionLineConstant*burgersNorm))*pow(shearConstantStrength[i]*RjNj/Nj_sh,1.5);
            }
        }
        else {error.Fatal("Just 'triangularPath' is implemented in mechanical model 1");}
        
        //computation of sigmaPreciI and total "sigmaPrecipitates (that is the quadratic sum of each precipitates contribution)
        sigmaTempI=sqrt(sigmaSh*sigmaSh+sigmaBp*sigmaBp);
        sigmaPreciItemp.push_back(sigmaTempI);
        sigmaPreciTemp=sigmaPreciTemp+sigmaTempI*sigmaTempI;
        
        //update attribut of class for precipitates
        dsigmaPreciI[i]=(sigmaTempI-sigmaPreciI[i])/_dt;
        sigmaPreciI[i]=sigmaTempI;
        sigmaPreciIsh[i]=sigmaSh;
        sigmaPreciIbp[i]=sigmaBp;
        
        //
        dfv_bp[i]=(fv_bp_temp-fv_bp[i])/_dt;
        fv_bp[i]=fv_bp_temp;
        dmeanR_bp[i]=(meanR_bp_temp-meanR_bp[i])/_dt;
        meanR_bp[i]=meanR_bp_temp;
        dmeanL_bp[i]=(meanL_BP_temp-meanL_bp[i])/_dt;
        meanL_bp[i]=meanL_BP_temp;
        dNtot_bp[i]=(Nj_bp-Ntot_bp[i])/_dt;
        Ntot_bp[i]=Nj_bp;
        //dans mon modele il s'agit de distance entre PPT contournés
        ddistanceBetweenPPT[i]=(distanceBetweenPPT_temp-distanceBetweenPPT[i])/_dt;
        distanceBetweenPPT[i]=distanceBetweenPPT_temp;
        //ici je remet la distance entre PPT contournés mais celle aussi entre les cisaillés
        ddistancePPTsh[i]=(distancePPTsh_temp-distancePPTsh[i])/_dt;
        distancePPTsh[i]=distancePPTsh_temp;
        ddistancePPTbp[i]=(distancePPTbp_temp-distancePPTbp[i])/_dt;
        distancePPTbp[i]=distancePPTbp_temp;
        ddistancePPTall[i]=(distancePPTall_temp-distancePPTall[i])/_dt;
        distancePPTall[i]=distancePPTall_temp;
    }
    sigmaPreciTemp=sqrt(sigmaPreciTemp);
    //-------------------- Hall Petch ---------------------
    double sigmaGrainTemp=K_HP*pow(grainSize,-0.5);
    
    //-------------------- final stress ---------------------
    //double sigmaFlowMicroTemp=initialYield+sigmaGrainTemp+sigmaSSTemp+pow(pow(sigmaDisloTemp,powSum)+pow(sigmaPreciTemp,powSum),1.0/powSum);
    //error.Fatal("Different values given here in ABalan code (see line below)");
    double sigmaFlowMicroTemp=initialYield+sigmaSSTemp+sqrt(sigmaDisloTemp*sigmaDisloTemp+sigmaPreciTemp*sigmaPreciTemp);
    
    //#######################################################
    //###        update all global stress variables       ###
    //#######################################################
    dsigmaGrain=(sigmaGrainTemp-sigmaGrain)/_dt;
    dsigmaDislo=(sigmaDisloTemp-sigmaDislo)/_dt;     dsigmaSS=(sigmaSSTemp-sigmaSS)/_dt;
    dsigmaPreci=(sigmaPreciTemp-sigmaPreci)/_dt;     dsigmaFlowMicro=(sigmaFlowMicroTemp-sigmaFlowMicro)/_dt;
    sigmaDislo=sigmaDisloTemp;                       sigmaSS=sigmaSSTemp;
    sigmaPreci=sigmaPreciTemp;                       sigmaFlowMicro=sigmaFlowMicroTemp;
    sigmaGrain=sigmaGrainTemp;
    //#######################################################
}

void Mechanical::ModelTwo(Matrix const& _matrix,vector<Element> const& _Elements,vector<Precipitate> const& _Precipitates,double _currentTime,double _dt)
{
    if(structure!=1) {error.Fatal("In model n°2 just 'cfc' structure is considered");}
    //###################################################################
    //###            Brechet/Deschamps/Myhr/Grong model's             ###
    //###                   adapted for other path                    ###
    //###                   and full distribution                     ###
    //###################################################################
    //------------------- load constant ---------------------
    currentYoung=GetYoung();
    currentPoisson=GetPoisson();
    currentShearModulus=currentYoung/(2*(1+currentPoisson));
    //----------- compute SS & dislo contributions  ---------
    double sigmaDisloTemp=ComputeDisloContributionModel1();
    double sigmaSSTemp=ComputeSScontributionModel1(_Elements);
    
    //-------------- precipitate contribution --------------
    //initialization
    double sigmaPreciTemp=0.,sumFjNj=0.,sumLjNj=0.,sumNj=0.,aspectRatio=0.,Rj=0.,Nj=0.;
    double sigmaTempI=0.,shearConstantStrength=0.,meanF=0.;
    vector<double> sigmaPreciItemp;sigmaPreciItemp.clear();
    
    //tension line
    double tensionLine=tensionLineConstant*currentShearModulus*burgersNorm*burgersNorm;
    
    //stress contribution for each precipitates
    for (size_t i=0;i<_Precipitates.size();i++)    {
        //----------------------------------------
        if (_Precipitates[i].GetShapeIndex()!=2) {error.Fatal("Mechanical model n°2 is just implemented for rods");}
        //----------------------------------------
        //load all data and initializations
        shearConstantStrength=2*tensionLineConstant*burgersNorm/transitionRadius[i];
        aspectRatio=0.,Nj=0.,Rj=0.,sumNj=0.,sumLjNj=0.,sumFjNj=0.,meanF=0.;
        
        if (PathStructure[i]==2) {aspectRatio=_Precipitates[i].GetAspectRatio();}
        
        //strength associed to each classes
        for (size_t j=0;j<_Precipitates[i].GetNumberOfClass();j++)    {
            Nj=_Precipitates[i].GetNumber(j);
            Rj=_Precipitates[i].GetRadius(j);
            sumNj=sumNj+Nj;
            //it's zero if is sphere
            sumLjNj=sumLjNj+Nj*Rj*aspectRatio;
            //computate mean strength "F" (independant of path type)
            if (Rj>=transitionRadius[i]) {sumFjNj=sumFjNj+Nj*2*tensionLine;}                   //by passing
            else {sumFjNj=sumFjNj+Nj*shearConstantStrength*currentShearModulus*burgersNorm*Rj;}//shearing
        }
        if (sumNj!=0) {meanF=sumFjNj/sumNj;}
        else {meanF=0.;}
        
        sigmaTempI=0.;
        //sigmaTempI computation for each kind of path
        if (PathStructure[i]==2) {
            sigmaTempI=(taylorFactor*pow(meanF,1.5)/burgersNorm)*sqrt(sumLjNj/(2*sqrt(3.0)*tensionLine));        }
        else {error.Fatal("Just 'triangularPath' is implemented in mechanical model n°2");}
        sigmaPreciItemp.push_back(sigmaTempI);
        
        //sigmaPrecipitates is the quadratic sum of each precipitates contribution
        sigmaPreciTemp=sigmaPreciTemp+sigmaTempI*sigmaTempI;
        
        //update attribut of class for precipitates
        dsigmaPreciI[i]=(sigmaTempI-sigmaPreciI[i])/_dt;
        sigmaPreciI[i]=sigmaTempI;
    }
    sigmaPreciTemp=sqrt(sigmaPreciTemp);
    //-------------------- final stress ---------------------
    double sigmaFlowMicroTemp=initialYield+sigmaSSTemp+sqrt(sigmaDisloTemp*sigmaDisloTemp+sigmaPreciTemp*sigmaPreciTemp);
    
    //#######################################################
    //###        update all global stress variables       ###
    //#######################################################
    dsigmaDislo=(sigmaDisloTemp-sigmaDislo)/_dt;     dsigmaSS=(sigmaSSTemp-sigmaSS)/_dt;
    dsigmaPreci=(sigmaPreciTemp-sigmaPreci)/_dt;     dsigmaFlowMicro=(sigmaFlowMicroTemp-sigmaFlowMicro)/_dt;
    sigmaDislo=sigmaDisloTemp;                       sigmaSS=sigmaSSTemp;
    sigmaPreci=sigmaPreciTemp;                       sigmaFlowMicro=sigmaFlowMicroTemp;
    //#######################################################
}

void Mechanical::ModelThree(Matrix const& _matrix,vector<Element> const& _Elements,vector<Precipitate> const& _Precipitates,double _currentTime,double _dt)
{
    if(structure!=1) {error.Fatal("In model n°3 just 'cfc' structure is considered");}
    //###################################################################
    //###            Brechet/Deschamps/Myhr/Grong model's             ###
    //###            without full distribution approach               ###
    //###               (adapted for triangulat path)                 ###
    //###################################################################
    //------------------- load constant ---------------------
    currentYoung=GetYoung();
    currentPoisson=GetPoisson();
    currentShearModulus=currentYoung/(2*(1+currentPoisson));
    //----------- compute SS & dislo contributions  ---------
    double sigmaDisloTemp=ComputeDisloContributionModel1();
    double sigmaSSTemp=ComputeSScontributionModel1(_Elements);
    
    //-------------- precipitate contribution --------------
    //initialization
    double sigmaPreciTemp=0.,sumFjNj=0.,friedelLength=0.,sumNj=0.,Rj=0.,Nj=0.;
    double meanF=0.,meanR=0.,fv=0.,sigmaTempI=0.,shearConstantStrength=0;
    vector<double> sigmaPreciItemp;sigmaPreciItemp.clear();
    
    //tension line
    double tensionLine=tensionLineConstant*currentShearModulus*burgersNorm*burgersNorm;
    
    //stress contribution for each precipitates
    for (size_t i=0;i<_Precipitates.size();i++)    {
        //----------------------------------------
        if (_Precipitates[i].GetShapeIndex()!=2) {error.Fatal("Mechanical model n°3 is just implemented for rods");}
        //----------------------------------------
        //read transition radius and compute shearConstantStrength
        shearConstantStrength=2*tensionLineConstant*burgersNorm/transitionRadius[i];
        Nj=0.,Rj=0.,sumNj=0.,sumFjNj=0.,meanF=0.;
        
        for (size_t j=0;j<_Precipitates[i].GetNumberOfClass();j++)    {
            Nj=_Precipitates[i].GetNumber(j);
            Rj=_Precipitates[i].GetRadius(j);
            sumNj=sumNj+Nj;
            //computate strength "Fi" of each class (independant of path)
            if (Rj>=transitionRadius[i]) {sumFjNj=sumFjNj+Nj*2*tensionLine;}                   //by passing
            else {sumFjNj=sumFjNj+Nj*shearConstantStrength*currentShearModulus*burgersNorm*Rj;}//shearing
        }
        if (sumNj!=0) {meanF=sumFjNj/sumNj;}
        else {meanF=0.;}
        meanR=_Precipitates[i].MeanRadius();
        fv=_Precipitates[i].VolumeFraction();
        
        if (meanR==0 || fv==0) {sigmaTempI=0.;}
        else {
            if (PathStructure[i]==1)      {
                friedelLength=meanR*sqrt((2*tensionLine*2*M_PI)/(meanF*3*fv));}
            else if (PathStructure[i]==2) {
                friedelLength=meanR*sqrt((sqrt(3.0)*tensionLine*2*M_PI)/(meanF*fv));}
            else {error.Fatal("Just 'regularPath' and 'triangularPath' are implemented in mechanical model n°3");}
            sigmaTempI=(taylorFactor*meanF)/(friedelLength*burgersNorm);
        }
        sigmaPreciItemp.push_back(sigmaTempI);
        //sigmaPrecipitates is the quadratic sum of each precipitates contribution
        sigmaPreciTemp=sigmaPreciTemp+sigmaTempI*sigmaTempI;
        
        //update attribut of class for precipitates
        dsigmaPreciI[i]=(sigmaTempI-sigmaPreciI[i])/_dt;
        sigmaPreciI[i]=sigmaTempI;
    }
    sigmaPreciTemp=sqrt(sigmaPreciTemp);
    //-------------------- final stress ---------------------
    double sigmaFlowMicroTemp=initialYield+sigmaSSTemp+sqrt(sigmaDisloTemp*sigmaDisloTemp+sigmaPreciTemp*sigmaPreciTemp);
    
    //#######################################################
    //###        update all global stress variables       ###
    //#######################################################
    dsigmaDislo=(sigmaDisloTemp-sigmaDislo)/_dt;     dsigmaSS=(sigmaSSTemp-sigmaSS)/_dt;
    dsigmaPreci=(sigmaPreciTemp-sigmaPreci)/_dt;     dsigmaFlowMicro=(sigmaFlowMicroTemp-sigmaFlowMicro)/_dt;
    sigmaDislo=sigmaDisloTemp;                       sigmaSS=sigmaSSTemp;
    sigmaPreci=sigmaPreciTemp;                       sigmaFlowMicro=sigmaFlowMicroTemp;
    //#######################################################
}

void Mechanical::ModelFour(Matrix const& _matrix,vector<Element> const& _Elements,vector<Precipitate> const& _Precipitates,double _currentTime,double _dt)
{
    if(structure!=1) {error.Fatal("In model n°4 just 'cfc' structure is considered");}
    //###################################################################
    //###            Brechet/Deschamps mean radius model              ###
    //###               (adapted for triangular path)                 ###
    //###################################################################
    //------------------- load constant ---------------------
    currentYoung=GetYoung();
    currentPoisson=GetPoisson();
    currentShearModulus=currentYoung/(2*(1+currentPoisson));
    //----------- compute SS & dislo contributions  ---------
    double sigmaDisloTemp=ComputeDisloContributionModel1();
    double sigmaSSTemp=ComputeSScontributionModel1(_Elements);
    
    //-------------- precipitate contribution --------------
    //initialization
    double shearConstantStrength=0.,meanR=0.,fv=0.,meanF=0.;
    double friedelLength=0.,sigmaPreciTemp=0.,sigmaTempI=0.;
    vector<double> sigmaPreciItemp;sigmaPreciItemp.clear();
    
    //tension line
    double tensionLine=tensionLineConstant*currentShearModulus*burgersNorm*burgersNorm;
    
    //stress contribution for each precipitates
    for (size_t i=0;i<_Precipitates.size();i++)    {
        //----------------------------------------
        if (_Precipitates[i].GetShapeIndex()!=2) {error.Fatal("Mechanical model n°4 is just implemented for rods");}
        //----------------------------------------
        //read transition radius and compute shearConstantStrength
        shearConstantStrength=2*tensionLineConstant*burgersNorm/transitionRadius[i];
        meanR=_Precipitates[i].MeanRadius();
        fv=_Precipitates[i].VolumeFraction();
        
        //computation of strength
        if (meanR>=transitionRadius[i]) {meanF=2*tensionLine;}                   //by passing
        else {meanF=shearConstantStrength*currentShearModulus*burgersNorm*meanR;}//shearing
        
        if (meanR==0 || fv==0) {sigmaTempI=0.;}
        else {
            if (PathStructure[i]==1)      {
                friedelLength=meanR*sqrt((2*tensionLine*2*M_PI)/(meanF*3*fv));}
            else if (PathStructure[i]==2) {
                friedelLength=meanR*sqrt((sqrt(3.0)*tensionLine*2*M_PI)/(meanF*fv));}
            else {error.Fatal("Just 'regularPath' and 'triangularPath' are implemented in mechanical model n°3");}
            sigmaTempI=(taylorFactor*meanF)/(friedelLength*burgersNorm);
        }
        sigmaPreciItemp.push_back(sigmaTempI);
        //sigmaPrecipitates is the quadratic sum of each precipitates contribution
        sigmaPreciTemp=sigmaPreciTemp+sigmaTempI*sigmaTempI;
        
        //update attribut of class for precipitates
        dsigmaPreciI[i]=(sigmaTempI-sigmaPreciI[i])/_dt;
        sigmaPreciI[i]=sigmaTempI;
    }
    sigmaPreciTemp=sqrt(sigmaPreciTemp);
    //-------------------- final stress ---------------------
    double sigmaFlowMicroTemp=initialYield+sigmaSSTemp+sqrt(sigmaDisloTemp*sigmaDisloTemp+sigmaPreciTemp*sigmaPreciTemp);
    
    //#######################################################
    //###        update all global stress variables       ###
    //#######################################################
    dsigmaDislo=(sigmaDisloTemp-sigmaDislo)/_dt;     dsigmaSS=(sigmaSSTemp-sigmaSS)/_dt;
    dsigmaPreci=(sigmaPreciTemp-sigmaPreci)/_dt;     dsigmaFlowMicro=(sigmaFlowMicroTemp-sigmaFlowMicro)/_dt;
    sigmaDislo=sigmaDisloTemp;                       sigmaSS=sigmaSSTemp;
    sigmaPreci=sigmaPreciTemp;                       sigmaFlowMicro=sigmaFlowMicroTemp;
    //#######################################################
}

void Mechanical::BehaviourCoupledIntegration(double _currentTime,double _dt)
{
    if(mechanicalHardeningCoupling!=true) {error.Fatal("You cannot go in the function 'BehaviourCoupledIntegration' if 'mechanicalHardeningCoupling' is not true");}
    //1) we must load 'nextStrain' for function 'modelImplementationAndComputation'
    //2) we must load 'strainRate' for function 'functionRk45adapt'
    double nextStrain=GetStrain(_currentTime+_dt);
    strainRate=(nextStrain-currentStrain)/_dt;
    // we load the model
    modelImplementationAndComputation(_currentTime,_dt,nextStrain);
}

void Mechanical::BehaviourSemiCoupledIntegration(size_t const& _timeMechaIndex)
{
    if(mechanicalSemiHardeningCoupling!=true) {error.Fatal("You cannot go in the function 'BehaviourSemiCoupledIntegration' if 'mechanicalSemiHardeningCoupling' is not true");}
    //1) we must load 'nextStrain' for function 'modelImplementationAndComputation'
    //2) we must load 'strainRate' for function 'functionRk45adapt'
    double previousStrain=GetStrainWithIndex(_timeMechaIndex-1),       nextStrain=GetStrainWithIndex(_timeMechaIndex);
    double previousTime=GetMechanicalTimeWithIndex(_timeMechaIndex-1), nextTime=GetMechanicalTimeWithIndex(_timeMechaIndex);
    double _dt=nextTime-previousTime;
    strainRate=(nextStrain-previousStrain)/_dt;
    // we load the model
    modelImplementationAndComputation(previousTime,_dt,nextStrain);
}

vector<vector<double> > Mechanical::BehaviourUncoupledIntegration()
{
    //--------if uncoupled no increment of microstructure at the beginning--------
    //-------- of this computation but it can exist during iterations if --------
    //-------- strong coupling between plasticity and precipitation (dynamic preciptiatin)--------
    dsigmaSS=0;dsigmaDislo=0;dsigmaPreci=0;dsigmaFlowMicro=0;
    dsigmaPreciI.clear();   dfv_bp.clear();   dmeanR_bp.clear(); dmeanL_bp.clear(); dNtot_bp.clear();
    for (size_t i=0;i<nbOfPrecipitates;i++) {dsigmaPreciI.push_back(0.);dfv_bp.push_back(0.);dmeanR_bp.push_back(0.);dmeanL_bp.push_back(0.);}
    //--------verification--------
    if(mechanicalHardeningCoupling || mechanicalSemiHardeningCoupling) {
        error.Fatal("You cannot go in 'BehaviourUncoupledIntegration' if you have an hardening coupling option");}
    //--------initialization--------
    vector< vector<double> > matrixOfResults;matrixOfResults.clear();
    vector<double> tempMatrix;               tempMatrix.clear();
    double _dt=0.;
    if (hardeningModelChosen>=1 && hardeningModelChosen<=8) {
        tempMatrix.push_back(TimeMechanic[0]);         tempMatrix.push_back(StainMechanic[0]);
        tempMatrix.push_back(stressMechanic_initial);  tempMatrix.push_back(sigmaFlowMicro);
        tempMatrix.push_back(R);                       tempMatrix.push_back(X); }
    else if(hardeningModelChosen==16)    {
        //generalities
        tempMatrix.push_back(TimeMechanic[0]);         tempMatrix.push_back(StainMechanic[0]);
        tempMatrix.push_back(stressMechanic);          tempMatrix.push_back(epsP);
        tempMatrix.push_back(epsPcum);
        //check errors
        if (DislocationsConstantsLoaded==false || PrecipitateConstantsLoaded==false) {
            error.Fatal("DislocationsConstants and PrecipitateConstants must be loaded for physical hardening model");
        }
        if (nbOfPrecipitates>1) {error.Fatal("Physical model not adapted when number of preciptiates > 1.");}
        //initializations
        Zdislo=initialDislocDensity*burgersNorm;
        tempMatrix.push_back(Zdislo/burgersNorm);
        
        if (grainSize==0) {X_G=0.;}
        else {X_G=(taylorFactor*2*tensionLineConstant*currentShearModulus*burgersNorm*nG)/grainSize;}
        tempMatrix.push_back(nG);
        tempMatrix.push_back(X_G);
        
        //fill isotrope hardening as function of model
        double sigmaDsimple=taylorFactor*dislocStrength*currentShearModulus*burgersNorm*sqrt(Zdislo/burgersNorm);
        if(grainSizeLoaded==false) {error.Fatal("Grainsize must be loaded for model 16");}
        R=sigmaSS+sigmaGrain+pow(pow(sigmaPreci,powSum)+pow(sigmaDsimple,powSum),1/powSum);
        tempMatrix.push_back(R);
        
        //fill other information
        tempMatrix.push_back(fv_bp[0]);
    }
    else if(hardeningModelChosen>=9 && hardeningModelChosen<=15)    {
        //generalities
        tempMatrix.push_back(TimeMechanic[0]);         tempMatrix.push_back(StainMechanic[0]);
        tempMatrix.push_back(stressMechanic);          tempMatrix.push_back(epsP);
        tempMatrix.push_back(epsPcum);
        
        //check errors
        if (DislocationsConstantsLoaded==false || PrecipitateConstantsLoaded==false) {
            error.Fatal("DislocationsConstants and PrecipitateConstants must be loaded for physical hardening model");
        }
        if (nbOfPrecipitates>1) {error.Fatal("Physical model not adapted when number of preciptiates > 1.");}
        
        //initializations
        Zdislo=initialDislocDensity*burgersNorm;
        tempMatrix.push_back(Zdislo/burgersNorm);
        ZdisloPPT=2*M_PI*fabs(n_ppt)*Ntot_bp[0]*meanR_bp[0]*phiPPT[0]*burgersNorm;
        tempMatrix.push_back(ZdisloPPT/burgersNorm);
        
        if (grainSize==0) {X_G=0.;}
        else {X_G=(taylorFactor*2*tensionLineConstant*currentShearModulus*burgersNorm*nG)/grainSize;}
        tempMatrix.push_back(nG);
        tempMatrix.push_back(X_G);
        
        if (meanL_bp[0]==0) {Xppt=0.;}
        else {Xppt=factorKineticContribution[0]*phiPPT[0]*(fv_bp[0]/meanL_bp[0])*n_ppt;}
        
        tempMatrix.push_back(n_ppt);
        tempMatrix.push_back(Xppt);
        
        //fill isotrope hardening as function of model
        double sigmaDsimple=taylorFactor*dislocStrength*currentShearModulus*burgersNorm*sqrt(Zdislo/burgersNorm);
        double sigmaDwithPPT=taylorFactor*dislocStrength*currentShearModulus*burgersNorm*sqrt(Zdislo/burgersNorm+ZdisloPPT/burgersNorm);
        
        if(hardeningModelChosen==9) {R=sigmaDsimple;tempMatrix.push_back(R);}
        else if(hardeningModelChosen==11) {
            if(grainSizeLoaded==false) {error.Fatal("Grainsize must be loaded for model 11,12 and 15");}
            R=sigmaDsimple;tempMatrix.push_back(R);        }
        else if(hardeningModelChosen==10) {R=sigmaSS+sqrt(sigmaPreci*sigmaPreci+sigmaDsimple*sigmaDsimple);tempMatrix.push_back(R);}
        else if(hardeningModelChosen==12) {
            if(grainSizeLoaded==false) {error.Fatal("Grainsize must be loaded for model 11,12 and 15");}
            R=sigmaSS+sqrt(sigmaPreci*sigmaPreci+sigmaDsimple*sigmaDsimple);tempMatrix.push_back(R);}
        else if(hardeningModelChosen==13) {
            R=sigmaDwithPPT;tempMatrix.push_back(R);
        }
        else if(hardeningModelChosen==14) {R=sigmaSS+sqrt(sigmaPreci*sigmaPreci+sigmaDwithPPT*sigmaDwithPPT);tempMatrix.push_back(R);}
        else if(hardeningModelChosen==15) {
            if(grainSizeLoaded==false) {error.Fatal("Grainsize must be loaded for model 11,12 and 15");}
            R=sigmaSS+sigmaGrain+sqrt(sigmaPreci*sigmaPreci+sigmaDwithPPT*sigmaDwithPPT);tempMatrix.push_back(R);}
        else {error.Fatal("Error in physical model initialization, hardeningModelChosen");}
        
        
        tempMatrix.push_back(fv_bp[0]);
        tempMatrix.push_back(meanL_bp[0]);
        tempMatrix.push_back(distanceBetweenPPT[0]);
        
    }
    else {error.Fatal("This hardening model is not implemented in 'BehaviourUncoupledIntegration'");}
    //--------save first step--------
    matrixOfResults.push_back(tempMatrix);
    //--------compute each step times--------
    for (size_t i=1;i<TimeMechanic.size();i++) {
        //--------------
        _dt=TimeMechanic[i]-TimeMechanic[i-1];
        //1) we must load 'nextStrain' for function 'modelImplementationAndComputation'
        //2) we must load 'strainRate' for function 'functionRk45adapt'
        strainRate=(StainMechanic[i]-StainMechanic[i-1])/_dt;
        modelImplementationAndComputation(TimeMechanic[i-1],_dt,StainMechanic[i]);
        //--------------
        if(notVerboseBool==false) {ostringstream timeMecaSTR;timeMecaSTR << TimeMechanic[i];cout << "Mechanical computation " << timeMecaSTR.str() << endl;}
        //--------------
        if (hardeningModelChosen>=1 && hardeningModelChosen<=8) {
            tempMatrix.clear();
            tempMatrix.push_back(TimeMechanic[i]); tempMatrix.push_back(StainMechanic[i]);
            tempMatrix.push_back(stressMechanic);  tempMatrix.push_back(sigmaFlowMicro);
            tempMatrix.push_back(R);               tempMatrix.push_back(X);
            matrixOfResults.push_back(tempMatrix);
        }
        else if(hardeningModelChosen>=9 && hardeningModelChosen<=15) {
            tempMatrix.clear();
            tempMatrix.push_back(TimeMechanic[i]);         tempMatrix.push_back(StainMechanic[i]);
            tempMatrix.push_back(stressMechanic);          tempMatrix.push_back(epsP);
            tempMatrix.push_back(epsPcum);                 tempMatrix.push_back(Zdislo/burgersNorm);
            tempMatrix.push_back(ZdisloPPT/burgersNorm);   tempMatrix.push_back(nG);
            tempMatrix.push_back(X_G);                     tempMatrix.push_back(n_ppt);
            tempMatrix.push_back(Xppt);                    tempMatrix.push_back(R);
            tempMatrix.push_back(fv_bp[0]);                tempMatrix.push_back(meanL_bp[0]);
            tempMatrix.push_back(distanceBetweenPPT[0]);
            matrixOfResults.push_back(tempMatrix);
        }
        else if(hardeningModelChosen==16) {
            tempMatrix.clear();
            tempMatrix.push_back(TimeMechanic[i]);         tempMatrix.push_back(StainMechanic[i]);
            tempMatrix.push_back(stressMechanic);          tempMatrix.push_back(epsP);
            tempMatrix.push_back(epsPcum);                 tempMatrix.push_back(Zdislo/burgersNorm);
            tempMatrix.push_back(nG);                      tempMatrix.push_back(X_G);
            tempMatrix.push_back(R);                       tempMatrix.push_back(fv_bp[0]);
            matrixOfResults.push_back(tempMatrix);
        }
        else {error.Fatal("Error in hardening choice");}
    }
    return matrixOfResults;
}

void Mechanical::modelImplementationAndComputation(double const& timeBeginComputation,double const& _dt,double const& _nextStrain)
{
    if (hardeningModelChosen>=1 && hardeningModelChosen<=16) {
        
        elastoPlasticSolving(timeBeginComputation,_dt,_nextStrain);
    }
    else {error.Fatal("This hardening mode lis not implemented in 'modelImplementationAndComputation'");}
    
}

void Mechanical::elastoPlasticSolving(double const& timeBeginComputation,double const& _dt,double const& _nextStrain)
{
    //initialisation of local variables
    double sigma_trial=0.,psi_trial=0.,f_trial=0.,E=currentYoung;
    size_t nbTtimes;
    vector<double> timeINI_END,CI; timeINI_END.clear();CI.clear();
    vector<vector<double> > timesAndResults; timesAndResults.clear();
    
    //SOLVE PROBLEM
    sigma_trial=E*(_nextStrain-epsP);
    if (hardeningModelChosen>=1 && hardeningModelChosen<=8) {
        psi_trial=sigma_trial-X;
        f_trial=fabs(psi_trial)-(sigmaFlowMicro+R); //sigmaFlowMicro
    }
    else if(hardeningModelChosen>=9 && hardeningModelChosen<=15) {
        psi_trial=sigma_trial-X_G-Xppt;
        f_trial=fabs(psi_trial)-(initialYield+R);
        
        if(activedMicrostructuralModel!=1) {error.Fatal("If 'activedMicrostructuralModel' is not one the physical hardening 9-15 are not usable");}
        
    }
    else if(hardeningModelChosen==16) {
        psi_trial=sigma_trial-X_G;
        f_trial=fabs(psi_trial)-(initialYield+R);
        
        if(activedMicrostructuralModel!=1) {error.Fatal("If 'activedMicrostructuralModel' is not one the physical hardening 16 is not usable");}
        
    }
    else {error.Fatal("in elastoPlasticSolving problem in hardenng model choice");}
    if (f_trial<=0) {
        stressMechanic=sigma_trial;
    }
    else {
        //times for resolution
        timeINI_END.push_back(timeBeginComputation);          timeINI_END.push_back(timeBeginComputation+_dt);
        //intial conditions (number is model dependant)
        //############### one isotrop variable ######################
        if (hardeningModelChosen==1 || hardeningModelChosen==4) {
            CI.push_back(epsP);CI.push_back(epsPcum);CI.push_back(stressMechanic);CI.push_back(R);
            timesAndResults=rk45adapt(_dt,timeINI_END,CI);
            nbTtimes=timesAndResults.size();
            epsP=timesAndResults[nbTtimes-1][1];           epsPcum=timesAndResults[nbTtimes-1][2];
            stressMechanic=timesAndResults[nbTtimes-1][3]; R=timesAndResults[nbTtimes-1][4];
            X=0;    }
        //############### one kinematic variable ######################
        else if (hardeningModelChosen==2 || hardeningModelChosen==5 || hardeningModelChosen==6) {
            CI.push_back(epsP);CI.push_back(epsPcum);CI.push_back(stressMechanic);CI.push_back(X);
            timesAndResults=rk45adapt(_dt,timeINI_END,CI);
            nbTtimes=timesAndResults.size();
            epsP=timesAndResults[nbTtimes-1][1];           epsPcum=timesAndResults[nbTtimes-1][2];
            stressMechanic=timesAndResults[nbTtimes-1][3]; X=timesAndResults[nbTtimes-1][4];
            R=0;   }
        //############### one isotrop & one kinematic variable ######################
        else if (hardeningModelChosen==3 || hardeningModelChosen==7 || hardeningModelChosen==8 ) {
            CI.push_back(epsP);CI.push_back(epsPcum);CI.push_back(stressMechanic);CI.push_back(R);CI.push_back(X);
            timesAndResults=rk45adapt(_dt,timeINI_END,CI);
            nbTtimes=timesAndResults.size();
            epsP=timesAndResults[nbTtimes-1][1];           epsPcum=timesAndResults[nbTtimes-1][2];
            stressMechanic=timesAndResults[nbTtimes-1][3]; R=timesAndResults[nbTtimes-1][4];
            X=timesAndResults[nbTtimes-1][5];        }
        //############### one physical isotrop ######################
        else if (hardeningModelChosen==9 || hardeningModelChosen==10 ) {
            CI.push_back(epsP);CI.push_back(epsPcum);CI.push_back(stressMechanic);CI.push_back(R);CI.push_back(Zdislo);
            timesAndResults=rk45adapt(_dt,timeINI_END,CI);
            nbTtimes=timesAndResults.size();
            epsP=timesAndResults[nbTtimes-1][1];           epsPcum=timesAndResults[nbTtimes-1][2];
            stressMechanic=timesAndResults[nbTtimes-1][3]; R=timesAndResults[nbTtimes-1][4];
            Zdislo=timesAndResults[nbTtimes-1][5];        }
        //############### one physical isotrop/kinetic grain ######################
        else if (hardeningModelChosen==11 || hardeningModelChosen==12 ) {
            CI.push_back(epsP);   CI.push_back(epsPcum);CI.push_back(stressMechanic);CI.push_back(R);
            CI.push_back(Zdislo); CI.push_back(nG);    CI.push_back(X_G);
            timesAndResults=rk45adapt(_dt,timeINI_END,CI);
            nbTtimes=timesAndResults.size();
            epsP=timesAndResults[nbTtimes-1][1];           epsPcum=timesAndResults[nbTtimes-1][2];
            stressMechanic=timesAndResults[nbTtimes-1][3]; R=timesAndResults[nbTtimes-1][4];
            Zdislo=timesAndResults[nbTtimes-1][5];         nG=timesAndResults[nbTtimes-1][6];
            X_G=timesAndResults[nbTtimes-1][7];}
        //############### one physical isotrop/kinetic PPT ######################
        else if (hardeningModelChosen==13 || hardeningModelChosen==14 ) {
            CI.push_back(epsP);   CI.push_back(epsPcum); CI.push_back(stressMechanic); CI.push_back(R);
            CI.push_back(Zdislo); CI.push_back(n_ppt);   CI.push_back(Xppt);
            timesAndResults=rk45adapt(_dt,timeINI_END,CI);
            nbTtimes=timesAndResults.size();
            epsP=timesAndResults[nbTtimes-1][1];           epsPcum=timesAndResults[nbTtimes-1][2];
            stressMechanic=timesAndResults[nbTtimes-1][3]; R=timesAndResults[nbTtimes-1][4];
            Zdislo=timesAndResults[nbTtimes-1][5];         n_ppt=timesAndResults[nbTtimes-1][6];
            Xppt=timesAndResults[nbTtimes-1][7];           ZdisloPPT=2*M_PI*fabs(n_ppt)*phiPPT[0]*Ntot_bp[0]*meanR_bp[0]*burgersNorm;}
        //############### one physical isotrop and two kinetic grain+PPT ######################
        else if (hardeningModelChosen==15 ) {
            CI.push_back(epsP);   CI.push_back(epsPcum); CI.push_back(stressMechanic); CI.push_back(R);
            CI.push_back(Zdislo); CI.push_back(n_ppt);   CI.push_back(Xppt);           CI.push_back(nG);
            CI.push_back(X_G);
            timesAndResults=rk45adapt(_dt,timeINI_END,CI);
            nbTtimes=timesAndResults.size();
            epsP=timesAndResults[nbTtimes-1][1];           epsPcum=timesAndResults[nbTtimes-1][2];
            stressMechanic=timesAndResults[nbTtimes-1][3]; R=timesAndResults[nbTtimes-1][4];
            Zdislo=timesAndResults[nbTtimes-1][5];         n_ppt=timesAndResults[nbTtimes-1][6];
            Xppt=timesAndResults[nbTtimes-1][7];           ZdisloPPT=2*M_PI*fabs(n_ppt)*phiPPT[0]*Ntot_bp[0]*meanR_bp[0]*burgersNorm;
            nG=timesAndResults[nbTtimes-1][8];             X_G=timesAndResults[nbTtimes-1][9];
        }
        //############### one physical isotrop and one kinetic grain + slip irreversibility ######################
        else if (hardeningModelChosen==16 ) {
            CI.push_back(epsP);   CI.push_back(epsPcum); CI.push_back(stressMechanic); CI.push_back(R);
            CI.push_back(Zdislo); CI.push_back(nG);      CI.push_back(X_G);
            timesAndResults=rk45adapt(_dt,timeINI_END,CI);
            nbTtimes=timesAndResults.size();
            epsP=timesAndResults[nbTtimes-1][1];           epsPcum=timesAndResults[nbTtimes-1][2];
            stressMechanic=timesAndResults[nbTtimes-1][3]; R=timesAndResults[nbTtimes-1][4];
            Zdislo=timesAndResults[nbTtimes-1][5];
            nG=timesAndResults[nbTtimes-1][6];             X_G=timesAndResults[nbTtimes-1][7];
        }
        else {error.Fatal("This hardening model is not implemented in 'elastoPlasticSolving'");}
    }
    currentStrain=_nextStrain;
}

vector<double> Mechanical::functionRk45adapt(double const& t_k_part,vector<double> const& ykWithoutCoeff,vector<double> const& addPartY)
{
    //########## GENERAL INITIALIZATIONS FOR ALL MODEL ############
    if (hardeningComputation!=true) {error.Fatal("The hardening model can't be called if 'hardeningComputation' is false");}
    double signPsi=0.,dotLambda=0.,E=0.;
    double Az=0.,Bz=0.,sigmaDz=0.,Cz=0.,Hz=0.,T=0.,F=0.,G=0.,J=0.,Rz=0.,I=0.,O=0.,K=0.,N=0.,A=0.,C=0.;
    double signNppt=0.,densiteDisloPpt=0.;
    double omega=1.0;
    E=GetYoung();
    vector<double> f_k,yk;
    size_t nbOfEquations=ykWithoutCoeff.size();
    for (size_t i=0;i<nbOfEquations;i++) {f_k.push_back(0.0);yk.push_back(0);yk[i]=ykWithoutCoeff[i]+addPartY[i];}
    
    //################ isotropLinearHardening 1D ######################
    if (hardeningModelChosen==1) {//legend-->index0=defP index1=p index2=sigma index3=R
        //sign and dotLambda computation
        if (yk[2]>0) {signPsi=1;}else if (yk[2]<0) {signPsi=-1;}else {signPsi=0.;}
        dotLambda=((E/(E+K_iso))*strainRate*signPsi);
        //differential system
        f_k[0]=dotLambda*signPsi;                  f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi);   f_k[3]=K_iso*dotLambda; }
    //############### kinematicLinearHardening 1D ######################
    else if (hardeningModelChosen==2) {//legend-->index0=defP index1=p index2=sigma index3=X
        //sign and dotLambda computation
        if (yk[2]-yk[3]>0) {signPsi=1;}else if (yk[2]-yk[3]<0) {signPsi=-1;}else {signPsi=0.;}
        dotLambda=((E/(E+K_kin))*strainRate*signPsi);
        //differential system
        f_k[0]=dotLambda*signPsi;                f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi); f_k[3]=K_kin*dotLambda*signPsi; }
    //############### mixteLinearHardening 1D ######################
    else if (hardeningModelChosen==3) {//legend-->index0=defP index1=p index2=sigma index3=R index4=X
        //sign and dotLambda computation
        if (yk[2]-yk[4]>0) {signPsi=1;}else if (yk[2]-yk[4]<0) {signPsi=-1;}else {signPsi=0.;}
        dotLambda=((E/(E+K_iso+K_kin))*strainRate*signPsi);
        //differential system
        f_k[0]=dotLambda*signPsi;                f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi); f_k[3]=K_iso*dotLambda;
        f_k[4]=K_kin*dotLambda*signPsi;  }
    //############### isotropVoce 1D ######################
    else if (hardeningModelChosen==4) {//legend-->index0=defP index1=p index2=sigma index3=R
        //sign and dotLambda computation
        if (yk[2]>0) {signPsi=1;}else if (yk[2]<0) {signPsi=-1;}else {signPsi=0.;}
        dotLambda=(E*strainRate*signPsi)/(E+b_iso*(Rinf_iso-yk[3]));
        //differential system
        f_k[0]=dotLambda*signPsi;                f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi); f_k[3]=b_iso*(Rinf_iso-yk[3])*dotLambda; }
    //############### kinematicAmstrongFred 1D ######################
    else if (hardeningModelChosen==5) {//legend-->index0=defP index1=p index2=sigma index3=X
        //sign and dotLambda computation
        if (yk[2]-yk[3]>0) {signPsi=1;}else if (yk[2]-yk[3]<0) {signPsi=-1;}else {signPsi=0.;}
        dotLambda=(E*strainRate*signPsi)/(E+c_kin-gamma_kin*yk[3]*signPsi);
        //differential system
        f_k[0]=dotLambda*signPsi;                f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi); f_k[3]=c_kin*dotLambda*signPsi-gamma_kin*dotLambda*yk[3]; }
    //######## kinematicAmstrongFredWithGammaEvolution 1D ###########
    else if (hardeningModelChosen==6) {//legend-->index0=defP index1=p index2=sigma index3=X
        //sign and dotLambda computation
        if (yk[2]-yk[3]>0) {signPsi=1;}else if (yk[2]-yk[3]<0) {signPsi=-1;}else {signPsi=0.;}
        double Gamma=gammaInf_kin+(gamma0_kin-gammaInf_kin)*exp(-gammaK_kin*yk[1]);
        dotLambda=(E*strainRate*signPsi)/(E+c_kin-Gamma*yk[3]*signPsi);
        //differential system
        f_k[0]=dotLambda*signPsi;                f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi); f_k[3]=c_kin*dotLambda*signPsi-Gamma*dotLambda*yk[3]; }
    //################ mixteVoceAmstrongFred 1D ######################
    else if (hardeningModelChosen==7) {//legend-->index0=defP index1=p index2=sigma index3=R index4=X
        //sign and dotLambda computation
        if (yk[2]-yk[4]>0) {signPsi=1;}else if (yk[2]-yk[4]<0) {signPsi=-1;}else {signPsi=0.;}
        dotLambda=(E*strainRate*signPsi)/(E+b_iso*(Rinf_iso-yk[3])+c_kin-gamma_kin*yk[4]*signPsi);
        //differential system
        f_k[0]=dotLambda*signPsi;                f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi); f_k[3]=b_iso*(Rinf_iso-yk[3])*dotLambda;
        f_k[4]=c_kin*dotLambda*signPsi-gamma_kin*dotLambda*yk[4];  }
    //################ mixteVoceAmstrongFredWithGammaEvolution 1D ######################
    else if (hardeningModelChosen==8) {//legend-->index0=defP index1=p index2=sigma index3=R index4=X
        //sign and dotLambda computation
        if (yk[2]-yk[4]>0) {signPsi=1;}else if (yk[2]-yk[4]<0) {signPsi=-1;}else {signPsi=0.;}
        double Gamma=gammaInf_kin+(gamma0_kin-gammaInf_kin)*exp(-gammaK_kin*yk[1]);
        dotLambda=(E*strainRate*signPsi)/(E+b_iso*(Rinf_iso-yk[3])+c_kin-Gamma*yk[4]*signPsi);
        //differential system
        f_k[0]=dotLambda*signPsi;                f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi); f_k[3]=b_iso*(Rinf_iso-yk[3])*dotLambda;
        f_k[4]=c_kin*dotLambda*signPsi-Gamma*dotLambda*yk[4];  }
    //################ physical one isotrope hardening without metallurgical yield ######################
    else if (hardeningModelChosen==9) {//legend-->index0=epsP index1=epsPcum index2=stressMechanic index3=R index4=Zdislo
        //sign computation
        if (yk[2]>0) {signPsi=1;}else if (yk[2]<0) {signPsi=-1;}else {signPsi=0.;}
        //intermediate constantes
        Az=taylorFactor*burgersNorm*(k1*sqrt(yk[4]/burgersNorm)-k2*(yk[4]/burgersNorm));
        Bz=0.5*taylorFactor*taylorFactor*dislocStrength*currentShearModulus*burgersNorm*(k1-k2*sqrt(yk[4]/burgersNorm));
        //dotLambda computation
        dotLambda=(E*strainRate*signPsi)/(E+Bz);
        //differential system
        f_k[0]=dotLambda*signPsi;                f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi); f_k[3]=dotLambda*Bz;
        f_k[4]=dotLambda*Az;
    }
    //################ physical one isotrope hardening with metallurgical yield ######################
    else if (hardeningModelChosen==10) {//legend-->index0=epsP index1=epsPcum index2=stressMechanic index3=R index4=Zdislo
        //sign computation
        if (yk[2]>0) {signPsi=1;}else if (yk[2]<0) {signPsi=-1;}else {signPsi=0.;}
        //intermediate constantes
        Az=taylorFactor*burgersNorm*(k1*sqrt(yk[4]/burgersNorm)-k2*(yk[4]/burgersNorm));
        Bz=0.5*taylorFactor*taylorFactor*dislocStrength*currentShearModulus*burgersNorm*(k1-k2*sqrt(yk[4]/burgersNorm));
        sigmaDz=taylorFactor*dislocStrength*currentShearModulus*burgersNorm*sqrt(yk[4]/burgersNorm);
        //dotLambda computation
        dotLambda=(E*strainRate*signPsi-dsigmaSS-(sigmaPreci*dsigmaPreci)/sqrt(sigmaPreci*sigmaPreci+sigmaDz*sigmaDz)) \
        /(E+Bz*sigmaDz/sqrt(sigmaPreci*sigmaPreci+sigmaDz*sigmaDz));
        //differential system
        f_k[0]=dotLambda*signPsi;                f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi);
        f_k[3]=dsigmaSS+(1/sqrt(sigmaPreci*sigmaPreci+sigmaDz*sigmaDz))*(sigmaPreci*dsigmaPreci+sigmaDz*dotLambda*Bz);
        f_k[4]=dotLambda*Az;
    }
    //################ physical one isotrope hardening one grainKinematic without metallurgical yield ######################
    else if (hardeningModelChosen==11) {
        //legend-->index0=epsP index1=epsPcum index2=stressMechanic index3=R index4=Zdislo index5=nG index6=X_G
        //sign computation
        if (yk[2]-yk[6]>0) {signPsi=1;}else if (yk[2]-yk[6]<0) {signPsi=-1;}else {signPsi=0.;}
        //intermediate constantes
        if(nG_star==0 || grainSize==0) {error.Fatal("If 'nG_star=0' or 'grainSize=0' model 11 have singularities");}
        Cz=taylorFactor*burgersNorm*(k1*sqrt(yk[4]/burgersNorm)-k2*(yk[4]/burgersNorm)+(k3/burgersNorm/grainSize)*(1-fabs(yk[5]/nG_star)));
        Hz=0.5*taylorFactor*taylorFactor*dislocStrength*currentShearModulus*burgersNorm*(k1-k2*sqrt(yk[4]/burgersNorm)+\
                                                                                         (k3/burgersNorm/grainSize/sqrt(yk[4]/burgersNorm))*(1-fabs(yk[5]/nG_star)));
        T=(taylorFactor*lambdaG/burgersNorm)*(signPsi-yk[5]/nG_star);
        F=-taylorFactor*2*tensionLineConstant*currentShearModulus*burgersNorm*yk[5]*dgrainsize/grainSize/grainSize;
        G=taylorFactor*2*tensionLineConstant*currentShearModulus*burgersNorm/grainSize;
        //dotLambda computation
        dotLambda=(E*strainRate*signPsi-F*signPsi) \
        /(E+Hz+G*T*signPsi);
        //differential system
        f_k[0]=dotLambda*signPsi;                f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi); f_k[3]=dotLambda*Hz;
        f_k[4]=dotLambda*Cz;                     f_k[5]=dotLambda*T;
        f_k[6]=F+dotLambda*G*T;
    }
    //################ physical one isotrope hardening one grainKinematic with metallurgical yield ######################
    else if (hardeningModelChosen==12) {
        //legend-->index0=epsP index1=epsPcum index2=stressMechanic index3=R index4=Zdislo index5=nG index6=X_G
        //sign computation
        if (yk[2]-yk[6]>0) {signPsi=1;}else if (yk[2]-yk[6]<0) {signPsi=-1;}else {signPsi=0.;}
        //intermediate constantes
        if(nG_star==0 || grainSize==0) {error.Fatal("If 'nG_star=0' or 'grainSize=0' model 12 have singularities");}
        Cz=taylorFactor*burgersNorm*(k1*sqrt(yk[4]/burgersNorm)-k2*(yk[4]/burgersNorm)+(k3/burgersNorm/grainSize)*(1-fabs(yk[5]/nG_star)));
        Hz=0.5*taylorFactor*taylorFactor*dislocStrength*currentShearModulus*burgersNorm*(k1-k2*sqrt(yk[4]/burgersNorm)+\
                                                                                         (k3/burgersNorm/grainSize/sqrt(yk[4]/burgersNorm))*(1-fabs(yk[5]/nG_star)));
        T=(taylorFactor*lambdaG/burgersNorm)*(signPsi-yk[5]/nG_star);
        F=-taylorFactor*2*tensionLineConstant*currentShearModulus*burgersNorm*yk[5]*dgrainsize/grainSize/grainSize;
        G=taylorFactor*2*tensionLineConstant*currentShearModulus*burgersNorm/grainSize;
        sigmaDz=taylorFactor*dislocStrength*currentShearModulus*burgersNorm*sqrt(yk[4]/burgersNorm);
        //dotLambda computation
        dotLambda=(E*strainRate*signPsi-F*signPsi-dsigmaSS-(sigmaPreci*dsigmaPreci)/sqrt(sigmaPreci*sigmaPreci+sigmaDz*sigmaDz)) \
        /(E+(sigmaDz*Hz)/sqrt(sigmaPreci*sigmaPreci+sigmaDz*sigmaDz)+G*T*signPsi);
        //differential system
        f_k[0]=dotLambda*signPsi;                f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi);
        f_k[3]=dsigmaSS+(1/sqrt(sigmaPreci*sigmaPreci+sigmaDz*sigmaDz))*(sigmaPreci*dsigmaPreci+sigmaDz*dotLambda*Hz);
        f_k[4]=dotLambda*Cz;                     f_k[5]=dotLambda*T;
        f_k[6]=F+dotLambda*G*T;
    }
    //################ physical one isotrope hardening one pptKinematic without metallurgical yield ######################
    else if (hardeningModelChosen==13) {
        //legend-->index0=epsP index1=epsPcum index2=stressMechanic index3=R index4=Zdislo index5=n_ppt index6=Xppt index7=ZdisloPPT
        //sign computation
        if (yk[2]-yk[6]>0) {signPsi=1;}else if (yk[2]-yk[6]<0) {signPsi=-1;}else {signPsi=0.;}
        if (yk[5]>0) {signNppt=1;}else if (yk[5]<0) {signNppt=-1;}else {signNppt=0.;}
        //k2 modification if precipitation
        if(disableK2modif) {k2=k2_0;}
        else {k2=k2_0*exp(-phiPPT[0]/distanceBetweenPPT[0]/sqrt(yk[4]/burgersNorm))+k2_P*(1-exp(-phiPPT[0]/distanceBetweenPPT[0]/sqrt(yk[4]/burgersNorm)));}
        //intermediate constantes
        if(nPPT_star[0]==0) {error.Fatal("If 'nPPT_star=0' model 13 have singularities");}
        Az=taylorFactor*burgersNorm*(k1*sqrt(yk[4]/burgersNorm)-k2*(yk[4]/burgersNorm));
        A=taylorFactor*(k1*sqrt(yk[4]/burgersNorm)-k2*(yk[4]/burgersNorm));
        Bz=0.5*taylorFactor*taylorFactor*dislocStrength*currentShearModulus*burgersNorm*(k1-k2*sqrt(yk[4]/burgersNorm));
        I=factorKineticContribution[0]*phiPPT[0];
        J=(taylorFactor/burgersNorm/sqrt(3.0))*(signPsi-yk[5]/nPPT_star[0]);
        
        K=2*M_PI*phiPPT[0]*fabs(yk[5])*(dNtot_bp[0]*meanR_bp[0]+Ntot_bp[0]*dmeanR_bp[0]);
        N=2*M_PI*phiPPT[0]*signNppt*Ntot_bp[0]*meanR_bp[0];
        densiteDisloPpt=2*M_PI*fabs(yk[5])*phiPPT[0]*Ntot_bp[0]*meanR_bp[0];
        
        if(disableRhoPPTcouplingBool)  {
            K=0;
            N=0;
            densiteDisloPpt=0;
        }
        
        Rz=0.5*taylorFactor*dislocStrength*currentShearModulus*burgersNorm/sqrt(yk[4]/burgersNorm+densiteDisloPpt);
        if(meanL_bp[0]==0) {O=0.;}
        else {O=(dfv_bp[0]*meanL_bp[0]-fv_bp[0]*dmeanL_bp[0])*yk[5]/meanL_bp[0]/meanL_bp[0];}
        //dotLambda computation
        dotLambda=(E*strainRate*signPsi-K*Rz-signPsi*I*O) \
        /(E+Rz*(A+N*J*meanL_bp[0])+signPsi*I*J*fv_bp[0]);
        //differential system
        f_k[0]=dotLambda*signPsi;                       f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi);        f_k[3]=dotLambda*Rz*(A+N*J*meanL_bp[0])+K*Rz;
        f_k[4]=dotLambda*Az;                            f_k[5]=dotLambda*J*meanL_bp[0];
        f_k[6]=I*O+I*(fv_bp[0])*J*dotLambda;
    }
    //################ physical one isotrope hardening one pptKinematic with metallurgical yield ######################
    else if (hardeningModelChosen==14) {
        //legend-->index0=epsP index1=epsPcum index2=stressMechanic index3=R index4=Zdislo index5=n_ppt index6=Xppt index7=ZdisloPPT
        //sign computation
        if (yk[2]-yk[6]>0) {signPsi=1;}else if (yk[2]-yk[6]<0) {signPsi=-1;}else {signPsi=0.;}
        if (yk[5]>0) {signNppt=1;}else if (yk[5]<0) {signNppt=-1;}else {signNppt=0.;}
        
        //k2 modification if precipitation
        if(disableK2modif) {k2=k2_0;}
        else {k2=k2_0*exp(-phiPPT[0]/distanceBetweenPPT[0]/sqrt(yk[4]/burgersNorm))+k2_P*(1-exp(-phiPPT[0]/distanceBetweenPPT[0]/sqrt(yk[4]/burgersNorm)));}
        
        //intermediate constantes
        if(nPPT_star[0]==0) {error.Fatal("If 'nPPT_star=0' model 14 have singularities");}
        Az=taylorFactor*burgersNorm*(k1*sqrt(yk[4]/burgersNorm)-k2*(yk[4]/burgersNorm));
        A=taylorFactor*(k1*sqrt(yk[4]/burgersNorm)-k2*(yk[4]/burgersNorm));
        J=taylorFactor*(signPsi-yk[5]/nPPT_star[0])/burgersNorm/sqrt(3.0);
        
        K=2*M_PI*phiPPT[0]*fabs(yk[5])*(dNtot_bp[0]*meanR_bp[0]+Ntot_bp[0]*dmeanR_bp[0]);
        N=2*M_PI*phiPPT[0]*signNppt*Ntot_bp[0]*meanR_bp[0];
        densiteDisloPpt=2*M_PI*fabs(yk[5])*phiPPT[0]*Ntot_bp[0]*meanR_bp[0];
        
        if(disableRhoPPTcouplingBool)  {
            K=0;
            N=0;
            densiteDisloPpt=0;
        }
        
        if(meanL_bp[0]==0) {
            O=0.;}
        else {
            O=(dfv_bp[0]*meanL_bp[0]-fv_bp[0]*dmeanL_bp[0])*yk[5]/meanL_bp[0]/meanL_bp[0];
        }
        Rz=0.5*taylorFactor*dislocStrength*currentShearModulus*burgersNorm/sqrt(yk[4]/burgersNorm+densiteDisloPpt);
        I=factorKineticContribution[0]*phiPPT[0];
        sigmaDz=taylorFactor*dislocStrength*currentShearModulus*burgersNorm*sqrt(yk[4]/burgersNorm+densiteDisloPpt);
        //dotLambda computation
        dotLambda=(E*strainRate*signPsi-dsigmaSS-(1/sqrt(sigmaPreci*sigmaPreci+sigmaDz*sigmaDz))*(sigmaPreci*dsigmaPreci+sigmaDz*K*Rz)-signPsi*I*O) \
        /(E+sigmaDz*Rz*(A+N*J*meanL_bp[0])/sqrt(sigmaPreci*sigmaPreci+sigmaDz*sigmaDz)+signPsi*I*J*fv_bp[0]);
        //differential system
        f_k[0]=dotLambda*signPsi;                       f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi);
        f_k[3]=dsigmaSS+(1/sqrt(sigmaPreci*sigmaPreci+sigmaDz*sigmaDz))* \
        (sigmaPreci*dsigmaPreci+sigmaDz*K*Rz+dotLambda*sigmaDz*Rz*(A+N*J*meanL_bp[0]));
        f_k[4]=dotLambda*Az;                            f_k[5]=dotLambda*J*meanL_bp[0];
        f_k[6]=I*O+I*(fv_bp[0])*J*dotLambda;
    }
    //################ physical one isotrope hardening one pptKinematic and one grainkinematic with metallurgical yield ######################
    else if (hardeningModelChosen==15) {
        //legend-->index0=epsP index1=epsPcum index2=stressMechanic index3=R index4=Zdislo index5=n_ppt index6=Xppt index7=ZdisloPPT index8=nG index9=X_G
        //sign computation
        if (yk[2]-yk[6]-yk[8]>0) {signPsi=1;}else if (yk[2]-yk[6]-yk[8]<0) {signPsi=-1;}else {signPsi=0.;}
        if (yk[5]>0) {signNppt=1;}else if (yk[5]<0) {signNppt=-1;}else {signNppt=0.;}
        
        //k2 modification if precipitation
        if(disableK2modif) {k2=k2_0;}
        else {k2=k2_0*exp(-phiPPT[0]/distanceBetweenPPT[0]/sqrt(yk[4]/burgersNorm))+k2_P*(1-exp(-phiPPT[0]/distanceBetweenPPT[0]/sqrt(yk[4]/burgersNorm)));}
        
        //intermediate constantes
        if(nPPT_star[0]==0) {error.Fatal("If 'nPPT_star=0' model 15 have singularities");}
        if(nG_star==0 || grainSize==0) {error.Fatal("If 'nG_star=0' or 'grainSize=0' model 15 have singularities");}
        Cz=taylorFactor*burgersNorm*(k1*sqrt(yk[4]/burgersNorm)-k2*(yk[4]/burgersNorm)+(k3/burgersNorm/grainSize)*(1-fabs(yk[7]/nG_star)));
        C=taylorFactor*(k1*sqrt(yk[4]/burgersNorm)-k2*(yk[4]/burgersNorm)+(k3/burgersNorm/grainSize)*(1-fabs(yk[7]/nG_star)));
        N=2*M_PI*phiPPT[0]*signNppt*Ntot_bp[0]*meanR_bp[0];
        J=taylorFactor*(signPsi-yk[5]/nPPT_star[0])/burgersNorm/sqrt(3.0);
        K=2*M_PI*phiPPT[0]*fabs(yk[5])*(dNtot_bp[0]*meanR_bp[0]+Ntot_bp[0]*dmeanR_bp[0]);
        T=(taylorFactor*lambdaG/burgersNorm)*(signPsi-yk[7]/nG_star);
        F=-taylorFactor*2*tensionLineConstant*currentShearModulus*burgersNorm*yk[7]*dgrainsize/grainSize/grainSize;
        G=taylorFactor*2*tensionLineConstant*currentShearModulus*burgersNorm/grainSize;
        I=factorKineticContribution[0]*phiPPT[0];
        if(meanL_bp[0]==0) {
            O=0.;}
        else {
            O=(dfv_bp[0]*meanL_bp[0]-fv_bp[0]*dmeanL_bp[0])*yk[5]/meanL_bp[0]/meanL_bp[0];
        }
        
        densiteDisloPpt=2*M_PI*fabs(yk[5])*phiPPT[0]*Ntot_bp[0]*meanR_bp[0];
        
        if(disableRhoPPTcouplingBool)  {
            K=0;
            N=0;
            densiteDisloPpt=0;
        }
        
        
        Rz=0.5*taylorFactor*dislocStrength*currentShearModulus*burgersNorm/sqrt(yk[4]/burgersNorm+densiteDisloPpt);
        sigmaDz=taylorFactor*dislocStrength*currentShearModulus*burgersNorm*sqrt(yk[4]/burgersNorm+densiteDisloPpt);
        //dotLambda computation
        dotLambda=(E*strainRate*signPsi-dsigmaSS-(1/sqrt(sigmaPreci*sigmaPreci+sigmaDz*sigmaDz))*(sigmaPreci*dsigmaPreci+sigmaDz*K*Rz)-signPsi*(F+I*O)) \
        /(E+sigmaDz*Rz*(C+N*J*meanL_bp[0])/sqrt(sigmaPreci*sigmaPreci+sigmaDz*sigmaDz)+signPsi*(I*J*fv_bp[0]+G*T));
        
        //differential system
        f_k[0]=dotLambda*signPsi;
        f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi);
        f_k[3]=dsigmaSS+(1/sqrt(sigmaPreci*sigmaPreci+sigmaDz*sigmaDz))* \
        (sigmaPreci*dsigmaPreci+sigmaDz*K*Rz+dotLambda*sigmaDz*Rz*(C+N*J*meanL_bp[0]));
        f_k[4]=dotLambda*Cz;
        f_k[5]=dotLambda*J*meanL_bp[0];
        f_k[6]=I*O+I*J*fv_bp[0]*dotLambda;
        f_k[7]=dotLambda*T;
        f_k[8]=F+G*T*dotLambda;
    }
    //################ physical one isotrope hardening one pptKinematic and one grainkinematic with metallurgical yield ######################
    else if (hardeningModelChosen==16) {
        //        double rhoDisloc=(yk[4]/burgersNorm);
        //        //legend-->index0=epsP index1=epsPcum index2=stressMechanic index3=R index4=Zdislo index5=nG index6=X_G
        //        //effective stress sign computation
        //        if (yk[2]-yk[6]>0) {signPsi=1;}else if (yk[2]-yk[6]<0) {signPsi=-1;}else {signPsi=0.;}
        //        //sign of path change
        //        if (strainRate*yk[0]>0) {omega=1;}else if (strainRate*yk[0]<0) {omega=-1;}else {omega=0.;}
        //        //k2 modification if precipitation
        //        k2=k2_0*exp(-phiPPT[0]/distancePPTbp[0]/sqrt(rhoDisloc))+k2_P*(1-exp(-phiPPT[0]/distancePPTbp[0]/sqrt(rhoDisloc)));
        //        //verification qu'il n'y ai pas de singularité
        //        if(nG_star==0 || grainSize==0) {error.Fatal("If 'nG_star=0' or 'grainSize=0' model 16 have singularities");}
        //        //definitions constantes
        //        double Arho,An,Ax,deltaSigmaD,kappaSS,kappaD,kappaG,kappaP,Iss,Id,Ig,Ip,AIss,AId,AIg,AIp,Adisloc,AR;
        //        double distance_d=1/sqrt(rhoDisloc),distance_G=grainSize,distance_P=distancePPTall[0],q=powSum;
        //        Arho=taylorFactor*burgersNorm*(k1*sqrt(rhoDisloc)-k2*rhoDisloc+(k3/burgersNorm/grainSize)*(1-fabs(yk[5]/nG_star)));
        //        An=(taylorFactor*lambdaG/burgersNorm)*(signPsi-yk[5]/nG_star);
        //        Ax=2*taylorFactor*taylorFactor*tensionLineConstant*currentShearModulus*lambdaG/grainSize*(signPsi-yk[5]/nG_star);
        //        deltaSigmaD=taylorFactor*dislocStrength*currentShearModulus*burgersNorm*sqrt(rhoDisloc);
        //        //activation (ou pas) de l'irreversibility
        //        if (!activeSSreversibility) {kappaSS=0.0;}
        //        else{error.Fatal("distance_SS for SS reversibility is not implemented");}
        //        if (!activeDreversibility) {kappaD=0.0;}
        //        if (!activeHreversibility) {kappaG=0.0;}
        //        if (!activePreversibility) {kappaP=0.0;}
        //        //autres definitions
        //        Iss=1;//Iss=1-kappaSS*exp(-yk[0]*omega/burgersNorm/distance_SS/
        //        Id=1-kappaD*exp(-yk[0]*omega/burgersNorm/distance_d/(rhoDisloc));
        //        Ig=1-kappaG*exp(-yk[0]*omega/burgersNorm/distance_G/(rhoDisloc));
        //        Ip=1-kappaP*exp(-yk[0]*omega/burgersNorm/distance_P/(rhoDisloc));
        //        AIss=1.0;//AIss=kappaSS*(omega/distance_SS/burgersNorm/rhoDisloc/rhoDisloc)*(signPsi*rhoDisloc-yk[0]*Arho)*exp(-yk[0]*omega/burgersNorm/distance_SS/rhoDisloc);
        //        AId=kappaD*(omega/distance_d/burgersNorm/rhoDisloc/rhoDisloc)*(signPsi*rhoDisloc-yk[0]*Arho)*exp(-yk[0]*omega/burgersNorm/distance_d/rhoDisloc);
        //        AIg=kappaG*(omega/distance_G/burgersNorm/rhoDisloc/rhoDisloc)*(signPsi*rhoDisloc-yk[0]*Arho)*exp(-yk[0]*omega/burgersNorm/distance_G/rhoDisloc);
        //        AIp=kappaP*(omega/distance_P/burgersNorm/rhoDisloc/rhoDisloc)*(signPsi*rhoDisloc-yk[0]*Arho)*exp(-yk[0]*omega/burgersNorm/distance_P/rhoDisloc);
        //        Adisloc=AId*deltaSigmaD+Id*Arho*0.5*taylorFactor*dislocStrength*currentShearModulus*burgersNorm/sqrt(rhoDisloc);
        //        AR=AIss*sigmaSS+AIg*sigmaGrain+((AIp*sigmaPreci)*pow(Ip*sigmaPreci,q-1)+(AId*deltaSigmaD+Id*0.5*taylorFactor*dislocStrength*currentShearModulus*burgersNorm/sqrt(rhoDisloc))*pow(Id*deltaSigmaD,q-1))* \
        //        pow(pow(Ip*sigmaPreci,q)+pow(Id*deltaSigmaD,q),(1-q)/q);
        //        //dotLambda computation
        //        dotLambda=(E*strainRate*signPsi) \
        //        /(E+Ax*signPsi+AR) ;
        //        //differential system
        //        //legend-->index0=epsP index1=epsPcum index2=stressMechanic index3=R index4=Zdislo index5=nG index6=X_G
        //        f_k[0]=dotLambda*signPsi;
        //        f_k[1]=dotLambda;
        //        f_k[2]=E*(strainRate-dotLambda*signPsi);
        //        f_k[3]=AR*dotLambda;
        //        f_k[4]=Arho*dotLambda; //on multiplie par "burgersNorm" pour notre "normalisation en Z"
        //        f_k[5]=An*dotLambda;
        //        f_k[6]=Ax*dotLambda;
        double zDisloc=yk[4];
        //legend-->index0=epsP index1=epsPcum index2=stressMechanic index3=R index4=Zdislo index5=nG index6=X_G
        //effective stress sign computation
        if (yk[2]-yk[6]>0) {signPsi=1;}else if (yk[2]-yk[6]<0) {signPsi=-1;}else {signPsi=0.;}
        //sign of path change
        if (strainRate*yk[0]>0) {omega=1;}else if (strainRate*yk[0]<0) {omega=-1;}else {omega=0.;}
        //k2 modification if precipitation
        k2=k2_0*exp(-phiPPT[0]/distancePPTbp[0]/sqrt(zDisloc/burgersNorm))+k2_P*(1-exp(-phiPPT[0]/distancePPTbp[0]/sqrt(zDisloc/burgersNorm)));
        //verification qu'il n'y ai pas de singularité
        if(nG_star==0 || grainSize==0) {error.Fatal("If 'nG_star=0' or 'grainSize=0' model 16 have singularities");}
        //definitions constantes
        double Az,An,Ax,deltaSigmaD,kappaSS,kappaD,kappaG,kappaP,Izss,Izd,Izg,Izp,AIzss,AIzd,AIzg,AIzp,Azdisloc,AzR;
        double distance_d=1/sqrt(zDisloc/burgersNorm),distance_G=grainSize,distance_P=distancePPTbp[0],q=powSum;
        Az=taylorFactor*burgersNorm*(k1*sqrt(zDisloc/burgersNorm)-k2*zDisloc/burgersNorm+(k3/burgersNorm/grainSize)*(1-fabs(yk[5]/nG_star)));
        An=(taylorFactor*lambdaG/burgersNorm)*(signPsi-yk[5]/nG_star);
        Ax=2*taylorFactor*taylorFactor*tensionLineConstant*currentShearModulus*lambdaG/grainSize*(signPsi-yk[5]/nG_star);
        deltaSigmaD=taylorFactor*dislocStrength*currentShearModulus*burgersNorm*sqrt(zDisloc/burgersNorm);
        //activation (ou pas) de l'irreversibility
        if (!activeSSreversibility) {kappaSS=0.0;}
        else{error.Fatal("distance_SS for SS reversibility is not implemented");}
        if (!activeDreversibility) {kappaD=0.0;}
        if (!activeHreversibility) {kappaG=0.0;}
        if (!activePreversibility) {kappaP=0.0;}
        //autres definitions
        Izss=1;//Iss=1-kappaSS*exp(-yk[0]*omega/burgersNorm/distance_SS/
        Izd=1-kappaD*exp(-yk[0]*omega/distance_d/zDisloc);
        Izg=1-kappaG*exp(-yk[0]*omega/distance_G/zDisloc);
        Izp=1-kappaP*exp(-yk[0]*omega/distance_P/zDisloc);
        AIzss=1.0;//AIss=kappaSS*(omega/distance_SS/burgersNorm/rhoDisloc/rhoDisloc)*(signPsi*rhoDisloc-yk[0]*Arho)*exp(-yk[0]*omega/burgersNorm/distance_SS/rhoDisloc);
        AIzd=kappaD*(omega/(distance_d*zDisloc*zDisloc/burgersNorm))*(signPsi*zDisloc/burgersNorm-yk[0]*Az/burgersNorm)*exp(-yk[0]*omega/distance_d/zDisloc);
        AIzg=kappaG*(omega/(distance_G*zDisloc*zDisloc/burgersNorm))*(signPsi*zDisloc/burgersNorm-yk[0]*Az/burgersNorm)*exp(-yk[0]*omega/distance_G/zDisloc);
        AIzp=kappaP*(omega/(distance_P*zDisloc*zDisloc/burgersNorm))*(signPsi*zDisloc/burgersNorm-yk[0]*Az/burgersNorm)*exp(-yk[0]*omega/distance_P/zDisloc);
        Azdisloc=AIzd*deltaSigmaD+Izd*Az*0.5*taylorFactor*dislocStrength*currentShearModulus/sqrt(zDisloc/burgersNorm);
        AzR=AIzss*sigmaSS+AIzg*sigmaGrain+(AIzp*sigmaPreci*pow(Izp*sigmaPreci,q-1)+Azdisloc*pow(Izd*deltaSigmaD,q-1))* \
        pow(pow(Izp*sigmaPreci,q)+pow(Izd*deltaSigmaD,q),(1-q)/q);
        //dotLambda computation
        dotLambda=(E*strainRate*signPsi) \
        /(E+Ax*signPsi+AzR) ;
        //differential system
        //legend-->index0=epsP index1=epsPcum index2=stressMechanic index3=R index4=Zdislo index5=nG index6=X_G
        f_k[0]=dotLambda*signPsi;
        f_k[1]=dotLambda;
        f_k[2]=E*(strainRate-dotLambda*signPsi);
        f_k[3]=AzR*dotLambda;
        f_k[4]=Az*dotLambda;
        f_k[5]=An*dotLambda;
        f_k[6]=Ax*dotLambda;
    }
    else {error.Fatal("This hardening model is not implemented in 'functionRK45adapt'");}
    
    return f_k;
}

//###############################################################################################################################################
//###############                                         GENERAL AUTONOME ROUTINES                                               ###############
//###############################################################################################################################################

void Mechanical::Parse(string _dump, vector<string>&  _arg)
{                                                   //with _arg[0] _arg[1] _arg[2]...
    size_t pos=0;
    _arg.clear();
    if(_dump.size()!=0)    {
        while(1)        {
            pos=_dump.find_first_of(" \t\n\b\r");
            if(pos==string::npos){
                _arg.push_back(_dump);
                break;
            } else
                if(pos!=0) _arg.push_back(_dump.substr(0,pos));
            if(pos>=_dump.size()-1) break;
            _dump=_dump.substr(pos+1);
        }
    }
}

//choisi de ne pas mettre dans classe mathematique pour conserver cette resolution dans class mechanic car
//peut être indépendante des classes de precipitations
//les algo de resolution mecanique sont volontairement mis dans cette classe
vector<vector<double> > Mechanical::rk45adapt(double initialDt,vector<double> const& tempsINI_FIN,vector<double> const& CI)
{
    //j'ai implémenté cet algo lors de ma these en m'inspirant des travaux de Hairer. Les paramètres de bases ont été choisi
    //après plusieurs confrontations avec les algo de matlab. A priori dans cet état il donne des résultats très précis
    //(j'avais eu de meilleurs résultats qu'avec matlab)
    if(tempsINI_FIN.size()!=2) {std::cout << "vector temps must have size 2" << std::endl;exit(1);}
    size_t sizeVector=CI.size();
    double tol=1e-8,coeffLowerBound=0.2,coeffUpperBound=10.0,AbsTol=1e-15,RelTol=1e-10,safeCoeff=0.8;
    double h_k=initialDt,t_k=tempsINI_FIN[0],h_opt=0;
    vector<double> k1,k2,k3,k4,k5,k6,k7,f,ykAdditionalVect,yk,Y_kp1,zeros;
    k1.assign(sizeVector,0);k2=k1;k3=k1;k4=k1;k5=k1;k6=k1;k7=k1;
    ykAdditionalVect=k1;yk=k1;Y_kp1=k1;zeros=k1;
    vector<double> initLine; for (size_t i=0;i<sizeVector;i++) {initLine.push_back(0.0);}
    vector<vector<double> > Results; Results.push_back(initLine);
    vector<double> Times;       Times.push_back(t_k);
    yk=CI;Results[0]=yk;
    double a1=0;
    double a2=1./5.,b21=1./5.;
    double a3=3./10.,b31=3./40.,b32=9./40.;
    double a4=4./5.,b41=44./45.,b42=-56./15.,b43=32./9.;
    double a5=8./9.,b51=19372./6561.,b52=-25360./2187.,b53=64448./6561.,b54=-212./729.;
    double a6=1.,b61=9017./3168.,b62=-355./33.,b63=46732./5247.,b64=49./176.,b65=-5103./18656.;
    double a7=1.,b71=35./384.,b72=0.,b73=500./1113.,b74=125./192.,b75=-2187./6784.,b76=11./84.;
    //schema 5eme order (we use hypothesis of local extrapolation)
    double d1=b71,d2=b72,d3=b73,d4=b74,d5=b75,d6=b76,d7=0;
    //error coefficient
    double e1=71./57600.,e2=0.0,e3=-71./16695.,e4=71./1920.,e5=-17253./339200.,e6=22./525.,e7=-1./40.;
    //main loop
    double localError=0,divisionPrErreur=0,y0abs=0,y1abs=0,mesureGlobaleError=0;
    while (t_k<tempsINI_FIN[1]) {
        f=functionRk45adapt(t_k+a1*h_k,yk,zeros);
        for (size_t i=0;i<sizeVector;i++) {k1[i]=h_k*f[i]; ykAdditionalVect[i]=b21*k1[i];}
        f=functionRk45adapt(t_k+a2*h_k,yk,ykAdditionalVect);
        for (size_t i=0;i<sizeVector;i++) {k2[i]=h_k*f[i]; ykAdditionalVect[i]=b31*k1[i]+b32*k2[i];}
        f=functionRk45adapt(t_k+a3*h_k,yk,ykAdditionalVect);
        for (size_t i=0;i<sizeVector;i++) {k3[i]=h_k*f[i]; ykAdditionalVect[i]=b41*k1[i]+b42*k2[i]+b43*k3[i];}
        f=functionRk45adapt(t_k+a4*h_k,yk,ykAdditionalVect);
        for (size_t i=0;i<sizeVector;i++) {k4[i]=h_k*f[i]; ykAdditionalVect[i]=b51*k1[i]+b52*k2[i]+b53*k3[i]+b54*k4[i];}
        f=functionRk45adapt(t_k+a5*h_k,yk,ykAdditionalVect);
        for (size_t i=0;i<sizeVector;i++) {k5[i]=h_k*f[i]; ykAdditionalVect[i]=b61*k1[i]+b62*k2[i]+b63*k3[i]+b64*k4[i]+b65*k5[i];}
        f=functionRk45adapt(t_k+a6*h_k,yk,ykAdditionalVect);
        for (size_t i=0;i<sizeVector;i++) {k6[i]=h_k*f[i]; ykAdditionalVect[i]=b71*k1[i]+b72*k2[i]+b73*k3[i]+b74*k4[i]+b75*k5[i]+b76*k6[i];}
        f=functionRk45adapt(t_k+a7*h_k,yk,ykAdditionalVect);
        localError=0;divisionPrErreur=0;
        for (size_t i=0;i<sizeVector;i++) {
            k7[i]=h_k*f[i];
            Y_kp1[i]=yk[i]+d1*k1[i]+d2*k2[i]+d3*k3[i]+d4*k4[i]+d5*k5[i]+d6*k6[i]+d7*k7[i];
            y0abs=fabs(yk[i]);y1abs=fabs(Y_kp1[i]);
            if (y0abs<y1abs) { divisionPrErreur=AbsTol+RelTol*y1abs;}
            else {divisionPrErreur=AbsTol+RelTol*y0abs;}
            localError=localError+pow(((e1*k1[i]+e2*k2[i]+e3*k3[i]+e4*k4[i]+e5*k5[i]+e6*k6[i]+e7*k7[i])/divisionPrErreur),2);
        }
        mesureGlobaleError=sqrt((1.0/sizeVector)*localError);
        h_opt=safeCoeff*h_k*pow(tol/mesureGlobaleError,1.0/5.0);
        if (mesureGlobaleError<=tol) {
            t_k=t_k+h_k;           yk=Y_kp1;
            Times.push_back(t_k);  Results.push_back(yk);
            if (h_opt<tempsINI_FIN[1]-t_k) {if (h_opt/h_k>coeffUpperBound) {h_k=coeffUpperBound*h_k;} else {h_k=h_opt;}}
            else {h_k=tempsINI_FIN[1]-t_k;}
        }
        else {if (h_opt/h_k<coeffLowerBound) {h_k=coeffLowerBound*h_k;} else {h_k=h_opt;}}
    }
    //we fill result matrix
    vector<double> tempVect;
    vector< vector<double> > timeAndResults;
    for (size_t i=0;i<Times.size();i++) {
        tempVect.clear();
        tempVect.push_back(Times[i]);
        for (size_t j=0;j<Results[i].size();j++) {tempVect.push_back(Results[i][j]);}
        timeAndResults.push_back(tempVect);
    }
    return timeAndResults;
}
