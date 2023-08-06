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
from ..kernels import CompactKernel, WhiteNoiseKernel
from .hypercube import sample_hypercube 

######## Autofit ########

def fit_compact_nd(
                   x_train, y_train,
                   whitenoise=0.0,
                   sparse=True,
                   use_cython=True,
                   xpy=None,
                   order=1,
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
    k1 = CompactKernel.fit(
                           x_train,
                           method="scott",
                           sparse=sparse,
                           use_cython=use_cython,
                           order=order,
                          )

    # Use noise
    if not whitenoise==0.0:
        k2 = WhiteNoiseKernel.fit(
                                  x_train,
                                  method="simple",
                                  sparse=sparse,
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

def train_function(
                   true_pdf,
                   dim,
                   limits=None,
                   train_res=10,
                   xnoise=0.,
                   ynoise=0.,
                   seed=10,
                  ):
    '''\
    Generate training data for an arbitrary function on a grid
    
    Inputs:
        true_pdf: a function to evaluate the pdf on
        dim: number of dimensions
        limits ndarray[:,2]: list of [min,max] pairs
        res: sample resolution for TRAINING
        xnoise = input noise for data
        ynoise: output noise for data
        seed: numpy random state or int
    '''
    # Generate a random state
    if str(type(seed)) == "<class 'numpy.random.mtrand.RandomState'>":
        random_state = seed
    else:
        random_state = np.random.RandomState(seed)

    # Find nsample
    nsample = train_res**dim

    # Generate reasonable limits
    if limits is None:
        # Assume limits are between zero and one
        # You'd be suprised how often this is good enough
        print("Warning: train_function called without limits. Assuming [0,1]",
            file=sys.stderr)
        limits = np.zeros((dim,2))
        limits[:,1] = 1.
    else:
        if not (limits.shape == (dim, 2)):
            raise ValueError("Conflicting limits and dim")

    # Find sample space
    x_model = sample_hypercube(limits, train_res)

    # Generate training data
    x_train = x_model.copy()
    # Find y values
    y_model = true_pdf(x_train)
    y_train = y_model.copy()

    # Add noise
    if xnoise != 0:
        for i in range(dim):
            x_train[:,i] += random_state.normal(scale=xnoise,size=nsample)
    if ynoise !=0:
        y_train += random_state.normal(scale=ynoise,size=nsample)

    return x_train, y_train
        
