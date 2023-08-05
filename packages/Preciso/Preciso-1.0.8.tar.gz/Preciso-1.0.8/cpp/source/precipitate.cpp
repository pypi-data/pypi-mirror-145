/// \file precipitate.cpp
/// \brief Methods of the class Precipitate
#include <iostream>
#include <fstream>  
#include <vector>
#include <algorithm>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "precipitate.h"
#include "constants.h"
#include "mathematic.h"
#include "error.h"

using namespace std;

Precipitate::Precipitate(vector<Element> const& _Elements)
{
    name="";        atomicVolume=0.0;    surfaceEnergy=0.;    surfaceEnergy0=0.; surfaceEnergySigma=0.0;
    solProdA=0.;    solProdB=0.;  solProdC=0;
    nucleationType="";  heteroNucleation=0.; heteroSites=0.;
    shapeString=""; aspectRatio=0.;     nbOfClass=0;         sizeElement=_Elements.size();
    shape=1; //1 is for sphere, 2 for rods, 3 for cylinder, 4 for cylinder with aspect ratio defined with three linear functions, 5 for Cylinder from Fisk study (2014), 6 for rods with aspect ratio = a0*L+b1
    nucleationChoice=1; //1 for homogeneous, 2 for heterogeneous
    siteSaturation=false; siteSaturationType="";
    
    ElementList.assign(sizeElement,"");
    for(size_t i=0;i<sizeElement;i++) {ElementList[i]=_Elements[i].GetName();}
    Chemistry.assign(sizeElement,0);  ContentAtFrac.assign(sizeElement,0);
    Radius.clear();                        Number.clear();
    randomWalk=0.;       superSaturation=0.; drivingForce=0.;          rStar=0.;
    atomsPerMolecule=0.; totalNumber=0.;     callClassManagement=false;
    solubilityFraction=0.;
    
    volumeOfTheAssociedNode=1.;
    
    // Options default values
    //The following default values should not be modified without discussion with all developpers.
    diffusionCoefficientRatio=1.0e4;     targetClassNumber=500;
    changeNumberInClass=0.01;            unstationnaryNucleation=false;
    classManagementType=1; //1=no,2=old,3=lin,4=distrib,5=quad,6=oldWithLess
    minDissolutionLimit=1e-10;           maxDissolutionLimit=2e-10;
    limitOfpreciInClassForDissolution=0.;
    nonLinearAlgorithm=1; //1=NR (NewtonRaphson),2=CNR (constrained NewtonRaphson),3=brent (brent),4=dicho (dichotomy)
    
    boostPrecipitateDiffusion=1.;
    dormant=false;
    //#############################################
    // outputs for unstationnary nucleation publi
    //#############################################
    //JS_publi=0;
    //incubationCoef_publi=0;
    //tau_publi=0;
    //dN_dt_publi=0;
    //dN_publi=0;
    //randomWalk_publi=0;
    //delta_publi=0;
    //Z_publi=0;
    //betaStar_publi=0;
    //rStarKbT_publi=0;
    //rStar_publi=0;
    //##############################################
    
}

Precipitate::~Precipitate() {}

void Precipitate::DefinePrecipitate(vector<string>& _arg)
{
    
    if(_arg[2]=="dormant"){
        dormant=true;
        _arg.erase(_arg.begin() + 2);
    }
    
    char* endCharact=NULL;
    
    // Check if optional parameter solProdC is given or not
    char* p;
    double converted = strtod(_arg[6].c_str(), &p);
    if (!*p) {
        // arg[6] is a number => solProdC
        solProdC=strtod(_arg[6].c_str(),&endCharact);
        // arg[6] is deleted, back to normal situation without solPordC parameter
        _arg.erase(_arg.begin() + 6);
    }
    
    name=_arg[1];
    atomicVolume=strtod(_arg[2].c_str(),&endCharact);
    if (atomicVolume<0.) {error.Fatal("Invalid atomic volume for precipitate: " + name);}
    surfaceEnergy0=strtod(_arg[3].c_str(),&endCharact);
    if (surfaceEnergy<0.) {error.Fatal("Invalid surface energy for precipitate: " + name);}
    solProdA=strtod(_arg[4].c_str(),&endCharact);
    solProdB=strtod(_arg[5].c_str(),&endCharact);
    shapeString=_arg[6];
    if (shapeString=="sphere")    {aspectRatio=1;shape=1;}
    //aspect ratio is the length divided by the radius in PreciSo in this case !!!
    else if (shapeString=="rod")    {
        shape=2;
        aspectRatio=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
    }
    else if (shapeString=="cylinder")   {
        shape=3;
        aspectRatio=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        // error.Warning("Not all coarsening and growth equations implemented for cylindrical precipitates");
    }
    else if (shapeString=="cylinderFunction")   {
        shape=4;
        a0=strtod(_arg[7].c_str(),&endCharact);
        aspectRatio=a0; // rajout pour initialisation MP
        _arg.erase(_arg.begin() + 7);
        a1=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        b1=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        a2=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        b2=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        r1=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        r2=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        //error.Warning("Not all coarsening and growth equations implemented for cylindrical precipitates");
    }
    else if (shapeString=="FiskCylinder")   {
        error.Fatal("FiskCylinder option valid only for debugging");
        shape=5;
        a0=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        a1=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        b1=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        a2=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        b2=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        r1=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        r2=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        //aspectRatio=strtod(_arg[8]0.55.c_str(),&endCharact);
        
        // for (size_t i=1;7;i+=1)    {_arg.erase(_arg.begin() + 8);}
        //error.Warning("Not all coarsening and growth equations implemented for cylindrical precipitates");
    }
    else if (shapeString=="RodFunction")   {
        shape=6;
        a0=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        b1=strtod(_arg[7].c_str(),&endCharact);
        _arg.erase(_arg.begin() + 7);
        aspectRatio=b1;
    }
    else {error.Fatal("Undefined shape for precipitate: " + shapeString + ", should be sphere, rod, cylinder, cylinderFunction");}
    nucleationType=_arg[7];
    if (nucleationType=="homogeneous")    {
        nucleationChoice=1;
        heteroNucleation=1.0;
        heteroSites=0.;    }
    else if (nucleationType=="heterogeneous")    {
        nucleationChoice=2;
        heteroNucleation=strtod(_arg[8].c_str(),&endCharact);
        if ((heteroNucleation<0.)||(heteroNucleation>1.)) {error.Fatal("Invalid heterogeneous nucleation coefficient for precipitate: " + name);}
        heteroSites=strtod(_arg[9].c_str(),&endCharact);
        if (heteroSites<0.) {error.Fatal("Invalid heterogeneous nucleation sites density for precipitate: " + name);}
        _arg.erase(_arg.begin()+8);
        _arg.erase(_arg.begin()+8);    }
    else {error.Fatal("Invalid nucleation type: " + nucleationType + ", should be homogeneous or heterogeneous");}
    
    if(_arg[8]=="siteSaturation"){
        siteSaturation=true;
        if(_arg[9]=="lin"){
            siteSaturationType="lin";
            _arg.erase(_arg.begin()+8);
            _arg.erase(_arg.begin()+8);
        } else if(_arg[9]=="surf"){
            siteSaturationType="surf";
            _arg.erase(_arg.begin()+8);
            _arg.erase(_arg.begin()+8);
        } else if(_arg[9]=="surf"){
            siteSaturationType="vol";
            _arg.erase(_arg.begin()+8);
            _arg.erase(_arg.begin()+8);
        } else error.Fatal("Invalid siteSaturation type: should be 'lin', 'surf' or 'vol' !");
        
    }
    
    for (size_t i=8;i<_arg.size();i+=2)    {
        string tempString = _arg[i];
        int index=-1;
        for (size_t j=0;j<sizeElement;j++) {if (ElementList[j]==tempString) {index=j;}}
        if (index==-1) {error.Fatal("element " + tempString + " for precipitates not found in defined elements.");}
        else  {
            Chemistry[index]=strtod(_arg[i+1].c_str(),&endCharact);
            if (Chemistry[index]<0.) {error.Fatal("Invalid chemistry for precipitate: " + name);}
        }
    }
    for (size_t i=0;i<sizeElement;i++) {atomsPerMolecule+=Chemistry[i];}
    for (size_t i=0;i<sizeElement;i++) {ContentAtFrac[i]=Chemistry[i]/atomsPerMolecule;}
}

void Precipitate::DefineInitialDistribution(vector<double> const& _InitialRadius,vector<double> const& _InitialNumber)
{
    Radius=_InitialRadius;
    Number=_InitialNumber;
    nbOfClass=Radius.size();
}

string Precipitate::GetName() const {return name;}

double Precipitate::GetAtomicVolume() const {return atomicVolume;}

double Precipitate::GetSurfaceEnergy() const {return surfaceEnergy;}

double Precipitate::GetSolProdA() const {return solProdA;}

double Precipitate::GetSolProdB() const {return solProdB;}

double Precipitate::GetSolProdC() const {return solProdC;}

double Precipitate::GetHeteroNucleation() const {return heteroNucleation;}

double Precipitate::GetHeteroSites() const {return heteroSites;}

string Precipitate::GetShape() const {return shapeString;}

