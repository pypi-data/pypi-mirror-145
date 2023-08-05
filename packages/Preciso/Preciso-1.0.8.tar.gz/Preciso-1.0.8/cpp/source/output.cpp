/// \file output.cpp
/// \brief Methods of the class Output
#include <iostream>
#include <string>
#include <string.h> //to use strncmp
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <fstream>
#include "input.h"
#include "error.h"
#include "precipitate.h"
#include "element.h"
#include "temperature.h"
#include "matrix.h"
#include "output.h"
#include "mechanical.h"
#include "constants.h"

using namespace std;

Output::Output()
{   // Default values
    firstCallStepOutputs=true; firstCallDistrib=true;  firstCallPlotDistrib=true;
    saveThermoEach=10;   saveDistribEach=10;    firstCallPlotThermo=true;
    plotDistribEach=10;  plotThermoEach=10;
    /// \warning By default we must have very high precision in inputs because if we round we can obtain "inf" for density
    outputPrecision=15;

    thermoOutputFile="resultsThermo"; distribOutputFile="distribution";
    // to detect coupling
    couplingDistribBool=false; couplingThermoBool=false;

    //test number of writing results
    nbOfThermoResults=0; nbOfDistribResults=0;

    //is we want to write mechanical results
    mechanicalOutputActived=false;
    //1for mechanical model1, 2 for model2...etc [see mechanical class]
    activedMicrostructuralModel=1;

    nodeToPlotDistrib=nodeToPlotThermo=nodeToPlotFinal=-1;

    heavyOuputs=false;
}

Output::~Output() {}

void Output::SetNodeToPlotDistrib(string const& _nodeIndexPlot) {nodeToPlotDistrib=atoi(_nodeIndexPlot.c_str());}

void Output::SetNodeToPlotThermo(string const& _nodeIndexPlot) {nodeToPlotThermo=atoi(_nodeIndexPlot.c_str());}

void Output::SetNodeToPlotFinal(string const& _nodeIndexPlot) {nodeToPlotFinal=atoi(_nodeIndexPlot.c_str());}

void Output::DefineThermoOutputs(vector<string> const& _arg)
{
    //for string argument we check the 8 first char to have more robust test
    //(because keyword with after a space can bug for example on some editors)
    thermoOutputFile=_arg[1];
    if (_arg[2].size()>7) {
        if (strncmp(_arg[2].c_str(),"coupling",8)==0) {couplingThermoBool=true;}
        else {error.Fatal("either 'savethermodynamics' don't begin by 'coupling' either nb is grather than 999999");}    }
    else {
        saveThermoEach=atoi(_arg[2].c_str());
        if (saveThermoEach<=0 || saveThermoEach>999999) {error.Fatal("'savethermodynamics' number argument must be in ]0,999999]");}
    }
}

void Output::DefineDistributionOutputs(vector<string> const& _arg)
{
    //for string argument we check the 8 first char to have more robust test
    //(because keyword with after a space can bug for example on some editors)
    distribOutputFile=_arg[1];
    if (_arg[2].size()>7) {
        if (strncmp(_arg[2].c_str(),"coupling",8)==0) {couplingDistribBool=true;}
        else {error.Fatal("either 'savedistribution' don't begin by 'coupling' either nb is grather than 999999");}    }
    else {
        saveDistribEach=atoi(_arg[2].c_str());
        if (saveDistribEach<=0 || saveDistribEach>999999) {error.Fatal("'savedistribution' number argument must be in ]0,999999]");}
    }
}

void Output::DefinePlotDistributionOutputs(vector<string> const& _arg, vector<Precipitate> const& _Precipitates)
{
    plotDistribEach=atoi(_arg[2].c_str());

    // fill the ThermoToPlot array to decide which precipitate data will be plotted
    DistribToPlot.assign(_Precipitates.size(),false);
    for(size_t i=3;i<_arg.size();i++) {
        if(_arg[i]=="all") {
            DistribToPlot.assign(_Precipitates.size(),true);
            break;            }
    }
    for(size_t j=0;j<_Precipitates.size();j++) for(size_t i=3;i<_arg.size();i++)
        if(_Precipitates[j].GetName()==_arg[i])
            DistribToPlot[j]=true;
}

void Output::DefinePlotThermoOutputs(vector<string> const& _arg,vector<Precipitate> const& _Precipitates)
{
    plotThermoEach=atoi(_arg[2].c_str());

    // fill the ThermoToPlot array to decide which precipitate data will be plotted
    ThermoToPlot.assign(_Precipitates.size(),false);
    for(size_t i=3;i<_arg.size();i++)
        if(_arg[i]=="all") {
            ThermoToPlot.assign(_Precipitates.size(),true);
            break;
        }
    for(size_t j=0;j<_Precipitates.size();j++) for(size_t i=3;i<_arg.size();i++)
        if(_Precipitates[j].GetName()==_arg[i])
            ThermoToPlot[j]=true;
}

void Output::DefinePlotFinalOutputs(vector<string> const& _arg,vector<Precipitate> const& _Precipitates)
{
    // fill the ThermoToPlot array to decide which precipitate data will be plotted
    FinalToPlot.assign(_Precipitates.size(),false);
    for(size_t i=2;i<_arg.size();i++)
        if(_arg[i]=="all") {
            FinalToPlot.assign(_Precipitates.size(),true);
            break;
        }
    for(size_t j=0;j<_Precipitates.size();j++) for(size_t i=2;i<_arg.size();i++)
        if(_Precipitates[j].GetName()==_arg[i])
            FinalToPlot[j]=true;
}

