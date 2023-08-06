# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution("apollinaire").version
except DistributionNotFound:
    __version__ = "unknown version"


sys.path.insert(0, os.path.abspath('../../apollinaire'))
 
autodoc_mock_imports = ['numpy', 'scipy', 'matplotlib', 'matplotlib.pyplot',
                        'scipy.optimize', 'matplotlib.ticker', 'corner', 'emcee', 'pandas', 'astropy',
                        'numdifftools', 'george', 'tqdm', 'dill', 'pathos', 'pathos.multiprocessing',
                        'h5py', 'statsmodels.nonparametric.smoothers_lowess', 'pycorrelate', 'numba',
                        'scipy.io', 'statsmodels', 'np', 'pd', 'plt', 'scipy.interpolate',
                        'astropy.stats', 'scipy.signal', 'joblib']

# -- Project information -----------------------------------------------------

project = 'apollinaire'
copyright = '2020, Sylvain N. Breton'
author = 'Sylvain N. Breton'
master_doc = 'index'
source_suffix = ".rst"

# The full version, including alpha/beta/rc tags
release = __version__
version = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 
              'sphinx.ext.napoleon',
              'sphinx.ext.mathjax', 
              'sphinx_book_theme', 
              'IPython.sphinxext.ipython_console_highlighting']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['notebooks/golf_timing']


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_title = "apollinaire"
html_logo = "apollinaire_logo.png"
html_theme_options = {
     "path_to_docs": "docs",
     "repository_url": "https://gitlab.com/sybreton/apollinaire/",
     "use_repository_button": True,
     "use_download_button": True,
     "logo_only": True,
     }
html_sidebars = {
    "**": [
     "sidebar-logo.html",
     "search-field.html", 
     "sbt-sidebar-nav.html", 
     "sbt-sidebar-footer.html"
          ]
     }
numpydoc_show_class_members = False
