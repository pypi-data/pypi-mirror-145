/// \file mathematic.cpp
/// \brief Methods of the class Mathematic
#include <iostream>
#include "error.h"
#include "element.h"
#include "matrix.h"
#include "mathematic.h"
#include "constants.h"
#include <string>
#include <vector>
#include <math.h>
#include <sstream>

using namespace std;

Mathematic::Mathematic() {
    //Default values
    tol_Brent_Dicho=1e-9;
    tol_divideResidu_NR=1000.;
    NRmaximumCount=100.;
}
Mathematic::~Mathematic() {}

void Mathematic::Initialize() {}

void Mathematic::SetTolerance_Brent_Dicho(double const &_tolerance) {tol_Brent_Dicho=_tolerance;}

void Mathematic::SetNRmaximumCount(double const& _maxNbOfIterations) {NRmaximumCount=_maxNbOfIterations;}

void Mathematic::SetTolerance_NewtonRaphson(double const &_tolerance) {tol_divideResidu_NR=_tolerance;}

double Mathematic::LinearInterpolation(double const& _x, double const& _x1, double const& _x2, double const& _y1, double const& _y2)
{   
    return _y1+(_x-_x1)*(_y2-_y1)/(_x2-_x1);
}

double Mathematic::LagrangeInterpolation(double const& _x, double const& _x1, double const& _x2, double const& _x3, double const& _y1, double const& _y2, double const& _y3)
{
    double L1=0.,L2=0.,L3=0.;
    //we compute bases fonctions
    L1=((_x -_x2)/(_x1-_x2))*((_x-_x3)/(_x1-_x3));
    L2=((_x -_x1)/(_x2-_x1))*((_x-_x3)/(_x2-_x3));
    L3=((_x -_x2)/(_x3-_x2))*((_x-_x1)/(_x3-_x1));
    //we project in this base
    return L1*_y1+L2*_y2+L3*_y3;
}

double Mathematic::Dichotomy(double _lowerBound,double _upperBound,string _typeOfFuncion,double const& _alpha, \
                             vector<double> const& _coeffNonLinEq,vector<vector<double> > const& _coeffNonLinEq2)
{
    double xM=0.,residuLower=0.,residuUpper=0.,residuMiddle=0.;
    if (_typeOfFuncion=="2elementSphere"){
        residuLower= Sphere2elem(_lowerBound,_coeffNonLinEq);
        residuUpper= Sphere2elem(_upperBound,_coeffNonLinEq);
        if (residuLower*residuUpper>0){
            //error.Warning("Dicho Sphere2elem: initial upper bound increased");
            _upperBound=_alpha*_upperBound;
            residuLower= Sphere2elem(_lowerBound,_coeffNonLinEq);
            residuUpper= Sphere2elem(_upperBound,_coeffNonLinEq);
        }
        if (residuLower*residuUpper>0){error.Fatal("Dicho Sphere2elem: invalid bounds f");}
        while ( fabs(_upperBound-_lowerBound) > tol_Brent_Dicho) {
            xM=(_upperBound+_lowerBound)/2;
            residuMiddle= Sphere2elem(xM,_coeffNonLinEq);
            residuLower= Sphere2elem(_lowerBound,_coeffNonLinEq);
            residuUpper= Sphere2elem(_upperBound,_coeffNonLinEq);
            if (residuLower*residuUpper>0){error.Fatal("Dicho Sphere2elem: invalid bounds f during treatment!!!!");}
            if (residuMiddle*residuLower>0) {_lowerBound=xM;}  else {_upperBound=xM;}
        }
        return (_upperBound+_lowerBound)/2;
    }
    else if(_typeOfFuncion=="generalSphere") {       
        residuLower= SphereNelem(_lowerBound,_coeffNonLinEq,_coeffNonLinEq2);
        residuUpper= SphereNelem(_upperBound,_coeffNonLinEq,_coeffNonLinEq2);
        if (residuLower*residuUpper>0){
            error.Fatal("Dicho SphereNelem: initial upper bound increased");
            _upperBound=100*_upperBound;
            residuLower= SphereNelem(_lowerBound,_coeffNonLinEq,_coeffNonLinEq2);
            residuUpper= SphereNelem(_upperBound,_coeffNonLinEq,_coeffNonLinEq2);
        }
        if (residuLower*residuUpper>0){error.Fatal("Dicho SphereNelem: invalid bounds f");}
        while ( fabs(_upperBound-_lowerBound) > tol_Brent_Dicho) {
            xM=(_upperBound+_lowerBound)/2;
            residuMiddle= SphereNelem(xM,_coeffNonLinEq,_coeffNonLinEq2);
            residuLower= SphereNelem(_lowerBound,_coeffNonLinEq,_coeffNonLinEq2);
            residuUpper= SphereNelem(_upperBound,_coeffNonLinEq,_coeffNonLinEq2);
            if (residuLower*residuUpper>0){error.Fatal("Dicho SphereNelem: invalid bounds f during treatment!!!!");}
            if (residuMiddle*residuLower>0) {_lowerBound=xM;}  else {_upperBound=xM;}
        }
        return (_upperBound+_lowerBound)/2;
    }
    else {error.Fatal("Dichotomy not implemented for this");return -1;}
}


