'''\
Utilities for the gp_api package

Vera Del Favero
utilities.py

Long description goes here.
'''

######## Module Imports ########
import numpy as np
import sys

from ..gaussian_process import GaussianProcess
from ..kernels import MaternKernel, WhiteNoiseKernel
from .hypercube import sample_hypercube 

######## Autofit ########

def fit_matern_nd(
                   x_train, y_train,
                   whitenoise=0.0,
                   nu=0.5,
                   use_cython=True,
                   xpy=None,
                   **kwargs
                  ):
    '''\
    Fit data for an arbitrary function using the compact kernel
    
    Inputs:
        x_train ndarray[npts, dim]: Training data samples
        y_train ndarray[npts]: Training data values
        whitenoise: Whitenoise kernel threshold
        sparse: Use sparse matrix operations from scikit-sparse?
        use_cython: Use compiled cython code?
        xpy: numpy equivalent (alternatively cupy)
    '''
    # Extract dimensions from data
    if len(x_train.shape) == 2:
        npts, dim = x_train.shape
    elif len(x_train.shape) == 1:
        npts, dim = x_train.size, 1
    else:
        raise TypeError("Data is not of shape (npts, dim)")

    # Check for invalid options
    if use_cython and not (xpy is None):
        import numpy as np
        if not (xpy == np):
            raise RuntimeError("use_cython is incompatible with alternative numpy")

    # Create the compact kernel
    k1 = MaternKernel.fit(
                          x_train,
                          method="sample_covariance",
                          nu=nu,
                          use_cython=use_cython,
                         )

    # Use noise
    if not whitenoise==0.0:
        k2 = WhiteNoiseKernel.fit(
                                  x_train,
                                  method="simple",
                                  sparse=False,
                                  scale=whitenoise,
                                  use_cython=use_cython,
                                 )
        # Add kernels
        kernel = k1 + k2
    else:
        # No noise
        kernel = k1

    # Fit the training data
    gp_fit = GaussianProcess.fit(x_train, y_train, kernel=kernel, **kwargs)

    return gp_fit
