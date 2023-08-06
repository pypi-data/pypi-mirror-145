from typing import List

import numpy as np

from sonusai.metrics import averages


def generate_snr_summary(mstat: np.ndarray, smetrics: np.ndarray, snrfloat: List[float], tasnridx: List[int]) -> str:
    # Generate summary for each SNR
    # mstat:    config params like target snr, levels, etc. [NNF, NTF, NSNR, NAUG, 23]
    # smetrics: metric data summed by SNR, must be shape [NSNR, num_classes, 12]
    # snrfloat: snr values for each NSNR dim in mstat & metsnr
    # tasnridx: index into snrfloat sorted (i.e. for highest to lowest snr)
    #
    # mstat fields:
    # [mi, tsnr, ssnrmean, ssnrmax, ssnrpk80, tgain, metrics[tridx,12], TN, FN, FP, TP, rmse[tridx]
    # metsnr fields: ACC, TPR, PPV, TNR, FPR, HITFA, F1, MCC, NT, PT, TP, FP]

    assert mstat.ndim == 5, 'mstat must be 5-dimensional.'

    NNF, NTF, NSNR, NAUG, _ = mstat.shape
    NMIX = NNF * NTF * NSNR * NAUG
    num_classes = smetrics.shape[1]

    result = f'--- NN Performance over {NMIX / NSNR} mixtures per Global SNR ---\n'
    result += '| SNR |  PPV% |  TPR% |  F1%  |  FPR% |  ACC% | SgSNRavg | SgSNR80p |\n'
    for si in range(NSNR):
        snri = tasnridx[si]
        tmpif = np.isfinite(mstat[:, :, snri, :, 2])
        mssnravg = np.mean(mstat[:, :, snri, :, 2][tmpif])  # mean segmsnr, unweighted avg, ignoring nans
        tmpif = np.isfinite(mstat[:, :, snri, :, 4])
        segsnr80pc = np.mean(mstat[:, :, snri, :, 4][tmpif])  # segmsnr80pc, unweighted avg, ignoring nans
        metavg = averages(smetrics[snri,])  # multiclass uses class averages
        # metavg fields: [PPV, TPR, F1, FPR, ACC, TPSUM]
        result += f'| {max(min(round(mstat[0, 0, snri, 0, 1]), 99), -99):+3.0f} '
        result += f'| {metavg[0, 0] * 100:5.1f} '
        result += f'| {metavg[0, 1] * 100:5.1f} '
        result += f'| {metavg[0, 2] * 100:5.1f} '
        result += f'| {metavg[1, 3] * 100:5.1f} '
        result += f'| {metavg[1, 4] * 100:5.1f} '
        result += f'|   {max(min(round(mssnravg), 99), -99):+3.0f}    '
        result += f'|   {max(min(round(segsnr80pc), 99), -99):+3.0f}    '
        result += f'|\n'

    if num_classes > 1:
        result += f'PPV,TPR,F1 are macro-avg, FPR, ACC are micro-avg over {num_classes:>6} classes.\n'

    return result
