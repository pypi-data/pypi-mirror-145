/// \file matrix.cpp
/// \brief Methods of the class Matrix
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include "constants.h"
#include "matrix.h"
#include "element.h"

using namespace std;

Matrix::Matrix()
{
    name=""; latticeParameter=0.; atomicVolume=0.; molarMass=0.;
    atomicVolumeSS=0.; //(must be changed after each massBalance)
    computationOfAtomicVolumeSS=true;
    volumeOfTheAssociedNode=1.;
}

Matrix::~Matrix() {}

void Matrix::DefineMatrix(vector<string> const& _arg)
{
    char* endCharact = NULL;
    name=_arg[1];
    latticeParameter=strtod(_arg[2].c_str(),&endCharact);
    if (latticeParameter<0.) {error.Fatal("Invalid lattice parameter for the matrix");}
    atomicVolume=strtod(_arg[3].c_str(),&endCharact);
    if (atomicVolume<0.) {error.Fatal("Invalid atomic volume for the matrix");}
    molarMass=strtod(_arg[4].c_str(),&endCharact);
    if (molarMass<0.) {error.Fatal("Invalid molar mass for the matrix");}
    //by default "atomicVolumeSS=atomicVolume" but for new management it will be updated in
    //"InitializeAtomicVolumeSS" and in "GenericMassBalance"
    atomicVolumeSS=atomicVolume;
}

string Matrix::GetName() const {return name;}

double Matrix::GetLatticeParameter() const {return latticeParameter;}

double Matrix::GetAtomicVolume() const {return atomicVolume;}

double Matrix::GetMolarMass() const {return molarMass;}

void Matrix::SetName(string const& _name) {name=_name;}

void Matrix::SetLatticeParameter(double const& _latticeParameter) {latticeParameter=_latticeParameter;}

void Matrix::SetAtomicVolume(double const& _atomicVolume) {atomicVolume=_atomicVolume;}

void Matrix::SetMolarMass(double const& _molarMass) {molarMass=_molarMass;}

double Matrix::GetAtomicVolumeSS() const {return atomicVolumeSS;}

void Matrix::SetAtomicVolumeSS(vector<Element> const& _Elements,bool _firstCall)
{
    if (computationOfAtomicVolumeSS)    {
        double sumOfIntersticialX=0.;double bbb=0.;
        string nameElement;
        //-1 because matrix is last element
        for (size_t i=0;i<_Elements.size()-1;i++)    {
            nameElement=_Elements[i].GetName();
            if (nameElement=="C" || nameElement=="N" || nameElement=="H")   {
                if (_firstCall){bbb=_Elements[i].GetContentAtFrac();}
                else {bbb=_Elements[i].GetSolidSolContent();}
                sumOfIntersticialX=sumOfIntersticialX+bbb;
            }
        }
        atomicVolumeSS=(1-sumOfIntersticialX)*atomicVolume;
    }
}

void Matrix::setVatSSbool(bool _VatSScomputation) {computationOfAtomicVolumeSS=_VatSScomputation;}

void Matrix::SetVolumeNode(double const& _volume) {volumeOfTheAssociedNode=_volume;}

double Matrix::GetVolumeNode() const {return volumeOfTheAssociedNode;}
