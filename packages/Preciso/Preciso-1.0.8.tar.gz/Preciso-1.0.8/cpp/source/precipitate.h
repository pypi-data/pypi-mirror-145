#ifndef PRECIPITATE_H
#define PRECIPITATE_H

/// \file precipitate.h
/// \brief Header of the class Precipitate
#include <string>
#include <vector>
#include "element.h"
#include "mathematic.h"
#include "error.h"

/// \brief Forward declaration of class Element, necessary for the compilation (Element needs Precipitate and vice-versa)
class Element;

/// \brief Properties and computation of one family of precipitates involved in the studied material.
class Precipitate
{
public:
    
    /// \brief Constructor of the class Precipitate, initializing all properties values to zero. The list of elements involved in the computation if defined and the chemistries of this precipitate are set to 0.
    /// \param _Elements The list of Elements for this computation.
    /// \callgraph
    Precipitate(std::vector<Element> const& _Elements);
    
    /// \brief Destructor of the class Precipitate, no specific effect.
    /// \callgraph
    ~Precipitate();
    
    /// \brief Definition of the properties of a precipitate from a vector of string containing all the informations in the following order
    /// \todo Modify this comments and the name of Precipitate attributes to be consistent with the new datafile
    /// - Name of the precipitate.
    /// - Atomic volume of this precipitate in m3.
    /// - Surface energy of the precipitate in J/m≤.
    /// - A value of the product of solubility for log10(Ks) = log10( X_A^i X_B^j ) = -A/T + B, X_A and X_B in at. fraction, precipitate AiBj
    /// - B value of the product of solubility for log10(Ks) = log10( X_A^i X_B^j ) = -A/T + B, X_A and X_B in at. fraction, precipitate AiBj
    /// - Adjustment coefficient for the Gibbs energy of heterogeneous nucleation (1 if homogeneous nucleation), unitless.
    /// - Number of additional nucleation sites for heterogeneous nucleation in m^(-3).
    /// - Shape of the precipitate, possible values : "sphere".
    /// - Aspect ratio of the precipitate, set to 1 automatically for a sphere, unitless.
    /// - A list of the elements constituing the precipitate
    ///   - Name of the element
    ///   - Chemistry of the element
    /// \return Nothing
    /// \param _arg Vector of string containint the informations necessary to define an element.
    /// \callgraph
    void DefinePrecipitate(std::vector<std::string>& _arg);
    
    /// \brief We add here the initial distribution
    /// \return Nothing.
    /// \callgraph
    void DefineInitialDistribution(std::vector<double> const&_InitialRadius,std::vector<double> const&_InitialNumber);
    /// \return The name of this family of precipitates.
    /// \callgraph
    std::string GetName() const;
    
    /// \return The Atomic volume of this precipitate in m3.
    /// \callgraph
    double GetAtomicVolume() const;
    
    /// \return The surface energy of the precipitate in J/m≤.
    /// \callgraph
    double GetSurfaceEnergy() const;
    
    /// \return The A value of the product of solubility for log10(Ks) = log10( X_A^i X_B^j ) = C/T^2 -A/T + B, X_A and X_B in at. fraction, precipitate AiBj
    /// \callgraph
    double GetSolProdA() const;
    
    /// \return The B value of the product of solubility for log10(Ks) = log10( X_A^i X_B^j ) = C/T^2 -A/T + B, X_A and X_B in at. fraction, precipitate AiBj
    /// \callgraph
    double GetSolProdB() const;
    
    /// \return The C value of the product of solubility for log10(Ks) = log10( X_A^i X_B^j ) = C/T^2 -A/T + B, X_A and X_B in at. fraction, precipitate AiBj
    /// \callgraph
    double GetSolProdC() const;
    
    /// \return The adjustment coefficient for the Gibbs energy of heterogeneous nucleation (1 if homogeneous nucleation), unitless.
    /// \callgraph
    double GetHeteroNucleation() const;
    
    /// \return The number of additional nucleation sites for heterogeneous nucleation in m^(-3).
    /// \callgraph
    double GetHeteroSites() const;
    
    /// \return The shape of the precipitate, possible values : "sphere,rods,plates".
    /// \callgraph
    std::string GetShape() const;
    
    /// \return The shape of the precipitate with a number index
    /// \callgraph
    int GetShapeIndex() const;
    