double Mathematic::BrentAlgorithm(double _lowerBound,double _upperBound,string type,double const& _alpha, \
                                  vector<double> const& _coeffEq,vector<vector<double> > const& _coeffEq2)
{
    if (type=="2elementSphere"){
        //initialization
        double a=_lowerBound, b=_upperBound,c=0.0, d=0.0, s=0.0, temp1=0.0, temp2=0.0, borne_sup=0.0, borne_inf=0.0;
        bool flag;
        double residuA=Sphere2elem(a,_coeffEq),residuB=Sphere2elem(b,_coeffEq),residuC=0.;
        //fisrt test
        if (residuA*residuB>0){
            //error.Warning("Brent Sphere2elem: initial upper bound increased");
            b=_alpha*b;
            residuA=Sphere2elem(a,_coeffEq);residuB=Sphere2elem(b,_coeffEq);
        }
        if (residuA*residuB>0){error.Fatal("Brent Sphere2elem: invalid bounds f");}
        if (fabs(residuA) < fabs(residuB)) {temp1=b;temp2=a;a=temp1;b=temp2;}
        c=a;flag=true;
        residuA=Sphere2elem(a,_coeffEq);
        residuB=Sphere2elem(b,_coeffEq);
        residuC=Sphere2elem(c,_coeffEq);
        while ( residuB!=0 && fabs(b-a)> tol_Brent_Dicho )    {
            if(residuA!=residuC &&  residuB!=residuC) {
                s=(a*residuB*residuC)/((residuA-residuB)*(residuA-residuC)) \
                        + (b*residuA*residuC)/((residuB-residuA)*(residuB-residuC)) \
                        + (c*residuA*residuB)/((residuC-residuA)*(residuC-residuB));            }
            else {s=b-residuB*((b-a)/(residuB-residuA));}
            if (   (0.25*3.0*(a+b)) > b   ) {borne_inf=b; borne_sup=(0.25*3.0*(a+b));}
            else {borne_sup=b; borne_inf=(0.25*3.0*(a+b));}
            if((s>borne_inf && s<borne_sup)||(flag==true && fabs(s-b)>=fabs(b-c)/2)||(flag==false&&fabs(s-b)>=fabs(c-d)/2)){s=(a+b)/2; flag=true;}
            else {flag=false;}
            d=c; c=b;
            if( Sphere2elem(a,_coeffEq)*Sphere2elem(s,_coeffEq)<0 ) {b=s;} else {a=s;}
            if ( fabs(Sphere2elem(a,_coeffEq)) < fabs(Sphere2elem(b,_coeffEq)) ) {temp1=b;temp2=a;a=temp1;b=temp2;}
        }
        return b;
    }
    else if(type=="generalSphere") {
        //initialization
        double a=_lowerBound, b=_upperBound,c=0.0, d=0.0, s=0.0, temp1=0.0, temp2=0.0, borne_sup=0.0, borne_inf=0.0;
        bool flag;
        double residuA=SphereNelem(a,_coeffEq,_coeffEq2),residuB=SphereNelem(b,_coeffEq,_coeffEq2),residuC=0.;
        //fisrt test
        if (residuA*residuB>0){
            error.Fatal("Brent SphereNelem: initial upper bound increased???");
            b=b*100;
            residuA=SphereNelem(a,_coeffEq,_coeffEq2);residuB=SphereNelem(b,_coeffEq,_coeffEq2);
        }
        if (residuA*residuB>0){error.Fatal("Brent SphereNelem: invalid bounds f");}
        if (fabs(residuA) < fabs(residuB)) {temp1=b;temp2=a;a=temp1;b=temp2;}
        c=a;flag=true;
        residuA=SphereNelem(a,_coeffEq,_coeffEq2);
        residuB=SphereNelem(b,_coeffEq,_coeffEq2);
        residuC=SphereNelem(c,_coeffEq,_coeffEq2);
        while ( residuB!=0 && fabs(b-a)> tol_Brent_Dicho )    {
            if(residuA!=residuC &&  residuB!=residuC) {
                s=(a*residuB*residuC)/((residuA-residuB)*(residuA-residuC)) \
                        + (b*residuA*residuC)/((residuB-residuA)*(residuB-residuC)) \
                        + (c*residuA*residuB)/((residuC-residuA)*(residuC-residuB));
            }
            else {s=b-residuB*((b-a)/(residuB-residuA));}
            if (   (0.25*3.0*(a+b)) > b   ) {borne_inf=b; borne_sup=(0.25*3.0*(a+b));}
            else {borne_sup=b; borne_inf=(0.25*3.0*(a+b));}
            if((s>borne_inf && s<borne_sup)||(flag==true && fabs(s-b)>=fabs(b-c)/2)||(flag==false&&fabs(s-b)>=fabs(c-d)/2)){s=(a+b)/2; flag=true;}
            else {flag=false;}
            d=c; c=b;
            if( SphereNelem(a,_coeffEq,_coeffEq2)*SphereNelem(s,_coeffEq,_coeffEq2)<0 ) {b=s;} else {a=s;}
            if ( fabs(SphereNelem(a,_coeffEq,_coeffEq2)) < fabs(SphereNelem(b,_coeffEq,_coeffEq2)) ) {temp1=b;temp2=a;a=temp1;b=temp2;}
        }
        return b;
    }
    else {error.Fatal("Brent not implemented for this");return -1;}
}

