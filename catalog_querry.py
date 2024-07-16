from astropy import units as u
from astropy.coordinates import SkyCoord
from astroquery.sdss import SDSS
import numpy as np
import matplotlib.pyplot as plt

def get_sdss_catalog(ra, dec, radius=1.0):
    """
    Function to get the SDSS catalog around a given RA and DEC
    """
    # create a SkyCoord object
    c = SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg), frame='icrs')
    # query the SDSS catalog
    xid = SDSS.query_region(c, radius=radius*u.deg)

def get_random_coordinates():
    """
    Function to generate random coordinates
    """
    ra = np.random.uniform(0, 360)
    dec = np.random.uniform(-90, 90)
    return ra, dec

