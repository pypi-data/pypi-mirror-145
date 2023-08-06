import numpy as np


def gethz(teff, Lstar):
    seff = [0, 0, 0, 0, 0, 0]
    seffsun = [1.776, 1.107, 0.356, 0.320, 1.188, 0.99]
    a = [2.136e-4, 1.332e-4, 6.171e-5, 5.547e-5, 1.433e-4, 1.209e-4]
    b = [2.533e-8, 1.580e-8, 1.698e-9, 1.526e-9, 1.707e-8, 1.404e-8]
    c = [-1.332e-11, -8.308e-12, -3.198e-12, -2.874e-12, -8.968e-12, -7.418e-12]
    d = [-3.097e-15, -1.931e-15, -5.575e-16, -5.011e-16, -2.084e-15, -1.713e-15]

    if teff <= 7201.0:
        tstar = teff - 5780.0

        # maximum greenhouse
        seffmax = seffsun[2] + a[2]*tstar + b[2] * \
            tstar**2 + c[2]*tstar**3 + d[2]*tstar**4
        # runaway
        seffmin = seffsun[1] + a[1]*tstar + b[1] * \
            tstar**2 + c[1]*tstar**3 + d[1]*tstar**4

        #Seff = Lstar/a^2
        amin = np.sqrt(Lstar/seffmin)
        amax = np.sqrt(Lstar/seffmax)
    else:
        amin = None
        amax = None
    return amin, amax
