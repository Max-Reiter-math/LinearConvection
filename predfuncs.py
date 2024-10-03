"""
Definition of prescribed stationary velocity field and initial mass density
"""
import numpy as np

def initial_velocity(x: np.ndarray, dim: int=2) -> np.ndarray:
    if dim not in [2,3]: raise ValueError("Dimension "+str(dim)+" not supported.")
    # x hase shape (dimension, points)
    values = np.zeros((dim, x.shape[1]))
    # values[0] = -(x[1]-0.5)
    # values[1] = (x[0]-0.5)
    amplitude = 5
    freqx = 1.0
    freqy = 1.0
    rescaledx = freqx * np.pi*x[0] +np.pi*0.5 
    rescaledy = freqy * np.pi*x[1] +np.pi*0.5 
    values[0] = - np.cos(rescaledx) * np.sin(rescaledy)
    values[1] =   np.sin(rescaledx) * np.cos(rescaledy)
    if dim == 3: values[2] = 0.0
    return amplitude*values

def init_mass(x: np.ndarray, dim: int=1) -> np.ndarray:
    # x hase shape (dimension, points)
    values = np.zeros((dim, x.shape[1]))
    dofs = (x[0] <=0.5)
    values[0][dofs] = 1.0
    return values