void Output::TimeStepOutput(Mechanical const& _mechanical,Matrix const& _matrix,vector<Element> const& _Elements,vector<Precipitate> const& _Precipitates,Temperature const& _temperatureObject, \
                            size_t const& _currentTimeIndex,double const& _time, double const& _temperature, double const& _dt, int const& timestep, size_t const& nodeIndex, bool _forceWriting)
{
    double lastTime=_temperatureObject.GetTotalTime();
    double timeMinusTimeIndex=fabs(_time-_temperatureObject.GetTimeWithIndex(_currentTimeIndex));
    double timeMinusLastTime=fabs(_time-lastTime);
    //#########################################################################################
    //#####--------- general results of precipitation and mechanical outputs -------------#####
    //#########################################################################################
    //if we want to write result at a specific time (coupling option)
    if (couplingThermoBool==true) {
        if (timeMinusTimeIndex<=NUMERICLIMITDOUBLE || timeMinusLastTime<=NUMERICLIMITDOUBLE || _forceWriting==true) {
            size_t nbOfTime=_temperatureObject.GetNumberOfTime();
            TimeStepThermoResults(_time, _dt, _temperature,_matrix, _Elements, _Precipitates, nodeIndex);
            if (mechanicalOutputActived)            {
                TimeStepMechanicalResults(_time, _dt, _temperature, _mechanical, _Elements, _Precipitates, nodeIndex);
            }
            nbOfThermoResults=nbOfThermoResults+1;
            if (_currentTimeIndex-1==nbOfTime && nbOfThermoResults!=nbOfTime) {error.Fatal("Nb of coupling ThermoResults must have same size as time vector");}
            if (firstCallStepOutputs){firstCallStepOutputs=false;}
        }
    }
    //if we want to save result each iterations
    else {
        if (timestep%saveThermoEach==0 || timeMinusLastTime<=NUMERICLIMITDOUBLE || _forceWriting==true)    {
            TimeStepThermoResults(_time, _dt, _temperature,_matrix, _Elements, _Precipitates, nodeIndex);
            if (mechanicalOutputActived)            {
                TimeStepMechanicalResults(_time, _dt,_temperature, _mechanical, _Elements, _Precipitates, nodeIndex);
            }
            if (firstCallStepOutputs){firstCallStepOutputs=false;}
        }
    }
    //#########################################################################################
    //#####------------------ distribution results of precipitation ----------------------#####
    //#########################################################################################
    // write distrib results at a specific time (coupling option)
    if (couplingDistribBool==true) {
        if (timeMinusTimeIndex<=NUMERICLIMITDOUBLE || timeMinusLastTime<=NUMERICLIMITDOUBLE || _forceWriting==true) {
            size_t nbOfTime=_temperatureObject.GetNumberOfTime();
            TimeStepDistributionResults(_time, _temperature,_Precipitates, nodeIndex);
            nbOfDistribResults=nbOfDistribResults+1;
            if (_currentTimeIndex-1==nbOfTime && nbOfDistribResults!=nbOfTime) {error.Fatal("Nb of coupling nbOfDistribResults must have same size as time vector");}
            if (firstCallDistrib){firstCallDistrib=false;}
        }
    }
    //if we want to save distribution each iterations
    else {
        if (timestep%saveDistribEach==0 || _forceWriting==true)    {
            TimeStepDistributionResults(_time, _temperature,_Precipitates, nodeIndex);
            if (firstCallDistrib){firstCallDistrib=false;}
        }
    }
    //#########################################################################################
    //#####------------------------ plotting GNUPLOT or OTHER ----------------------------#####
    //#########################################################################################
    // Plotting with GNUPLOT or other

    if ((nodeToPlotDistrib==nodeIndex)&&(timestep%plotDistribEach==0))    {
        PlotDistribution(_time, _temperature,_Precipitates);
        if (firstCallPlotDistrib){firstCallPlotDistrib=false;}
    }
    if ((nodeToPlotThermo==nodeIndex)&&(timestep%plotThermoEach==0)){
        PlotThermo(_time, _temperature,_Elements,_Precipitates);
        if (firstCallPlotThermo) firstCallPlotThermo=false;
    }
    if ((nodeToPlotFinal==nodeIndex) && timeMinusLastTime<=NUMERICLIMITDOUBLE) {
        FinalOutputPlot(_Elements,_Precipitates,_time,_temperature, _dt,timestep);

    }
    //#########################################################################################
}

