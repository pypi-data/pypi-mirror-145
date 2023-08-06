import pandas as pd


def readspec(specfile, case='A'):
    dat = pd.read_csv(specfile, index_col=0, delimiter=',')

    return dat


def expanddat(dat, case):
    print(case)
    stellar_temperature = float(dat.ix['stellar_temperature', case])
    lambda_micron = float(dat.ix['lambda_micron', case])
    dpc = float(dat.ix['dpc', case])
    rsol = float(dat.ix['rsol', case])
    dtel = float(dat.ix['dtel', case])
    dstel = float(dat.ix['dstel', case])
    dlam_micron = float(dat.ix['dlam_micron', case])
    throughput = float(dat.ix['throughput', case])
    th = float(dat.ix['th', case])
    nd = float(dat.ix['nd', case])
    npix = float(dat.ix['npix', case])
    tr = float(dat.ix['tr', case])
    nr = float(dat.ix['nr', case])
    mu = float(dat.ix['mu', case])  # dup factor for 1 frame#

    b = (dat.ix['b', case])

    return stellar_temperature, lambda_micron, dpc, rsol, dtel, dstel, dlam_micron, throughput, th, nd, npix, tr, nr, mu, b


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Compute stellar counts using planck function')
    parser.add_argument('-f', nargs=1, help='spec file ex. ejas.txt')
    parser.add_argument('-c', nargs=1, default=['A'], help='case')

    args = parser.parse_args()
    specfile = args.f[0]
    case = args.c[0]
    dat = readspec(specfile, case)

    print(dat.to_latex())
