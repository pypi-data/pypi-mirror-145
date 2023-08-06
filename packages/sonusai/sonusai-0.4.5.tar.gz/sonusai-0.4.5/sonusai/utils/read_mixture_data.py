import h5py
import numpy as np


def read_mixture_data(filename: str) -> (np.ndarray, np.ndarray, np.ndarray):
    if not filename:
        return None, None, None

    with h5py.File(name=filename, mode='r') as f:
        return f['mixture'][:], f['target'][:], f['noise'][:]
