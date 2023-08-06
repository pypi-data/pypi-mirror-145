from typing import List

import numpy as np


def format_confusion_matrix(cm: np.ndarray, labels: List[str] = None) -> str:
    # print confusion matrix from float variable cm and optional labels list
    return f'{cm.astype(int)}\n'
