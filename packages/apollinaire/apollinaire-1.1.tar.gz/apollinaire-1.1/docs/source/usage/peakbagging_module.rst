The peakbagging module
**********************

.. py:module:: apollinaire.peakbagging

.. _fit_functions:

Fit functions
#############

.. autofunction:: apollinaire.peakbagging.stellar_framework

.. autofunction:: apollinaire.peakbagging.peakbagging

.. autofunction:: apollinaire.peakbagging.perform_mle_background

.. autofunction:: apollinaire.peakbagging.explore_distribution_background

.. _chain_management:

Chain management functions
##########################

.. autofunction:: apollinaire.peakbagging.read_chain

.. autofunction:: apollinaire.peakbagging.cornerplot_flatchain

.. autofunction:: apollinaire.peakbagging.hdf5_to_a2z

.. autofunction:: apollinaire.peakbagging.hdf5_to_pkb

.. autofunction:: apollinaire.peakbagging.chain_to_a2z

.. _input_output:

Input/output files management functions
#######################################

.. autofunction:: apollinaire.peakbagging.read_a2z

.. autofunction:: apollinaire.peakbagging.save_a2z

.. autofunction:: apollinaire.peakbagging.save_pkb

.. autofunction:: apollinaire.peakbagging.a2z_to_pkb

.. autofunction:: apollinaire.peakbagging.test_a2z

.. _quality_assurance:

Quality assurance functions
###########################

.. autofunction:: apollinaire.peakbagging.bayes_factor

.. _plot:

Plot functions
##############

.. autofunction:: apollinaire.peakbagging.plot_from_param

.. autofunction:: apollinaire.peakbagging.banana_diagram

.. _model_building:

Model building functions
########################

.. autofunction:: apollinaire.peakbagging.compute_model

.. autofunction:: apollinaire.peakbagging.compute_model_from_pattern

.. autofunction:: apollinaire.peakbagging.build_background

Convenience functions
#####################

.. autofunction:: apollinaire.peakbagging.create_background_guess_arrays

.. autofunction:: apollinaire.peakbagging.create_pattern_guess_arrays

.. autofunction:: apollinaire.peakbagging.hide_modes

.. autofunction:: apollinaire.peakbagging.remove_pattern
