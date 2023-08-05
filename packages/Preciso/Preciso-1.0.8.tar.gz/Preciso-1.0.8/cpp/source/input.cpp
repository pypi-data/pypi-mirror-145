/// \file input.cpp
/// \brief Methods of the class Input
#include <iostream>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>  //For file read/write options
#include "input.h"
#include "string.h"
#include "error.h"
#include "constants.h"

using namespace std;

Input::Input() {}

Input::~Input() {}

string Input::FileName(int const& argc, const char *argv[])
{
    string path;             //Default value : current folder
    string fileName("data"); //Default value : "data"

    for (int i=1;i<argc;i++){
        if(strcmp(argv[i],"-path")==0) {if (i+1<argc) {path=argv[i+1];} else {error.Fatal("PreciSo have been launch with an incorrect number of arguments");}}
        if(strcmp(argv[i],"-file")==0) {if (i+1<argc) {fileName=argv[i+1];} else {error.Fatal("PreciSo have been launch with an incorrect number of arguments");}}
    }
    return path + fileName ;
}

void Input::LinesStartingWithKeyword(string const& _inputFileName,string const& _keyword, vector<vector<string> > &_lines, bool _optional)
{
    vector<string> arg;
    string dump;
    //Reinitialize the lines variable
    _lines.clear();
    //Opening _inputFileName converted in a table of chars, ios::in indicates a read only
    ifstream datafile(_inputFileName.c_str(), ios::in);
    //End of programme if no datafile
    if (!datafile) {error.Fatal("File "+ _inputFileName +" not found");}

    while (!datafile.eof())    {
        //while the file has not been completely read
        //we read line by line in the text "database"
        getline(datafile,dump);
        arg.clear();
        Parse(dump,arg);

        if (arg.size()!=0 && arg[0]==_keyword)        {
            //The line starts with the sought keyword
            //Adding the line information to the vector _lines
            _lines.push_back(arg);
        }
    }
    datafile.close();

    if (!_optional) if (_lines.size()==0) error.Fatal("keyword " + _keyword + " not found in datafile.");
}

//function to enumerate the number of word in a line and to access easily on each word
void Input::Parse(string _dump, vector<string>&  _arg)
{                                                   //with _arg[0] _arg[1] _arg[2]...
    size_t pos=0;
    _arg.clear();
    if(_dump.size()!=0)    {
        while(1)        {
            pos=_dump.find_first_of(" \t\n\b\r");
            if(pos==string::npos){
                _arg.push_back(_dump);
                break;
            } else
                if(pos!=0) _arg.push_back(_dump.substr(0,pos));
            if(pos>=_dump.size()-1) break;
            _dump=_dump.substr(pos+1);
        }
    }
}
