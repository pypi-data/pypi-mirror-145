import nstar
import nreadout
import ndark
import argparse

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
    parser.add_argument('-npix', nargs=1,default=[10],help='pixel number')
    parser.add_argument('-nd', nargs=1,default=[30.0],help='dark noise [e-/sec]')
    parser.add_argument('-tr', nargs=1,default=[7.1],help='one shot exposure [sec]')
    parser.add_argument('-nr', nargs=1,default=[30.0],help='read out noise [e-/pix/read]')

    args = parser.parse_args()           
    stellar_temperature=float(args.t[0])
    lambda_micron=float(args.micron[0])
    dpc=float(args.d[0])
    rsol=args.r[0]
    dtel=args.Dm[0]
    dstel=args.Dsm[0]
    dlam_micron=float(args.dmicron[0])
    throughput=float(args.tp[0])
    th=float(args.th[0])
    nd=args.nd[0]
    npix=args.npix[0]
    tr=args.tr[0]
    nr=args.nr[0]

    flux,photonf,photon,sign=nstar.Nstar(lambda_micron,stellar_temperature,rsol,dpc,dtel,dstel,dlam_micron,throughput,th,info=True)
    sigd=ndark.Ndark(th,nd,npix)
    sigr=nreadout.Nreadout(th,tr,nr,npix,mode="linear")

    print("star,dark,readout")
    print(sign,sigd,sigr)
