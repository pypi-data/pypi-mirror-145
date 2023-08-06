import numpy as np
import importlib.resources
from astropy.io import fits
import apollinaire.timeseries as timeseries


def load_light_curve (star='saxo') :
  '''
  Load a light curve stored in the ``timeseries`` submodule.

  Parameters
  ----------

  star: str 
    star id or nickname.

  Returns
  -------
  tuple of array
    timestamp (Julian date) and photometric variation (in ppm).
  '''
  if type (star) != int and star.isdigit () :
    star = int (star)

  if star=='saxo' or star==6603624 :
    basename = 'kplr006603624_52_COR_filt_inp.fits'
  else :
    raise Exception ('Unkown stellar identifier.')
  f = importlib.resources.path (timeseries, basename)
  with f as filename :
      hdu = fits.open (filename) [0]
  data = np.array (hdu.data)
  t = data[:,0]
  v = data[:,1]

  return t, v

def load_golf_timeseries () :
  '''
  Load a 365-day GOLF timeseries corresponding to the
  instrument first year of operation.

  Returns
  -------
  array
    radial velocity array with a 20s sampling.
  '''

  basename = 'golf_11041996_10041997.fits'
  f = importlib.resources.path (timeseries, basename)
  with f as filename :
      hdu = fits.open (filename) [0]
  v = np.array (hdu.data)

  return v
