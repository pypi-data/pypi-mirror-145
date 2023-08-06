import numpy as np
import pandas as pd
from .fit_tools import *

'''
A collection of function to make
a2z DataFrame manipulations easier.
'''

def add_parameter (df, value=0, bounds=[0, 0], param_type='split',
                   extent='mode') :
  '''
  Add new parameter to given a2z DataFrame,
  to extent required by the user.
  '''
  if extent not in ['global', 'order', 'even', 'odd', 'mode'] :
    raise Exception ('Accepted extent are "global", "order", "even", "odd" and "mode"')

  if param_type=='freq' :
    raise Exception ('"freq" parameter cannot be added with this function, use add_mode instead.')

  if extent=='global' :
    rows = np.array (['a', 'a', param_type, extent, value, 
                     0, 0, bounds[0], bounds[1]]).reshape (1, 9)
  if extent=='order' : 
    orders = np.unique (df.loc[df[0]!='a',0])
    rows = np.array ([[o, 'a', param_type, extent, value, 
                      0, 0, bounds[0], bounds[1]] for o in orders])
  if extent in ['even', 'odd', 'mode'] :
    modes = df.loc[(df[2]=='freq'),[0,1]].to_numpy ().astype (int)
    if extent=='even' :
      modes = modes[modes[:,1]%2==0]
    if extent=='odd' :
      modes = modes[modes[:,1]%2==1]
    rows = np.array ([[elt[0], elt[1], param_type, extent, value, 
                       0, 0, bounds[0], bounds[1]] for elt in modes])
   
  aux = pd.DataFrame (data=rows)
  df = pd.concat ([df, aux])
  df = sort_a2z (df)

  return df

def add_mode (value=0, order=0, degree=0,
              bounds=[0,0], height=None, width=None,
              split=None, asym=None, bounds_height=None,
              bounds_width=None, bounds_split=None,
              bounds_asym=None) : 
  '''
  Add frequency for a new mode to be fitted
  at a given order and degree.
  '''

  row = [[order, degree, 'freq', 'mode', value, 0, 0, bounds[0], bounds[1]]]
  if height is None :
    row = [[order, degree, 'height', 'mode', value, 0, 0, bounds_height[0], bounds_height[1]]]
  if width is None :
    row = [[order, degree, 'width', 'mode', value, 0, 0, bounds_width[0], bounds_width[1]]]
  if split is None :
    row = [[order, degree, 'split', 'mode', value, 0, 0, bounds_split[0], bounds_split[1]]]
  if asym is None :
    row = [[order, degree, 'asym', 'mode', value, 0, 0, bounds_asym[0], bounds_asym[1]]]
  rows = np.array (rows)
  aux = pd.DataFrame (data=rows)
  df = pd.concat ([df, aux])
  df = sort_a2z (df)

  return df