void Output::TimeStepThermoResults(double const& _time, double const& _dt, double const& _temperature, Matrix const& _matrix,vector<Element> const& _Elements, vector<Precipitate> const& _Precipitates,size_t const& nodeIndex)
{
    //----------------------initializations------------------------
    ostringstream node,volumeNode;
    node << nodeIndex;
    volumeNode << _matrix.GetVolumeNode();
    string indexForNode = node.str(),nameElement,namePrecipitate;
    size_t sizeElements=_Elements.size(),sizePrecipitate=_Precipitates.size();
    string extension=".dat";
    string totalNameFile=thermoOutputFile+"_"+indexForNode+extension;
    //----------------------title writing------------------------
    if (firstCallStepOutputs)    {
        //Writing the file header
        ofstream file(totalNameFile.c_str(), ios::trunc);
        if(file)        {
            file.precision(outputPrecision);
            file << "Elements: ";
            for (size_t i=0;i<sizeElements-1;i++) {file << _Elements[i].GetName() << " ";}
            file << _Elements[sizeElements-1].GetName() << endl;
            file << "(volume=" << volumeNode.str() << "m3)";
            if (sizePrecipitate>0) {
                file << "Precipitates: ";
                for (size_t i=0;i<sizePrecipitate-1;i++) {file << _Precipitates[i].GetName() << " ";}
                file << _Precipitates[sizePrecipitate-1].GetName();
            }
            file << endl;
            //----------------------unit/legend writing------------------------
            file << "t[s] dt[s] T[K] ";

            if (heavyOuputs) {for (size_t i=0;i<sizeElements;i++) {nameElement=_Elements[i].GetName();file << "X_" << nameElement << " C_wtPer_" << nameElement << " ";}}
            else {for (size_t i=0;i<sizeElements;i++) {nameElement=_Elements[i].GetName();file << "X_" << nameElement << " ";}}

            for (size_t i=0;i<sizePrecipitate;i++)            {
                namePrecipitate=_Precipitates[i].GetName();    file << "rmean_" << namePrecipitate << "[m] ";
                file << "r*_" << namePrecipitate << "[m] ";    file << "fv_" << namePrecipitate << " ";
                file << "N_" << namePrecipitate << " ";        file << "Nclass_" << namePrecipitate << " ";
            }
            file << endl;
        }
        else {error.Warning("Unable to open file:"+totalNameFile+". Computation continues.");}
        file.close();
    }
    //----------------------write data------------------------
    ofstream file(totalNameFile.c_str(), ios::app);  //writing mode (app is to write at the end of the file without erase the content)
    if (!file) {error.Warning("Unable to open file:"+totalNameFile+". Computation continues.");}
    file.precision(outputPrecision);
    file << _time << " " << _dt << " " << _temperature << " ";

    if (heavyOuputs) {for (size_t i=0;i<sizeElements;i++) {file << _Elements[i].GetSolidSolContent() << " " << _Elements[i].SolidSolContentWtPercent(_Elements) << " ";};}
    else {for (size_t i=0;i<sizeElements;i++) {file << _Elements[i].GetSolidSolContent()  << " ";}}

    for (size_t i=0;i<sizePrecipitate;i++)    {
        file << _Precipitates[i].MeanRadius() << " ";        file << _Precipitates[i].GetRStar() << " ";
        file << _Precipitates[i].VolumeFraction() << " ";    file << _Precipitates[i].TotalNumberOfPrecipitates() << " ";
        file << _Precipitates[i].GetNumberOfClass() << " ";


        //#############################################
        // outputs for unstationnary nucleation publi
        //#############################################
        //file << _Precipitates[i].JS_publi << " ";
        //file << _Precipitates[i].incubationCoef_publi << " ";
        //file << _Precipitates[i].tau_publi << " ";
        //file << _Precipitates[i].dN_dt_publi << " ";
        //file << _Precipitates[i].dN_publi << " ";
        //file << _Precipitates[i].randomWalk_publi << " ";
        //file << _Precipitates[i].delta_publi << " ";
        //file << _Precipitates[i].Z_publi << " ";
        //file << _Precipitates[i].betaStar_publi << " ";
        //file << _Precipitates[i].rStarKbT_publi << " ";
        //file << _Precipitates[i].rStar_publi << " ";
        //#############################################

    }
    file << endl;    file.close();
    //------------------------------------------------------------
}

void Output::SetMechanicalModelWritting(int _modelKind) {activedMicrostructuralModel=_modelKind;}

