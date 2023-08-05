/// \file error.cpp
/// \brief Methods of the class Error
#include <iostream>
#include <sstream>
#include <fstream>
#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "error.h"
#include "constants.h"


using namespace std;

Error::Error(){}

Error::~Error(){}

void Error::Fatal(string _errorMessage) const
{
    cout << "FATAL ERROR: " << _errorMessage << endl;
    //writing mode (app is to write at the end of the file without erase the content)
    ofstream file("log.log", ios::app);
    if(file) {file << "FATAL ERROR: " << _errorMessage << endl;}
    else  {cout << "WARNING: Unable to open file log.log." << endl;}
    file.close();
    exit(1);
}

void Error::Warning(string _warningMessage) const
{
    //writing mode (app is to write at the end of the file without erase the content)
    ofstream file("log.log", ios::app);
    if(file) {file << "WARNING: " << _warningMessage << endl;}
    else  {cout << "WARNING: Unable to open file log.log." << endl;}
    file.close();
}

void Error::Log(string _logMessage) const
{
    //cout << _logMessage << endl;
    //writing mode (app is to write at the end of the file without erase the content)
    ofstream file("log.log", ios::app);
    if(file) {file << _logMessage << endl;}
    else  {cout << "WARNING: Unable to open file log.log." << endl;}
    file.close();
}