    /// \return The aspect ratio of the precipitate, 0 for a sphere, unitless.
    /// \callgraph
    double GetAspectRatio() const;
    
    /// \todo Comment this procedure
    double GetAtomsPerMolecule() const;
    
    /// \brief Get the chemistry of a specific element for this precipitate
    /// \return The chemistry of the element.
    /// \param _element The name of the element.
    /// \callgraph
    double GetThisElementChemistry(std::string const& _element) const;
    
    /// \brief Get the chemistry of a specific element for this precipitate
    /// \return The chemistry of the element.
    /// \param _elementInde The index of the element.
    /// \callgraph
    double GetThisElementChemistry(size_t const& _elementIndex) const;
    
    /// \brief Set the name of the precipitate.
    /// \return Nothing
    /// \param _name
    /// \callgraph
    void SetName(std::string const&);
    
    /// \brief Set the lattice parameter of the precipitate.
    /// \return Nothing
    /// \param _atomicVolume
    /// \callgraph
    void SetAtomicVolume(double const&);
    
    /// \brief Set the surface energy of the precipitate.
    /// \return Nothing
    /// \param _surfaceEnergy
    /// \callgraph
    void SetSurfaceEnergy(double const&);
    
    /// \brief Set the A solubility product of the precipitate.
    /// \return Nothing
    /// \param _solProdA
    /// \callgraph
    void SetSolProdA(double const&);
    
    /// \brief Set the B solubility product of the precipitate.
    /// \return Nothing
    /// \param _solProdB
    /// \callgraph
    void SetSolProdB(double const&);
    
    /// \brief Set the C solubility product of the precipitate.
    /// \return Nothing
    /// \param _solProdC
    /// \callgraph
    void SetSolProdC(double const&);
    
    
    /// \brief Set the heterogeneous nucleation of the precipitate.
    /// \return Nothing
    /// \param _heteroNucleation
    /// \callgraph
    void SetHeteroNucleation(double const&);
    
    /// \brief Set the number of heterogeneous nucleation sites of the precipitate.
    /// \return Nothing
    /// \param _heteroSites
    /// \callgraph
    void SetHeteroSites(double const&);
    
    /// \brief Set the shape of the precipitate.
    /// \return Nothing
    /// \param _shape
    /// \callgraph
    void SetShape(std::string const& _shape);
    
    /// \brief Set the shape of the precipitate in index mode
    /// \return Nothing
    /// \param _shape
    /// \callgraph
    void SetShapeIndex(int const& _shape);
    
    /// \brief Set the aspect ratio of the precipitate.
    /// \return Nothing
    /// \param _aspectRatio
    /// \callgraph
    void SetAspectRatio(double const&);
    
    /// \brief Set the chemistry of a given element of the precipitate.
    /// \return Nothing
    /// \param _element The name of the element.
    /// \param _chemistry The chemistry of the element
    /// \callgraph
    void SetThisElementChemistry(std::string const& _element, double const& _chemistry);
    
    /// \brief Calculates the number of nucleated precipitates a the given temperature and for this time increment and adds them to the list of precipitates.
    /// \return Nothing
    /// \param _Elements The vector of elements in the material
    /// \param _matrix The matrix of the material
    /// \param _t The current time in seconds
    /// \param _dt The time increment in seconds
    /// \param _T The temperature during this time increment in K
    /// \callgraph
    void Nucleation(std::vector<Element> const&, Matrix const&, double const&, double const&, double const&, double const&, int const&);
    
    /// \todo Comment this procedure
    void Growth(std::vector<Element> const&, Matrix const&, double const&, double const&);
    
    /// \todo Comment this procedure
    void GrowthOneElement(double const, double const&, double const&,std::vector<Element> const&,std::vector<Element> const&);
    
    /// \todo Comment this procedure
    void GrowthTwoElementNumeric(double const, double const&, double const&,std::vector<Element> const&,std::vector<Element> const&);
    
    /// \todo Comment this procedure
    void GrowthGeneral(double const, double const&, double const&,std::vector<Element> const&,std::vector<Element> const&);
    
    /// \todo Comment this procedure
    void SortDistribution();
    
    /// \todo Comment this procedure
    void ClassManagement();
    
    /// \todo Comment this procedure
    void QuadClassManagement();
    