int Precipitate::GetShapeIndex() const {return shape;}

double Precipitate::GetAspectRatio() const {return aspectRatio;}

double Precipitate::GetAtomsPerMolecule() const {return atomsPerMolecule;}

double Precipitate::GetThisElementChemistry(size_t const& _elementIndex) const
{
    if (_elementIndex<sizeElement) {return Chemistry[_elementIndex];}
    else {
        error.Fatal("Element exceeds the maximum number of elements.");
        return -1;
    }
}

double Precipitate::GetThisElementChemistry(string const& _element) const
{
    bool found(false);
    double thisElementChemistry(0);
    for (size_t i=0;i<sizeElement;i++)    {
        if (ElementList[i]==_element) {thisElementChemistry=Chemistry[i];found=true;}
    }
    if (found) {return thisElementChemistry;}
    else {error.Fatal("element unfound in element list.");return -1;}
}

void Precipitate::SetName(string const& _name) {name=_name;}

void Precipitate::SetAtomicVolume(double const& _atomicVolume) {atomicVolume=_atomicVolume;}

void Precipitate::SetSurfaceEnergy(double const& _surfaceEnergy) {surfaceEnergy=_surfaceEnergy;}

void Precipitate::SetSolProdA(double const& _solProdA) {solProdA=_solProdA;}

void Precipitate::SetSolProdB(double const& _solProdB) {solProdB=_solProdB;}

void Precipitate::SetSolProdC(double const& _solProdC) {solProdC=_solProdC;}

void Precipitate::SetHeteroNucleation(double const& _heteroNucleation) {heteroNucleation=_heteroNucleation;}

void Precipitate::SetHeteroSites(double const& _heteroSites) {heteroSites=_heteroSites;}

void Precipitate::SetShape(string const& _shape) {shapeString=_shape;}

void Precipitate::SetShapeIndex(int const& _shape) {shape=_shape;}

void Precipitate::SetAspectRatio(double const& _aspectRatio) {aspectRatio=_aspectRatio;}

void Precipitate::SetThisElementChemistry(string const& _element, double const& _chemistry)
{
    bool found(false);
    for (size_t i=0;i<sizeElement;i++)    {
        if (ElementList[i]==_element) {Chemistry[i]=_chemistry;found=true;}
    }
    if (!found) {error.Fatal("element unfound in element list.");}
}

void Precipitate::Nucleation(vector<Element> const& _Elements, Matrix const& _matrix, double const& _t, double const& _dt, double const& _T, double const& _firstTime, int const& _timeStepManagement)
{
    double deltaGStar=0.,Z=0.,diffusionI=0.,tau=0.,JS=0.,incubationCoef=0.;
    double betaStar=0.,delta=0.,dN_dt=0.,dN=0.,rStarKbT=0.;
    
    // Calculation of the actual surface energy of the (hypothetical) new class
    if(surfaceEnergySigma!=0){
        double u1= ((double) rand()/RAND_MAX);
        double u2= ((double) rand()/RAND_MAX);
        // Use of Box-Muller transform !
        surfaceEnergy=surfaceEnergy0+surfaceEnergySigma*sqrt(-2.0*log(u1))*cos(2*M_PI*u2);
        if (u1==0) surfaceEnergy=0;
    }
    else surfaceEnergy=surfaceEnergy0;
    if(surfaceEnergy<0) surfaceEnergy=surfaceEnergy0;
    
    totalNumber=TotalNumberOfPrecipitates();
   
    SuperSaturationCalculation(_Elements, _T);
    DrivingForceCalculation(_T);
    /// \warning R star need to be updated even if there is no nucleation because it is used to validate the time step length.
    RStarCalculation(_T);
    if (superSaturation>0.)    {
        double kBT=KB*_T;
        
        //Energy barrier and Zeldovich number computation
        if (shape==1)    {
            deltaGStar=heteroNucleation*(16.0/3.0)*M_PI*surfaceEnergy*surfaceEnergy*surfaceEnergy/(drivingForce*drivingForce);
            Z=(atomicVolume*atomsPerMolecule/(2.0*M_PI*rStar*rStar))*sqrt(surfaceEnergy/kBT);        }
        else if((shape==2)||(shape==6))   { // is shape = rod
            deltaGStar=heteroNucleation*(32.0/3.0)*M_PI*surfaceEnergy*surfaceEnergy*surfaceEnergy*aspectRatio*aspectRatio*aspectRatio\
            /(drivingForce*drivingForce*(3.0*aspectRatio-2.0)*(3.0*aspectRatio-2.0));
            Z=(atomicVolume*atomsPerMolecule/((3.0*aspectRatio-2.0)*M_PI*rStar*rStar))*sqrt(2.0*aspectRatio*surfaceEnergy/kBT);
        }
        else if((shape==3)||(shape==4))     {
            //error.Fatal("Nucleation not yet implemented for cylinders");
            deltaGStar=heteroNucleation*(16.0/3.0)*M_PI*surfaceEnergy*surfaceEnergy*surfaceEnergy/(drivingForce*drivingForce) \
            *(aspectRatio+2)*(aspectRatio+2)*(aspectRatio+2)/(18*aspectRatio);
            Z=(atomicVolume*atomsPerMolecule/(3*M_PI*rStar*rStar))*sqrt(surfaceEnergy*aspectRatio*(aspectRatio+2)/(2*kBT));
        }
        //else if(shape==4)     {
        //    //error.Fatal("Nucleation not yet implemented for cylinders with variable aspect ratio");
        //    //double tempAspectRatio=AspectRatioFromCylinderFunction(rStar); //At the the nucleation step, the aspect ratio is supposed equal to the initial value a0;
        //    deltaGStar=heteroNucleation*(16.0/3.0)*M_PI*surfaceEnergy*surfaceEnergy*surfaceEnergy/(drivingForce*drivingForce) \
        //    *(aspectRatio+2)*(aspectRatio+2)*(aspectRatio+2)/(18*aspectRatio);
        //    //*(tempAspectRatio+2)*(tempAspectRatio+2)*(tempAspectRatio+2)/(18*tempAspectRatio);
        //    Z=(atomicVolume*atomsPerMolecule/(3*M_PI*rStar*rStar))*sqrt(surfaceEnergy*aspectRatio*(aspectRatio+2)/(2*kBT));
        //}
        else if(shape==5)     {
            error.Fatal("Nucleation not yet implemented for cylinders with variable aspect ratio");
            double tempAspectRatio=a0; //At the the nucleation step, the aspect ratio is supposed equal to the initial value a0;
            deltaGStar=heteroNucleation*tempAspectRatio*tempAspectRatio/8*(16.0/3.0)*M_PI*surfaceEnergy*surfaceEnergy*surfaceEnergy/(drivingForce*drivingForce);
            Z=1/30;
        }
        else {error.Fatal("This shape is not implemented in nucleation");}
        
        ///Condensation rate betaStar computation
        double a=_matrix.GetLatticeParameter();
        double inverseEffectiveDiffusion=0.;
        /// \warning Use solidSolContent and not contentAtFrac
        /// \todo Alert other coders to use solidSolidcontent to compute betaStar and update betaStar in the code
        for (size_t i=0;i<sizeElement;i++)        {
            diffusionI=_Elements[i].GetDiffusionCoefficient(_T)*boostPrecipitateDiffusion;
            if (Chemistry[i]!=0. && diffusionI!=0) {
                inverseEffectiveDiffusion+=ContentAtFrac[i]/(diffusionI*_Elements[i].GetSolidSolContent());
            }
        }
        betaStar=4.0*M_PI*rStar*rStar/(a*a*a*a*inverseEffectiveDiffusion);
        
        ///Incubation time tau computation
        tau=4.0/(2.0*M_PI*betaStar*Z*Z);
        
        ///Number of nucleation site
        double nuclSiteNumber=0;
        if (nucleationChoice==1) {nuclSiteNumber=(1.0/_matrix.GetAtomicVolumeSS());}
        else if (nucleationChoice==2) {nuclSiteNumber=heteroSites;}
        else {error.Fatal("This nucleation is not implemented");}
        
        ///SiteSaturation
        if(siteSaturation==true){
            double rmean=MeanRadius();
            if(siteSaturationType=="lin")
                nuclSiteNumber-=totalNumber*rmean/a;
            else if(siteSaturationType=="surf")
                nuclSiteNumber-=totalNumber*M_PI*(rmean/a)*(rmean/a);
            else if(siteSaturationType=="vol")
                nuclSiteNumber-=totalNumber*4.0/3.0*M_PI*(rmean/a)*(rmean/a)*(rmean/a);
            if(nuclSiteNumber<0) nuclSiteNumber=0;
        }
        
        ///Stationnary value of nucleation
        JS=nuclSiteNumber*Z*betaStar*exp(-deltaGStar/kBT);
        
        ///Incremental calculation of incubation time
        incubationCoef=0.;
        //Energetic step to travel for nucleation
        delta=sqrt(2.0*betaStar*tau);
        
        if(_timeStepManagement==1) {
            incubationCoef=1.0-exp(-(_t)/tau);}
        else {
            if (unstationnaryNucleation)        {
                
                //call RK45 for resolution
                vector<double> timeINI_END,CI,constantesToDefineDiffSystem;
                timeINI_END.clear();CI.clear();
                constantesToDefineDiffSystem.push_back(delta);
                constantesToDefineDiffSystem.push_back(tau);
                vector<vector<double> > timesAndResults; timesAndResults.clear();
                CI.push_back(randomWalk);
                timeINI_END.push_back(_t);
                timeINI_END.push_back(_t+_dt);
                int indexFonctionAresoudre=1;
                timesAndResults=mathematic.rk45adaptive(_dt,timeINI_END,CI,indexFonctionAresoudre,constantesToDefineDiffSystem);
                size_t nbTtimes=timesAndResults.size();
                randomWalk=timesAndResults[nbTtimes-1][1];
                if ((randomWalk/delta>0) && (randomWalk/delta<1)) {incubationCoef=randomWalk/delta;}
                if ((randomWalk/delta>1) && (randomWalk/delta<2)) {incubationCoef=2-randomWalk/delta;}        }
            else {
                incubationCoef=1.0-exp(-(_t+_dt-_firstTime)/tau);// new version
                //incubationCoef=1.0-exp(-(_t)/tau); // old version
            }
        }
        
        //Precipitates nucleation radius considering thermal agitation
        rStarKbT=rStar+1.0/2.0*sqrt(kBT/(M_PI*surfaceEnergy));
        
        ///Nucleation rate computation
        dN_dt=0.;
        dN=0.;
        dN_dt=JS*incubationCoef;
        
        //if(_t>1e3)
        //dN_dt=0;
        dN=dN_dt*_dt;
        if ((dN/(totalNumber+1.0))>1.0e-5)        {
            //totalNumber+=dN; // totalNumber is calculated at each nucleation step
            Radius.push_back(rStarKbT);
            Number.push_back(dN);
            if(Radius.size()>targetClassNumber*10) //If there is a very long nucleation phase, the number of classes can increase too drastically. Normally class management isn't call during nucleation. Here the class management call is forced to prevent a high number of class during long nucleation.
                callClassManagement=true;
            else
                callClassManagement=false;
        }
        else {
            callClassManagement=true;
        }
    }
    else {
        callClassManagement=true;
    }
    nbOfClass=Radius.size();
    
    
    //#############################################
    // outputs for unstationnary nucleation publi
    //#############################################
    //JS_publi=JS;
    //incubationCoef_publi=incubationCoef;
    //tau_publi=tau;
    //dN_dt_publi=dN_dt;
    //dN_publi=dN;
    //randomWalk_publi=randomWalk;
    //delta_publi=delta;
    //Z_publi=Z;
    //betaStar_publi=betaStar;
    //rStarKbT_publi=rStarKbT;
    //rStar_publi=rStar;
    //#############################################
}

