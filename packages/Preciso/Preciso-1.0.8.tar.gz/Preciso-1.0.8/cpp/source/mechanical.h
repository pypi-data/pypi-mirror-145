#ifndef MECHANICAL_H
#define MECHANICAL_H

/// \file mechanical.h
/// \brief Header of the class Mechanical
#include <iostream>
#include "error.h"
#include "constants.h"
#include "element.h"
#include "precipitate.h"
#include "matrix.h"
#include "mathematic.h"
#include <string>
#include <vector>
#include <math.h>
#include <sstream>

/// \brief Mechanical optionnal routine
class Mechanical
{
public:
    /// \brief Constructor of the class Mechanical, initializing all values to zero.
    /// \callgraph
    Mechanical();
    /// \brief Destructor of the class Mechanical, no specific effect.
    /// \callgraph
    ~Mechanical();

    double GetMechanicalTimeWithIndex(size_t const &) const;

    double GetStrainWithIndex(size_t const&) const;

    size_t GetNumberOfMechanicalTime() const;

    double GetIsotropHardening() const;

    double GetKinematicHardening_phenomeno() const;

    double GetCurrentStrain() const;

    double GetCurrentStressMechanic() const;

    double GetStrain(double const&) const;

    double GetEndMechanicalTime() const;

    double GetFirstMechanicalTime() const;

    void SetVerboseMode(bool);

    void SetMechanicalHardeningCoupling(bool);

    void SetMechanicalSemiHardeningCoupling(bool);

    bool GetMechanicalHardeningCoupling() const;

    bool GetMechanicalSemiHardeningCoupling() const;

    int GetHardeningModel() const;

    void SetModel(int);

    void SetTemperature(double);

    void DefineSScontribution(std::vector<std::vector<std::string> >,std::vector<Element> const&);

    void DefinePrecipitateConstants(std::vector<std::vector<std::string> >,std::vector<Precipitate> const&);

    void DefineDislocationsConstants(std::vector<std::string>);

    void DefineGrainSize(std::vector<std::string>);

    void DefineCristalloConstant(std::vector<std::string>);

    void DefineCoefficientsForHardeningModel(std::vector<std::string>);

    void DefineYoungModulus(std::vector<std::string>);

    void DefinePoissonCoeff(std::vector<std::string>);

    void CheckMechanicalModel();

    int GetModel() const;

    /// \brief Get the Young modulus at a specific temperature with linear interpolation between the input values.
    /// \return The interpolated Young in K.
    /// \param _temperature The Tempearture to interpolate the Young
    /// \callgraph
    double GetYoung() const;

    /// \brief Get the Young modulus at a specific temperature with linear interpolation between the input values.
    /// \return The interpolated Young in K.
    /// \param _temperature The Tempearture to interpolate the Young
    /// \callgraph
    double GetPoisson() const;

    double GetSSconstantI(size_t const&) const;

    std::string GetSSunitI(size_t const&) const;

    double GetTransitionRadiusI(size_t const&) const;

	double GetshearConstantStrength(size_t const&) const;

    double GetInitialYield() const;

    double GetSigmaSS() const;

    double GetSigmaGrain() const;

    double GetDsigmaSS() const;

    double GetSigmaDislo() const;

    double GetDsigmaDislo() const;

    double GetSigmaPreci() const;

    double GetDsigmaPreci() const;

    double GetSigmaPreciI(size_t) const;

    double GetSigmaPreciIsh(size_t) const;

    double GetSigmaPreciIbp(size_t) const;

    double GetDsigmaPreciI(size_t) const;

    double GetsigmaFlowMicro() const;

    double GetDsigmaFlowMicro() const;

    int GetIndexStructure() const;

    double Get_epsP() const;

    double Get_epsPcum() const;

    double Get_dislo() const;

    double Get_disloPPT() const;

    double Get_nG() const;

    double Get_X_G() const;

    double Get_n_ppt() const;

    double Get_Xppt() const;

    std::string GetNameStructure() const;

    double ComputeDisloContributionModel1();

    double ComputeSScontributionModel1(std::vector<Element> const&);

    double ComputeSScontributionModelAlex(std::vector<Element> const&);

    double ComputeSScontributionModelAlex_sqrt(std::vector<Element> const&);

    void ModelAlex(Matrix const&,std::vector<Element> const&,std::vector<Precipitate> const&,double,double);

    void ModelAlexSphere(Matrix const&,std::vector<Element> const&,std::vector<Precipitate> const&,double,double);

