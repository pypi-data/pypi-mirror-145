"""Stellar photon count module."""
import numpy as np
from astropy import constants as const
from astropy import units as u


def Blambda(T, lamb):
    """Planck distrintuion.

    Args:
       T: temperature with the astropy.unit of Kelvin, e.g. 1000.0*u.K
       lamb: wavelength with the astropy.unit of length, e.g. 1.0*u.m

    Returns:
       planck function B_lambda with the astropy unit
    """
    lamb5 = (lamb.to(u.m))**5
    fac = const.h*const.c/(lamb.to(u.m)*const.k_B*T)
    bl = 2.0*(const.c**2)*const.h/lamb5/(np.exp(fac)-1)
    return bl


def photon_Blambda(T, lamb):
    """Photon count Planck distrintuion.

    Args:
       T: temperature with the astropy.unit of Kelvin, e.g. 1000.0*u.K
       lamb: wavelength with the astropy.unit of length, e.g. 1.0*u.m

    Returns:
       B_lambda/(h nu) with the astropy unit
    """
    pB = Blambda(T, lamb)/(const.h*const.c/(lamb.to(u.m)))

    return pB


def getbbflux(Target, lamb):
    """compute blackbody flux of Target at wavelength of lambda.

    Args:
       Target: TargetClass instance
       lamb: wavelength with the astropy.unit of length, e.g. 1.0*u.m

    Returns:
       flux
    """

    tstar = Target.teff
    d = Target.d
    r = Target.rstar
    flux = np.pi*Blambda(tstar, lamb)*r*r/(d*d)
#    return flux.to(u.erg/u.cm/u.cm/u.micron/u.s)
    return flux.to(u.J/u.m/u.m/u.micron/u.s)


def getbbfluxph(Target, lamb):
    """compute blackbody photon flux of Target at wavelength of lambda.

    Args:
       Target: TargetClass instance
       lamb: wavelength with the astropy.unit of length, e.g. 1.0*u.m

    Returns:
       photon flux
    """

    tstar = Target.teff
    d = Target.d
    r = Target.rstar
    flux = np.pi*photon_Blambda(tstar, lamb)*r*r/(d*d)
    return flux.to(1/u.m/u.m/u.micron/u.s)


def getbbfluxJy(Target, lamb):
    """compute blackbody flux of Target at wavelength of lambda in the unit of
    Jansky.

    Args:
       Target: TargetClass instance
       lamb: wavelength with the astropy.unit of length, e.g. 1.0*u.m

    Returns:
       flux in Jansky
    """

    tstar = Target.teff
    d = Target.d
    r = Target.rstar
    flux = np.pi*Blambda(tstar, lamb)*r*r/(d*d)*lamb*lamb/const.c
    flux = flux.to(u.Jy)
    return flux


def Nstar(Inst, Target, Obs, info=True, integrate=True, Nintegrate=128):
    ppm = 1.e6
    texp = Obs.texposure
    a = np.pi*(Inst.dtel/2.0)**2 - np.pi*(Inst.dstel/2.0)**2
    if integrate:
        ddl = Inst.dlam/Nintegrate
        lamarr = Inst.lamb+np.linspace(-Inst.dlam/2, Inst.dlam/2, Nintegrate)
        fluxarr = []
        photonfarr = []
        photonarr = []
        for j, lamlow in enumerate(lamarr[:-1]):
            lamc = (lamarr[j+1]+lamlow)/2.0
            dll = lamarr[j+1]-lamlow
            flux = np.pi*Blambda(Target.teff, lamc)*Target.rstar * \
                Target.rstar/(Target.d*Target.d)*Target.contrast
            photonf = np.pi*photon_Blambda(Target.teff, lamc)*Target.rstar * \
                Target.rstar/(Target.d*Target.d)*Target.contrast
            photon = photonf*a*dll*Obs.texposure*Inst.throughput
            fluxarr.append(flux)
            photonfarr.append(photonf)
            photonarr.append(photon)

        photon = np.sum(photonarr)
    else:
        flux = np.pi*Blambda(Target.teff, Inst.lamb)*Target.rstar * \
            Target.rstar/(Target.d*Target.d)*Target.contrast
        photonf = np.pi*photon_Blambda(Target.teff, Inst.lamb) * \
            Target.rstar*Target.rstar/(Target.d*Target.d)*Target.contrast
        photon = photonf*a*Inst.dlam*Obs.texposure*Inst.throughput
        photon = photon.to(1)

    flux = np.pi*Blambda(Target.teff, Inst.lamb)*Target.rstar * \
        Target.rstar/(Target.d*Target.d)*Target.contrast
    photonf = np.pi*photon_Blambda(Target.teff, Inst.lamb) * \
        Target.rstar*Target.rstar/(Target.d*Target.d)*Target.contrast

    if info:
        print_info(Target, Obs, Inst, flux, photonf, photon)

    Nphoton = photon
    Obs.nphoton_exposure = Nphoton
    Obs.nphoton_frame = Nphoton*(Obs.tframe/Obs.texposure).to(1)
    Obs.sign = np.sqrt(Nphoton)
    Obs.flux = flux
    Obs.photonf = photonf
    Obs.sign_relative = Obs.sign/Obs.nphoton_exposure*ppm


def print_info(Target, Obs, Inst, flux, photonf, photon):
    """print info."""
    print('B(lambda) for', Target.teff, 'at ', Inst.lamb)
    print('{:e}'.format(Blambda(Target.teff, Inst.lamb).to(
        u.erg/u.cm/u.cm/u.angstrom/u.s)))
    print('{:e}'.format(Blambda(Target.teff, Inst.lamb).to(
        u.erg/u.cm/u.cm/u.micron/u.s)))
    print('{:e}'.format(Blambda(Target.teff, Inst.lamb).to(u.J/u.m/u.m/u.m/u.s)))
    print('---------------------')
    print('FLUX from a sphere with r=', Target.rstar,
          '[Rsol] and', 'dpc=', Target.d, '[pc]')
    print(flux.to(u.erg/u.cm/u.cm/u.micron/u.s))
    print('Photon FLUX from a sphere with  r=',
          Target.rstar, '[Rsol] and', 'dpc=', Target.d, '[pc]')
    print(photonf.to(1/u.cm/u.cm/u.micron/u.s))
    print('---------------------')
    print('Photon Count with observation:')
    print('  telescope diameter', Inst.dtel, '[m]')
    print('  band width', Inst.dlam, '[micron]')
    print('  exposure', Obs.texposure,
          '[hour] = ', Obs.texposure.to(u.min), ' [min]')
    print('  throughput', Inst.throughput)
    print('N=', '{:e}'.format(photon))
    print('photon noise 1/sqrt(N)=', np.sqrt(1.0/photon)*1e6, '[ppm]')
    print('photon noise 1/sqrt(N)=', np.sqrt(1.0/photon)*1e2, '[%]')
    print('7 sigma depth=', np.sqrt(1.0/photon)*1e2*7.0, '[%]')