double Precipitate::SolProdGibbsThomsonCalculation(double const& _T, double const& _r)
{
    if (_r==0) {
        return 0.;
    }
    else {
        double kBT=KB*_T,factorGT=0;
        //double tempAspectRatio=a0;//aspectRatio;//AspectRatioFromCylinderFunction(_r);
        //double Ks=exp(log(10.0)*(solProdB-solProdA/_T));
        double Ks=exp(log(10.0)*(solProdC/_T/_T+solProdB-solProdA/_T));
        if (shape==1)  {factorGT=exp(2.0*surfaceEnergy*atomicVolume*atomsPerMolecule/(_r*kBT));}
        else if((shape==2)||(shape==6)){factorGT=exp(4.0*aspectRatio*surfaceEnergy*atomicVolume*atomsPerMolecule/((3.0*aspectRatio-2.0)*_r*kBT));}
        else if((shape==3)||(shape==4)) {factorGT=exp(2.0*surfaceEnergy*atomicVolume*atomsPerMolecule*(aspectRatio+2)/(3.0*_r*kBT));}
        //else if(shape==4) {factorGT=exp(2.0*surfaceEnergy*atomicVolume*atomsPerMolecule*(tempAspectRatio+2)/(3.0*_r*kBT));} //
        //else if(shape==4) {factorGT=exp(2.0*surfaceEnergy*atomicVolume*atomsPerMolecule*(aspectRatio+2)/(3.0*_r*kBT));} //
        else if(shape==5) {error.Fatal("FiskCylinder option valid only for debugging");factorGT=exp(surfaceEnergy*atomicVolume*atomsPerMolecule/(_r*kBT));}
        else {error.Fatal("This shape is not implemented in nucleation");}
        
        
        return Ks*factorGT;
        // pour tester les Èquation cylindre
        //return Ks;
    }
}

void Precipitate::Growth(vector<Element> const& _Elements, Matrix const& _matrix, double const& _dt, double const& _T)
{
    //cout << boostPrecipitateDiffusion << endl;
    
    size_t nbOfMatrix=1;
    //----- We determine which precipitate is fast (matrix or high diffusional elements) and wich is low -----
    vector<Element> SlowElements;SlowElements.clear();
    vector<Element> FastElements;FastElements.clear();
    vector<bool> keepSlowElement(sizeElement,true);
    vector<bool> keepFastElement(sizeElement,false);
    
    // Alpha
    double alpha=_matrix.GetAtomicVolumeSS()/atomicVolume;
    
    string nameMatrix=_matrix.GetName();
    for (size_t i=0;i<sizeElement;i++)    {
        if (Chemistry[i]==0)                               {keepSlowElement[i]=false;keepFastElement[i]=false;}
        if (ElementList[i]==nameMatrix && Chemistry[i]!=0) {keepSlowElement[i]=false;keepFastElement[i]=true;}
    }
    //we check if one diffusion coefficient is much higher than others
    double ratio=0.;
    for (size_t i=0;i<sizeElement-nbOfMatrix;i++)    {
        for (size_t j=0;j<sizeElement-nbOfMatrix;j++)        {
            if ((i!=j)&&(keepSlowElement[i])&&(keepSlowElement[j]))            {
                //double D_Mo=_Elements[0].GetDiffusionCoefficient(_T);
                //double D_C=_Elements[1].GetDiffusionCoefficient(_T);
                //double Ratio_Mo_C=D_Mo/D_C;
                ratio=((_Elements[i].GetDiffusionCoefficient(_T))/(_Elements[j].GetDiffusionCoefficient(_T)))/diffusionCoefficientRatio;
                if (ratio>1.0) {keepSlowElement[i]=false; keepFastElement[i]=true;}
            }
        }
    }
    for (size_t i=0;i<sizeElement;i++) {
        if (keepSlowElement[i]) {SlowElements.push_back(_Elements[i]);}
        if (keepFastElement[i]) {FastElements.push_back(_Elements[i]);}
    }
    
    //--------------------------- The slow elements determine the size of the system -------------------------
    if (SlowElements.size()==1) {
        GrowthOneElement(alpha,_dt,_T,SlowElements,FastElements);
    }
    else if (SlowElements.size()==2) {
        GrowthTwoElementNumeric(alpha,_dt,_T,SlowElements,FastElements);}
    else {
        GrowthGeneral(alpha,_dt,_T,SlowElements,FastElements);
    }
    
    // update the aspectRatio for the case shape=4 i.e. when the aspect ratio varies with the size of precipitates and ensure a constant volumeFraction
    if(shape==4){
        double trueVolumeFraction=VolumeFraction();
        aspectRatio=AspectRatioFromCylinderFunction(MeanRadius());
        double currentVolumeFraction=VolumeFraction();
        //Normalization to keep volume fraction constant
        for (size_t i=0;i<nbOfClass;i++) {Number[i]=Number[i]*trueVolumeFraction/currentVolumeFraction;}
    }
    // update the aspectRatio for the case shape=6 i.e. when the aspect ratio varies with the size of precipitates and ensure a constant volumeFraction
    else if(shape==6){
        double trueVolumeFraction=VolumeFraction();
        aspectRatio=AspectRatioFromRodFunction(MeanRadius());
        double currentVolumeFraction=VolumeFraction();
        //Normalization to keep volume fraction constant
        for (size_t i=0;i<nbOfClass;i++) {Number[i]=Number[i]*trueVolumeFraction/currentVolumeFraction;}
    }
    
    //! uncomment to check growth2elementNumeric on VC precipitate
    //    SlowElements.clear();
    //    FastElements.clear();
    //    SlowElements.push_back(_Elements[0]);
    //    SlowElements.push_back(_Elements[1]);
    //    if (SlowElements.size()==2) {
    //    GrowthTwoElementNumeric(alpha,_dt,_T,SlowElements,FastElements);
    //    }
    //    else{error.Fatal("twoSlow!!!");}
    
    //-----------------------------------------------------------------------------------------------------------
}