    /// \todo Comment this procedure
    void LinClassManagement();
    
    /// \todo Comment this procedure
    void DistribClassManagement();
    
    /// \todo Comment this procedure
    void OldClassManagement();
    
    void OldClassManagementWithLessClass();
    
    /// \todo Comment this procedure
    double SolProdGibbsThomsonCalculation(double const&, double const&);
    
    /// \brief Calculates the superSaturation.
    /// \return Nothing
    /// \param _Elements The vector of elements in the material
    /// \param _T The current temperature in K
    /// \callgraph
    void SuperSaturationCalculation(std::vector<Element> const&, double const&);
    
    /// \brief Calculates the dirving force in J/m^3
    /// \return Nothing
    /// \param _T The current temperature in K
    /// \callgraph
    void DrivingForceCalculation(double const&);
    
    /// \brief Calculates the critical radius and the nucleation radisu of the precipitates accounting for thermal agitation.
    /// \return Nothing
    /// \param _T The current temperature in K
    /// \callgraph
    void RStarCalculation(double const&);
    
    /// \brief  To dissolve classes too small
    /// \return Nothing
    /// \param Nothing
    /// \callgraph
    void Dissolution();
    
    /// \brief  To compute and get volume fraction of current "number" and "radisu" arrays
    /// \return volume fraction
    /// \param Nothing
    /// \callgraph
    double VolumeFraction() const;
    
    /// \brief  To compute and get mean radius of current "number" and "radisu" arrays
    /// \return mean radius
    /// \param Nothing
    /// \callgraph
    double MeanRadius() const;
    
    /// \brief  To compute and get star radius of current "number" and "radisu" arrays
    /// \return Rstar radius
    /// \param Nothing
    /// \callgraph
    double GetRStar() const;
    
    /// \brief to get the number of classes
    /// \return size of "Number" and "Radius" arrays
    /// \param Nothing
    /// \callgraph
    size_t GetNumberOfClass() const;
    
    /// \brief to get the number of the choosen class
    /// \return number per unit of volume
    /// \param the index of the class that we want
    /// \callgraph
    double GetNumber(size_t const&) const;
    
    /// \brief to get the radius of the choosen class
    /// \return radius of the class
    /// \param the index of the class that we want
    /// \callgraph
    double GetRadius(size_t const&) const;
    
    /// \brief to know the total number of precipitates per unit volum
    /// \return total number of precipitates per unit volum
    /// \param Nothing
    /// \callgraph
    double TotalNumberOfPrecipitates() const;
    
    /// \brief Compute the aspect ratio for cylinders from a 3 step linear function
    /// \return Aspect ratio (unitless)
    /// \param The current radius of the precipiate
    /// \callgraph
    double AspectRatioFromCylinderFunction(double const &_radius) const;
    
    /// \brief Compute the aspect ratio for rods from a hyperbolla function
    /// \return Aspect ratio (unitless)
    /// \param The current radius of the precipiate
    /// \callgraph
    double AspectRatioFromRodFunction(double const &_radius) const;
    
    /// \brief to get the solubility fraction (obsolete?)
    /// \return Solubility Fraction
    /// \param Nothing
    /// \callgraph
    double GetSolubilityFraction() const;
    
    /// \brief Sets the algorithm BrentDicho tolerance of the mathematic instance of precipitates
    void SetBrentDichoAlgorithmTolerance(double const &_tolerance);
    
    /// \brief Sets the algorithm NewtonRaphson tolerance of the mathematic instance of precipitates
    void SetNewtonRaphsonAlgorithmTolerance(double const &_tolerance);
    
    /// \brief Sets the algorithm NewtonRaphson maxiNbOfIterations of the mathematic instance of precipitates
    void SetNRmaximumCount(double const &);
    
    /// \brief Sets the nonLinearAlgorithm that is used
    void SetNonLinearAlgorithm(double&);
    
    /// \brief Sets limitOfpreciInClassForDissolution
    void SetLimitOfpreciInClassForDissolution(double const &_limitNbDissolution);
    
    /// \brief Set the value of diffusionCoefficientRatio (default value 1.0e4)
    void SetDiffusionCoefficientRatio(double const &_diffusionCoefficientRatio);
    
    /// \brief Set the value of targetClassNumber (default value 500)
    void SetTargetClassNumber(unsigned int const &_targetClassNumber);
    
