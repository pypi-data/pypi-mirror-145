import nstar
import nreadout
import ndark
import readspec
import argparse
import convmag
import numpy as np
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute stellar counts using planck function')
    parser.add_argument('-f', nargs=1, help='spec file ex. ejas.txt')
    parser.add_argument('-c', nargs=1, default=["A"],help='case')

    args = parser.parse_args()           
    specfile=args.f[0]
    case=args.c[0]

    dat=readspec.readspec(specfile,case=case)
    stellar_temperature,lambda_micron,dpc,rsol,dtel,dstel,dlam_micron,throughput,th,nd,npix,tr,nr,mu,b=readspec.expanddat(dat,case)

    flux,photonf,Nphoton,sign=nstar.Nstar(lambda_micron,stellar_temperature,rsol,dpc,dtel,dstel,dlam_micron,throughput,th,info=False)
    sigd=ndark.Ndark(th,nd,npix,mu)
    sigr=nreadout.Nreadout(th,tr,nr,npix,mu,mode="linear")

    print("band:",b)
    magdict=convmag.get_magdict()
    print("magnitude=",convmag.get_mag(b,flux,magdict))

    print("star,dark,readout")
    print(sign,sigd,sigr)

    Nread=(th*3600)/tr
    Nave=Nphoton/Nread/npix
    print("Average photon counts: e-/pix/read: ",Nave)

    print("[ppm] star,dark,readout")
    Ntot=Nphoton
    ppm=1.e6
    print(sign/Ntot*ppm,sigd/Ntot*ppm,sigr/Ntot*ppm)
