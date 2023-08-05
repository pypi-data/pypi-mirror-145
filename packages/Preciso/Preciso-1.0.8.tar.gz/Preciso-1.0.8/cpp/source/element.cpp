/// \file element.cpp
/// \brief Methods of the class Element

#include <iostream>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string>
#include "element.h"
#include "matrix.h"
#include "constants.h"
#include "precipitate.h"

using namespace std;

Element::Element(vector<string> const& _arg, int _index)
{
    char* endCharact = NULL;
    name=_arg[1];
    contentWtPc=strtod(_arg[2].c_str(), &endCharact);
    if ((contentWtPc>100.)||(contentWtPc<0.)) error.Fatal("Invalid content in wt% for element: " + name);
    molarMass=strtod(_arg[3].c_str(), &endCharact);
    if (molarMass<0.) error.Fatal("Invalid molar mass for element: " + name);
    diffusionD0=strtod(_arg[4].c_str(), &endCharact);
    if (diffusionD0<0.) error.Fatal("Invalid diffusion D0 for element: " + name);
    diffusionQ=strtod(_arg[5].c_str(), &endCharact);
    if (diffusionQ<0.) error.Fatal("Invalid diffusion Q for element: " + name);
    index=_index;
    //The following default values should not be modified without discussion with all developpers.
    solidSolContent=0.;
    contentAtFrac=0.;
    simplifiedMassBalance=true;
    inflateDiffusionCoeff=1;
}

Element::~Element() {}

string Element::GetName() const { return name;}

double Element::SolidSolContentWtPercent(vector<Element> const& _Elements) const
{
    double sumSolidSolMolarMass=0.;
    for (size_t i=0;i<_Elements.size();i++) {sumSolidSolMolarMass+=_Elements[i].solidSolContent*_Elements[i].molarMass;}

    return 100.0*(solidSolContent*molarMass)/sumSolidSolMolarMass;
}

double Element::GetContentWtPc() const { return contentWtPc;}

double Element::GetContentAtFrac() const { return contentAtFrac;}

double Element::GetMolarMass() const { return molarMass;}

double Element::GetDiffusionD0() const { return diffusionD0;}

double Element::GetDiffusionQ() const { return diffusionQ;}

double Element::GetSolidSolContent() const { return solidSolContent;}

double Element::GetDiffusionCoefficient(double const& _T) const
{
    double RT=RGAZCONSTANT*_T;
    return diffusionD0*exp(-diffusionQ/RT);
}

void Element::SetName(string const& _name) {name=_name;}

void Element::SetIndex(size_t const& _index) {index=_index;}

void Element::SetContentWtPc(double const& _contentWtPc) {contentWtPc=_contentWtPc;}

void Element::SetMolarMass(double const& _molarMass) {molarMass=_molarMass;}

void Element::SetDiffusionD0(double const& _diffusionD0) {diffusionD0=_diffusionD0;}

void Element::SetDiffusionQ(double const& _diffusionQ) {diffusionQ=_diffusionQ;}

void Element::SetSolidSolContent(double const& _solidSolContent) {solidSolContent=_solidSolContent;}

void Element::SetContentAtFrac(double const& _contentAtFrac) {contentAtFrac=_contentAtFrac;}

void Element::SetFirstMassBalance(bool const booleenValue) {firstMassBalance=booleenValue;}

void Element::SetImprovedMassBalance() {simplifiedMassBalance=false;}

bool Element::GetSimplifiedMassBalance() {return simplifiedMassBalance;}

void Element::MassBalance(Matrix& _matrix, vector<Precipitate> &_Precipitates,vector<Element> const& _Elements)
{
    if (simplifiedMassBalance) {SimplifiedMassBalance(_matrix,_Precipitates);}
    else {GenericMassBalance(_matrix,_Precipitates,_Elements);}
}