void Output::TimeStepMechanicalResults(double const& _time, double const& _dt, double const& _temperature,Mechanical const& _mechanical,vector<Element> const& _Elements, vector<Precipitate> const& _Precipitates,size_t const& nodeIndex)
{
    //----------------------initializations------------------------
    ostringstream node,convertToString;
    node << nodeIndex;
    string indexForNode = node.str();
    string extension=".dat";
    size_t sizeElements=_Elements.size(),sizePrecipitate=_Precipitates.size();
    string totalNameFile=thermoOutputFile+"Mechanic_"+indexForNode+extension;
    vector<size_t> indexSS;indexSS.clear();
    //----------------------title writing------------------------
    if (firstCallStepOutputs)    {
        //Writing the file header
        ofstream file(totalNameFile.c_str(), ios::trunc);
        if(file)    {
            file.precision(outputPrecision);
            //----------------------initial yield---------------------
            convertToString << _mechanical.GetInitialYield();
            file << "Initial yield='" << convertToString.str() << "'" << endl;
            //----------------------Solid solution contribution---------------------
            file << "Elements SS contribution: ";
            //check which is a SS element and keep its index
            for (size_t i=0;i<sizeElements;i++) {if (fabs(_mechanical.GetSSconstantI(i))>NUMERICLIMITDOUBLE){indexSS.push_back(i);}}

            //write title for SS elements (if exist)
            if (indexSS.size()>0) {
                for (size_t i=0;i<indexSS.size();i++) {file << _Elements[indexSS[i]].GetName() << " [" << _mechanical.GetSSunitI(indexSS[i]) << "] ";}
                file << " " << endl;
            }
            else {file << "no SS contribution" << endl;}

            //----------------------Precipitate contribution---------------------
            if (sizePrecipitate>0) {
                file << "Precipitates: ";
                for (size_t i=0;i<sizePrecipitate-1;i++) {
                    ostringstream convertToString1;
                    convertToString1<< _mechanical.GetTransitionRadiusI(i);
                    file << _Precipitates[i].GetName() << " " << convertToString1.str();
                }
                ostringstream convertToString2;
                convertToString2 << _mechanical.GetTransitionRadiusI(sizePrecipitate-1);
                file << _Precipitates[sizePrecipitate-1].GetName() << " Rc=" << convertToString2.str() << "[m]" << endl;
            }
            //----------------------unit/legend writing------------------------
            file << "t[s] dt[s] T[K] SigmaDislo[MPa] SigmaSS[MPa] SigmaGrain[MPa] SigmaPreciTOT[MPa] sigmaFlowMicro[MPa] ";
            for (size_t i=0;i<sizePrecipitate;i++) {file << "sigma" << _Precipitates[i].GetName() << "[MPa] ";}
            for (size_t i=0;i<sizePrecipitate;i++) {file << "sigma" << _Precipitates[i].GetName() << "_sh[MPa] ";}
            for (size_t i=0;i<sizePrecipitate;i++) {file << "sigma" << _Precipitates[i].GetName() << "_bp[MPa] ";}

            //----------------------if hardening coupling------------------------
            bool fullMechanicalCoupling=_mechanical.GetMechanicalHardeningCoupling();
            if (fullMechanicalCoupling) {
                int hardeningModelChosen=_mechanical.GetHardeningModel();
                if (hardeningModelChosen>=1 && hardeningModelChosen<=8) {
                    file << "strain[] flowStress[MPa] isotropHard[MPa] kinematicHard[MPa]";
                }
                else if (hardeningModelChosen>=9 && hardeningModelChosen<=15) {
                    file << "epsP[] epsPcum[] dislo[m^-2] disloPPT[m^-2] nG[] X_G[MPa] nPPT[] Xppt[MPa] R[MPa]";
                }
                else if (hardeningModelChosen==16) {
                    file << "epsP[] epsPcum[] dislo[m^-2] nG[] X_G[MPa] R[MPa]";
                }
                else {error.Fatal("hardening model not implemented in 'output.TimeStepMechanicalResults'");}
            }
            //-------------------------------------------------------------------
            file << endl;
            file.close();
        }
        else {error.Warning("Unable to open file:"+totalNameFile+". Computation continues.");}
    }
    //----------------------write data------------------------
    ofstream file(totalNameFile.c_str(), ios::app);  //writing mode (app is to write at the end of the file without erase the content)
    if (!file) {error.Warning("Unable to open file:"+totalNameFile+". Computation continues.");}
    file.precision(outputPrecision);
    file << _time << " " << _dt << " " << _temperature << " " << _mechanical.GetSigmaDislo()*1e-6 << " ";
    file << _mechanical.GetSigmaSS()*1e-6 << " "  << _mechanical.GetSigmaGrain()*1e-6 << " " << _mechanical.GetSigmaPreci()*1e-6 << " " << _mechanical.GetsigmaFlowMicro()*1e-6 << " ";
    for (size_t i=0;i<sizePrecipitate;i++) {file << _mechanical.GetSigmaPreciI(i)*1e-6 << " ";}
    for (size_t i=0;i<sizePrecipitate;i++) {file << _mechanical.GetSigmaPreciIsh(i)*1e-6 << " ";}
    for (size_t i=0;i<sizePrecipitate;i++) {file << _mechanical.GetSigmaPreciIbp(i)*1e-6 << " ";}
    //----------------------if hardening coupling------------------------
    bool fullMechanicalCoupling=_mechanical.GetMechanicalHardeningCoupling();
    if (fullMechanicalCoupling) {
        int hardeningModelChosen=_mechanical.GetHardeningModel();
        if (hardeningModelChosen>=1 && hardeningModelChosen<=8) {
            ostringstream strain,stress,X,R;
            strain << _mechanical.GetCurrentStrain();
            stress << _mechanical.GetCurrentStressMechanic()*1e-6;
            R << _mechanical.GetIsotropHardening()*1e-6;
            X << _mechanical.GetKinematicHardening_phenomeno()*1e-6;
            file << strain.str() << " " << stress.str() << " " << R.str() << " " << X.str() << " ";
        }
        else if (hardeningModelChosen>=9 && hardeningModelChosen<=15) {
            ostringstream epsP,epsPcum,dislo,disloPPT,nG,X_G,n_ppt,Xppt,R;
            epsP << _mechanical.Get_epsP();
            epsPcum << _mechanical.Get_epsPcum();
            dislo << _mechanical.Get_dislo();
            disloPPT << _mechanical.Get_disloPPT();
            nG << _mechanical.Get_nG();
            X_G << _mechanical.Get_X_G()*1e-6;
            n_ppt << _mechanical.Get_n_ppt();
            Xppt << _mechanical.Get_Xppt()*1e-6;
            R << _mechanical.GetIsotropHardening()*1e-6;
            file << epsP.str() << " " << epsPcum.str() << " " << dislo.str() << " " << disloPPT.str() << " " << nG.str() << " " \
                 << X_G.str() << " " << n_ppt.str() << " " << Xppt.str() << " " << R.str() << " ";
        }
        else if (hardeningModelChosen==16) {
            ostringstream epsP,epsPcum,dislo,nG,X_G,R;
            epsP << _mechanical.Get_epsP();
            epsPcum << _mechanical.Get_epsPcum();
            dislo << _mechanical.Get_dislo();
            nG << _mechanical.Get_nG();
            X_G << _mechanical.Get_X_G()*1e-6;
            R << _mechanical.GetIsotropHardening()*1e-6;
            file << epsP.str() << " " << epsPcum.str() << " " << dislo.str() << " " << nG.str() << " " \
                 << X_G.str() << " " << R.str() << " ";
        }
        else {error.Fatal("hardening model not implemented in 'output.TimeStepMechanicalResults'");}
    }
    //-------------------------------------------------------------------
    file << endl;
    file.close();
    //------------------------------------------------------------
}