void Precipitate::GrowthOneElement(double const _alpha, double const& _dt, double const& _T,\
                                   vector<Element> const& _SlowElements,vector<Element> const& _FastElements)
{
    /// \todo Reduce if possible the use of GetThisElementChemistry function
    //! Analytical resolution : we compute Xi for slow and inject in dr/dt of slow element
    double coeffDiffu0=_SlowElements[0].GetDiffusionCoefficient(_T)*boostPrecipitateDiffusion,coeffDiffu=0.;
    //    double coeffDiffu1=0,Rd0=0,fc=0;
    if(shape==1) {coeffDiffu=coeffDiffu0;}
    else if((shape==2)||(shape==6)) {coeffDiffu=(3.0/(4.0*aspectRatio))*coeffDiffu0;}
    else if((shape==3)||(shape==4)) {
        //error.Fatal("Warning: difference with ABalan code, see line below");
        //coeffDiffu=coeffDiffu0/4; //In preciSo_v3
        //coeffDiffu=2*aspectRatio*coeffDiffu0/M_PI; //In ABalan's phD code
        coeffDiffu=coeffDiffu0*aspectRatio/2; // Hillert
    }
    //else if(shape==4) {coeffDiffu=coeffDiffu0*aspectRatio/2; // Hillert}
    else if(shape==5) {error.Fatal("FiskCylinder option valid only for debugging");coeffDiffu=2*coeffDiffu0/M_PI;} //coeffDiffu calculated for each radius after
    else {error.Fatal("This shape is not implemented in growth 1 elements");}
    //Initialization
    double slowElementChemistry=GetThisElementChemistry(_SlowElements[0].GetName());
    double SolProdGibbsThomson=0.,slowElementXi=0.,multiFastXiPowerStoechio=0.,XRatio=0.,dr_dt=0.;
    //    double dr_dt1=0;
    multiFastXiPowerStoechio=1;
    //We compute the multiplication of Xi^Stoechio (which=X0^Stoechio) for fastElements
    for (size_t j=0;j<_FastElements.size();j++) {
        multiFastXiPowerStoechio*=pow(_FastElements[j].GetSolidSolContent(),GetThisElementChemistry(_FastElements[j].GetName()));
    }
    //We can compute for each radius Xi of the slow element K(r)/Pi(rapidElementsXi^stoechio) & determine dr/dt
    double solidSol0=_SlowElements[0].GetSolidSolContent(),radiusI;
    for (size_t i=0;i<nbOfClass;i++)    {
        radiusI=Radius[i];
        if (radiusI==0) {error.Fatal("we can't have radius equal to 0 in growth");}
        
        
        // MODIFICATION FOR FeCu
        //surfaceEnergy=min(0.3+radiusI/3e-9*0.3,0.6);
        // END OF MODIFICATION
        
        // shape==5 AspectRatio depends on radiusI Alexandre BALAN!
        //if ((shape==5)|(shape==4)) {//tempAspectRatio=AspectRatioFromCylinderFunction( radiusI);
        //coeffDiffu=coeffDiffu0*tempAspectRatio/2; // Hillert
        //coeffDiffu=coeffDiffu0*aspectRatio/2; // Hillert
        //                       coeffDiffu=2*coeffDiffu0*tempAspectRatio/M_PI; // [Fisk 2014]
        //                       Rd0=2*surfaceEnergy*atomicVolume/(3*_T*KB);
        //                       coeffDiffu1=8*tempAspectRatio*coeffDiffu0*Rd0/(27*M_PI);
        //}
        
        
        SolProdGibbsThomson=SolProdGibbsThomsonCalculation(_T,radiusI);
        slowElementXi=pow(SolProdGibbsThomson/multiFastXiPowerStoechio,1/slowElementChemistry);
        XRatio=(solidSol0-slowElementXi)/fabs(_alpha*slowElementChemistry/atomsPerMolecule-slowElementXi);
        dr_dt=(coeffDiffu/radiusI)*XRatio;
        
        // shape==4 une fonction pour croissance + 1 fonction pour la coalescence!
        //      if ((shape==5)|(shape==4)) {
        //        dr_dt1=(coeffDiffu1/(radiusI*radiusI))*XRatio;
        //        fc=1-Erf(4*(radiusI/(rStar*a0)-1));
        //        Radius[i]+=(1-fc)*dr_dt*_dt+fc*dr_dt1*_dt;
        //    }
        //      else {
        
        Radius[i]+=dr_dt*_dt;
        if(Radius[i]>1e-6)
            XRatio=XRatio;
        //
    }
}

void Precipitate::GrowthTwoElementNumeric(double _alpha, double const& _dt, double const& _T,\
                                          vector<Element> const& _SlowElements,vector<Element> const& _FastElements)
{
    //! Numeric resolution : we write our system as a function of only 1 Xi and we deduce it by algo. After we can have dr/dt
    //! the eq. that we have to solve is : a*pow(xi,(X+Y)/Y)+b*pow(xi,X/Y)+c*x+d=0 to have Xi and then dr/dt
    double d0_temp=_SlowElements[0].GetDiffusionCoefficient(_T)*boostPrecipitateDiffusion,d1_temp=_SlowElements[1].GetDiffusionCoefficient(_T)*boostPrecipitateDiffusion,d0=0.,d1=0.;
    double tempAspectRatio;
    if(shape==1)     {
        d0=d0_temp;
        d1=d1_temp;    }
    else if((shape==2)||(shape==6))  {
        d0=(3.0/(4.0*aspectRatio))*d0_temp;
        d1=(3.0/(4.0*aspectRatio))*d1_temp;
    }
    else if((shape==3)||(shape==4)) {
        d0=d0_temp*aspectRatio/2;
        d1=d1_temp*aspectRatio/2;
    }
    //else if(shape==4) {
    //    d0=d0_temp/4;
    //    d1=d1_temp/4;}
    else if(shape==5)  { //d0 and d1 are calculated for each radius after
        error.Fatal("FiskCylinder option valid only for debugging");
        d0=2*d0_temp*a0/M_PI;
        d1=2*d1_temp*a0/M_PI;
    }
    else error.Fatal("This shape is not implemented in growth 2 elements");
    
    //coeffDiffu=coeffDiffu0*aspectRatio/2;
    
    
    //Initialization of "multiFastXiPowerStoechio" term to correct after the Gibbs Thomson eq. with fast elements
    double multiFastXiPowerStoechio=0.,KsGT=0.;
    multiFastXiPowerStoechio=1;
    
    //We compute the multiplication of Xi^Stoechio (which=X0^Stoechio) for fastElements
    for (size_t j=0;j<_FastElements.size();j++) {
        multiFastXiPowerStoechio*=pow(_FastElements[j].GetSolidSolContent(),GetThisElementChemistry(_FastElements[j].GetName()));
    }
    //Initialization
    double chemistry0=GetThisElementChemistry(_SlowElements[0].GetName()), chemistry1=GetThisElementChemistry(_SlowElements[1].GetName());
    double xM0=_SlowElements[0].GetSolidSolContent(),                      xM1=_SlowElements[1].GetSolidSolContent();
    double xP0=chemistry0/atomsPerMolecule,                                xP1=chemistry1/atomsPerMolecule;
    double lowerBound=0.;
    double upperBound=xP0;
    //double upperBound=_alpha*xP0;
    double a=0.,b=0.,c=0.,d=0.,Xinterface0Solution=0.,dr_dt=0.;
    vector<double> CoeffNonLinEq(0);
    vector<vector<double> > nullVect; nullVect.push_back(CoeffNonLinEq);
    CoeffNonLinEq.assign(6,0);
    CoeffNonLinEq[4]=chemistry0;
    CoeffNonLinEq[5]=chemistry1;
    
    //For each radius we compure K(r) (that we divide by multiFastXiPowerStoechio) ans we can apply our non linear eq.
    double radiusI=0.;
    for (size_t i=0;i<nbOfClass;i++)    {
        radiusI=Radius[i];
        if (radiusI==0) {error.Fatal("we can't have radius equal to 0 in growth");}
        //Gibbs Thomson solubility corrected by fast elements
        
        // shape==5 AspectRatio depends on radiusI !
        if(shape==5)  {error.Fatal("FiskCylinder option valid only for debugging");
            tempAspectRatio=AspectRatioFromCylinderFunction(radiusI);
            d0=2*d0_temp*tempAspectRatio/M_PI;
            d1=2*d1_temp*tempAspectRatio/M_PI;    }
        KsGT=SolProdGibbsThomsonCalculation(_T,radiusI);
        KsGT=KsGT/multiFastXiPowerStoechio;
        //computation of coeff for non linear equation
        a=d1*xM1-d0*_alpha*xP1;                              CoeffNonLinEq[0]=a;
        b=d0*xM0*_alpha*xP1-d1*xM1*_alpha*xP0;               CoeffNonLinEq[1]=b;
        c=(d0-d1)*pow(KsGT,1.0/chemistry1);                  CoeffNonLinEq[2]=c;
        d=(d1*_alpha*xP0-d0*xM0)*pow(KsGT,1.0/chemistry1);   CoeffNonLinEq[3]=d;
        //we call an algorithm for the resolution
        if (nonLinearAlgorithm==1) {
            Xinterface0Solution=mathematic.newtonRaphson(lowerBound,upperBound,"2elementSphere",_alpha,CoeffNonLinEq,nullVect);}
        if (nonLinearAlgorithm==2) {
            Xinterface0Solution=mathematic.constrainedNewtonRaphson(lowerBound,upperBound,"2elementSphere",_alpha,CoeffNonLinEq,nullVect);}
        if (nonLinearAlgorithm==3) {
            Xinterface0Solution=mathematic.BrentAlgorithm(lowerBound,upperBound,"2elementSphere",_alpha,CoeffNonLinEq,nullVect);}
        if (nonLinearAlgorithm==4) {
            Xinterface0Solution=mathematic.Dichotomy(lowerBound,upperBound,"2elementSphere",_alpha,CoeffNonLinEq,nullVect);}
        
        //we return solution
        dr_dt=(d0/radiusI)*((xM0-Xinterface0Solution)/fabs(_alpha*xP0-Xinterface0Solution));
        Radius[i]+=dr_dt*_dt;
    }
}

