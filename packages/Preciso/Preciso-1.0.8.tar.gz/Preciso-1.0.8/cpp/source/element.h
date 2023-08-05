#ifndef ELEMENT_H
#define ELEMENT_H

/// \file element.h
/// \brief Header of the class Element
#include <string>
#include <vector>
#include "error.h"
#include "matrix.h"

/// \brief Forward declaration of class Precipiate, necessary for the compilation (Element needs Precipitate and vice-versa)
class Precipitate;
/// \brief Forward declaration of class Matrix, necessary for the compilation (Element needs Matrix and vice-versa)
class Matrix;
/// \brief One of the elements constituing the studied material.
class Element
{
public:
    /// \brief Constructor: definition of the properties of an element from a vector of string containing all the informations in the following order
    /// - Name of the element.
    /// - Content of this element in the material in wt.%.
    /// - Molar mass of the element in kg/mol.
    /// - Pre-exponential factor of diffusion (following Fick's law) of this element in the matrix in m²/s.
    /// - Energy of activation of diffusion (following Fick's law) of this element in the matrix in J/mol.
    /// \return Nothing
    /// \param _arg Vector of string containint the informations necessary to define an element.
    /// \param _index Index of the element in the vector of elements
    /// \callgraph
    Element(std::vector<std::string> const& _arg, int _index);

    /// \brief Destructor of the class Element, no specific effect.
    /// \callgraph
    ~Element();

    /// \return The solid solution content of this element in Wt% (useful for mechanical models).
    /// \callgraph
    double SolidSolContentWtPercent(std::vector<Element> const& _Elements) const;

    /// \return The name of this element.
    /// \callgraph
    std::string GetName() const;

    /// \return The content of this element in the material in wt.%.
    /// \callgraph
    double GetContentWtPc() const;

    /// \return The content of this element in the material in at. fraction.
    /// \callgraph
    double GetContentAtFrac() const;

    /// \return The molar mass of the element in kg/mol.
    /// \callgraph
    double GetMolarMass() const;

    /// \return The pre-exponential factor of diffusion (following Fick's law) of this element in the matrix in m²/s.
    /// \callgraph
    double GetDiffusionD0() const;

    /// \return The energy of activation of diffusion (following Fick's law) of this element in the matrix in J/mol.
    /// \callgraph
    double GetDiffusionQ() const;

    /// \return The current solid solution content in at. fraction.
    /// \callgraph
    double GetSolidSolContent() const;

    /// \brief Calculate the diffusion coefficient of the element at a given temperature
    /// \return The diffusion coefficient in m^2/s
    /// \param _T Temperature in K
    /// \callgraph
    double GetDiffusionCoefficient(double const& _T) const;

    /// \brief Set the name of the element.
    /// \return Nothing
    /// \param _name Name of the element.
    /// \callgraph
    void SetName(std::string const& _name);

    /// \brief Set the content in wt% of the element.
    /// \return Nothing
    /// \param _contentWtPc Content in wt% of the element.
    /// \callgraph
    void SetContentWtPc(double const& _contentWtPc);

    /// \brief Set the content in at. fraction of the element.
    /// \return Nothing
    /// \param _contentAtFrac Content in at. fraction of the element.
    /// \callgraph
    void SetContentAtFrac(double const&_contentAtFrac);

    /// \brief Set the molar mass of the element.
    /// \return Nothing
    /// \param _molarMass Molar mass of the element.
    /// \callgraph
    void SetMolarMass(double const& _molarMass);

    /// \brief Set the pre-exponential factor of diffusion of the element.
    /// \return Nothing
    /// \param _diffusionD0 Pre-exponential factor of diffusion of the element.
    /// \callgraph
    void SetDiffusionD0(double const& _diffusionD0);

    /// \brief Set the energy of activation of diffusion of the element.
    /// \return Nothing
    /// \param _diffusionQ Energy of activation of diffusion of the element.
    /// \callgraph
    void SetDiffusionQ(double const& _diffusionQ);

