/// \file main.cpp
/// \brief Main function of the program PreciSo_3
/// \param argc Number of executable input arguments
/// \param argv Table of pointers to the input arguments
/// \callgraph

#define _USE_MATH_DEFINES
#include <cmath>
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include "nodepreciso.h"
#include "constants.h"
#include "time.h"

using namespace std;

/// \todo OPTIMIZATION OF COMPUTATION TIME :
///  |Gain| |implemented?|
///  (good)     OK        -minimisation of ".size()" of "[]" of "Get..." and "comparaison between string"
///  (good)     OK        -noDeclarations in loops
///  (?)                  -sauvegarder les calculs de plusieurs pas de temps et les copiers toutes les "n" iterations pr eviter appel au disque dur
///  (?)                  -pour ecriture des fichiers texte, ouvrir une fois au d�but et ne pas fermer les fichiers ensuite, ne fermer qu'une fois � la fin
///  (?)                  -convert vector<vector>> by one vector of size N�?
///  (?)                  -pas de comparaison entre string juste en nombre (cf. chimistry array for exemple)
///  (huge)               -RESOLUTION OF NON LINEAR EQ.
///  (good)               -improve time step criterion (adaptative)
///  (huge?)               -parallelisation
/// - si r* change de signe quand il y a dissolution (a confirmer) alors on peut automatiquement detecter que c'est un step de dissolution et dire qu'au pas de temps suivant on reprend le pas de temps qu'on avait juste avant, donc on accelere tout de suite.
/// - on peut jouer sur le dt mini mais je pense qu'il est deja, assez restrictif actuellement, a moins de fixer un critere qui l'augmente. Du type : si le nombre de pas de temps rejete (que l'on connait) sur le nombre de pas de temps totaux (que l'on connait aussi) depasse x% (5% par exemple) alors on augmente le dt mini.
/// - et on peut meme coupler en disant que si on est dans le cas d'avant (dt rejete/dt totaux (acceptes+rejetes)>5%) et que c'est � cause de dissolution, on augmente de meme automatiquement le rayon de dissolution. Physiquement cela revient a dire que l'on a une grosse phase de dissolution et qu'on la traite de maniere un peu plus globale.
/// - decouplage des noeuds non lies => TC
/// - decouplage pas de temps diffusion et precipitation => TC

/// \todo �crire les resultats ds deux dossiers separes ???
/// \todo problem avec lin class managment ? (cf. discontinuit� ds newBenInput1node)
/// \todo if node number not differents we have to launch the method "error.fatal"
/// \todo GNU plot still have problems or not ? (don't find directory ?)
/// \todo Increase the precision of constants ? (R=8.3144621, kB=1.381e-23)
/// \todo implement instationnay diffusion
/// \todo correction of numeric resolution for nb of slowElement > 2
/// \todo Modify minimum time step criterion to an absolute criterion (not dependent on the current simulation time)
/// \todo Sell preciso $1M
/// \todo Add credits in the files (PreciSo_v3, developped by ..., contact ...)
/// \todo create OCTAVE/MATLAB files which check automaticly all test codes with their associed input
/// \todo certain parametre mechanical ne sont pas d�fini dans les nodeProperty (type de model que l'on choisi par exemple)

#include <stdio.h>
#include <stdlib.h>

int main(int argc, const char *argv[])
{
    //PreciSo_3 -path .\blabla\ -file data.txt
    
    cout << "Welcome to PreciSo v3.0 (Dec. 2021)" << endl;

    //ofstream fileTemp("saveParticularResults.txt", ios::trunc);
    //fileTemp.close();


//    double time=0.;
//    clock_t tStart, tInitilization, tEnd;
    
    remove("computation.end");remove("log.log");
//    tStart = clock();
    NodePreciso nodepreciso;
    nodepreciso.Initialize(argc, argv);
//    tInitilization = clock();
//    time = (float)(tInitilization-tStart)/CLOCKS_PER_SEC;
//    cout << "Time for initialization: " << time << "s" << endl;
    nodepreciso.Run();
//    tEnd = clock();
//    time = (float)(tEnd-tInitilization)/CLOCKS_PER_SEC;
//    cout << "End -> Time for computation: " << time << "s" << endl;
    ofstream file("computation.end", ios::trunc);file.close();
    
    return 0;
}

//
