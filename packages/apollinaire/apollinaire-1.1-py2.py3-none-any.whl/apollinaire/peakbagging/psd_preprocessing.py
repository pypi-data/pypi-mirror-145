# coding: utf-8

import numpy as np


'''
A series of functions designed for PSD preprocessing.
'''

def hide_modes (freq, psd, pkb, back, l=1, n_width=4,
                remove_left=True, remove_zero_bin=True) :
  '''
  Hide PSD region around modes of given l.

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: power vector
  :type psd: ndarray

  :param back: background power vector
  :type back: ndarray

  :param pkb: pkb array with modes parameters.
  :type pkb: ndarray

  :param l: mode degrees to remove. Optional, default ``1``.
  :type l: int

  :param n_width: frequency bins will be removed ``n_width`` from 
    the central frequency of the remaining modes. Optional, default ``4``.
  :type n_width: float

  :param remove_left: if set to ``True``, remove a region Dnu/2 wide
    before the first mode given in the pkb. Optional, default ``True``. 
  :type remove_left: bool

  :param remove_zero_bin: if set to ``True``, bins with zero values will be removed from
    returned vector. Optional, default ``True``.
  :type remove_zero_bin: bool 
  '''

  psd = np.copy (psd)
  dnu = np.mean (np.diff (pkb[pkb[:,1]==0, 2]))
  if pkb.shape[1]==20 :
    i_width = 8
  else :
    i_width = 6

  if remove_left :
    w = pkb[0,i_width]
    f = pkb[0,2]
    cond = (freq>f-dnu/2)&(freq<f-n_width*w)
    psd[cond] = 0

  for ii, elt in enumerate (pkb) :
    if elt[1]==l :
      w = elt[i_width]
      if ii > 0 :
        f1 = pkb[ii-1, 2]
      else :
        f1 = elt[2] - dnu/2
      if ii+1 < pkb.shape[0] :
        f2 = pkb[ii+1, 2]
      else :
        f2 = elt[2] + dnu/2
      cond = (freq>f1+n_width*w)&(freq<f2-n_width*w)
      psd[cond] = 0

  if remove_zero_bin :
    freq = freq[psd!=0]
    back = back[psd!=0]
    psd = psd[psd!=0]

  return freq, psd, back

def remove_pattern (freq, psd, back, pkb, l=[0,2]) :
  '''
  Remove a given pattern from the PSD by dividing the
  PSD by the computed model.  

  :param freq: frequency vector
  :type freq: ndarray

  :param psd: power vector
  :type psd: ndarray

  :param back: background power vector
  :type back: ndarray

  :param pkb: pkb array with modes parameters.
  :type pkb: ndarray

  :param l: mode degrees to remove. Optional, default ``[0,2]``.
  :type l: int or array-like
  '''

  if pkb.shape[1]==20 :
    raise Exception ('This function cannot be used with an extended pkb array.' //
                     'Use a classical pkb instead.')

  pkb = pkb[np.isin (pkb[:,1], l),:]

  model = compute_model (freq, pkb)
  model = model + back
  psd = psd / model

  return psd

def clear_modes (freq, psd, l02_freq, 
                 coeff=6):
    '''
    Clean PSD using a median clipping. 

    First version was written by V. Delsanti,
    refactored by SNB.
    
    Returns
    -------
      Cleaned PSD. 
    '''
    psd_copy = np.copy (psd)
    cond = (freq<l02_freq[-1])&(freq>l02_freq[0])
    psd = median_clip_modes(psd, np.median(psd), coeff=coeff,
                            nloop=3)
    for i in range(0, l02_freq.size-1, 2):
        cond = (freq<l02_freq[i+1])&(freq>l02_freq[i])
        psd[cond] = psd_copy[cond]
         
    return psd

def median_clip_modes(psd, med, coeff=3, nloop=1):
    '''
    Mode median clipping. 

    First version was written by V. Delsanti,
    refactored by SNB.

    Returns
    -------
      PSD after refactoring.
    '''
    
    for _ in range (nloop) :
        psd[psd>med*coeff] = 0
        mask = np.zeros (psd.size, dtype=bool)
        jj = 0
        sequence = False
        for ii in range (psd.size) :
            if psd[ii]==0 :
                mask[ii] = True
                if not sequence :
                    sequence = True
                    jj = max (0, ii-1)
            elif sequence :
                ll = min (psd.size-1, ii+1)
                value = (psd[jj] + psd[ll]) / 2
                psd[mask] = value
                mask = np.zeros (psd.size, dtype=bool)
                sequence = False

    return psd 