void Output::TimeStepDistributionResults(double const& _time, double const& _temperature, vector<Precipitate> const& _Precipitates,size_t const& nodeIndex)
{
    ostringstream node;
    node << nodeIndex;
    string indexForNode = node.str(),extension,totalNameFile;
    size_t nbOfClassI;
    for (size_t i=0;i<_Precipitates.size();i++)    {
        nbOfClassI=_Precipitates[i].GetNumberOfClass();
        extension=".dat";
        totalNameFile=distribOutputFile+_Precipitates[i].GetName()+"_"+indexForNode+extension;

        if (firstCallDistrib)        {
            //Erasing the previous result file
            ofstream file(totalNameFile.c_str(), ios::trunc);
            if(!file) {error.Warning("Unable to open file:"+totalNameFile+". Computation continues.");}
            file << "R*(t) R(i) R(i+1) ..." << endl;
            file << "t[s] N(i) N(i+1) ..." << endl;
            file << "t[s] D(i) D(i+1) ..." << endl;
            file.close();
        }

        ofstream file(totalNameFile.c_str(), ios::app);  //writing mode (app is to write at the end of the file without erase the content)
        if (!file) error.Warning("Unable to open file:"+totalNameFile+". Computation continues.");
        file.precision(outputPrecision);
        
        double Nmin=pow(10,-outputPrecision);
        
        if (nbOfClassI>1)
        {//If there are more than 2 classes, the radii, number and distribution of each class are written in lines
            double rStar=_Precipitates[i].GetRStar();
            file << rStar << " ";
            for (size_t j=0;j<(nbOfClassI-1);j++) if(_Precipitates[i].GetNumber(j)>Nmin)            {
                file << _Precipitates[i].GetRadius(j)<< " ";
            }
            size_t index=nbOfClassI-1;
            file << _Precipitates[i].GetRadius(index) << endl;

            file << _time << " ";
            for (size_t j=0;j<(nbOfClassI-1);j++) if(_Precipitates[i].GetNumber(j)>Nmin)           {
                file << _Precipitates[i].GetNumber(j)<< " ";
            }
            index=nbOfClassI-1;
            file << _Precipitates[i].GetNumber(index) << endl;

            //            if (firstCallDistrib) {
            //                file << _time << " ";
            //                for (size_t j=0;j<(nbOfClassI-1);j++){file << "0.0 ";}
            //                file << "0.0" << endl;
            //            }
            //            else {
            file << _time << " ";
            for (size_t j=0;j<(nbOfClassI-1);j++) if(_Precipitates[i].GetNumber(j)>Nmin)           {
                file << _Precipitates[i].GetNumber(j)/fabs(_Precipitates[i].GetRadius(j+1)-_Precipitates[i].GetRadius(j)) << " ";
            }
            index=nbOfClassI-1;
            file << _Precipitates[i].GetNumber(index)/fabs(_Precipitates[i].GetRadius(index-1)-_Precipitates[i].GetRadius(index)) << endl;
            //            }
        }
        else if (nbOfClassI==0)
        {//When there is zero class we put all 0 at 0
            file << _time << " ";
            file << "0.0" << endl;

            file << _time << " ";
            file << "0.0" << endl;

            file << _time << " " << "0.0" << endl;
        }
        else if (nbOfClassI==1)
        {//When there is only one class only the radius and number are written
            file << _time << " ";
            file << _Precipitates[i].GetRadius(0) << endl;
            file << _time << " ";
            file << _Precipitates[i].GetNumber(0) << endl;
            file << _time << " " << "0.0" << endl;
        }
        file.close();
    }
}

void Output::PlotDistribution(double const& _time, double const& _temperature, vector<Precipitate> const& _Precipitates)
{
    //targetClassNumber here is only used for size of plot in gnuplot. It is set to the default value, 500.
    int targetClassNumber=500;
    string gnuplotTerminal=LIVEGNUPLOTTERMINAL;
    string gnuplotPath=GNUPLOTPATH;

    if (firstCallPlotDistrib)    {
        #ifdef _WIN32
            gnuplotDistrib=_popen(gnuplotPath.c_str(),"w");
        #else
            gnuplotDistrib=popen(gnuplotPath.c_str(),"w");
        #endif
        
        if (!gnuplotDistrib) error.Warning("Unable to open gnuplot. Computation continues.");
        fprintf(gnuplotDistrib, "set terminal %s\n",gnuplotTerminal.c_str());
        //fprintf(gnuplotDistrib,"set size 1.0, 1.0\n");
        //fprintf(gnuplotDistrib,"set xrange [0:%e]\n",xmax);
        fprintf(gnuplotDistrib,"set xrange [0:]\n");
        //fprintf(gnuplotDistrib,"set yrange [0:%e]\n",ymax);
        fprintf(gnuplotDistrib,"set boxwidth %e\n", 4e-10/targetClassNumber);
    }

    unsigned int numberOfDistributionToPlot=0;
    for (size_t j=0;j<DistribToPlot.size();j++) if (DistribToPlot[j]==true) numberOfDistributionToPlot++;
    fprintf(gnuplotDistrib,"set multiplot layout %i,1\n",numberOfDistributionToPlot);

    if (DistribToPlot.size()>0) for(size_t j=0;j<_Precipitates.size();j++) if (DistribToPlot[j]==true)    {
        double rStar=_Precipitates[j].GetRStar();

        fprintf(gnuplotDistrib,"set format x \"%%g\"\n");
        //fprintf(gnuplotDistrib,"set origin 0.0, %f\n",static_cast<double>(j)/_Precipitates.size());
        //fprintf(gnuplotDistrib,"set size 1.0, %f\n",1.0/_Precipitates.size());
        fprintf(gnuplotDistrib,"set title \"%s - time(s)=%.4f\"\n",_Precipitates[j].GetName().c_str(),_time);
        fprintf(gnuplotDistrib,"plot '-' t \"Sub-critical\" w boxes ,'-' t \"Super-critical\" w boxes lt 3\n");
        fprintf(gnuplotDistrib,"0 0 \n");
        // Plot sub-critical classes
        for (size_t i=1;i<_Precipitates[j].GetNumberOfClass();i++) if (_Precipitates[j].GetRadius(i) < rStar) {
            fprintf(gnuplotDistrib,"%.20E %.20E\n", _Precipitates[j].GetRadius(i), _Precipitates[j].GetNumber(i)/fabs( _Precipitates[j].GetRadius(i-1)- _Precipitates[j].GetRadius(i)));
        }
        fprintf(gnuplotDistrib,"e\n");
        // Plot super-critical classes
        fprintf(gnuplotDistrib,"0 0 \n");
        for (size_t i=1;i<_Precipitates[j].GetNumberOfClass();i++) if (_Precipitates[j].GetRadius(i) > rStar) {
            fprintf(gnuplotDistrib,"%.20E %.20E\n", _Precipitates[j].GetRadius(i), _Precipitates[j].GetNumber(i)/fabs( _Precipitates[j].GetRadius(i-1)- _Precipitates[j].GetRadius(i)));
        }
        fprintf(gnuplotDistrib,"e\n");
    }
    if(_Precipitates.size()>1) {fprintf(gnuplotDistrib,"unset multiplot\n");}
    fflush(gnuplotDistrib);
}

