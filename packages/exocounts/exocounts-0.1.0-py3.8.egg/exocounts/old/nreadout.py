#!/usr/bin/python
import sys
import argparse
import numpy as np
from io import StringIO
import csv
from astropy import constants as const
from astropy import units as u

def Nreadout(th,tr,nr,npix,mu,mode="linear"):
    #mu = 1 for CCD, mu = 2 for IR array
    hr2sec=3600.0
    
    if mode=="linear":
        return np.sqrt(mu*npix*th*hr2sec/tr)*nr
    else:
        print("No model")
        return 0
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute stellar counts using planck function')
    parser.add_argument('-th', nargs=1,default=[0.0833],help='exposure [hour]')
    parser.add_argument('-tr', nargs=1,default=[7.1],help='one shot exposure [sec]')
    parser.add_argument('-nr', nargs=1,default=[30.0],help='read out noise [e-/read]')
    parser.add_argument('-npix', nargs=1,default=[10],help='pixel number')

    args = parser.parse_args()           
    th=args.th[0]
    tr=args.tr[0]
    nr=args.nr[0]
    npix=args.npix[0]

    sigr=Nreadout(th,tr,nr,npix,mode="linear")
    print("exposure time for 1 frame:",th,"[hour/frame]")
    print("1 read time:",tr,"[sec/read]")
    print("readout noise/pix :",nr,"[e-/pix/read]")
    print("pixel number :",npix,"[pix]")
    print("===========================")
    print("Readout Noise/frame: ",sigr)
