Creating synthetic spectra
==========================

You might want to generate synthetic spectra in order to use them as toy
models to test **apollinaire** functionalities. This tutorial presents
the basic of synthetic spectra generation and introduce the concept of
banana diagrams.

.. code:: ipython3

    import numpy as np
    import matplotlib.pyplot as plt
    import apollinaire as apn

We are going to generate our synthetic spectrum by using results
obtained from a fit of the Kepler target Saxo. First, let’s generate the
frequency vector we will use for this work. The considered Nyquist
frequency is approximately the Nyquist frequency of Kepler short cadence
observations.

.. code:: ipython3

    freq = np.linspace (0, 8333, 50_000)

Let’s read the background parameters and the mode parameters that we are
going to use to build our synthetic spectrum.

.. code:: ipython3

    param_back = np.loadtxt ('synthetic_spectrum_tutorial/saxo_param_back.txt')[:,0]
    pkb = np.loadtxt ('synthetic_spectrum_tutorial/saxo_pkb.txt')

We are also going to set the splittings and inclination angles values to
a given value.

.. code:: ipython3

    i = 30
    nu_s = .4
    
    pkb[:, 11] = i
    pkb[:, 14] = nu_s

Now, let’s create our synthetic PSD vector (and a noise-free version for
comparison) !

.. code:: ipython3

    noise_free, entropy = apn.simulate.create_synthetic_psd (freq, pkb, param_back=param_back, 
                                                             noise_free=True)
    psd, entropy = apn.simulate.create_synthetic_psd (freq, pkb, param_back=param_back, 
                                                      entropy=127138838169534406638366956769226291439)
    
    fig, ax = plt.subplots ()
    ax.plot (freq, psd, color='black')
    ax.plot (freq, noise_free, color='cornflowerblue', lw=2)
    ax.set_xlabel (r'Frequency ($\mu$Hz)')
    ax.set_ylabel (r'Synthetic PSD')
    
    ax.set_xscale ('log')
    ax.set_yscale ('log')



.. image:: synthetic_spectrum_files/synthetic_spectrum_9_0.png


Here is a nice synthetic spectrum for which we are going to be able to
compute the so-called *banana diagram* (see Ballot et al. 2006 and
García & Ballot 2019) !

.. code:: ipython3

    back = apn.peakbagging.build_background (freq, param_back)
    grid, fig = apn.peakbagging.banana_diagram (freq, psd, back, pkb, n=50, k=50,
                                          figsize=(9,6), shading='gouraud', marker_color='black', cmap='plasma', 
                                          contour_color='grey', marker='*', add_colorbar=True,
                                          pcolormesh_options={'vmin':-9010, 'vmax':-8990},
                                          contour_options={'levels':np.linspace (-8995, -8990, 10)})
    fig.get_axes ()[0].scatter (i, nu_s, marker='x', color='black')


.. parsed-literal::

    100%|██████████| 50/50 [00:12<00:00,  3.96it/s]




.. parsed-literal::

    <matplotlib.collections.PathCollection at 0x7fb250420f70>




.. image:: synthetic_spectrum_files/synthetic_spectrum_11_2.png


It is interesting to note that the maximal likelihood is quite far from
the splittings/angle couple we considered when creating the synthetic
spectrum ! Be careful that inclination angle and rotational splittings
are strongly correlated parameters !

