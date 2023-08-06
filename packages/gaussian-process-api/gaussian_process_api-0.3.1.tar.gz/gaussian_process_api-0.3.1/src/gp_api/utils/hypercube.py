'''\
Utilities for the gp_api package

Vera Del Favero
utilities.py

Long description goes here.
'''

######## Module Imports ########
import numpy as np
import sys
from scipy.stats import multivariate_normal

from ..gaussian_process import GaussianProcess
from ..kernels import CompactKernel, WhiteNoiseKernel

######## Autofit ########

def sample_hypercube(limits, res):
    '''\
    Generate a list of points for a hypercube with shape (res**dim, dim)
    
    Inputs:
        limits ndarray[:,2]: list of [min,max] pairs
        res int: sample resolution in one dimension
    '''
    # Check resolution
    if not type(res) == int:
        raise TypeError("Resolution must be an integer")

    # Extract dimensionality
    dim = len(limits)

    # Find the total number of sample points
    nsample = res**dim

    # Initialize the mgrid eval string
    evalstr = "np.mgrid["
    # Loop through each dimension
    for i in range(dim):
        # Be careful what you evaluate
        xmin, xmax = float(limits[i][0]), float(limits[i][1])
        # Append to eval string
        evalstr += "%f:%f:%dj,"%(xmin, xmax, res)
    # Finish the evalstring
    evalstr += "]"

    # Find the sample space
    sample_space = eval(evalstr, None, None)
    # Reshape the sample space
    # This step prevents garbling of dimensions
    sample_space = sample_space.reshape(dim, nsample)
    # Transpose the sample space for list of points
    sample_space = sample_space.T

    return sample_space

