#!/usr/bin/python
import sys
import argparse
import numpy as np
from io import StringIO
import csv
from astropy import constants as const
from astropy import units as u
import magflux

def Blambda(T,lamb):
    lamb5=(lamb.to(u.m))**5    
    fac=const.h*const.c/(lamb.to(u.m)*const.k_B*T)
    bl=2.0*(const.c**2)*const.h/lamb5/(np.exp(fac)-1)
    return bl.to(u.erg/u.cm/u.cm/u.angstrom/u.s)

def Blunitless(T,lamb):
    lamb5=(lamb.to(u.m))**5    
    fac=const.h*const.c/(lamb.to(u.m)*const.k_B*T)
    bl=2.0*(const.c**2)*const.h/lamb5/(np.exp(fac)-1)
    return bl


def photon_Blunitless(T,lamb):
    pB=Blambda(T,lamb)/(const.h*const.c/(lamb.to(u.m)))

    return pB

def Nstar(lambda_micron,stellar_temperature,rsol,dpc,dtel,dstel,dlam_micron,throughput,texphour,info=False):
    tstar=stellar_temperature*u.K    
    lamin=lambda_micron*u.micron
    d=dpc*u.pc
    runit=const.R_sun            
    r=rsol*runit        
    flux=np.pi*Blunitless(tstar,lamin)*r*r/(d*d)
    photonf=np.pi*photon_Blunitless(tstar,lamin)*r*r/(d*d)
    a=np.pi*(dtel/2.0*u.m)**2 - np.pi*(dstel/2.0*u.m)**2
    dl=dlam_micron*u.micron
    texp=texphour*u.h
    photon=photonf*a*dl*texp*throughput
    
    if info:
        print("B(lambda) for",tstar,"at ",lamin)
        print('{:e}'.format(Blunitless(tstar,lamin).to(u.erg/u.cm/u.cm/u.angstrom/u.s)))
        print('{:e}'.format(Blunitless(tstar,lamin).to(u.erg/u.cm/u.cm/u.micron/u.s)))
        print('{:e}'.format(Blunitless(tstar,lamin).to(u.J/u.m/u.m/u.m/u.s)))
        print("---------------------")
        print("FLUX from a sphere with r=",rsol,"[Rsol] and","dpc=",d,"[pc]")
        print(flux.to(u.erg/u.cm/u.cm/u.micron/u.s))
        print("Photon FLUX from a sphere with  r=",rsol,"[Rsol] and","dpc=",d,"[pc]")
        print(photonf.to(1/u.cm/u.cm/u.micron/u.s))
        print("---------------------")
        print("Photon Count with observation:")
        print("  telescope diameter", dtel, "[m]")
        print("  band width", dlam_micron,"[micron]")
        print("  exposure", texphour,"[hour] = ",texphour*60.0," [min]")
        print("  throughput", throughput)
        print("N=",'{:e}'.format(photon.to(1)))
        print("photon noise 1/sqrt(N)=",np.sqrt(1.0/photon.to(1))*1e6,"[ppm]")
        print("photon noise 1/sqrt(N)=",np.sqrt(1.0/photon.to(1))*1e2,"[%]")
        print("7 sigma depth=",np.sqrt(1.0/photon.to(1))*1e2*7.0,"[%]")


    Nphoton=photon.to(1)
    sign=np.sqrt(Nphoton)
    return flux,photonf,Nphoton,sign

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute stellar counts using planck function')
    parser.add_argument('-t', nargs=1,default=[3000.0], help='temperature [K]')
    parser.add_argument('-micron', nargs=1,default=[1.4], help='lambda (micron)')

    parser.add_argument('-d', nargs=1,default=[20.0],help='distance [pc]')
    parser.add_argument('-r', nargs=1,default=[0.2],help='radius in unit of Rsolar',type=float)

    parser.add_argument('-Dm', default=[0.31],nargs=1,help='telescope diameter [m]')
    parser.add_argument('-Dsm', default=[0.09],nargs=1,help='secondary telescope diameter [m]')
    
    parser.add_argument('-dmicron', nargs=1,default=[0.6],help='band width [micron]')
    parser.add_argument('-th', nargs=1,default=[0.0833],help='exposure [hour]')
    parser.add_argument('-tp', nargs=1,default=[0.7],help='throughput')
    parser.add_argument('-b', nargs=1, default=["H"],help='Choose band from U,B,V,R,I,J,H,Ks,L,M,N,Q')

    args = parser.parse_args()           
    stellar_temprature=float(args.t[0])
    lambda_micron=float(args.micron[0])
    dpc=float(args.d[0])
    rsol=args.r[0]
    dtel=args.Dm[0]
    dstel=args.Dsm[0]
    dlam_micron=float(args.dmicron[0])
    throughput=float(args.tp[0])
    texphour=float(args.th[0])
    
    flux,photonf,photon,sign=Nstar(lambda_micron,stellar_temperature,rsol,dpc,dtel,dstel,dlam_micron,throughput,texphour,info=True)
