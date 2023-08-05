#ifndef TEMPERATURE_H
#define TEMPERATURE_H

/// \file temperature.h
/// \brief Header of the class temperature
#include <string>
#include <vector>
#include "error.h"

/// \brief Temperature history
class Temperature
{
public:
    
    /// \brief Constructor of the class Temperature, initializing the vectors.
    /// \callgraph
    Temperature();
    
    /// \brief Destructor of the class Temperature, no specific effect.
    /// \callgraph
    ~Temperature();
    
    /// \brief Definition of the history of temperature from a vector of string containing all the informations in the following order
    /// - First time value in seconds
    /// - First temperature value in K.
    /// - Second time value in seconds
    /// - Second temperature value in K.
    /// - ...
    /// \return Nothing
    /// \param _arg A list of time and temperatures.
    /// \callgraph
    void DefineTemperature(std::vector<std::string> const& _arg);
    
    /// \brief Get the temperature at a specific time with linear interpolation between the input values.
    /// \return The interpolated temperature in K.
    /// \param _time The time to interpolate the temperature in s.
    /// \callgraph
    double GetTemperature(double const&) const;
    
    /// \return The final time of the simulation in s.
    /// \callgraph
    double GetTotalTime() const;
    
    /// \return The initial time of the simulation in s (and check time and temperature vector!).
    /// \callgraph
    double GetAndCheckInitialTime() const;

    /// \return The initial time of the simulation in s.
    /// \callgraph
    double GetInitialTime() const;
    
    /// \return The number of time points defined.
    /// \callgraph
    size_t GetNumberOfTime() const;
    
    /// \brief we provide the index of the time and we get the associated time
    double GetTimeWithIndex(size_t const &) const;

    
private:
    /// \brief Error instance of this class
    Error error;
    /// \brief
    std::vector<double> Time; //in seconds;
    /// \brief
    std::vector<double> TemperatureValues; //in K;
    /// \brief The size of vectors Time and TemperatureValues (to optimize computation time)
    size_t sizeTime;
    
};

#endif // TEMPERATURE_H
