from astropy import units as u
import numpy as np


def ld(lamb, d):
    return (lamb/d).to(1)/np.pi*180.0*3600*u.arcsec


print(ld(1.4*u.micron, 0.3*u.m))
# print(ld(0.5*u.micron,2*u.m))
