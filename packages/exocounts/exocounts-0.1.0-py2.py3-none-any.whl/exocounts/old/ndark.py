#!/usr/bin/python
import sys
import argparse
import numpy as np
from io import StringIO
import csv
from astropy import constants as const
from astropy import units as u

def Ndark(th,nd,npix,mu):
    hr2sec=3600.0
    ndframe=th*hr2sec*nd 
    
    return np.sqrt(mu*npix*ndframe)        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute stellar counts using planck function')
    parser.add_argument('-th', nargs=1,default=[0.0833],help='exposure [hour]')
    parser.add_argument('-nd', nargs=1,default=[30.0],help='dark noise [e-/sec]')
    parser.add_argument('-npix', nargs=1,default=[10],help='pixel number')

    args = parser.parse_args()           
    th=args.th[0]
    nd=args.nd[0]
    npix=args.npix[0]

    sigd=Ndark(th,nd,npix)
    print("exposure time for 1 frame:",th,"[hour/frame]")
    print("dark noise/pix :",nr,"[e-/pix/sec]")
    print("pixel number :",npix,"[pix]")
    print("===========================")
    print("Dark Noise/frame: ",sigd)