void Output::PlotThermo(double const& _time, double const& _temperature, vector<Element> const& _Elements, vector<Precipitate> const& _Precipitates)
{
    string gnuplotPath=GNUPLOTPATH;
    string gnuplotTerminal=LIVEGNUPLOTTERMINAL;
    if (firstCallPlotThermo){
        #ifdef _WIN32
            gnuplotThermo=_popen(gnuplotPath.c_str(),"w");
        #else
            gnuplotThermo=popen(gnuplotPath.c_str(),"w");
        #endif
        if (!gnuplotThermo) {error.Warning("Unable to open gnuplot. Computation continues.");}
       fprintf(gnuplotThermo, "set terminal %s\n",gnuplotTerminal.c_str());
        fprintf(gnuplotThermo, "set output 'results.eps'\n");
    }
    // Plot 6 graphs in the window (2*3)
    fprintf(gnuplotThermo,"set multiplot layout 2,3\n");
    GnuPlotThermo(_time,_temperature,_Elements,_Precipitates);
    fprintf(gnuplotThermo,"unset multiplot\n");
}

void Output::FinalOutputPlot(vector<Element> const& _Elements,vector<Precipitate> const& _Precipitates, double const& _time, double const& _temperature, double const& _dt, int const& timestep)
{
    string gnuplotPath=GNUPLOTPATH;
    string gnuplotTerminal=FINALGNUPLOTTERMINAL;

    //    if(plotFinal==true){
    //        if(plotThermo==false) {
    #ifdef _WIN32
        gnuplotThermo=_popen(gnuplotPath.c_str(),"w");
    #else
        gnuplotThermo=popen(gnuplotPath.c_str(),"w");
    #endif
    
    if (!gnuplotThermo) {error.Warning("Unable to open gnuplot. Computation continues.");}
    //        }
    fprintf(gnuplotThermo, "set terminal %s\n",gnuplotTerminal.c_str());
    fprintf(gnuplotThermo, "set output 'Results.eps'\n");
    fprintf(gnuplotThermo, "set size .75,.75\n");
    fflush(gnuplotThermo);
    ThermoToPlot=FinalToPlot;
    GnuPlotThermo(_time,_temperature,_Elements,_Precipitates);
    #ifdef _WIN32
        _pclose(gnuplotThermo);
    #else
        pclose(gnuplotThermo);
    #endif
    
    //    }
    //    else if(plotThermo==true) {pclose(gnuplotThermo);}

}