    /// \brief Set the value of changeNumberInClass (default value 0.01)
    void SetChangeNumberInClass(double const &_changeNumberInClass);
    
    /// \brief Set the value of unstationnaryNuclation (default value false)
    void SetUnstationnaryNucleation(bool const &_unstationnaryNuclation);
    
    /// \brief Set the value of classManagementType (default value "lin")
    void SetClassManagementType(double &_classManagementType);
    
    /// \brief Set the value of minDissolutionLimit (default value 1e-10)
    void SetMinDissolutionLimit(double const &_minDissolutionLimit);
    
    /// \brief Set the value of maxDissolutionLimit (default value 2e-10)
    void SetMaxDissolutionLimit(double const &_maxDissolutionLimit);
    
    /// \brief to set the volume of the associated node and know it in this class
    void SetVolumeNode(double const&);
    
    /// \brief to get the associated volume of this class
    double GetVolumeNode() const;
    
    /// \brief to set the boost factor of the diffusion coefficient associated to a precipitate
    void SetBoostPrecipitateDiffusion(double const&);
    
    /// \brief to get the info if the precipitate is dormant
    bool IsDormant() const;
    
    
    // test
    //    /// \brief First parameter for aspect ratio function for cylinders
    //    double a0;
    //    /// \brief 2nd parameter for aspect ratio function for cylinders
    //    double a1;
    //    /// \brief 3rd parameter for aspect ratio function for cylinders
    //    double b1;
    //    /// \brief 4th parameter for aspect ratio function for cylinders
    //    double a2;
    //    /// \brief 5th parameter for aspect ratio function for cylinders
    //    double b2;
    //    /// \brief 6th parameter for aspect ratio function for cylinders
    //    double r1;
    //    /// \brief 7th parameter for aspect ratio function for cylinders
    //    double r2;
    
    
    
    //    /// \brief erf function
    //    double Erf(double x);
    
