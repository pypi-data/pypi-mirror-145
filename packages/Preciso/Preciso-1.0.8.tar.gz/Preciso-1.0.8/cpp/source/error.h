#ifndef ERROR_H
#define ERROR_H

/// \file error.h
/// \brief Header of the class Error
#include <string>

/// \brief Error class returning warnings or terminating the programm in case of fatal errors.
class Error
{
public:
    
    /// \brief Constructor of the class Error, no specific effect.
    /// \callgraph
    Error();
    
    /// \brief Destructor of the class Error, no specific effect.
    /// \callgraph
    ~Error();
    
    /// \brief Indicates a fatal error and shuts the program.
    /// \return Nothing
    /// \param _errorMessage The description of the fatal error causing the termination.
    /// \callgraph
    void Fatal(std::string _errorMessage) const;
    
    /// \brief Indicates a warning, the execution of the program goes on.
    /// \return Nothing
    /// \param _warningMessage The description of the error causing the warning.
    /// \callgraph
    void Warning(std::string _warningMessage) const;
    
    /// \brief Writes in the log file
    /// \param _logMessage message to be printed in the log file
    void Log(std::string _logMessage) const;
    
private:
    
};

#endif // ERROR_H