    /// \brief Set the solid solution content of the element.
    /// \return Nothing
    /// \param _solidSolContent Solid solution content of the element.
    /// \callgraph
    void SetSolidSolContent(double const& _solidSolContent);

    /// \brief Set the index of the element in the vector of elements.
    /// \return Nothing
    /// \param _index index of the element.
    /// \callgraph
    void SetIndex(size_t const& _index);

    /// \brief Set the variable simplifiedMassBalance to true and thus use the "simplified" mass balance.
    void SetImprovedMassBalance();

    /// \brief Get the variable simplifiedMassBalance to true and thus use the "simplified" mass balance.
    bool GetSimplifiedMassBalance();

    /// \brief Calculate the atomic fraction of the element in the material
    /// \return Nothing
    /// \param _Elements Vector of elements, that are objects instance of class Element
    /// \param _matrix object matrix, that is an element of class Matrix
    /// \param _Precipitates Vector of precipitates that are objects instance of class Precipitate
    /// \callgraph
    void Initialize(std::vector<Element> const& _Elements, Matrix& _matrix, std::vector<Precipitate>& _Precipitates,bool _firstCall);

    /// \brief Perform Mass Balance to calculate solid solution content of all elements
    /// - Old version with the hypothesis that precipitates volume is negligible compared to matrix's
    /// \return Nothing
    /// \param _matrix object matrix, that is an element of class Matrix
    /// \param _Precipitates Vector of precipitates that are objects instance of class Precipitate
    void SimplifiedMassBalance(Matrix const& _matrix, std::vector<Precipitate>& _Precipitates);

    /// \brief Perform Mass Balance to calculate solid solution content of all elements
    /// \return Nothing
    /// \param _matrix object matrix, that is an element of class Matrix
    /// \param _Precipitates Vector of precipitates that are objects instance of class Precipitate
    void GenericMassBalance(Matrix& _matrix, std::vector<Precipitate> &_Precipitates,std::vector<Element> const& _Elements);

    /// \brief Perform Mass Balance to calculate solid solution content of all elements (chooses the mass balance routine depending on the input options)
    /// \return Nothing
    /// \param _matrix object matrix, that is an element of class Matrix
    /// \param _Precipitates Vector of precipitates that are objects instance of class Precipitate
    void MassBalance(Matrix& _matrix, std::vector<Precipitate> &_Precipitates,std::vector<Element> const& _Elements);

    /// \brief Set the booleen "firstMassBalance" on true or false
    /// \return Nothing
    /// \param _index index of the element.
    /// \callgraph
    void SetFirstMassBalance(bool const);

    /// \brief Set the value of inflateDiffusionCoeff (default value 1)
    void SetInflateDiffusionCoeff(double const &_inflateDiffusionCoeff);

    /// \brief Get the value of inflateDiffusionCoeff (default value 1)
    double GetInflateDiffusionCoeff() const;

private:
    //Initial data of the element (from the input file)
    /// \param error error instance of this class
    Error error;
    /// \brief name Name of the element
    std::string name;
    /// \brief Content of this element in the material in wt.%.
    double contentWtPc;
    /// \bried Content of this element in the material in at. fraction
    double contentAtFrac;
    /// \brief Molar mass of the element in kg/mol
    double molarMass;
    /// \brief Pre-exponential factor of diffusion (following Fick's law) of this element in the matrix in m²/s
    double diffusionD0;
    /// \brief Energy of activation of diffusion (following Fick's law) of this element in the matrix in J/mol
    double diffusionQ;
    //Other data for the element
    /// \brief Current solid solution content in at. fraction
    double solidSolContent; //in at. fraction
    /// \brief Index of this element
    size_t index;
    /// \brief To test if is the first massBalance if yes & solidSolContent is <0 we have an invalid initialDistrib
    bool firstMassBalance;
    /// \brief Decides if the old or new mass balance must be used (default value = false)
    bool simplifiedMassBalance;
    /// \brief inflateDiffusionCoeff is to boost the growth for phenomenogical modelisations
    double inflateDiffusionCoeff;

};

#endif // ELEMENT_H