void Precipitate::GrowthGeneral(double const _alpha, double const& _dt, double const& _T\
                                , vector<Element> const& _SlowElements,vector<Element> const& _FastElements)
{
    error.Fatal("Still a bug in GrowthGeneral resolution");
    //! Numeric resolution : we write our system as a function of only 1variable : dr/dt. After we after to find zero
    double coeffShape=0;
    double tempAspectRatio;
    
    if(shape==1) coeffShape=1;
    else if((shape==2)||(shape==6)) coeffShape=3.0/(4.0*aspectRatio);
    else if((shape==3)||(shape==4)) coeffShape=aspectRatio/2;
    //else if(shape==4) {coeffShape=1/4;}
    else if(shape==5) {error.Fatal("FiskCylinder option valid only for debugging");coeffShape=2*a0/M_PI;} //coeffShape is calculated for each radius after
    else {error.Fatal("This shape is not implemented in general growth");}
    
    //Initialization
    vector<double> slowElementChemistry(0),D(0),X0(0),XP(0);
    for (size_t j=0;j<_SlowElements.size();j++) {
        slowElementChemistry.push_back(GetThisElementChemistry(_SlowElements[j].GetName()));
        D.push_back(coeffShape*_SlowElements[j].GetDiffusionCoefficient(_T)*boostPrecipitateDiffusion);
        X0.push_back(_SlowElements[j].GetSolidSolContent());
        XP.push_back(slowElementChemistry[j]/atomsPerMolecule);
    }
    vector< vector<double> > Coeff(0);
    Coeff.push_back(slowElementChemistry); Coeff.push_back(D);                 Coeff.push_back(X0);               Coeff.push_back(XP);
    Coeff.push_back(vector<double>(0));    Coeff.push_back(vector<double>(0)); Coeff.push_back(vector<double>(0));
    Coeff[4].push_back(0);                 Coeff[5].push_back(0);              Coeff[6].push_back(0);
    vector<double> NullVect(0);
    //We compute the multiplication of Xi^Stoechio (which=X0^Stoechio) for fastElements
    double multiFastXiPowerStoechio=0.,KsGT=0.;
    multiFastXiPowerStoechio=1;
    for (size_t j=0;j<_FastElements.size();j++) {
        multiFastXiPowerStoechio*=pow(_FastElements[j].GetSolidSolContent(),GetThisElementChemistry(_FastElements[j].GetName()));
    }
    //For each radius we compute the extrems bounds and K(r) (that we divide by multiFastXiPowerStoechio) ans we can apply our non linear eq
    double dr_dt=0.,drdtLowerBound=0.,drdtUpperBound=0.,drdtTestmin=0.,drdtTestmax=0.;
    
    double radiusI;
    for (size_t i=0;i<nbOfClass;i++)    {
        radiusI=Radius[i];
        if (radiusI==0) {error.Fatal("we can't have radius equal to 0 in growth");}
        
        // shape==5 AspectRatio depends on radiusI !
        if(shape==5) {error.Fatal("FiskCylinder option valid only for debugging");
            tempAspectRatio=AspectRatioFromCylinderFunction(radiusI);
            coeffShape=2*tempAspectRatio/M_PI;}
        
        //calculation of GibbsThomson solubility modified by fast elements
        KsGT=SolProdGibbsThomsonCalculation(_T,radiusI);
        KsGT=KsGT/multiFastXiPowerStoechio;
        Coeff[4][0]=KsGT;
        Coeff[5][0]=_alpha;
        Coeff[6][0]=radiusI;
        
        //calculation of extrem bounds
        drdtLowerBound=1e300;  drdtUpperBound=1e-300;
        for (size_t j=0;j<_SlowElements.size();j++) {
            drdtTestmin=(D[j]*X0[j])/(radiusI*_alpha*XP[j]);
            drdtTestmax=-sqrt(2*D[j]/_dt);
            if (drdtTestmin<drdtLowerBound) {drdtLowerBound=drdtTestmin;}
            if (drdtTestmax>drdtUpperBound) {drdtUpperBound=drdtTestmax;}
        }
        //Call Brent's algorithm to find the root of non lin eq.
        if (nonLinearAlgorithm==1) {
            dr_dt=mathematic.newtonRaphson(drdtLowerBound,drdtUpperBound,"generalSphere",_alpha,NullVect,Coeff);}
        if (nonLinearAlgorithm==2) {
            dr_dt=mathematic.constrainedNewtonRaphson(drdtLowerBound,drdtUpperBound,"generalSphere",_alpha,NullVect,Coeff);}
        if (nonLinearAlgorithm==3) {
            dr_dt=mathematic.BrentAlgorithm(drdtLowerBound,drdtUpperBound,"generalSphere",_alpha,NullVect,Coeff);}
        if (nonLinearAlgorithm==4) {
            dr_dt=mathematic.Dichotomy(drdtLowerBound,drdtUpperBound,"generalSphere",_alpha,NullVect,Coeff);}
        
        Radius[i]+=dr_dt*_dt;
    }
}

void Precipitate::SuperSaturationCalculation(vector<Element> const& _Elements, double const& _T)
{
    //double Ks=exp(log(10.0)*(solProdB-solProdA/_T));
    //double Ks=exp(log(10.0)*(solProdB-solProdA/_T));
    double Ks=exp(log(10.0)*(solProdC/_T/_T+solProdB-solProdA/_T));
    double product=1.0;
    for (size_t i=0;i<sizeElement;i++)    {
        product*=pow(_Elements[i].GetSolidSolContent(),Chemistry[i]);
    }
    solubilityFraction=product/Ks;
    superSaturation=log(solubilityFraction);
}

void Precipitate::DrivingForceCalculation(double const& _T)
{
    double kBT=KB*_T;
    atomsPerMolecule=0;
    for (size_t i=0;i<sizeElement;i++)    {atomsPerMolecule+=Chemistry[i];}
    drivingForce=-kBT*superSaturation/(atomicVolume*atomsPerMolecule);
    //solubilityFraction=drivingForce;//1/log(product/Ks);
}

void Precipitate::RStarCalculation(double const& _T)
{
    if(shape==1) rStar=-2.0*surfaceEnergy/drivingForce;
    else if((shape==2)||(shape==6)) rStar=(-4.0*surfaceEnergy*aspectRatio)/(3.0*drivingForce*(aspectRatio-2.0/3.0));
    else if((shape==3)||(shape==4)) rStar=(-2.0*surfaceEnergy*(aspectRatio+2))/(3.0*drivingForce);
    //else if(shape==4) {
    //double tempAspectRatio=a0; // during nucleation, aspect ratio is constant and equal to a0
    //rStar=(-2.0*surfaceEnergy*(tempAspectRatio+2))/(3.0*drivingForce);}
    //rStar=(-2.0*surfaceEnergy*(aspectRatio+2))/(3.0*drivingForce);} // MP: here we use aspectRatio as a constant updated each timestep when the mean radius is calculated
    else if(shape==5) {
        error.Fatal("FiskCylinder option valid only for debugging");
        double tempAspectRatio=a0;
        rStar=-2.0*tempAspectRatio*surfaceEnergy/drivingForce;}
    else {error.Fatal("This shape is not implemented in Rstar calculation");}
}

void Precipitate::SortDistribution()
{
    vector<PrecipitateClass> vecPrecipitateClass;
    vecPrecipitateClass.reserve((nbOfClass));
    for(size_t i=0;i<nbOfClass;i++)  {vecPrecipitateClass.push_back(PrecipitateClass(Radius[i],Number[i]));}
    
    sort(vecPrecipitateClass.begin(),vecPrecipitateClass.end());
    
    Radius.clear(); Number.clear();
    for(size_t i=0; i<nbOfClass; ++i){
        Radius.push_back(vecPrecipitateClass[i].radius);
        Number.push_back(vecPrecipitateClass[i].number);
    }
}

void Precipitate::ClassManagement()
{
    if (!callClassManagement) {return;}
    if (classManagementType==1) {return;}
    if (classManagementType==2) {OldClassManagement();}
    else if (classManagementType==3) {LinClassManagement();}
    else if (classManagementType==4) {DistribClassManagement();}
    else if (classManagementType==5) {QuadClassManagement();}
    else if (classManagementType==6) {OldClassManagementWithLessClass();}
    else {error.Fatal("Uncorrect choice of class management method.");}
    for (size_t k=0;k<Number.size();k++) if(Number[k]<0){
        error.Warning("Class management leads to negative number of precipitate in a class :-(");
    }
}

