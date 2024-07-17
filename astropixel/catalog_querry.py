from astropy import units as u
from astropy.coordinates import SkyCoord
from astroquery.vizier import Vizier
import numpy as np
import matplotlib.pyplot as plt

def get_2mass_catalog(coord, radius=1.0*u.arcmin):
    """
    Function to get 2MASS catalog
    """
    guide = Vizier(catalog="II/246").query_region(coord, radius=radius)[0]
    return guide

def get_random_coordinates():
    """
    Function to generate random coordinates
    """
    ra = np.random.uniform(0, 360)
    dec = np.random.uniform(-90, 90)
    return SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg), frame='icrs')

def get_random_coordinates_gal():
    """
    Function to generate random coordinates
    """
    l = np.random.uniform(0, 360)
    b = np.random.uniform(-5, 5)
    return SkyCoord(l=l, b=b, unit=(u.deg, u.deg), frame='galactic')