double Mathematic::newtonRaphson(double _lowerBound,double _upperBound,string type,double const& _alpha, \
                                 vector<double> const& _coeffEq,vector<vector<double> > const& _coeffEq2)
{

    if (type=="2elementSphere"){
        //the order of magnitude of residu is dependant of polynom, so we choice a residu that is a fraction of initial residu
        //function is : a*Xi^((x+y)/y)+b*Xi^x/y+c*Xi+D=0
        //derivation  : a*((x+y)/y)*Xi^x/y+b*(x/y)*Xi^(x-y)/y+c
        //delta=-function(Xi)/derivation(Xi)
        //Xplus1=Xi+delta;

        int count=1;
        double a=_coeffEq[0],b=_coeffEq[1],c=_coeffEq[2],d=_coeffEq[3],X=_coeffEq[4],Y=_coeffEq[5];
        double residu=1e30,upperResidu=1e30,lowerResidu=1e30,epsilon=0.,Xbrent=0.;
        //firt point for NR is first point of dichotomy because it's good approximation
        double xM=(_lowerBound+_upperBound)/2;

        upperResidu=fabs(a*pow(_upperBound,(X+Y)/Y)+b*pow(_upperBound,X/Y)+c*_upperBound+d);
        lowerResidu=fabs(a*pow(_lowerBound,(X+Y)/Y)+b*pow(_lowerBound,X/Y)+c*_lowerBound+d);
        residu=a*pow(xM,(X+Y)/Y)+b*pow(xM,X/Y)+c*xM+d;

        // we want "tol_Brent_Dicho" tolerance but if this tolerance is done at the beginning
        //we keep initial residu divided by "tol_divideResidu_NR"
        if (lowerResidu<tol_Brent_Dicho || upperResidu<tol_Brent_Dicho) {
            if (upperResidu<lowerResidu) {epsilon=upperResidu/tol_divideResidu_NR;}
            else {epsilon=lowerResidu/tol_divideResidu_NR;}        }
        else {epsilon=tol_Brent_Dicho;}

        //NR iterations
        while ( fabs(residu)>epsilon && count<NRmaximumCount ) {
            xM=xM-(a*pow(xM,(X+Y)/Y)+b*pow(xM,X/Y)+c*xM+d )/( a*((X+Y)/Y)*pow(xM,X/Y)+b*(X/Y)*pow(xM,(X-Y)/Y)+c);
            residu= a*pow(xM,(X+Y)/Y)+b*pow(xM,X/Y)+c*xM+d;
            count=count+1;
        }
        if (count>=NRmaximumCount) {
            error.Warning("NewtonRaphson met its maximum nb of iterations->switch on dichotomy algorithm");
            Xbrent=BrentAlgorithm(_lowerBound,_upperBound,type,_alpha,_coeffEq,_coeffEq2);
            return Xbrent;
        }
        else {return xM;}
    }
    else if(type=="generalSphere") {
        error.Fatal("Newton raphson not implemented for 'generalSphere'");return -1;
    }
    else{error.Fatal("Newton raphson not implemented for this growth equation");return -1;}
}

