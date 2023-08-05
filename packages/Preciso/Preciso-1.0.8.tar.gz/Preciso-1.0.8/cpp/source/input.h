#ifndef INPUT_H
#define INPUT_H

/// \file input.h
/// \brief Header of the class Input
#include <string>
#include <vector>
#include "error.h"

// /// \brief Forward declaration of class Preciso, necessary for the compilation
// class Preciso;

/// \brief Input data for the running of the code
class Input
{
public:
    
    /// \brief Constructor of the class Input, initializing all values to zero.
    /// \callgraph
    Input();
    
    /// \brief Destructor of the class Input, no specific effect.
    /// \callgraph
    ~Input();
    
    /// \brief Checks the number of input arguments to the programm and returns the path to the datafile
    /// argv must constain the keywords -path and -file followed by their respectives values.
    /// \return Nothing
    /// \param argc Number of executable input arguments
    /// \param argv Table of pointers to the input arguments
    /// \callgraph
    std::string FileName(int const& argc, const char *argv[]);

    /// \brief Gets from the input file all the lines starting with a given keyword. Warning the variable _lines is erased at the beginning of the routine.
    /// \return Nothing
    /// \param _inputFileName The name and path of the data file
    /// \param _keyword The keyword sought in the file
    /// \param _lines A matrix of strings containing the list of arguments (2nd dimension) for each line (1st dimension) where the keyword was found
    /// \param _optional Indicates if the keyword is optional, if not the program stops if the keyword is not found in the data file
    /// \callgraph
    void LinesStartingWithKeyword(std::string const& _inputFileName,std::string const& _keyword, std::vector<std::vector<std::string> >& _lines, bool _optional);

    /// \brief Cuts a string containing several words and/or numerical values separated by blanks into a vector of strings. A new element of the vector is created at each new blank.
    /// \return Nothing
    /// \param _dump The string of words and/or numerical values.
    /// \param _arg The vector of strings given as output.
    /// \callgraph
    void Parse(std::string _dump, std::vector<std::string>& _arg);
private:
    /// \brief Error instance of this class
    Error error;

};

#endif // INPUT_H
