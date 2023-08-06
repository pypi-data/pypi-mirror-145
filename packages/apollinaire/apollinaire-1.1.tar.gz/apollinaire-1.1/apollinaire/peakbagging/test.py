import apollinaire as apn
from apollinaire.peakbagging import *
import apollinaire.peakbagging.templates as templates
import apollinaire.timeseries as timeseries
import importlib.resources
import pandas as pd

def test_a2z (a2z_file, verbose=True) :

  '''
  Test a a2z file to check that it is valid. The function
  checks the bounds set for the parameters, convert the a2z
  DataFrame to pkb

  :param a2z_file: path of the a2z file to test.
  :type a2z_file: str

  :return: a2z DataFrame and pkb array.
  :rtype: tuple
  '''

  df_a2z = read_a2z (a2z_file)
  check_a2z (df_a2z, verbose=verbose) 
  pkb = a2z_to_pkb (df_a2z)
  df_pkb = pd.DataFrame (data=pkb)
  
  if verbose :
    print (df_a2z)
    print (df_pkb.to_string ())
    print (get_list_order (df_a2z))

  assert ~np.any (np.isnan (pkb)), 'The pkb array contains NaN.' 

  return df_a2z, pkb

def test_module (verbose=True) :
  '''
  Test module functions
  '''
  # Testing a2z and pkb arrays
  f = importlib.resources.path (templates, 'test.a2z')
  with f as filename :
    df_a2z, pkb = test_a2z (filename, verbose=verbose)
  assert np.all (get_list_order (df_a2z)==[5, 21, 22]), 'The list of order read from the a2z DataFrame is not correct'
  f = importlib.resources.path (templates, 'verif.pkb')
  with f as filename :
    verif_pkb = np.loadtxt (filename)
  residual = np.abs (pkb - verif_pkb)
  error = np.linalg.norm (residual.ravel(), ord=np.inf)
  assert error < 1.e-6, 'The pkb array does not contain the expected values.'
  freq = np.linspace (0, 5000, 10000)
  model = compute_model (freq, pkb)
  assert ~np.any (np.isnan (model)), 'The model built from the test pkb array contains NaN.'
  # Testing importation and light curves management function
  t, v = apn.timeseries.load_light_curve (star='006603624')
  dt = np.median (t[1:] - t[:-1]) * 86400
  freq, psd = apn.psd.series_to_psd (v, dt=dt, correct_dc=True)
  freq = freq*1e6
  psd = psd*1e-6
  guess, low_bounds, up_bounds, labels = create_background_guess_arrays (freq, psd, r=1.162, m=1.027, teff=5671.,
                                                                         n_harvey=2, spectro=False, power_law=False,
                                                                         high_cut_plaw=100., return_labels=True)
  assert ~np.any (np.isnan (guess)), 'The background guess array contains NaN'
  assert ~np.any (np.isnan (low_bounds)), 'The background low bounds array contains NaN'
  assert ~np.any (np.isnan (up_bounds)), 'The background up bounds array contains NaN'
  v = apn.timeseries.load_golf_timeseries ()

if __name__ == '__main__' :

  test_module (verbose=True)




