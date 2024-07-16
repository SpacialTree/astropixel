from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import matplotlib.pyplot as plt
from catalog_querry import get_random_coordinates
from astropy.wcs import WCS


def get_wcs(position, size=(1000, 1000)):
    wcs = WCS(naxis=2)
    wcs.wcs.crpix = [size[0]/2, size[1]/2]  # Set the reference pixel to the center of the image
    wcs.wcs.crval = [coord.ra.deg, coord.dec.deg]  # Set the reference value to the given coordinates
    wcs.wcs.cdelt = np.array([-0.001, 0.001])  # Set the pixel scale (assuming 0.001 degrees per pixel)
    return wcs

def plot_random_field():
    """
    Function to plot random field
    """

    coord = get_random_coordinates()
    wcs = get_wcs(coord)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection=wcs)

    ax.set_xlabel('RA')
    ax.set_ylabel('Dec')
    plt.show()