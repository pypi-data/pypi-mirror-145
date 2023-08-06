import numpy as np
from astropy import constants as const
from astropy import units as u


def lambert(beta):
    """ Lambert phase function

    Args:
       beta angle, i.e. observer-planet-star angle

    Returns:
       normalized Lambert phase function

    """
    return (np.sin(beta) + (np.pi - beta)*np.cos(beta))/np.pi


class PlanetClass(object):
    """Class for planet

    """    
    def __init__(self):
        self.teff = None
        self.rplanet = None  # in the unit of Earth radii
        self.a = None
        self.name = 'No Name'
        self.phase = None
        self.reflectivity = None
        self.albedo = None

    def compute_reflectivity(self):
        """Compute reflectivity assuming Lambertian with phase of self.phase
        """        
        ratio = (self.rplanet/self.a).to(1).value
        self.reflectivity = 2.0/3.0*lambert(self.phase)*ratio*ratio*self.albedo