double Mathematic::constrainedNewtonRaphson(double _lowerBound,double _upperBound,string type,double const& _alpha, \
                                            vector<double> const& _coeffEq,vector<vector<double> > const& _coeffEq2)
{

    if (type=="2elementSphere"){
        //the order of magnitude of residu is dependant of polynom, so we choice a residu that is a fraction of initial residu
        //function is : a*Xi^((x+y)/y)+b*Xi^x/y+c*Xi+D=0
        //derivation  : a*((x+y)/y)*Xi^x/y+b*(x/y)*Xi^(x-y)/y+c
        //delta=-function(Xi)/derivation(Xi)
        //Xplus1=Xi+delta;

        int count=1;
        double a=_coeffEq[0],b=_coeffEq[1],c=_coeffEq[2],d=_coeffEq[3],X=_coeffEq[4],Y=_coeffEq[5];
        double residu=1e30,upperResidu=1e30,lowerResidu=1e30,epsilon=0.,coeffRelaxation=0.,countRelax=1,Xbrent=0.;
        //firt point for NR is first point of dichotomy because it's good approximation
        double xM=(_lowerBound+_upperBound)/2,xM_temp;

        upperResidu=a*pow(_upperBound,(X+Y)/Y)+b*pow(_upperBound,X/Y)+c*_upperBound+d;
        lowerResidu=a*pow(_lowerBound,(X+Y)/Y)+b*pow(_lowerBound,X/Y)+c*_lowerBound+d;
        residu=a*pow(xM,(X+Y)/Y)+b*pow(xM,X/Y)+c*xM+d;

        // we want "tol_Brent_Dicho" tolerance but if this tolerance is done at the beginning
        //we keep initial residu divided by "tol_divideResidu_NR"
        if (fabs(lowerResidu)<tol_Brent_Dicho || fabs(upperResidu)<tol_Brent_Dicho) {
            if (fabs(upperResidu)<fabs(lowerResidu)) {epsilon=fabs(upperResidu)/tol_divideResidu_NR;}
            else {epsilon=fabs(lowerResidu)/tol_divideResidu_NR;}        }
        else {epsilon=tol_Brent_Dicho;}

        //NR iterations
        count=1;
        while ( fabs(residu)>epsilon && count<NRmaximumCount ) {
            xM_temp=xM-coeffRelaxation*(a*pow(xM,(X+Y)/Y)+b*pow(xM,X/Y)+c*xM+d )/( a*((X+Y)/Y)*pow(xM,X/Y)+b*(X/Y)*pow(xM,(X-Y)/Y)+c);
            if (xM_temp<lowerResidu || xM_temp>upperResidu){
                countRelax=1;
                while (xM_temp<lowerResidu && xM_temp>upperResidu && countRelax<100) {
                    coeffRelaxation=coeffRelaxation*0.5;
                    xM_temp=xM_temp-coeffRelaxation*(a*pow(xM,(X+Y)/Y)+b*pow(xM,X/Y)+c*xM+d )/( a*((X+Y)/Y)*pow(xM,X/Y)+b*(X/Y)*pow(xM,(X-Y)/Y)+c);
                    countRelax=countRelax+1;
                }
                xM=xM_temp;
                if (countRelax>=100) {error.Fatal("Huge relaxation in constrained NR->we strop algorithm");}            }
            else {xM=xM_temp;}
            residu= a*pow(xM,(X+Y)/Y)+b*pow(xM,X/Y)+c*xM+d;
            coeffRelaxation=1;
            count=count+1;
        }
        if (count>=NRmaximumCount) {
            error.Warning("Constraied NewtonRaphson met its maximum nb of iterations->switch on dichotomy algorithm");
            Xbrent=BrentAlgorithm(_lowerBound,_upperBound,type,_alpha,_coeffEq,_coeffEq2);
            return Xbrent;        }
        else {return xM;}
    }
    else if(type=="generalSphere") {
        error.Fatal("constrainedNewtonRaphson not implemented for 'generalSphere'");return -1;
    }
    else{error.Fatal("v not implemented for this growth equation");return -1;}
}

double Mathematic::Sphere2elem(double x,vector<double> const& _coeff)
{
    //a.Xi^(x+y)/y + b.Xi^x/y + c.Xi +d
    return _coeff[0]*pow(x,(_coeff[4]+_coeff[5])/_coeff[5])+_coeff[1]*pow(x,_coeff[4]/_coeff[5])+_coeff[2]*x+_coeff[3];
}

double Mathematic::SphereNelem(double _dotR,vector<double> const& _nullHere,vector<vector<double> > const& _coeff2)
{
    //Coeff[0] : slowElementChemistry      //Coeff[1] : D        //Coeff[2] : X0         //Coeff[3] : XP
    //Coeff[4] : KsGT                      //Coeff[5] : _alpha   //Coeff[6] : Radius[i]
    //Function ==> _alpha*XP-\frac{D.X0-D.alpha.XP}{dotR.R-D}
    double temp=0.,partJ=0.,fonction=1,coeff_5_0=_coeff2[5][0],coeff_6_0=_coeff2[6][0];
    for (size_t j=0;j<_coeff2[0].size();j++) {
        temp=coeff_5_0*_coeff2[3][j]- \
                (_coeff2[1][j]*_coeff2[2][j]-coeff_5_0*_coeff2[1][j]*_coeff2[3][j])/(_dotR*coeff_6_0-_coeff2[1][j]);
        partJ=pow(temp,_coeff2[0][j]);
        fonction=fonction*partJ;
    }
    return fonction-_coeff2[4][0];
}

