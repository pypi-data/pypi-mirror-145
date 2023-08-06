#!/usr/bin/python
import sys
import argparse
import numpy as np
from io import StringIO
import pandas as pd
from astropy import constants as const
from astropy import units as u


def get_magdict(maglist=None):
    magdict={}
    if(maglist is None):
        maglist="/home/kawahara/exocal/data/mag.list"

#    print "Read "+maglist

    maglist=pd.read_csv(maglist,delimiter=',')
    
    return maglist

def get_flux(band,mag,magdict):
    mask=magdict["band"]==band
    a = float(magdict["a"][mask].values[0])
    flux=10**(a - 0.4*mag)*u.erg/u.s/(u.cm)**2/u.micron
    return flux

def get_mag(band,flux,magdict):
    mask=magdict["band"]==band
    a = float(magdict["a"][mask].values[0])
    fluxcgs=flux.to(u.erg/u.s/(u.cm)**2/u.micron).value
    mag=2.5*(a - np.log10(fluxcgs))

    return mag

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert magnitude to flux based on Traub and Oppenheimer')
    parser.add_argument('-b', nargs=1,required=True,help='Choose band from U,B,V,R,I,J,H,Ks,L,M,N,Q')
    parser.add_argument('-m', nargs=1,required=True,help='magnitude' )
    args = parser.parse_args()    

    band=args.b[0]
    mag=float(args.m[0])
    print("Band=",band," Magnitude=",mag)
    magdict=get_magdict()
    print(magdict)
    mask=magdict["band"]==band

    print("center=",magdict["lambda0"][mask].values[0],"micron")
    print("width=",magdict["dlambda"][mask].values[0],"micron")
    print(get_flux(band,mag,magdict))
    flux=get_flux(band,mag,magdict)
    print(get_flux(band,mag,magdict).to(u.erg/u.s/u.m/u.m/u.nm))
    print(get_mag(band,flux,magdict))
