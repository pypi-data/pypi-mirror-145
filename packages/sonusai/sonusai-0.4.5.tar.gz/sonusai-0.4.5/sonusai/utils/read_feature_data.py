import json

import h5py
import numpy as np


def read_feature_data(filename: str) -> (dict, np.ndarray, np.ndarray, np.ndarray):
    with h5py.File(name=filename, mode='r') as f:
        return json.loads(f.attrs['mixdb']), f['feature'][:], f['truth_f'][:], f['segsnr'][:]
