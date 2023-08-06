import numpy as np
from scipy.stats import chi2
from apollinaire.simulate import initialise
from apollinaire.peakbagging import (compute_model, 
                                     build_background,
                                     sidelob_param)
from numpy.random import SeedSequence

'''
Use the background and p-mode models of the ``peakbagging`` module
to create synthetic PSD following a Chi2 with 2 degrees of 
freedom
'''

def create_noise_vector (freq, entropy=None) :
  '''
  Create a noise vector following a chi2 with two degrees 
  of freedom that can be applied on the model PSD.

  :param freq: input frequency vector on which to compute
    the noise vector.
  :type freq: ndarray

  :param entropy: entropy value to seed the random generator.
  :type entropy: int

  :return: the noise vector and the entropy value (for reproductibility)
    as a tuple.
  :rtype: tuple
  '''
 
  if entropy is None :
    sq = SeedSequence ()
    entropy = sq.entropy

  rng, entropy = initialise (entropy)
  noise_vector = chi2 (df=2).rvs (size=freq.size, random_state=rng)

  return noise_vector, entropy

def create_synthetic_psd (freq, pkb=None, back=None, param_back=None, n_harvey=2, wdw=None,
                          feature=None, instr='geometric', asym_profile='nigam-kosovichev', 
                          use_sinc=False, entropy=None, noise_free=False, fit_amp=False) :
  '''
  Create a synthetic psd vector from a frequency vector,
  modes parameters from a pkb arrays and, optionnally,
  a background profile.

  :param freq: input frequency vector on which to compute
    the synthetic PSD vector.
  :type freq: ndarray

  :param back: stellar background array, of same length as ``freq``. 
    Optional, default ``None``.
  :type back: ndarray

  :param param_back: stellar background parameters used to build the background
    vector. Will be used only if ``back`` is ``None``. Optional, default ``None``.
  :type param_back: ndarray

  :param n_harvey: number of Harvey law of the background profile. 
    Optional, default ``2``.
  :type n_harvey: int

  :param wdw: observation window to use to convolute the modes 
    profile in the model. 
  :type wdw: array

  :param feature: array of same length as ``freq``, to be used to add any 
    additionnal feature to the spectrum. This array will be summed to the
    model array before adding the chi2 noise. Optional, default ``None``.
  :type feature: ndarray

  :param instr: instrument to consider to compute m-height ratios. 
    Possible argument : ``geometric``, ``kepler``, ``golf``, ``virgo``.
    Optional, default ``geometric``. 
  :type instr: str

  :param use_sinc: if set to ``True``, mode profiles will be computed using
    cardinal sinus and not Lorentzians.  No asymmetry term will be used if it is
    the case. Optional, default ``False``.
  :type use_sinc: bool

  :param asym_profile: depending on the chosen argument, asymmetric profiles
    will be computed following Korzennik 2005 (``korzennik``) or Nigam & Kosovichev
    1998 (``nigam-kosovichev``). Default ``nigam-kosovichev``. 
  :type asym_profile: str  

  :param entropy: entropy value to seed the random generator.
  :type entropy: int

  :param noise_free: if set to ``True``, the function will return only an ideal
    model without added noise. Optional, default ``False``.
  :type noise_free: bool

  :return: the synthetic PSD vector and the entropy value (for reproductibility)
    as a tuple.
  :rtype: tuple
  '''

  if wdw is not None :
    dt = 1 / (2*freq[-1])
    param_wdw = sidelob_param (wdw, dt=dt)
  else :
    param_wdw = None

  if back is not None :
    pass
  elif param_back is not None :
    back = build_background (freq, param_back, n_harvey=n_harvey) 
  else : 
    back = np.ones (freq.size)

  if pkb is None :
    model = np.zeros (freq.size)
  else :
    model = compute_model (freq, pkb, param_wdw=param_wdw, instr=instr, fit_amp=fit_amp,  
                           asym_profile=asym_profile, use_sinc=use_sinc)
  model = model + back

  if feature is not None :
    model = model + feature

  nv, entropy = create_noise_vector (freq, entropy)

  if noise_free :
    psd = model
  else :
    psd = model * nv / 2

  return psd, entropy
  
if __name__=='__main__' :

  freq = np.linspace (0, 1000, 1000)
  nv, entropy = create_noise_vector (freq)
  