void Precipitate::OldClassManagement()
{   //Creates new classes when spacing between 2 classes is too large.
    //The number of classes can only increase.
    
    // ################################################################
    //      To insert classes if space between two classes is too large
    // ################################################################
    vector<double> NewRadius; NewRadius.clear();
    vector<double> NewNumber; NewNumber.clear();
    NewRadius=Radius;
    NewNumber=Number;
    double minimumRadius=0, maximumRadius=0;
    size_t l=0;
    minimumRadius=1.0e300;
    maximumRadius=1.0e-300;
    double oldVolumeFraction=VolumeFraction();
    while (l<nbOfClass)    {
        if (NewRadius[l]>maximumRadius)  maximumRadius=NewRadius[l];
        if (NewRadius[l]<minimumRadius)  minimumRadius=NewRadius[l];
        l++;
    }
    size_t n=1;
    //--------------------------------------------------
    if (nbOfClass>2)    {
        double newRadiusNminus1=0.,newNumberNminus1=0.,newRadiusN=0.;
        double newNumberN=0.,newRadiusNplus1=0.,newNumberNplus1=0.,nextRadius=0.,presentRadius=0.;
        double newNumberNminus1INIT=0.;
        do        {
            if((fabs(NewRadius[n-1]-NewRadius[n])>(2.0*maximumRadius-2.0*minimumRadius)/targetClassNumber) && (fabs(NewRadius[n]-NewRadius[n+1])>NUMERICLIMITDOUBLE)&&((NewRadius[n+1]-NewRadius[n])*(NewRadius[n]-NewRadius[n-1])>0))
            {
                //we insert a line at the line 0 + n (we use begin to have a pointer..)
                NewRadius.insert(NewRadius.begin()+n,0);
                NewNumber.insert(NewNumber.begin()+n,0);
                // keep n+1 and n-1 radius
                newRadiusNplus1=NewRadius[n+1];
                newRadiusNminus1=NewRadius[n-1];
                // Conservation of distribution density induces i+1:
                newNumberNplus1=NewNumber[n+1];
                // we put the new class betwen the previous and next radius
                newRadiusN=0.5*(NewRadius[n+1]+NewRadius[n-1]);
                // Conservation of distribution density ‡ n-1 induces:
                newNumberNminus1INIT=NewNumber[n-1];
                newNumberNminus1=0.5*newNumberNminus1INIT;
                // Continuity of density
                nextRadius=NewRadius[n+2];
                presentRadius=NewRadius[n+1];
                newNumberN=0.25*(newNumberNplus1*(presentRadius-newRadiusNminus1)/(nextRadius-presentRadius)+newNumberNminus1INIT);
                NewRadius[n-1]=newRadiusNminus1;
                NewNumber[n-1]=newNumberNminus1;
                NewRadius[n]=newRadiusN;
                NewNumber[n]=newNumberN;
                NewRadius[n+1]=newRadiusNplus1;
                NewNumber[n+1]=newNumberNplus1;
                Number=NewNumber;
                Radius=NewRadius;
                n++;
            }
            n++;
        }while(n<Radius.size()-2);
        //-----------------calcul fraction precipitate------------
        Number=NewNumber;
        Radius=NewRadius;
        nbOfClass=Radius.size();
        double newVolumeFraction=VolumeFraction();
        //-----------------redimensionnement de chaque classe pour avoir fraction precipitÈ concervÈe---------
        for (size_t vvv=0;vvv<nbOfClass;vvv++) {Number[vvv]=Number[vvv]*(oldVolumeFraction/newVolumeFraction);}
    }
}

void Precipitate::OldClassManagementWithLessClass()
{   //Similar to old class management except that if there are too many classes, some are deleted, their numbers of precipitates being redistributed between the two adjacent ones.
    // #############################################################
    //      To insert classes if space between two is too large
    // #############################################################
    vector<double> NewRadius; NewRadius.clear();
    vector<double> NewNumber; NewNumber.clear();
    NewRadius=Radius;
    NewNumber=Number;
    double minimumRadius=0, maximumRadius=0;
    size_t l=0;
    minimumRadius=1.0e300;
    maximumRadius=1.0e-300;
    double oldVolumeFraction=VolumeFraction();
    while (l<nbOfClass)    {
        if (NewRadius[l]>maximumRadius)  maximumRadius=NewRadius[l];
        if (NewRadius[l]<minimumRadius)  minimumRadius=NewRadius[l];
        l++;
    }
    size_t n=1;
    //--------------------------------------------------
    if (nbOfClass>2)    {
        double newRadiusNminus1=0.,newNumberNminus1=0.,newRadiusN=0.;
        double newNumberN=0.,newRadiusNplus1=0.,newNumberNplus1=0.,nextRadius=0.,presentRadius=0.;
        double newNumberNminus1INIT=0.;
        do        {
            if((fabs(NewRadius[n-1]-NewRadius[n])>(2.0*maximumRadius-2.0*minimumRadius)/targetClassNumber) && (fabs(NewRadius[n]-NewRadius[n+1])>NUMERICLIMITDOUBLE)&&((NewRadius[n+1]-NewRadius[n])*(NewRadius[n]-NewRadius[n-1])>0))
            {
                //we insert a line at the line 0 + n (we use begin to have a pointeur..)
                NewRadius.insert(NewRadius.begin()+n,0);
                NewNumber.insert(NewNumber.begin()+n,0);
                // keep n+1 and n-1 radius
                newRadiusNplus1=NewRadius[n+1];
                newRadiusNminus1=NewRadius[n-1];
                // Conservation of distribution density induces i+1:
                newNumberNplus1=NewNumber[n+1];
                // we put the new class betwen the previous and next radius
                newRadiusN=0.5*(NewRadius[n+1]+NewRadius[n-1]);
                // Conservation of distribution density ‡ n-1 induces:
                newNumberNminus1INIT=NewNumber[n-1];
                newNumberNminus1=0.5*newNumberNminus1INIT;
                // Continuity of density
                nextRadius=NewRadius[n+2];
                presentRadius=NewRadius[n+1];
                newNumberN=0.25*(newNumberNplus1*(presentRadius-newRadiusNminus1)/(nextRadius-presentRadius)+newNumberNminus1INIT);
                if (newNumberN<0)
                    newNumberN=newNumberN;
                NewRadius[n-1]=newRadiusNminus1;
                NewNumber[n-1]=newNumberNminus1;
                NewRadius[n]=newRadiusN;
                NewNumber[n]=newNumberN;
                NewRadius[n+1]=newRadiusNplus1;
                NewNumber[n+1]=newNumberNplus1;
                Number=NewNumber;
                Radius=NewRadius;
                
                n++;
            }
            n++;
        }while(n<Radius.size()-2);
        //-----------------calcul fraction precipitate------------
        Number=NewNumber;
        Radius=NewRadius;
        nbOfClass=Radius.size();
        double newVolumeFraction=VolumeFraction();
        //-----------------redimensionnement de chaque classe pour avoir fraction precipitÈ concervÈe---------
        for (size_t vvv=0;vvv<nbOfClass;vvv++) {Number[vvv]=Number[vvv]*(oldVolumeFraction/newVolumeFraction);}
        
        // ######################################################
        //         To erase classes if they are too close
        // ######################################################
        
        nbOfClass=Radius.size();
        l=0;
        double RRR=0.;
        minimumRadius=1.0e300;
        maximumRadius=1.0e-300;
        while (l<nbOfClass)    {
            RRR=Radius[l];
            if (RRR>maximumRadius)  {maximumRadius=RRR;}
            if (RRR<minimumRadius)  {minimumRadius=RRR;}
            l++;
        }
        //------
        size_t k=0;
        do {
            if((fabs(Radius[k+1]-Radius[k])<0.5*(maximumRadius-minimumRadius)/targetClassNumber)&& (fabs(Radius[k+1]-Radius[k])>NUMERICLIMITDOUBLE)&&((Radius[k+2]-Radius[k+1])*(Radius[k+1]-Radius[k])>0))
            {
                Number[k]*=(Radius[k+2]-Radius[k])/(Radius[k+1]-Radius[k]);
                Number.erase(Number.begin()+(k+1));
                Radius.erase(Radius.begin()+(k+1));
                k--;
            }
            k++;
        }while(k<Number.size()-2);
        nbOfClass=Radius.size();
        newVolumeFraction=VolumeFraction();
        //-----------------redimensionnement de chaque classe pour avoir fraction precipitÈ concervÈe---------
        for (size_t vvv=0;vvv<nbOfClass;vvv++) {
            Number[vvv]=Number[vvv]*(oldVolumeFraction/newVolumeFraction);
            if (Number[vvv]<0)
                {
                    error.Warning("Class management leads to negative number of precipitate in a class :-(");
                }
        }
    }
}

