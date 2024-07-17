from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import matplotlib.pyplot as plt
import catalog_querry
from astropy.wcs import WCS
import make_star


def get_wcs(coord, scale=2*u.arcmin, size=(1000, 1000)):
    """ 
    Function to get WCS
    """
    wcs = WCS(naxis=2)
    wcs.wcs.crpix = [size[0]/2, size[1]/2]  # Set the reference pixel to the center of the image
    wcs.wcs.crval = [coord.ra.deg, coord.dec.deg]  # Set the reference value to the given coordinates
    wcs.wcs.cdelt = np.array([-scale.to(u.deg).value/size[0], scale.to(u.deg).value/size[1]])  # Set the pixel scale (assuming 0.00001 degrees per pixel)
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

def magnitude_to_luminosity(magnitude):
    # Convert magnitude to flux
    flux = 10**(-0.4 * magnitude)
    
    # Convert flux to luminosity
    luminosity = 4 * np.pi * (10)**2 * flux
    
    return luminosity

def scale_the_magnitude(magnitude, scale=5):
    lum = magnitude_to_luminosity(magnitude)

    return lum**(1/scale)

def plot_starfield(coord, size=(1000, 1000), ax=None):
    """
    Function to plot star field
    """
    radius = 1*u.arcmin
    wcs = get_wcs(coord, scale=radius*2, size=size)
    cat = catalog_querry.get_2mass_catalog(coord, radius)
    star = make_star.GaussianCrossPSF(amplitude=1)

    psf = np.zeros((size[0], size[1]))
    for c in cat:
        coordi = SkyCoord(c['RAJ2000'], c['DEJ2000'], unit=(u.deg, u.deg), frame='icrs')
        pix_cord = coordi.to_pixel(wcs)
        std = scale_the_magnitude(c['Kmag'], scale=5)*5
        psf += star.generate_cross_psf(np.round(pix_cord[0]), np.round(pix_cord[1])+1, std, 0.5, grid_size=size[0])

    if ax is None:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection=wcs)

    ax.imshow(psf, origin='lower', cmap='gray', aspect='equal')
    ax.set_xlabel('Right Ascension')
    ax.set_ylabel('Declination')

    plt.tight_layout()
    return ax

def example_plot():
    coord = SkyCoord.from_name('Barnard\'s Star')
    frame = np.zeros((1000, 1000))
    ww = get_wcs(coord, size=frame.shape)
    cat = catalog_querry.get_2mass_catalog(coord, 1*u.arcmin)
    star = make_star.GaussianCrossPSF(amplitude=1)

    psf = np.zeros((1000, 1000))
    for c in cat:
        coordi = SkyCoord(c['RAJ2000'], c['DEJ2000'], unit=(u.deg, u.deg), frame='icrs')
        pix_cord = coordi.to_pixel(ww)
        std = scale_the_magnitude(c['Kmag'], scale=5)*50
        psf += star.generate_cross_psf(np.round(pix_cord[0]), np.round(pix_cord[1])+1, std, 0.5, grid_size=1000)

    fig = plt.figure(figsize=(10, 8))
    ax = plt.subplot(111, projection=ww)
    ax.imshow(psf, origin='lower', cmap='gray', aspect='equal')
    ax.set_xlabel('Right Ascension')
    ax.set_ylabel('Declination')
    plt.show()

def main():
    plot_random_field()

if __name__ == '__main__':
    main()