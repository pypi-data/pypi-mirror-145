Computing Bayes factors
=======================

This tutorial explains how to use the ``bayes_factor`` function provided
with the package in order to assess the quality of the p-mode fits
performed with **apollinaire**.

WARNING: You must have run the ``first_steps.ipynb`` (**Quickstart**
tutorial) notebook before running the code in this tutorial (in order to
create the hdf5 files that will be used to compute the Bayes factors).

.. code:: ipython3

    import apollinaire as apn
    import apollinaire.timeseries as timeseries
    import numpy as np
    import pandas as pd 
    import importlib.resources

First, we have to read again the data used to perform the fit. We also
need to read the a2z DataFrame that **apollinaire** created at the end
of the MCMC process.

.. code:: ipython3

    f = importlib.resources.path (timeseries, 'kplr006603624_52_COR_filt_inp.fits')
    with f as filename :
        hdu = fits.open (filename) [0]
    data = np.array (hdu.data)
    t = data[:,0]
    v = data[:,1]
    dt = np.median (t[1:] - t[:-1]) * 86400
    freq, psd = apn.psd.series_to_psd (v, dt=dt, correct_dc=True)
    freq = freq*1e6
    psd = psd*1e-6
    back = np.loadtxt ('background.dat')
    df_a2z = apn.peakbagging.read_a2z ('modes_param.a2z')

The Bayes factor is computed considering pairs of modes, even
:math:`\ell = \{0,2\}` or odd :math:`\ell = \{1,3\}`. Let’s extract from
the DataFrame the mode orders on which we performed the fit.

.. code:: ipython3

    aux_o = df_a2z.loc[(df_a2z[1]!='a')&(df_a2z[0]!='a')&((df_a2z[1]=='0')|(df_a2z[1]=='1')), 0].astype (np.int_)
    orders = np.unique (aux_o)

We now have to loop over the orders to compute the Bayes factor for each
pair of modes.

.. code:: ipython3

    bf_array = np.zeros ((orders.size*4, 3))
    
    for ii, n in enumerate (orders) :
        psw, ps, p0, _, = apn.peakbagging.bayes_factor (freq, psd, back, df_a2z, 
                                                        n, strategy='order', l02=True, 
                                                        size_window=40, thin=5, 
                                                        discard=400, instr='geometric', 
                                                        hdf5Dir='.', add_ampl=True, 
                                                        parallelise=True)
    
        lnKsw, lnKs = apn.peakbagging.compute_lnK (psw, ps, p0) 
        bf_array[ii*4,:] = n, 0, lnKs
        bf_array[ii*4+1,:] = n-1, 2, lnKsw
    
        psw, ps, p0, _, = apn.peakbagging.bayes_factor (freq, psd, back, df_a2z, 
                                                        n, strategy='order', l02=False, 
                                                        size_window=40, thin=5, 
                                                        discard=400, instr='geometric', 
                                                        hdf5Dir='.', add_ampl=True, 
                                                        parallelise=True)
    
        lnKsw, lnKs = apn.peakbagging.compute_lnK (psw, ps, p0)
        bf_array[ii*4+2,:] = n, 1, lnKs
        bf_array[ii*4+3,:] = n-1, 3, lnKsw


.. parsed-literal::

    Window width: 40.0 muHz


.. parsed-literal::

    100%|██████████| 20480/20480 [00:46<00:00, 443.67it/s]


.. parsed-literal::

    Window width: 40.0 muHz


.. parsed-literal::

    100%|██████████| 20480/20480 [00:43<00:00, 471.46it/s]


.. parsed-literal::

    Window width: 40.0 muHz


.. parsed-literal::

    100%|██████████| 20480/20480 [00:43<00:00, 468.05it/s]


.. parsed-literal::

    Window width: 40.0 muHz


.. parsed-literal::

    100%|██████████| 20480/20480 [00:43<00:00, 472.39it/s]


.. parsed-literal::

    Window width: 40.0 muHz


.. parsed-literal::

    100%|██████████| 20480/20480 [00:40<00:00, 501.57it/s]


.. parsed-literal::

    Window width: 40.0 muHz


.. parsed-literal::

    100%|██████████| 20480/20480 [00:42<00:00, 477.23it/s]


.. parsed-literal::

    Window width: 40.0 muHz


.. parsed-literal::

    100%|██████████| 20480/20480 [00:46<00:00, 440.76it/s]


.. parsed-literal::

    Window width: 40.0 muHz


.. parsed-literal::

    100%|██████████| 20480/20480 [00:46<00:00, 440.52it/s]


.. parsed-literal::

    Window width: 40.0 muHz


.. parsed-literal::

    100%|██████████| 20480/20480 [00:42<00:00, 476.63it/s]


.. parsed-literal::

    Window width: 40.0 muHz


.. parsed-literal::

    100%|██████████| 20480/20480 [00:46<00:00, 443.85it/s]


Let’s display the results. Having :math:`\ln K = \infty` means that all
tested models were favoured against H0 (and :math:`\ln K = \infty` means
that H0 was favoured against every tested model).

.. code:: ipython3

    quality = pd.DataFrame (data=bf_array[:,2],
                            index=pd.MultiIndex.from_arrays (np.transpose (bf_array[:,:2].astype (np.int_))),
                            columns=['ln K'])
    
    display (quality)



.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th></th>
          <th>ln K</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>18</th>
          <th>0</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>17</th>
          <th>2</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>18</th>
          <th>1</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>17</th>
          <th>3</th>
          <td>-inf</td>
        </tr>
        <tr>
          <th>19</th>
          <th>0</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>18</th>
          <th>2</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>19</th>
          <th>1</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>18</th>
          <th>3</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>20</th>
          <th>0</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>19</th>
          <th>2</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>20</th>
          <th>1</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>19</th>
          <th>3</th>
          <td>-1.972969</td>
        </tr>
        <tr>
          <th>21</th>
          <th>0</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>20</th>
          <th>2</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>21</th>
          <th>1</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>20</th>
          <th>3</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>22</th>
          <th>0</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>21</th>
          <th>2</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>22</th>
          <th>1</th>
          <td>inf</td>
        </tr>
        <tr>
          <th>21</th>
          <th>3</th>
          <td>-0.004883</td>
        </tr>
      </tbody>
    </table>
    </div>


