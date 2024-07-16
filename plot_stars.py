from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import matplotlib.pyplot as plt
import catalog_querry
from astropy.wcs import WCS


def get_wcs(coord, size=(1000, 1000)):
    """ 
    Function to get WCS
    """
    wcs = WCS(naxis=2)
    wcs.wcs.crpix = [size[0]/2, size[1]/2]  # Set the reference pixel to the center of the image
    wcs.wcs.crval = [coord.ra.deg, coord.dec.deg]  # Set the reference value to the given coordinates
    wcs.wcs.cdelt = np.array([-0.00005, 0.00005])  # Set the pixel scale (assuming 0.00001 degrees per pixel)
    wcs.wcs.ctype = ["RA---TAN", "DEC--TAN"]  # Set the coordinate type to RA/DEC

    return wcs

def plot_field(coord, cat, wcs, ax=None):
    """
    Function to plot field
    """

    if ax is None:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection=wcs)

    ax.scatter(cat['RAJ2000'], cat['DEJ2000'], s=50, marker='*', color='k')
    ax.scatter(coord.ra.deg, coord.dec.deg, s=100, edgecolor='r', facecolor='none')
    ax.scatter(coord.ra.deg, coord.dec.deg, s=100, marker='+', color='r')

    ax.set_xlabel('Right Ascension')
    ax.set_ylabel('Declination')

    plt.tight_layout()
    return ax

def plot_coord(coord, size=(1000, 1000), ax=None):
    """
    Function to plot field at coord
    """
    wcs = get_wcs(coord, size=size)
    cat = catalog_querry.get_2mass_catalog(coord, 1*u.arcmin)

    return plot_field(coord, cat, wcs, ax=ax)

def plot_random_field(size=(1000, 1000), ax=None):
    """
    Function to plot random field
    """

    coord = catalog_querry.get_random_coordinates()
    wcs = get_wcs(coord)
    try: 
        cat = catalog_querry.get_2mass_catalog(coord, 1*u.arcmin)
    except:
        print('No catalog found. Trying again...')

    i = 0
    while len(cat) < 10:
        coord = catalog_querry.get_random_coordinates()
        wcs = get_wcs(coord, size=size)
        cat = catalog_querry.get_2mass_catalog(coord, 1*u.arcmin) 
        i += 1
        if i > 25:
            print("No catalog found")
            break

    plot_field(coord, cat, wcs, ax=ax)

def main():
    plot_random_field()

if __name__ == '__main__':
    main()