void Element::GenericMassBalance(Matrix& _matrix, vector<Precipitate> &_Precipitates,vector<Element> const& _Elements)
{
    /// \warning This method modifies the attributes of elements, it should not be called before the time step is validated (or we must have tempElement)

    double sumFv=0, sumAlphaFv=0, sumXpAlphaFv=0, Xp=0,alpha=0,Fv=0;
    for (size_t i=0;i<_Precipitates.size();i++){
        Xp=_Precipitates[i].GetThisElementChemistry(name)/_Precipitates[i].GetAtomsPerMolecule();
        alpha=_matrix.GetAtomicVolumeSS()/_Precipitates[i].GetAtomicVolume();
        Fv=_Precipitates[i].VolumeFraction();
        sumFv+=Fv;
        sumAlphaFv+=alpha*Fv;
        sumXpAlphaFv+=Xp*alpha*Fv;
    }

 //   passer le mass balance pour tester les équation
// solidSolContent=contentAtFrac;
 solidSolContent=(contentAtFrac*(1-sumFv+sumAlphaFv)-sumXpAlphaFv)/(1-sumFv);

    if (firstMassBalance==true) {
        //f!=f false only for NaN (IEEE), isinf(n) return true is "n" is infinite
        if (solidSolContent>1 || solidSolContent<0 || solidSolContent!=solidSolContent || isinf(solidSolContent)) {
            error.Fatal("Initial Distribution leads to unphysical atomic fractions");
        }
    }
    //! We must run this after the massBalance on each elements to get the same alpha during one massBalance!!!
    //we must update VatSS when "solidSolContent" are updated
    //_matrix.SetAtomicVolumeSS(_Elements);
}

void Element::SimplifiedMassBalance(Matrix const& _matrix, vector<Precipitate> &_Precipitates)
{
    /// \warning This method modifies the attributes of elements, it should not be called before the time step is validated (or we must have tempElement)

    //Update the volume fractions
    vector<double> Alphas; Alphas.clear();
    for (size_t i=0;i<_Precipitates.size();i++)    {
        Alphas.push_back(_matrix.GetAtomicVolumeSS()/_Precipitates[i].GetAtomicVolume());
    }

    solidSolContent=contentAtFrac;
    double sumAlphaFv=0.;
    for (size_t i=0;i<_Precipitates.size();i++)    {
        //if (_Precipitates[i].GetThisElementChemistry(name)!=0.)        {
            solidSolContent-=Alphas[i]*_Precipitates[i].GetThisElementChemistry(name)/_Precipitates[i].GetAtomsPerMolecule()*_Precipitates[i].VolumeFraction();
            sumAlphaFv+=Alphas[i]*_Precipitates[i].VolumeFraction();
        //}
    }
    solidSolContent/=(1-sumAlphaFv);

    if (firstMassBalance==true) {
        //f!=f false only for NaN (IEEE), isinf(n) return true is "n" is infinite
        if (solidSolContent<0 || solidSolContent!=solidSolContent || isinf(solidSolContent)) {
            error.Fatal("X is not >0 for first massBalance, so initialDistrib have a problem");
        }
    }
}

void Element::Initialize(vector<Element> const& _Elements, Matrix& _matrix, vector<Precipitate> &_Precipitates,bool _firstCall)
{
    double sumContentsByMolarMass=0;
    for (size_t i=0;i<_Elements.size();i++) {sumContentsByMolarMass+=_Elements[i].contentWtPc/_Elements[i].molarMass;}
    contentAtFrac=(contentWtPc/molarMass)/(sumContentsByMolarMass);
    //Update the solid solution content accounting for potentiel initial distribution of precipitates
    if (_firstCall==false) {MassBalance(_matrix, _Precipitates,_Elements);}
}

void Element::SetInflateDiffusionCoeff(double const &_inflateDiffusionCoeff) {
    inflateDiffusionCoeff=_inflateDiffusionCoeff;
    diffusionD0=diffusionD0*inflateDiffusionCoeff;
}

double Element::GetInflateDiffusionCoeff() const {return inflateDiffusionCoeff;}