    void ModelFisk(Matrix const&,std::vector<Element> const&,std::vector<Precipitate> const&,double,double);

    void ModelOne(Matrix const&,std::vector<Element> const&,std::vector<Precipitate> const&,double,double);

    void ModelTwo(Matrix const&,std::vector<Element> const&,std::vector<Precipitate> const&,double,double);

    void ModelThree(Matrix const&,std::vector<Element> const&,std::vector<Precipitate> const&,double,double);

    void ModelFour(Matrix const&,std::vector<Element> const&,std::vector<Precipitate> const&,double,double);

    void loadStrainLoading(std::string const&,std::string const&);

    std::vector<std::string> GetNameExtensionHardeningFile() const;

    void SetHardeningModel(int);

    void SetInitialHardeningValues();

    void SetActivedHardening(bool);

    std::vector<std::vector<double> > BehaviourUncoupledIntegration();

    void BehaviourCoupledIntegration(double,double);

    void BehaviourSemiCoupledIntegration(size_t const&);

    void modelImplementationAndComputation(double const&,double const&,double const&);

    void elastoPlasticSolving(double const&,double const&,double const&);

    std::vector<double> functionRk45adapt(double const&,std::vector<double> const&,std::vector<double> const&);

    //general routines

    std::vector<std::vector<double> > rk45adapt(double,std::vector<double> const&,std::vector<double> const&);

    void Parse(std::string _dump, std::vector<std::string>& _arg);

private:
    /// \brief Error instance of this class
    Error error;
    /// \brief Mathematic instance of this class
    Mathematic mathematic;
    /// \brief Index of the model that is chosen in the input file
    int activedMicrostructuralModel;
    /// \brief Index of the hardening model that is chosen in the input file
    int hardeningModelChosen;
    /// \brief To active hardening computation
    bool hardeningComputation;
    /// \brief To active coupling for hardening computation
    bool mechanicalHardeningCoupling;
    /// \brief To active semi coupling for hardening computation
    bool mechanicalSemiHardeningCoupling;
    /// \brief To turn on or off the verbose mode in mechanical class
    bool notVerboseBool;
    /// \brief To have more rapidly the size of timeMechanical vector
    size_t timeMechanicalSize;
    //--------------- temperature -----------------
    double currentTemperature;
    double strainRate;
    //------------ timeStrainVariable -------------
    std::vector<double> TimeMechanic; //in seconds;
    std::vector<double> StainMechanic; //witout unity;
    std::string nameOfHardeningFile;
    std::string hardeningFileExtension;
    //----------- SScontribution ---------------
    /// \brief Solidsolution contribution for each elements
    std::vector<double> SSconstant;
    /// \brief Solidsolution unit for each elements
    std::vector<std::string> SSunit;
    //---------- precipitateConstants --------------
    /// \brief transitionRadius for each precipitates
    std::vector<double> transitionRadius;
    /// \brief pathStructure for each precipitates
    std::vector<int> PathStructure;

