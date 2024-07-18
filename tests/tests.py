import pytest
import numpy as np
import astropixel
from astropixel import catalog_querry
from astropixel import plot_stars
from astropixel import make_star
from astropixel.make_star import GaussianCrossPSF
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.table import Table

def test_generate_cross_psf():
    psf = make_star.GaussianCrossPSF(amplitude=1)
    x_center = 150
    y_center = 100
    stddev = 10
    background_factor = 0.1
    size = (300, 200)
    psf_cross = psf.generate_cross_psf(x_center, y_center, stddev, background_factor, size=size)
    assert psf_cross.shape == (200, 300)
    assert np.max(psf_cross) == pytest.approx(1, abs=1e-3)
    assert np.min(psf_cross) == pytest.approx(0, abs=1e-3)
    assert np.argmax(psf_cross) == 30150

def test_get_catalog():
    coord = SkyCoord(ra=10.68458, dec=41.26917, unit=(u.deg, u.deg))
    radius = 1.0*u.arcmin
    catalog_name = '2MASS'
    guide = catalog_querry.get_catalog(catalog_name, coord, radius=radius)
    assert isinstance(guide, Table)
    assert len(guide) > 0

def test_get_random_coordinates():
    coord = catalog_querry.get_random_coordinates()
    assert isinstance(coord, SkyCoord)
    assert coord.ra.value >= 0
    assert coord.ra.value <= 360
    assert coord.dec.value >= -90
    assert coord.dec.value <= 90

def test_get_random_coordinates_gal():
    coord = catalog_querry.get_random_coordinates_gal()
    assert isinstance(coord, SkyCoord)
    assert coord.l.value >= 0
    assert coord.l.value <= 360
    assert coord.b.value >= -5
    assert coord.b.value <= 5

if __name__ == "__main__":
    test_generate_cross_psf()
    test_get_catalog()
    test_get_random_coordinates()
    test_get_random_coordinates_gal()