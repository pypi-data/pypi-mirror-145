/// \file temperature.cpp
/// \brief Methods of the class Temperature
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include "temperature.h"
#include "constants.h"

using namespace std;

Temperature::Temperature()
{
    sizeTime=0;  Time.clear();  TemperatureValues.clear();
}
Temperature::~Temperature() {}

void Temperature::DefineTemperature(vector<string> const& _arg)  //Initialisation of the object
{
    char* endCharact = NULL;
    //Clear the vectors in case where the temperature are redefined for a node preciso
    Time.clear();   TemperatureValues.clear();

    for (size_t i=1;i<_arg.size()-2;i+=2){if(strtod(_arg[i+2].c_str(),&endCharact)<=strtod(_arg[i].c_str(),&endCharact)) {error.Fatal("Time value for temperature definition must be increasing");}}

    for (size_t i=1;i<_arg.size();i+=2)    {
        Time.push_back((strtod(_arg[i].c_str(),&endCharact)));
        if ((strtod(_arg[i].c_str(),&endCharact))<0.) {error.Fatal("Invalid time for time-temperature history");}
        TemperatureValues.push_back((strtod(_arg[i+1].c_str(),&endCharact)));
        if ((strtod(_arg[i+1].c_str(),&endCharact))<0.) {error.Fatal("Invalid temperature for time-temperature history");}
    }
    sizeTime=Time.size();
}

double Temperature::GetTemperature(double const& _time) const
{
    // ((_time<Time[0])||(_time>Time[sizeTime-1])) //be carful the last member is not Time[size()], is Time[size()-1]
    //so, if time is > (strictly) at Time[size()-1] then this time is out of range
    double timeI=0.;
    if ((_time<Time[0])||(_time>Time[sizeTime-1])) {
        error.Fatal("time out of range");
        return -1;    }
    else  {
        //the last member is sizeTime-1 but here we test sizeTime with < :(strictly less)
        //be carful for the linear interpolation we must don't enumerate the last indice because i+1 will be faulse
        for (size_t i=0;i<sizeTime;i++) {
            timeI=Time[i];
            if (_time==timeI) {return TemperatureValues[i];}
            else {
                if ((_time>timeI)&&(_time<Time[i+1])&&(i!=sizeTime-1))            {
                    return TemperatureValues[i]+((TemperatureValues[i+1]-TemperatureValues[i])/(Time[i+1]-timeI))*(_time-timeI);
                }
            }
        }
    }
    error.Fatal("Bad interpolation in GetTemperature");
    return -1;
}

double Temperature::GetTotalTime() const {return Time[sizeTime-1];}

double Temperature::GetInitialTime() const {return Time[0];}

double Temperature::GetAndCheckInitialTime() const
{
    double firstTime=Time[0];

    //-------we test if Temperature or Time vector is nul----------
    double testTime=0;
    for (size_t z=0;z<sizeTime;z++) {testTime=testTime+Time[z];}

    double testTemperature=0;
    for (size_t z=0;z<TemperatureValues.size();z++) {testTemperature=testTemperature+TemperatureValues[z];}

    if (testTime==0 || testTemperature==0) {error.Fatal("total time or Temperature is zero.");}

    return firstTime;
}

size_t Temperature::GetNumberOfTime() const {return sizeTime;}

double Temperature::GetTimeWithIndex(size_t const & _index) const
{
    if (_index>sizeTime-1) error.Fatal("Time index out of range");
    return Time[_index];
}