void Precipitate::DistribClassManagement()
{   //Creates a linear distribution of radii between the min. and max radii from the given distribution.
    //Redistributes each old class in the two adjacent new ones using the lever rule on the number of precipitates
    //if(nbOfClass>0.9*targetClassNumber)
        //return;
    nbOfClass=Radius.size();
    // check if class managment should be run
    if(nbOfClass<2) return;
    if(nbOfClass<0.9*targetClassNumber)
        return;
    // Check if it is necessary to sort the distribution
    for(size_t i=1;i<nbOfClass;i++) if (Radius[i]<Radius[i-1]){
        SortDistribution();
        break;
    }
    double trueVolumeFraction=VolumeFraction();
    double trueMeanRadius=MeanRadius();
    
    // declare a copy of Radius and Number arrays
    vector<double> RadiusCopy=Radius;
    vector<double> NumberCopy=Number;
    // delete old Radius and Number arrays
    Radius.clear(); Number.clear();
    // create new Radius and Number arrays full of 0
    Radius.assign(targetClassNumber,0);
    Number.assign(targetClassNumber,0);
    
    double rMin=RadiusCopy[0];
    //double rMin=minDissolutionLimit;
    double rMax=RadiusCopy[nbOfClass-1];
    double dr=(rMax-rMin)/(targetClassNumber-1);
    
    // fill the new Radius array
    for(size_t i=0;i<targetClassNumber;i++) Radius[i]=rMin+static_cast<double>(i)*dr;
    // fill the new Number array
    size_t indexInf, indexSup;
    double index=0.;
    for(size_t i=0;i<nbOfClass;i++){
        index=(RadiusCopy[i]-rMin)/(rMax-rMin+1.e-12)*static_cast<double>(targetClassNumber-1); //The 1e-12 is to avoid that the last old class will be entirely redistributed to the last new class
        indexInf=static_cast<size_t>(index);
        indexSup=indexInf+1;
        //        if ((static_cast<double>(indexSup)-index)>(index-static_cast<double>(indexInf))) {
        //            Number[indexInf]+=NumberCopy[i];}
        //        else {
        //            Number[indexSup]+=NumberCopy[i];}
        Number[indexInf]+=NumberCopy[i]*(static_cast<double>(indexSup)-index);
        Number[indexSup]+=NumberCopy[i]*(index-static_cast<double>(indexInf));
    }
    nbOfClass=Radius.size();
    double currentMeanRadius=MeanRadius();
    
    //Normalization to keep mean radius constant
    for (size_t i=0;i<nbOfClass;i++) {Radius[i]*=trueMeanRadius/currentMeanRadius;}
    
    double currentVolumeFraction=VolumeFraction();
    //Normalization to keep volume fraction constant
    for (size_t i=0;i<nbOfClass;i++) {Number[i]*=trueVolumeFraction/currentVolumeFraction;}
}

void Precipitate::LinClassManagement()
{   //Linear class management. Creates a linear distribution of radii between the min. and max radii from the given distribution.
    //Interpolates linearly the densities in this new radius distribution.
    
    //we must have more than two classes to manage classes !
    if (nbOfClass<2) return;
    
    //we check if sorting is necessary
    for (size_t i=1;i<nbOfClass;i++)
        if (Radius[i]<Radius[i-1]){
            SortDistribution();
            break;
        }
    
    // Save current volume fraction and mean radius for normatisation at the end
    double trueVolumeFraction=VolumeFraction();
    double trueMeanRadius=MeanRadius();
    
    // calculation of current densityDistribution
    vector<double> DistributionCopy; DistributionCopy.clear();
    for (size_t i=0;i<nbOfClass-1;i++)
        DistributionCopy.push_back(Number[i]/fabs(Radius[i+1]-Radius[i]));
    DistributionCopy.push_back(Number[nbOfClass-1]/fabs(Radius[nbOfClass-1]-Radius[nbOfClass-2]));
    
    //calculation of the true number of precipitates
    double trueNumberOfPrecipitates=0;
    for (size_t i=0;i<nbOfClass;i++)
        trueNumberOfPrecipitates+=Number[i];
    
    // declare a copy of Radius and Number arrays
    vector<double> RadiusCopy=Radius;  Radius.clear();
    vector<double> NumberCopy=Number;  Number.clear();
    
    // create new Radius and Number arrays full of 0
    Radius.assign(targetClassNumber,0);
    Number.assign(targetClassNumber,0);
    
    //futur density
    vector<double> Density;  Density.clear();
    Density.assign(targetClassNumber,0);
    
    //parameters for new classes
    double rMin=RadiusCopy[0];
    //double rMin=RadiusCopy[0]*0.9; //for test
    double rMax=RadiusCopy[nbOfClass-1];
    //double rMax=RadiusCopy[nbOfClass-1]*1.1; //for test
    double dr=(rMax-rMin)/(targetClassNumber-1);
    
    // fill the new Radius array
    for(size_t i=0;i<targetClassNumber;i++) Radius[i]=rMin+static_cast<double>(i)*dr;
    
    // fill the max and min classes (numbers and density)
    Number[0]=DistributionCopy[0]*dr;
    Number[Number.size()-1]=DistributionCopy[DistributionCopy.size()-1]*dr;
    Density[0]=DistributionCopy[0];
    Density[Density.size()-1]=DistributionCopy[DistributionCopy.size()-1];
    
    //Interpolation of density
    double interpDensity=0.;
    for (size_t i=1;i<nbOfClass;i++){               //we loop to have interpolation between [i] and [i-1]
        for (size_t j=1;j<targetClassNumber-1;j++)  {                         //we fill classes [j]
            if(Radius[j]>RadiusCopy[i-1] && Radius[j]<=RadiusCopy[i]) {   //if they are between [i] and [i-1]
                interpDensity=mathematic.LinearInterpolation(Radius[j],RadiusCopy[i-1],\
                                                             RadiusCopy[i],DistributionCopy[i-1],DistributionCopy[i]);
                Number[j]=interpDensity*dr;
            }
        }
    }
    //Normalization to keep mean radius constant
    nbOfClass=Radius.size();
    double currentMeanRadius=MeanRadius();
    for (size_t i=0;i<nbOfClass;i++) Radius[i]*=trueMeanRadius/currentMeanRadius;
    
    //Normalization to keep volume fraction constant
    double currentVolumeFraction=VolumeFraction();
    for (size_t i=0;i<nbOfClass;i++) {Number[i]*=trueVolumeFraction/currentVolumeFraction;}
    
    //    double newNumberOfPrecipitates=0;
    //    for (size_t i=0;i<nbOfClass;i++) newNumberOfPrecipitates+=Number[i];
    //    double ratio=((newNumberOfPrecipitates-trueNumberOfPrecipitates)/(newNumberOfPrecipitates))/changeNumberInClass;
    //    if (ratio>1.0) error.Fatal("Change in the number of precipiates during class management higher than the prescribed value");
}


void Precipitate::QuadClassManagement()
{   //Similar to Linear class management but with a quadratic interpolation of the densities.
    
    /// \todo buggy function: check where mean radius and volume fractions are updated
    /// \warning Set the conditions (max and min number of class) to call class management or not. What happens, if there is no nucleation or in other special cases
    /// \todo Set the conditions (max and min number of class) to call class management or not. What happens, if there is no nucleation or in other special cases
    //we must have more than two classes to manage !
    if (nbOfClass<2) return;
    
    //we chack if the sorting is necessary
    for (size_t i=1;i<nbOfClass;i++){
        if (Radius[i]<Radius[i-1]){SortDistribution();break;}
    }
    
    // get target number of classes, save current volume fraction and mean radius
    double trueVolumeFraction=VolumeFraction();
    double trueMeanRadius=MeanRadius();
    
    // calculation of current densityDistribution
    vector<double> DistributionCopy; DistributionCopy.clear();
    for (size_t i=0;i<nbOfClass-1;i++) DistributionCopy.push_back(Number[i]/fabs(Radius[i+1]-Radius[i]));
    DistributionCopy.push_back(Number[nbOfClass-1]/fabs(Radius[nbOfClass-1]-Radius[nbOfClass-2]));
    
    //calculation of the true number of precipitates
    double trueNumberOfPrecipitates=0;
    for (size_t i=0;i<nbOfClass;i++) {trueNumberOfPrecipitates+=Number[i];}
    
    // declare a copy of Radius and Number arrays
    vector<double> RadiusCopy=Radius;  Radius.clear();
    vector<double> NumberCopy=Number;  Number.clear();
    
    // create new Radius and Number arrays full of 0
    Radius.assign(targetClassNumber,0);
    Number.assign(targetClassNumber,0);
    
    //parameters for new classes
    double rMin=RadiusCopy[0];
    double rMax=RadiusCopy[nbOfClass-1];
    double dr=(rMax-rMin)/(targetClassNumber-1);
    
    // fill the new Radius array
    for(size_t i=0;i<targetClassNumber;i++) {Radius[i]=rMin+static_cast<double>(i)*dr;}
    
    // fill the max and min classes (numbers)
    Number[0]=DistributionCopy[0]*dr;
    Number[targetClassNumber-1]=DistributionCopy[nbOfClass-1]*dr;
    
    double a=0.,b=0.,measuredDistance=0.,inter1=0.,inter2=0.,inter3=0.,distance=0.,radiusI=0.;
    size_t closerRPosition;
    // fill other classes (numbers)
    for (size_t i=1;i<(targetClassNumber-1);i++)    {
        //Searching the closer radius in the older radius vector
        distance=rMax-rMin;
        closerRPosition=0;
        radiusI=Radius[i];
        for (size_t j=0;j<nbOfClass;j++) {
            a=radiusI;
            b=RadiusCopy[j];
            measuredDistance=fabs(a-b);
            if (measuredDistance<distance)  {
                distance=fabs(radiusI-RadiusCopy[j]);
                closerRPosition=j;
            }
        }
        
        //Interpolating the distribution of precipitates, for bound the linear interpolation must be used
        if (closerRPosition==0) {
            inter1=mathematic.LinearInterpolation(radiusI,RadiusCopy[closerRPosition],\
                                                  RadiusCopy[closerRPosition+1],DistributionCopy[closerRPosition],DistributionCopy[closerRPosition+1]);
            Number[i]=inter1*dr;        }
        else if (closerRPosition==nbOfClass-1) {
            inter2=mathematic.LinearInterpolation(radiusI,RadiusCopy[closerRPosition-1],RadiusCopy[closerRPosition],\
                                                  DistributionCopy[closerRPosition-1],DistributionCopy[closerRPosition]);
            Number[i]=inter2*dr;        }
        //but in the middle we can use quadratic interpolation on density ! (more accurate!!!)
        else {
            inter3=mathematic.LagrangeInterpolation(radiusI,RadiusCopy[closerRPosition-1],\
                                                    RadiusCopy[closerRPosition],RadiusCopy[closerRPosition+1],DistributionCopy[closerRPosition-1],\
                                                    DistributionCopy[closerRPosition],DistributionCopy[closerRPosition+1]);
            //The quadratic interpolation can return negative values, in case a linear interpolation is used, though less precise
            if (inter3<0) inter3=mathematic.LinearInterpolation(radiusI,RadiusCopy[closerRPosition-1],RadiusCopy[closerRPosition+1],\
                                                                DistributionCopy[closerRPosition-1],DistributionCopy[closerRPosition+1]);
            Number[i]=inter3*dr;
        }
    }
    
    //Normalization to keep mean radius constant
    nbOfClass=Radius.size();
    double currentMeanRadius=MeanRadius();
    for (size_t i=0;i<nbOfClass;i++) {Radius[i]*=trueMeanRadius/currentMeanRadius;}
    
    //Normalization to keep volume fraction constant
    double currentVolumeFraction=VolumeFraction();
    for (size_t i=0;i<nbOfClass;i++) {Number[i]*=trueVolumeFraction/currentVolumeFraction;}
}

