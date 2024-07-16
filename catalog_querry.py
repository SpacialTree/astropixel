from astropy import units as u
from astropy.coordinates import SkyCoord
from astroquery.sdss import SDSS
import numpy as np
import matplotlib.pyplot as plt

def get_sdss_catalog_circ(ra, dec, radius=1.0*u.deg):
    """
    Function to get the SDSS catalog around a given RA and DEC
    """
    # create a SkyCoord object
    c = SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg), frame='icrs')
    # query the SDSS catalog
    xid = SDSS.query_region(c, radius=radius)

def get_sdss_catalog_rect(ra, dec, width=1.0*u.deg, height=1.0*u.deg):
    """
    Function to get the SDSS catalog around a given RA and DEC
    """
    # create a SkyCoord object
    c = SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg), frame='icrs')
    # query the SDSS catalog
    xid = SDSS.query_region(c, width=width, height=height)

def get_sdss_image(ra, dec, radius=1.0):
    """
    Function to get the SDSS image around a given RA and DEC
    """
    # create a SkyCoord object
    c = SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg), frame='icrs')
    # get the SDSS image
    xid = SDSS.query_region(c, radius=radius*u.deg)
    img = SDSS.get_images(matches=xid)
    return img

def get_random_coordinates():
    """
    Function to generate random coordinates
    """
    ra = np.random.uniform(0, 360)
    dec = np.random.uniform(-90, 90)
    return ra, dec