void Output::GnuPlotThermo(double const& _time, double const& _temperature, vector<Element> const& _Elements, vector<Precipitate> const& _Precipitates)
{
    ostringstream node;
    node << nodeToPlotThermo;

    string thermoFileName=thermoOutputFile+"_"+node.str()+".dat";
    bool firstTime;
    unsigned int column;
    unsigned int nElements=static_cast<unsigned int>(_Elements.size());

    fprintf(gnuplotThermo,"set format y \"%%g\"\n");
    fprintf(gnuplotThermo,"set xlabel \"Time (s)\"\n");
    // Plot timestep => column 2
    fprintf(gnuplotThermo,"set ylabel \"Time Step (s)\"\n");
    fprintf(gnuplotThermo,"set logscale\n");
    fprintf(gnuplotThermo,"plot '%s' u 1:2 t \"dt\" w l lw 2\n",thermoFileName.c_str());
    // Plot mean radius and R* => column 4 + nElements
    fprintf(gnuplotThermo,"set ylabel \"Radius (m)\"\n");
    fprintf(gnuplotThermo,"set logscale\n");
    firstTime=true;
    column=4+nElements;
    if (DistribToPlot.size()>0) for(size_t j=0;j<_Precipitates.size();j++) if (ThermoToPlot[j]==true){
        if(firstTime){
            fprintf(gnuplotThermo,"plot ");
            firstTime=false;
        }
        else fprintf(gnuplotThermo,",");
        fprintf(gnuplotThermo,"'%s' u 1:%i t \"%s (<R>)\" w l lw 2,'%s' u 1:%i t \"%s (R*)\"w l lw 1",thermoFileName.c_str(),column+5*static_cast<unsigned int>(j),_Precipitates[j].GetName().c_str(),thermoFileName.c_str(),column+5*static_cast<unsigned int>(j)+1,_Precipitates[j].GetName().c_str());
    }
    fprintf(gnuplotThermo,"\n");

    // Plot Number density => column 7 + nElements
    fprintf(gnuplotThermo,"set ylabel \"Number density (#/m^3)\"\n");
    fprintf(gnuplotThermo,"set logscale\n");
    firstTime=true;
    column=7+nElements;
    if (DistribToPlot.size()>0) for(size_t j=0;j<_Precipitates.size();j++) if (ThermoToPlot[j]==true){
        if(firstTime){
            fprintf(gnuplotThermo,"plot ");
            firstTime=false;
        }
        else fprintf(gnuplotThermo,",");
        fprintf(gnuplotThermo,"'%s' u 1:%i t \"%s\" w l lw 2",thermoFileName.c_str(),column+5*static_cast<unsigned int>(j),_Precipitates[j].GetName().c_str());
    }
    fprintf(gnuplotThermo,"\n");
    // Plot element solute content => column 4
    fprintf(gnuplotThermo,"set ylabel \"Solute content (at. frac.)\"\n");
    fprintf(gnuplotThermo,"set logscale\n");
    firstTime=true;
    column=4;
    for(size_t j=0;j<_Elements.size();j++){
        if(firstTime){
            fprintf(gnuplotThermo,"plot ");
            firstTime=false;
        }
        else fprintf(gnuplotThermo,",");
        fprintf(gnuplotThermo,"'%s' u 1:%i t \"%s\" w l lw 2",thermoFileName.c_str(),column+static_cast<unsigned int>(j),_Elements[j].GetName().c_str());
    }
    fprintf(gnuplotThermo,"\n");

    // Plot precipitate volume fraction => column 6 + nElements
    fprintf(gnuplotThermo,"set ylabel \"Precipitate volume fraction\"\n");
    fprintf(gnuplotThermo,"unset logscale y\n");
    firstTime=true;
    column=6+nElements;
    if (DistribToPlot.size()>0) for(size_t j=0;j<_Precipitates.size();j++)if (ThermoToPlot[j]==true){
        if(firstTime){
            fprintf(gnuplotThermo,"plot ");
            firstTime=false;
        }
        else fprintf(gnuplotThermo,",");
        fprintf(gnuplotThermo,"'%s' u 1:%i t \"%s\" w l lw 2",thermoFileName.c_str(),column+5*static_cast<unsigned int>(j),_Precipitates[j].GetName().c_str());
    }
    fprintf(gnuplotThermo,"\n");

    // Plot class number => column 8 + nElements
    fprintf(gnuplotThermo,"set ylabel \"Number of classes\"\n");
    fprintf(gnuplotThermo,"unset logscale y\n");
    firstTime=true;
    column=8+nElements;
    if (ThermoToPlot.size()>0)for(size_t j=0;j<_Precipitates.size();j++)if (ThermoToPlot[j]==true){
        if(firstTime){
            fprintf(gnuplotThermo,"plot ");
            firstTime=false;
        }
        else fprintf(gnuplotThermo,",");
        fprintf(gnuplotThermo,"'%s' u 1:%i t \"%s\" w l lw 2",thermoFileName.c_str(),column+5*static_cast<unsigned int>(j),_Precipitates[j].GetName().c_str());
    }
    fprintf(gnuplotThermo,"\n");
    fflush(gnuplotThermo);
}

void Output::SetOutputPrecision(double const &_tolerance) {outputPrecision=_tolerance;}

void Output::SetActivationOfMechanicalOutputs(bool _active) {mechanicalOutputActived=_active;}

void Output::SetHeavyOuputs(bool _boolLightOrHeavyOutputs) {heavyOuputs=_boolLightOrHeavyOutputs;}