    std::vector<double> shearConstantStrength;
    /// \brief Multiplicative terme for shering force
    size_t nbOfPrecipitates;
    //--------- DislocationsConstants ----------
    /// \brief initial dislocation density noted 'rho0' in litterature
    double initialDislocDensity;
    /// \brief current dislocation density noted 'rho' in litterature
    double dislocDensity;
    /// \brief dislocation strength noted 'alpha' in litterature
    double dislocStrength;
    /// \brief dislocation tension Line noted 'beta' in litterature
    double tensionLineConstant;
    //----------- CristalloConstant ------------
    /// \brief initial yield noted 'sigma0' in litterature (friction de reseau)
    double initialYield;
    /// \brief the taylor's factor
    double taylorFactor;
    /// \brief norme of Burger's vector
    double burgersNorm;
    /// \brief structure (to know dense planes)
    int structure;
    std::string stringStructure;
    /// \brief puissance pour sommation des contributions
    double powSum;
    //----------- Young modulus ------------
    /// \brief temperature associed to young modulus
    std::vector<double> TemperatureYoung;
    /// \brief Young modulus as function of temperature
    std::vector<double> Young;
    /// \brief Size of young modulus vector
    size_t sizeYoung;
    /// \brief current young modulus for current temperature
    double currentYoung;
    //----------- elastic constants ------------
    /// \brief temperature associed to Poisson coeff
    std::vector<double> TemperaturePoisson;
    /// \brief Poisson coeff as function of temperature
    std::vector<double> Poisson;
    /// \brief Size of young modulus vector
    size_t sizePoisson;
    /// \brief current Poisson's coeff for current temperature
    double currentPoisson;
    /// \brief current ShearModulus for current temperature
    double currentShearModulus;
    //-------- booleen to check model ----------
    /// \brief Bool to check if SScontribution are Loaded
    bool SScontributionLoaded;
    /// \brief Bool to check if TransitionRadius are Loaded
    bool PrecipitateConstantsLoaded;
    /// \brief Bool to check if DislocationsConstants are Loaded
    bool DislocationsConstantsLoaded;
    /// \brief Bool to check if CristalloConstant are Loaded
    bool CristalloConstantLoaded;
    /// \brief Bool to check if young modulus are Loaded
    bool YoungModulusLoaded;
    /// \brief Bool to check if Poisson's coeff are Loaded
    bool PoissonCoeffLoaded;
    /// \brief Bool to check if grainSizeLoaded coeff are Loaded
    bool grainSizeLoaded;
    //-------- microstructural variables ----------
    double sigmaGrain;
    double dsigmaGrain;
    double sigmaSS;
    double dsigmaSS;
    double sigmaDislo;
    double dsigmaDislo;
    std::vector<double> sigmaPreciI;
    std::vector<double> dsigmaPreciI;
    std::vector<double> sigmaPreciIsh;
    std::vector<double> sigmaPreciIbp;
    std::vector<double> YoungModulusPreci;
    std::vector<double> PoissonCoeffPreci;
    std::vector<double> ShearModulusPreci;
    std::vector<double> omegaEshelby;
    std::vector<double> factorKineticContribution;
    double sigmaPreci;
    double dsigmaPreci;
    double sigmaFlowMicro;
    double dsigmaFlowMicro;
    //----------------microstructural for physical hardening-----------------
    std::vector<double> fv_bp;
    std::vector<double> dfv_bp;
    std::vector<double> meanR_bp;
    std::vector<double> dmeanR_bp;

    std::vector<double> meanT_bp;
    std::vector<double> dmeanT_bp;

    std::vector<double> meanL_bp;
    std::vector<double> dmeanL_bp;
    std::vector<double> Ntot_bp;
    std::vector<double> dNtot_bp;
    std::vector<double> distanceBetweenPPT; //dans mon modele (didier) c les PPT contournés
    std::vector<double> ddistanceBetweenPPT;
    double grainSize;
    double dgrainsize;
    //----------------detail des distances entre PPT (distances geometriques! eq26 de mon article Acta2014)-----------------
    std::vector<double> ddistancePPTsh;
    std::vector<double> distancePPTsh;
    std::vector<double> ddistancePPTbp;
    std::vector<double> distancePPTbp;
    std::vector<double> ddistancePPTall;
    std::vector<double> distancePPTall;
    // ################## CHOICE FOR HARENING LAW ########################
    //--------------GENERALITIES-------------------
    //initialPlasticStrain
    double currentStrain;
    double epsP;
    double epsPcum;
    double epsP_initial;
    double epsPcum_initial;
    //initialHardeningParameter
    double R;
    double X;
    double R_initial;
    double X_initial;
    double X_G;
    double Xppt;
    // stress
    double stressMechanic; //in Pa
    double stressMechanic_initial;

    //------------semiphenomenological didier's model 6061----
    //constant
    double K_kin;
    double K_iso;
    double c_kin;
    double gamma_kin;
    double b_iso;
    double Rinf_iso;
    double gamma0_kin;
    double gammaK_kin;
    double gammaInf_kin;
    //------------physical didier's model----
    double k1;
    double k2_0;
    double k2_P;
    double Zdislo;
    double ZdisloPPT;
    double nG;
    double nG_star;
    double lambdaG;
    double k2;
    double k3;
    std::vector<double> nPPT;
    double n_ppt; //scalar for physical hardenng that is used because we assume only one precipitate in physical hardening routine
    std::vector<double> nPPT_star;
    std::vector<double> phiPPT;
    bool disableK2modif;
    bool disableRhoPPTcouplingBool;
     //------------Hall-Petch constant for Alex's model----
    double K_HP;
    //---------------model with slip reversibility--------------
    bool activeSSreversibility;
    bool activeDreversibility;
    bool activeHreversibility;
    bool activePreversibility;

    //####################################################################
};

#endif // MECHANICAL_H