double Mathematic::radcubic(double nb)        //retourne le radical cubique du nombre
{
    if (nb>0)
        return pow(nb,1.0/3.0);            //pow ne marche pas bien avec des nombre negatifs
    else
        return -pow(-nb,1.0/3.0);
}
//!-----------------------------------------------------------------------------------------------------------------------
//! Donne la racine d'un polynome de degré 1 retourne le nombre de racines
//!-----------------------------------------------------------------------------------------------------------------------
int Mathematic::PolynomFirstDegree(double a,double b,complexe buffer[1])
{
    buffer[0].re = -b/a;
    buffer[0].im = 0;
    return 1;
}
//!-----------------------------------------------------------------------------------------------------------------------
//! Resolution d'une équation du deuxieme degré retourne le nombre de racines
//!-----------------------------------------------------------------------------------------------------------------------
int Mathematic::polynomSecondDegree(double a,double b,double c,complexe buffer[2])
{
    double delta=0.;
    if (a == 0) {return PolynomFirstDegree(b,c,buffer);}
    delta = b*b-4*a*c;

    if (delta>=0)        //racines réelles
    {
        buffer[0].re = (-b-sqrt(delta))/(2*a);
        buffer[0].im = 0;
        buffer[1].re = (-b+sqrt(delta))/(2*a);
        buffer[1].im = 0;
    }
    else            //racines complexes conjugées
    {
        buffer[0].re = -b/(2*a);
        buffer[0].im = (-sqrt(-delta))/(2*a);
        buffer[1].re = buffer[0].re;
        buffer[1].im = -buffer[0].im;
    }

    return 2;
}
//!-----------------------------------------------------------------------------------------------------------------------
//! Resolution d'une équation du troisième degré type (ax^3+bx^2+cx+d=0)
//! (ce type d'équation a toujours au moins une racine réelle)
//! Retourne le nombre de racines //http://gilles.costantini.pagesperso-orange.fr/prepas_fichiers/dg3.pdf
//!-----------------------------------------------------------------------------------------------------------------------
int Mathematic::polynomThirdDegree(double a,double b,double c,double d,complexe buffer[3])
{
    double p=0.,q=0.,delta=0.,r=0.,t=0.,arg=0.;
    int i=0;

    if (a == 0) {return polynomSecondDegree(b,c,d,buffer);}
    //on divise tout par a et on pose x=X-b/(3a)
    //on arrive a une équation du type X^3+pX+q = 0 avec

    p = (-b*b)/(3*a*a) + c/a;
    q = (2*b*b*b)/(27*a*a*a) - (b*c)/(3*a*a) + d/a; //facile a retrouver en posant le calcul

    //relations entre les racines
    //X1+X2+X3 = 0
    //X1*X2 + X2*X3 + X1*X3 = p
    //X1*X2*X3 = -q

    //on pose X = u+v en imposant 3u*v + p = 0
    //en remplacant on tombe sur l'équation u^3+v^3 = q
    //or on a uv = -p/3 ie u^3*v^3 = -p^3/27

    //On a la somme et le produit, on peut trouver u^3 et v^3
    //u^3 et v^3 solutions de Y^2 + qY -p^3/27 = 0
    delta = q*q/4.0 + p*p*p/27.0;

    //X1 = u+v, c'est la somme des racines cubiques des solutions
    //Et avec les relations coefficients-racines on a X2+X3 = -X1    et X2*X3 = -q/X1
    //donc X2 et X3 solutions de Z^2+X1*Z-q/X1
    if (delta>0)    {
        buffer[0].re = radcubic(-q/2.0+sqrt(delta))+radcubic(-q/2.0-sqrt(delta));
        buffer[0].im = 0;
        if (buffer[0].re != 0)
            polynomSecondDegree(1,buffer[0].re,-q/buffer[0].re,&buffer[1]);
        else    //sinon on peut factoriser par X (ca donne X^2+p=0)
            polynomSecondDegree(1,0,p,&buffer[1]);


        //on a trois solutions de l'equation en X mais on a posé x=X-b/3a
        //il suffit donc de faire -b/3a sur les parties réelles des solutions en X

        buffer[0].re += -b/(3*a);
        buffer[1].re += -b/(3*a);
        buffer[2].re += -b/(3*a);
    }
    else if (delta == 0)    {
        //on ne peut pas rallier ce cas a celui du dessus car le radical cubique d'un complexe
        //est difficile a exprimer (on peut le faire en fonction d'arctan et de sin)
        //Mais si delta == 0 on a une solution double donc en cette solution la dérivée
        //du polynome s'annule aussi en ce point ie
        //3X^2+p=0
        buffer[0].re = sqrt(-p/3);
        buffer[0].im = 0;
        if (buffer[0].re != 0)
            polynomSecondDegree(1,buffer[0].re,-q/buffer[0].re,&buffer[1]);
        else    //sinon on peut factoriser par X
            polynomSecondDegree(1,0,p,&buffer[1]);

        //pareil que si delta > 0
        buffer[0].re += -b/(3*a);
        buffer[1].re += -b/(3*a);
        buffer[2].re += -b/(3*a);
    }
    else                {//trois racines réelles
        //si delta < 0 on fait une autre méthode
        //u^3 et v^3 solutions de l'équation sont des complexes conjugés (delta<0)
        //ecrivons u^3 sous forme exponentielle
        //u^3 = r*e^(it) = -q/2+i*sqrt(delta) (solution de l'eq du deuxieme deg)
        //r est le module egal a la racine carrée de la somme des carrées de la partie
        //imaginaire et réelle, en reprenant l'expression de delta en trouve r=sqrt(-p^3/27)
        //(p<0    car delta < 0)
        //e^(it) = cos(t)+i*sint(t), en identifiant partie imaginaire et réelle
        //on trouve cos(t) = -q/(2r) (t =acos(-q/(2r)))
        //u^3 et v^3 conjugées donc les solutions sont réelles
        //les trois solutions sont les uk+vk avec uk = sqrt(-p/3)*e((t+2*k*M_PI)/3)
        //                                         vk = uk(barre)
        //Xk = 2*sqrt(-p/3)*cos((t+2k*M_PI)/3)
        //xk = Xk - b/(3a)
        r = sqrt(-p/3);
        arg = -q/(2*sqrt(-p*p*p/27));
        t = acos(arg);
        i=0;
        for (i=0;i<3;i++)    {
            buffer[i].re = 2*sqrt(-p/3)*cos((t+2*i*M_PI)/3.0)-b/(3*a);
            buffer[i].im = 0;
        }
    }
    return 3;
}
//!-----------------------------------------------------------------------------------------------------------------------
//! Resoud une équation du quatrième degré, renvoye le nombre de racines
//!-----------------------------------------------------------------------------------------------------------------------
int Mathematic::polynomFourthDegree(double a,double b,double c,double d,double e,complexe buffer[4])
{
    double A=0.,B=0.,C=0.,Z=0.,u=0.,x=0.,y=0.;
    int i=0;
    complexe sol3[3];
    complexe sol2[2];

    if (a == 0) {return polynomThirdDegree(b,c,d,e,buffer);}

    //on divise par a puis on remplace x=X-b/4a
    //on tombe sur un polynome du type X^4+AX^2+BX+C avec
    A = (-3*b*b)/(8*a*a) + c/a;
    B = (b*b*b)/(8*a*a*a) - (b*c)/(2*a*a) + d/a;
    C = -3*(b*b*b*b)/(256*a*a*a*a) + (c*b*b)/(16*a*a*a) - (d*b)/(4*a*a) +e/a;

    //Si B=0 on sait resoudre ! en prenant Z = X^2
    if (B == 0)    {
        //on calcule les Z
        polynomSecondDegree(1,A,C,sol2);

        //On fait ensuite + ou - la racine des sols pour avoir les X
        //Attention !! sqrt(a+i*b) != sqrt(a)+i*sqrt(b)
        //Formule générale :
        // sqrt (x+iy) = sqrt(2*(sqrt(x^2+y^2)+x))/2 + i*sqrt(2*(sqrt(x^2+y^2)-x))/2 * signe de y
        //on fait -b/4a et on a les x

        for (i=0;i<4;i++)        {
            x = sol2[i % 2].re;
            y = sol2[i % 2].im;

            buffer[i].re = sqrt(2*(sqrt(x*x + y*y)+x))/2*(1-(i/2)*2) - b/(4*a);
            buffer[i].im = sqrt(2*(sqrt(x*x + y*y)-x))/2*(1-(i/2)*2);
            if (y<0) {buffer[i].im = -buffer[i].im;}
        }
    }
    else   {
        //On suppose X racine : on essaye de factoriser X^4+AX^2 en (X^2+u/2)^2
        //or (X^2+u/2)^2 = X^4 + uX^2 + u^2/4
        //et X^4 = -AX^2 - BX - C (car X racine du polynome)
        //Donc au final (X^2+u/2)^2 = (u-A)X^2 - BX + (u^2)/4 - C
        //On a une equation du second degre, on cherche u tel que
        // * delta = 0
        // * u != A

        //On calcule le discriminant et on veut u = 0
        //on tombe sur u^3 - A*u^2 -4 *C*u + 4*A*C - B^2 = 0
        //si u = A alors B serait egal à 0 ce qui n'est pas le cas (distinction faite plus haut)
        //on calcule les valeurs possibles de u
        polynomThirdDegree(1,-A,-4*C,4*A*C-B*B,sol3);

        //on prend le u réel le plus grand (voir pour la suite)
        u=sol3[0].re;
        //Par convention, ma fonction troisième construit sol3 tq sol3[0] est reel

        for (i=0;i<3;i++)        {
            if (sol3[i].im == 0 && sol3[i].re > u)
                u = sol3[i].re;
        }

        //delta = 0 donc Z est solution double de (u-A)X^2 - bX + (u^2)/4 - C
        // avec Z = B/(2*(u-A))
        //on peut factoriser

        Z = B/(2*(u-A));

        //(X^2+u/2)^2 = (u-A)(X-Z)^2
        //Il existe au moins un u tel que u>A d'apres l'équation dont u est racine
        //les X solutions sont donc les sols de
        // X^2+u/2 = sqrt (u-A)*(X-Z)
        // X^2+u/2 = -sqrt (u-A)*(X-Z)
        polynomSecondDegree(1,-sqrt(u-A),u/2 + Z*sqrt(u-A),buffer);
        polynomSecondDegree(1, sqrt(u-A),u/2 - Z*sqrt(u-A),&buffer[2]);

        //on fait -4b/a pour chaque solution pour avoir les x
        for (i=0;i<4;i++) {buffer[i].re -= b/(4*a);}
    }
    return 4;
}