void Output::HardeningResults(bool _initialCall,bool uncoupledMechanic, double const& currentTimeFromPreciSo, \
                              Mechanical const& _mechanical,size_t const& nodeIndex,vector<vector<double> > const& UncoupledResults)
{
    //----------------------initializations------------------------
    ostringstream node;
    node << nodeIndex;
    string indexForNode = node.str();
    vector<string> nameAndExtensionOfFile=_mechanical.GetNameExtensionHardeningFile();
    string totalNameFile=nameAndExtensionOfFile[0]+"_node"+indexForNode+".dat";
    int hardeningModelChosen=_mechanical.GetHardeningModel();
    //----------------------title writing------------------------
    if(_initialCall)   {
        ofstream file(totalNameFile.c_str(), ios::trunc);
        if(file)     {
            file.precision(outputPrecision);
            file << "time[s] eps[] sig[MPa] ";
            if (hardeningModelChosen>=1 && hardeningModelChosen<=8) {
                file << "yield[MPa] R[MPa] X[MPa] ";
            }
            else if(hardeningModelChosen>=9 && hardeningModelChosen<=15) {
                file << "epsP[] epsPcum[] dislo[m^-2] disloPPT[m^-2] nG[] X_G[MPa] nPPT[] Xppt[MPa] R[MPa] 'fv_bp[0]' 'meanL_bp[0]' 'distanceBetweenPPT[0]'";
            }
            else if(hardeningModelChosen==16) {
                file << "epsP[] epsPcum[] dislo[m^-2] nG[] X_G[MPa] R[MPa] 'fv_bp[0]'";
            }
            else {error.Fatal("hardening model not implemented in 'output.HardeningResults'");}
        }
        else {error.Warning("Unable to open file:"+totalNameFile+". Computation continues.");}
        file << endl;
        file.close();
    }
    //-----------------RESULTS: if coupled resolution------------------------
    if (uncoupledMechanic==false) {
        ofstream file(totalNameFile.c_str(), ios::app);  //writing mode (app is to write at the end of the file without erase the content)
        if (!file) {error.Warning("Unable to open file:"+totalNameFile+". Computation continues.");}
        file.precision(outputPrecision);
        ostringstream timeMecha,strain,stress;
        timeMecha << currentTimeFromPreciSo;
        strain << _mechanical.GetCurrentStrain();
        stress << _mechanical.GetCurrentStressMechanic()*1e-6;
        file << timeMecha.str() << " " << strain.str() << " " << stress.str() << " ";
        if (hardeningModelChosen>=1 && hardeningModelChosen<=8) {
            ostringstream sigmaYmicro,R,X;
            sigmaYmicro << _mechanical.GetsigmaFlowMicro()*1e-6;
            R << _mechanical.GetIsotropHardening()*1e-6;
            X << _mechanical.GetKinematicHardening_phenomeno()*1e-6;
            file << sigmaYmicro.str() << " " << R.str() << " " << X.str() << " ";
        }
        else if(hardeningModelChosen>=9 && hardeningModelChosen<=15) {
            ostringstream epsP,epsPcum,dislo,disloPPT,nG,X_G,n_ppt,Xppt,R;
            epsP << _mechanical.Get_epsP();
            epsPcum << _mechanical.Get_epsPcum();
            dislo << _mechanical.Get_dislo();
            disloPPT << _mechanical.Get_disloPPT();
            nG << _mechanical.Get_nG();
            X_G << _mechanical.Get_X_G()*1e-6;
            n_ppt << _mechanical.Get_n_ppt();
            Xppt << _mechanical.Get_Xppt()*1e-6;
            R << _mechanical.GetIsotropHardening()*1e-6;
            file << epsP.str() << " " << epsPcum.str() << " " << dislo.str() << " " << disloPPT.str() << " " << nG.str() << " " \
                 << X_G.str() << " " << n_ppt.str() << " " << Xppt.str() << " " << R.str() << " ";
        }
        else if(hardeningModelChosen==16) {
            ostringstream epsP,epsPcum,dislo,disloPPT,nG,X_G,n_ppt,Xppt,R;
            epsP << _mechanical.Get_epsP();
            epsPcum << _mechanical.Get_epsPcum();
            dislo << _mechanical.Get_dislo();
            nG << _mechanical.Get_nG();
            X_G << _mechanical.Get_X_G()*1e-6;
            R << _mechanical.GetIsotropHardening()*1e-6;
            file << epsP.str() << " " << epsPcum.str() << " " << dislo.str() << " " << nG.str() << " " \
                 << X_G.str() << " " << " " << R.str() << " ";
        }
        else {error.Fatal("hardening model not implemented in 'output.HardeningResults'");}
        file << endl;
        file.close();
    }
    //-----------------RESULTS: if not coupled resolution------------------------
    if (_initialCall==false && uncoupledMechanic) {

        //-----open file-----
        ofstream file(totalNameFile.c_str(), ios::app);
        if (!file) {error.Warning("Unable to open file:"+totalNameFile+". Computation continues.");}
        file.precision(outputPrecision);

        //-----nb of several results-----
        size_t nbOfTimesResults=UncoupledResults.size();
        if (nbOfTimesResults<1) {error.Fatal("In 'Output.HardeningResults': 'nbOfTimesResults' must be >0");}
        size_t nbOfResults=UncoupledResults[0].size();
        if (nbOfResults<1) {error.Fatal("In 'Output.HardeningResults': 'nbOfResults' must be >0");}

        //-----check nb of column-----
        if (hardeningModelChosen>=1 && hardeningModelChosen<=8) {
            if (nbOfResults!=6) {error.Fatal("In 'ouput.HardeningResults', for this 'hardeningModelChosen' the nb of results must be 6");}
        }
        else if(hardeningModelChosen>=9 && hardeningModelChosen<=15) {
            if (nbOfResults!=15) {error.Fatal("In 'ouput.HardeningResults', for this 'hardeningModelChosen' the nb of results must be 14");}
        }
        else if(hardeningModelChosen==16) {
            if (nbOfResults!=10) {error.Fatal("In 'ouput.HardeningResults', for this 'hardeningModelChosen' the nb of results must be 10");}
        }
        else {error.Fatal("This hardening model is not implemented in 'output.HardeningResults'");}

        //-----write results-----
        for (size_t i=0;i<nbOfTimesResults;i++) {
            for (size_t j=0;j<nbOfResults;j++) {
                ostringstream toConvertInString;
                if (hardeningModelChosen>=1 && hardeningModelChosen<=8) {
                    if (j==0 || j==1) {toConvertInString << UncoupledResults[i][j]; }
                    else {toConvertInString << UncoupledResults[i][j]*1e-6; }
                    file << toConvertInString.str() << " ";
                }
                else if(hardeningModelChosen>=9 && hardeningModelChosen<=15) {
                    if (j==2 || j==8 || j==10 || j==11) {toConvertInString << UncoupledResults[i][j]*1e-6;}
                    else {toConvertInString << UncoupledResults[i][j];}
                    file << toConvertInString.str() << " ";
                }
                else if(hardeningModelChosen==16) {
                    if (j==2 || j==7 || j==8) {toConvertInString << UncoupledResults[i][j]*1e-6;}
                    else {toConvertInString << UncoupledResults[i][j];}
                    file << toConvertInString.str() << " ";
                }
            }
            file << endl;
        }
        file.close();
    }
    //------------------------------------------------------------------------
}