    //#############################################
    // outputs for unstationnary nucleation publi
    //#############################################
    //double JS_publi;
    //double incubationCoef_publi;
    //double tau_publi;
    //double dN_dt_publi;
    //double dN_publi;
    //double randomWalk_publi;
    //double delta_publi;
    //double Z_publi;
    //double betaStar_publi;
    //double rStarKbT_publi;
    //double rStar_publi;
    //#############################################
    
    
private:
    /// \brief Error instance of this class
    Error error;
    /// \brief Mathematic instance of this class
    Mathematic mathematic;
    /// \brief
    std::string name;
    /// \brief in m3
    double atomicVolume;
    /// \brief Surface Energy that (eventually) changes for each class (in J/m^2)
    double surfaceEnergy;
    /// \brief Surface Energy red from input file (in J/m^2)
    double surfaceEnergy0;
    /// \brief Distribution width for gaussian surface Energy generation (in J/m^2)
    double surfaceEnergySigma;
    /// \brief log10(Ks) = log10( X_A^i X_B^j ) = C/T^2 -A/T + B, X_A and X_B in at. fraction, precipitate AiBj
    double solProdA;
    /// \brief log10(Ks) = log10( X_A^i X_B^j ) = C/T^2 -A/T + B, X_A and X_B in at. fraction, precipitate AiBj
    double solProdB;
    /// \brief log10(Ks) = log10( X_A^i X_B^j ) = C/T^2 -A/T + B, X_A and X_B in at. fraction, precipitate AiBj
    double solProdC;
    /// \indicates if the nucleation of this precipitate is "homogenous" or "heterogenous"
    std::string nucleationType;
    /// \indicates in computation if the nucleation of this precipitate is "homogenous=1" or "heterogenous=2"
    unsigned int nucleationChoice;
    /// \brief unitless
    double heteroNucleation;
    /// \brief Density of heterogenous nucleation sites in m^(-3)
    double heteroSites;
    /// \brief Shape "sphere", "rod" (value put in input file)
    std::string shapeString;
    /// \brief Shape value that correspond to "1=sphere", "2=rod", "3=cylinder", "4=cylinderFunction"...etc (convertion or string value)
    int shape;
    /// \brief Aspect ratio of non spherical precipitates (unitless). For a cylinder of radius r and length h, the aspect ratio is equal to 2r/h
    double aspectRatio;
    /// \brief First parameter for aspect ratio function for cylinders
    double a0;
    /// \brief 2nd parameter for aspect ratio function for cylinders/rod
    double a1;
    /// \brief 3rd parameter for aspect ratio function for cylinders/rod
    double b1;
    /// \brief 4th parameter for aspect ratio function for cylinders
    double a2;
    /// \brief 5th parameter for aspect ratio function for cylinders
    double b2;
    /// \brief 6th parameter for aspect ratio function for cylinders
    double r1;
    /// \brief 7th parameter for aspect ratio function for cylinders
    double r2;
    /// \brief List of all elements of the material
    std::vector<std::string> ElementList;
    /// \brief Chemistry coefficients of each element of the material
    std::vector<double> Chemistry;
    /// \brief Associated atomic fraction in the precipitate (e.g. 0.75 0.25 for Fe3C)
    std::vector<double> ContentAtFrac;
    /// \brief Precipitate size distribution - radius in m, radius are stored in increasing value order when managed by ClassManagement
    std::vector<double> Radius;
    /// \brief Precipitate size distribution - number
    std::vector<double> Number;
    /// \brief Distance on the R axis that the system travelled, if randomWalk=delta, the incubation time is achieved in m
    double randomWalk;
    /// \brief supersaturation
    double superSaturation;
    /// \brif Driving force in J/m^3
    double drivingForce;
    /// \brief Precipitates critical radius
    double rStar;
    /// \brief Number of atoms per molecule (e.g. 4 in Fe3C)
    double atomsPerMolecule;
    /// \brief Total number of precipitates
    double totalNumber;
    /// \brief
    bool callClassManagement;
    /// \brief Ratio of diffusion coefficient for one element to be neglected in the growth (by default 1e4)
    double diffusionCoefficientRatio;
    /// \brief Target number of class for each precipitate family (by default 500)
    unsigned int targetClassNumber;
    /// \brief Maximum percentage of change of the number of precipitates in the class management (by default 0.01)
    double changeNumberInClass;
    /// \brief Use of unstationnary nucleation theory
    bool unstationnaryNucleation;
    /// \brief "5=quad" quadratic for interpolation, "3=lin" for linear, "4=distrib" for distributing of classes, "2=old" for PreciSo_2, "1=no" for no class management
    double classManagementType;
    /// \brief Minimum radius (in m) for a preciptate, below it dissolutes
    double minDissolutionLimit;
    /// \brief Upper limit radius (in m) for a preciptate to start to dissolute
    double maxDissolutionLimit;
    /// \brief limite of Nb of precipitates that we can have in a class, else dissolution
    double limitOfpreciInClassForDissolution;
    /// \brief Number of classes
    size_t nbOfClass;
    /// \brief Number of element
    size_t sizeElement;
    /// \brief choice of nonLinear algorithm
    double nonLinearAlgorithm;
    /// \brief Keep in attribut the computation of solubility fraction
    double solubilityFraction;
    /// \brief Volume of the associeted node
    double volumeOfTheAssociedNode;
    /// \brief to increase the diffusion coefficient of all elements
    double boostPrecipitateDiffusion;
    /// \brief boolean flag to set if precipitate is dormant or not
    bool dormant;
    /// \brief boolean flag to set if site saturation is accounted for
    bool siteSaturation;
    /// \brief type of site saturation. Can be 'lin', 'surf' or 'vol'
    std::string siteSaturationType;
    
};

/// \brief Appairing of Number and Radius from a precipitate class to sort them by radius
class PrecipitateClass
{
public:
    /// \brief sets the radius and number of an objet instance of classe PrecipitateClass
    /// \param radius radius of the precipitate class
    /// \param number number of the precipitate class
    PrecipitateClass(double radius, double number) {
        this->radius = radius; this->number = number;
    }
    /// \brief member radius of the PrecipitateClass class
    double radius;
    /// \brief member number of the PrecipitateClass class
    double number;
    /// \brief member surfaceEnergy of the PrecipitateClass class
    double surfaceEnergy;
};

/// \brief Defines an operator that is used to compare precipitate radii
/// \param rhsA First parameter to be compared
/// \param rhsB Second parameter to be compared
inline bool operator<(const PrecipitateClass& rhsA, const PrecipitateClass& rhsB)
{
    return rhsA.radius < rhsB.radius;
}

#endif // PRECIPITATE_H