vector<vector<double> > Mathematic::rk45adaptive(double initialDt,vector<double> const& tempsINI_FIN, \
                                 vector<double> const& CI,int const& indexFonctionAresoudre,vector<double> const& constantesToDefineDiffSystem)
{   //(version didier qui marche bien validée avec matlab)
    if(tempsINI_FIN.size()!=2) {error.Fatal("vector temps must have size 2");}
    size_t sizeVector=CI.size();
    double tol=1e-6,coeffLowerBound=0.2,coeffUpperBound=10.0,AbsTol=1e-15,RelTol=1e-10,safeCoeff=0.8;
    double h_k=initialDt,t_k=tempsINI_FIN[0],h_opt=0;
    vector<double> k1,k2,k3,k4,k5,k6,k7,f,ykAdditionalVect,yk,Y_kp1,zeros;
    k1.assign(sizeVector,0);k2=k1;k3=k1;k4=k1;k5=k1;k6=k1;k7=k1;
    ykAdditionalVect=k1;yk=k1;Y_kp1=k1;zeros=k1;
    vector<double> initLine; for (size_t i=0;i<sizeVector;i++) {initLine.push_back(0.0);}
    vector<vector<double> > Results; Results.push_back(initLine);
    vector<double> Times;       Times.push_back(t_k);
    yk=CI;Results[0]=yk;
    double a1=0;
    double a2=1./5.,b21=1./5.;
    double a3=3./10.,b31=3./40.,b32=9./40.;
    double a4=4./5.,b41=44./45.,b42=-56./15.,b43=32./9.;
    double a5=8./9.,b51=19372./6561.,b52=-25360./2187.,b53=64448./6561.,b54=-212./729.;
    double a6=1.,b61=9017./3168.,b62=-355./33.,b63=46732./5247.,b64=49./176.,b65=-5103./18656.;
    double a7=1.,b71=35./384.,b72=0.,b73=500./1113.,b74=125./192.,b75=-2187./6784.,b76=11./84.;
    //schema 5eme order (we use hypothesis of local extrapolation)
    double d1=b71,d2=b72,d3=b73,d4=b74,d5=b75,d6=b76,d7=0;
    //error coefficient
    double e1=71./57600.,e2=0.0,e3=-71./16695.,e4=71./1920.,e5=-17253./339200.,e6=22./525.,e7=-1./40.;
    //main loop
    double localError=0,divisionPrErreur=0,y0abs=0,y1abs=0,mesureGlobaleError=0;
    while (t_k<tempsINI_FIN[1]) {
        f=functionRk45(indexFonctionAresoudre,constantesToDefineDiffSystem,t_k+a1*h_k,yk,zeros);
        for (size_t i=0;i<sizeVector;i++) {k1[i]=h_k*f[i]; ykAdditionalVect[i]=b21*k1[i];}
        f=functionRk45(indexFonctionAresoudre,constantesToDefineDiffSystem,t_k+a2*h_k,yk,ykAdditionalVect);
        for (size_t i=0;i<sizeVector;i++) {k2[i]=h_k*f[i]; ykAdditionalVect[i]=b31*k1[i]+b32*k2[i];}
        f=functionRk45(indexFonctionAresoudre,constantesToDefineDiffSystem,t_k+a3*h_k,yk,ykAdditionalVect);
        for (size_t i=0;i<sizeVector;i++) {k3[i]=h_k*f[i]; ykAdditionalVect[i]=b41*k1[i]+b42*k2[i]+b43*k3[i];}
        f=functionRk45(indexFonctionAresoudre,constantesToDefineDiffSystem,t_k+a4*h_k,yk,ykAdditionalVect);
        for (size_t i=0;i<sizeVector;i++) {k4[i]=h_k*f[i]; ykAdditionalVect[i]=b51*k1[i]+b52*k2[i]+b53*k3[i]+b54*k4[i];}
        f=functionRk45(indexFonctionAresoudre,constantesToDefineDiffSystem,t_k+a5*h_k,yk,ykAdditionalVect);
        for (size_t i=0;i<sizeVector;i++) {k5[i]=h_k*f[i]; ykAdditionalVect[i]=b61*k1[i]+b62*k2[i]+b63*k3[i]+b64*k4[i]+b65*k5[i];}
        f=functionRk45(indexFonctionAresoudre,constantesToDefineDiffSystem,t_k+a6*h_k,yk,ykAdditionalVect);
        for (size_t i=0;i<sizeVector;i++) {k6[i]=h_k*f[i]; ykAdditionalVect[i]=b71*k1[i]+b72*k2[i]+b73*k3[i]+b74*k4[i]+b75*k5[i]+b76*k6[i];}
        f=functionRk45(indexFonctionAresoudre,constantesToDefineDiffSystem,t_k+a7*h_k,yk,ykAdditionalVect);
        localError=0;divisionPrErreur=0;
        for (size_t i=0;i<sizeVector;i++) {
            k7[i]=h_k*f[i];
            Y_kp1[i]=yk[i]+d1*k1[i]+d2*k2[i]+d3*k3[i]+d4*k4[i]+d5*k5[i]+d6*k6[i]+d7*k7[i];
            y0abs=fabs(yk[i]);y1abs=fabs(Y_kp1[i]);
            if (y0abs<y1abs) { divisionPrErreur=AbsTol+RelTol*y1abs;}
            else {divisionPrErreur=AbsTol+RelTol*y0abs;}
            localError=localError+pow(((e1*k1[i]+e2*k2[i]+e3*k3[i]+e4*k4[i]+e5*k5[i]+e6*k6[i]+e7*k7[i])/divisionPrErreur),2);
        }
        mesureGlobaleError=sqrt((1.0/sizeVector)*localError);
        h_opt=safeCoeff*h_k*pow(tol/mesureGlobaleError,1.0/5.0);
        if (mesureGlobaleError<=tol) {
            t_k=t_k+h_k;           yk=Y_kp1;
            Times.push_back(t_k);  Results.push_back(yk);
            if (h_opt<tempsINI_FIN[1]-t_k) {if (h_opt/h_k>coeffUpperBound) {h_k=coeffUpperBound*h_k;} else {h_k=h_opt;}}
            else {h_k=tempsINI_FIN[1]-t_k;}
        }
        else {if (h_opt/h_k<coeffLowerBound) {h_k=coeffLowerBound*h_k;} else {h_k=h_opt;}}
    }
    //we fill result matrix
    vector<double> tempVect;
    vector< vector<double> > timeAndResults;
    for (size_t i=0;i<Times.size();i++) {
        tempVect.clear();
        tempVect.push_back(Times[i]);
        for (size_t j=0;j<Results[i].size();j++) {tempVect.push_back(Results[i][j]);}
        timeAndResults.push_back(tempVect);
    }
    return timeAndResults;
}


vector<double> Mathematic::functionRk45(int const& indexFonctionAresoudre,vector<double> const& constantesToDefineDiffSystem,double const& t_k_part,vector<double> const& ykWithoutCoeff,vector<double> const& addPartY)
{
    //initialization of RK systeme
    size_t nbOfEquations=ykWithoutCoeff.size();
    vector<double> f_k,yk;
    for (size_t i=0;i<nbOfEquations;i++) {f_k.push_back(0.0);yk.push_back(0);yk[i]=ykWithoutCoeff[i]+addPartY[i];}

    //definition of systeme that we want to solve
    if(indexFonctionAresoudre==1)
    {   //solve unstationnary nucleation
        double delta=constantesToDefineDiffSystem[0];
        double tau=constantesToDefineDiffSystem[1];
        f_k[0]=(delta-yk[0])/tau;
    }
    else {error.Fatal("In functionRk45adapt, 'indexFonctionAresoudre' must be 1 or other functions have to be implemented");}

    return f_k;
}
