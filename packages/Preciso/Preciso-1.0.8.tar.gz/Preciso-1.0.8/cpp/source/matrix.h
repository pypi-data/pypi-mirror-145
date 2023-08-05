#ifndef MATRIX_H
#define MATRIX_H

/// \file matrix.h
/// \brief Header of the class Matrix
#include <string>
#include <vector>
#include "error.h"
#include "element.h"

/// \brief Forward declaration of class Element, necessary for the compilation (Element needs Matrix and vice-versa)
class Element;

/// \brief Matrix properties
class Matrix
{
public:

    /// \brief Constructor of the class Matrix, initializing all values to zero.
    /// \callgraph
    Matrix();

    /// \brief Destructor of the class Matrix, no specific effect.
    /// \callgraph
    ~Matrix();

    /// \brief Definition of the properties of the matrix from a vector of string containing all the informations in the following order:
    /// - Name of the matrix
    /// - Lattice parameter of the matrix (assumed cubic) in m
    /// - Atomic volume of the matrix in m3
    /// - Molar mass of the matrix in kg/mol
    /// \return Nothing
    /// \param _arg Vector of string containint the informations necessary to define the matrix.
    /// \callgraph
    void DefineMatrix(std::vector<std::string> const& _arg);

    /// \return The name of the matrix.
    /// \callgraph
    std::string GetName() const;

    /// \return The lattice parameter of the matrix (assumed cubic) in m.
    /// \callgraph
    double GetLatticeParameter() const;

    /// \return The atomic volume of the matrix in m3.
    /// \callgraph
    double GetAtomicVolume() const;

    /// \return The molar mass of the matrix in kg/mol.
    /// \callgraph
    double GetMolarMass() const;

    /// \brief Set the name of the matrix.
    /// \return Nothing
    /// \param _name Name of the matrix.
    /// \callgraph
    void SetName(std::string const& _name);

    /// \brief Set the lattice parameter of the element.
    /// \return Nothing
    /// \param _latticeParameter
    /// \callgraph
    void SetLatticeParameter(double const&);

    /// \brief Set the atomic volume of the element.
    /// \return Nothing
    /// \param _atomicVolume
    /// \callgraph
    void SetAtomicVolume(double const&);

    /// \brief Set the molar mass of the element.
    /// \return Nothing
    /// \param _molarMass
    /// \callgraph
    void SetMolarMass(double const&);

    /// \brief Set the atomic volume of the solid solution.
    /// \return Nothing
    /// \param _elementList
    /// \callgraph
    void SetAtomicVolumeSS(std::vector<Element> const& _Elements,bool _firstCall);

    /// \brief Get the Atomic Volume of the SS
    /// \return The atomic volume of solid solution in m3.
    /// \param Nothing
    /// \callgraph
    double GetAtomicVolumeSS() const;

    /// \brief To set the boolen that inform us if we have VatSS computation or no
    /// \return Nothing
    /// \param Nothing
    /// \callgraph
    void setVatSSbool(bool);

    /// \brief Set the volume of the node for matrix class
    /// \return Nothing
    /// \param Nothing
    /// \callgraph
    void SetVolumeNode(double const&);

    /// \brief Get the volume of the node for matrix class
    /// \return volume of the node
    /// \param Nothing
    /// \callgraph
    double GetVolumeNode() const;

private:
    /// \brief Error instance of this class
    Error error;
    /// \brief Name of the matrix
    std::string name;
    /// \brief Lattice parameter of the matrix (assumed cubic) in m.
    double latticeParameter;
    /// \brief Atomic volume of the matrix in m3.
    double atomicVolume;
    /// \brief Molar mass of the matrix in kg/mol.
    double molarMass;
    /// \brief Atomic volume of solidSolution in m3.
    double atomicVolumeSS;
    /// \brief Booleen to know if we have to compute VatSS rather than VatM
    bool computationOfAtomicVolumeSS;

    double volumeOfTheAssociedNode;

};

#endif // MATRIX_H