double Precipitate::VolumeFraction() const
{
    double volumeOfPrecipitates=0,radiusI;
    for(size_t i=0;i<nbOfClass;i++) {
        radiusI=Radius[i];
        if ((shape==5))     {//tempAspectRatio=AspectRatioFromCylinderFunction(radiusI);
            //volumeOfPrecipitates+=radiusI*radiusI*radiusI*Number[i]/tempAspectRatio;
            error.Fatal("Shape=5 i.e. variable aspect ratio to be implemented");
            volumeOfPrecipitates+=radiusI*radiusI*radiusI*Number[i]/aspectRatio;
        }
        else {volumeOfPrecipitates+=radiusI*radiusI*radiusI*Number[i];}
    }
    
    if (shape==1) volumeOfPrecipitates*=4.0/3.0*M_PI;
    else if((shape==2)||(shape==6)) volumeOfPrecipitates*=(aspectRatio-2.0/3.0)*M_PI;
    else if((shape==3)||(shape==4)) volumeOfPrecipitates*=2.0*M_PI/aspectRatio;
    //else if(shape==4)  {volumeOfPrecipitates*=2.0*M_PI;
    //error.Fatal("Volume of precipitates calculation not implemented for cylindrical precipitates with variable aspect ratio");
    //}
    else if(shape==5)  {error.Fatal("FiskCylinder option valid only for debugging");volumeOfPrecipitates*=2.0*M_PI;}
    else {error.Fatal("This shape is not implemented in VolumeFraction");}
    
    return volumeOfPrecipitates;
}

double Precipitate::MeanRadius() const
{
    double meanRadius=0.0,numberI,precipitatesSum=0;
    for (size_t i=0;i<nbOfClass;i++)    {
        numberI=Number[i];
        meanRadius+=numberI*Radius[i];
        precipitatesSum+=numberI;
    }
    if (precipitatesSum==0) {meanRadius=0;}
    else {meanRadius/=precipitatesSum;}
    
    return meanRadius;
}

double Precipitate::GetRStar() const {return rStar;}

void Precipitate::Dissolution()
{
    double radiusI=0.;
    if (shape!=1 && shape!=2 && shape!=3 && shape!=4 && shape!=5 && shape!=6) error.Fatal("Dissolution routine not defined for this shape");
    for (size_t i=0;i<nbOfClass;i++)    {
        radiusI=Radius[i];
        if (maxDissolutionLimit<=minDissolutionLimit) {
            if (radiusI<minDissolutionLimit || Number[i]<limitOfpreciInClassForDissolution)        {
                Radius.erase(Radius.begin()+i);
                Number.erase(Number.begin()+i);
                i--;
                nbOfClass=nbOfClass-1;
            }
        }
        else {
            if (radiusI<minDissolutionLimit || Number[i]<limitOfpreciInClassForDissolution)        {
                Radius.erase(Radius.begin()+i);
                Number.erase(Number.begin()+i);
                i--;
                nbOfClass=nbOfClass-1;            }
            else if (radiusI<maxDissolutionLimit) Number[i]*=(radiusI-minDissolutionLimit)/(maxDissolutionLimit-minDissolutionLimit);
        }
    }
}

size_t Precipitate::GetNumberOfClass() const {return nbOfClass;}

double Precipitate::GetNumber(size_t const& _index) const
{
    if (_index>nbOfClass){
        error.Fatal("Index is larger than size of Number vector");
        return 0;
    }
    if (nbOfClass==0) {return 0;}
    return Number[_index];
}

double Precipitate::GetRadius(size_t const& _index) const
{
    if (nbOfClass==0) {return 0;}
    return Radius[_index];
}

double Precipitate::TotalNumberOfPrecipitates() const
{
    double sumNi=0.;
    for (size_t i=0;i<nbOfClass;i++) {sumNi+=Number[i];}
    return sumNi;
}

double Precipitate::GetSolubilityFraction() const {return solubilityFraction;}

void Precipitate::SetBrentDichoAlgorithmTolerance(double const &_tolerance) {mathematic.SetTolerance_Brent_Dicho(_tolerance);}

void Precipitate::SetNewtonRaphsonAlgorithmTolerance(double const &_tolerance) {mathematic.SetTolerance_NewtonRaphson(_tolerance);}

void Precipitate::SetNRmaximumCount(double const &_maxNbIterations) {mathematic.SetNRmaximumCount(_maxNbIterations);}

void Precipitate::SetNonLinearAlgorithm(double &_algorithm) {nonLinearAlgorithm=_algorithm;}

void Precipitate::SetDiffusionCoefficientRatio(double const &_diffusionCoefficientRatio) {diffusionCoefficientRatio=_diffusionCoefficientRatio;}

void Precipitate::SetLimitOfpreciInClassForDissolution(double const &_limitNbDissolution) {limitOfpreciInClassForDissolution=_limitNbDissolution;}

void Precipitate::SetTargetClassNumber(unsigned int const &_targetClassNumber) {targetClassNumber=_targetClassNumber;}

void Precipitate::SetChangeNumberInClass(double const &_changeNumberInClass) {changeNumberInClass=_changeNumberInClass;}

void Precipitate::SetUnstationnaryNucleation(bool const &_unstationnaryNucleation) {unstationnaryNucleation=_unstationnaryNucleation;}

void Precipitate::SetClassManagementType(double &_classManagementType) {classManagementType=_classManagementType;}

void Precipitate::SetMinDissolutionLimit(double const &_minDissolutionLimit) {minDissolutionLimit=_minDissolutionLimit;}

void Precipitate::SetMaxDissolutionLimit(double const &_maxDissolutionLimit) {maxDissolutionLimit=_maxDissolutionLimit;}

void Precipitate::SetVolumeNode(double const& _volume) {volumeOfTheAssociedNode=_volume;}

double Precipitate::GetVolumeNode() const {return volumeOfTheAssociedNode;}

bool Precipitate::IsDormant() const {return dormant;}

double Precipitate::AspectRatioFromCylinderFunction (double const &_radius) const
{
    if (_radius<r1){
        return a0;
    }
    else if (_radius<r2) {
        return (a1*2*_radius+b1);
    }
    else {
        return (a2*2*_radius+b2);
    }
}

double Precipitate::AspectRatioFromRodFunction (double const &_radius) const
{
    double sss=b1/(1-a0*_radius);
    return b1/(1-a0*_radius);
}

void Precipitate::SetBoostPrecipitateDiffusion(double const &_boostPrecipitateDiffusion) {boostPrecipitateDiffusion=_boostPrecipitateDiffusion;}

//double  Precipitate::Erf(double x)
//{
//    // constants
//    double a11 =  0.254829592;
//    double a12 = -0.284496736;
//    double a13 =  1.421413741;
//    double a14 = -1.453152027;
//    double a15 =  1.061405429;
//    double p11  =  0.3275911;

//    // Save the sign of x
//    int sign = 1;
//    if (x < 0)
//        sign = -1;
//    x = fabs(x);

//    // A&S formula 7.1.26
//    double t = 1.0/(1.0 + p11*x);
//    double y = 1.0 - (((((a15*t + a14)*t) + a13)*t + a12)*t + a11)*t*exp(-x*x);

//    return sign*y;
//}

