"""evaluate

usage: evaluate [-hv] (-f FEATURE) [-m MIXTURE] [-n PREDICT] [-b BTHR] [-p PLOTNUM]

options:
   -h, --help
   -v, --verbose                    Be verbose.
   -f FEATURE, --feature FEATURE    Feature .h5 data file.
   -m MIXTURE, --mixture MIXTURE    Optional mixture .h5 data file.
   -n PREDICT, --predict PREDICT    Optional predict .h5 data file.
   -b BTHR, --bthr BTHR             Optional binary detection threshold, 0 = argmax(). [default: 0].
   -p PLOTNUM, --plotnum PLOTNUM    Optional plot mixture results (-1 is plot all, 0 is plot none) [default: 0].

The evaluate command measures performance of neural-network models from frame-by-frame truth and prediction data.
It supports data mixtures of target and noise files at various SNR levels as created by sonusai genft function.

Inputs:
    FEATURE     A SonusAI feature HDF5 file. Contains:
                    dataset:    feature
                    dataset:    truth_f
                    dataset:    segsnr
                    attribute:  mixdb
    MIXTURE     A SonusAI mixture HDF5 file. Contains:
                    dataset:    mixture
                    dataset:    target
                    dataset:    noise
    PREDICT     A SonusAI predict HDF5 file. Contains:
                    dataset:    predict (either [frames, num_classes] or [frames, timesteps, num_classes])
"""
from datetime import datetime
from os import mkdir
from os.path import basename
from os.path import splitext
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

import numpy as np
from docopt import docopt
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import sonusai
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import update_console_handler
from sonusai.metrics import averages
from sonusai.metrics import calculate_metrics
from sonusai.metrics import format_confusion_matrix
from sonusai.metrics import generate_snr_summary
from sonusai.metrics import generate_summary
from sonusai.metrics import one_hot
from sonusai.utils import int16_to_float
from sonusai.utils import read_feature_data
from sonusai.utils import read_mixture_data
from sonusai.utils import read_predict_data
from sonusai.utils import trim_docstring


def evaluate(mixdb: dict,
             feature: np.ndarray,
             truth: np.ndarray,
             segsnr: np.ndarray,
             output_dir: str,
             mixture: Union[None, np.ndarray] = None,
             target: Union[None, np.ndarray] = None,
             noise: Union[None, np.ndarray] = None,
             predict: Union[None, np.ndarray] = None,
             binary_detection_threshold: float = 0.0,
             plot_number: int = 0,
             verbose: bool = False):
    update_console_handler(verbose)
    initial_log_messages('evaluate')

    # Summarize the mixture data
    # Number of mixtures
    num_mixtures = len(mixdb['mixtures'])

    if plot_number < 0:
        # If plot_number is negative, plot all
        plot_number = [*range(num_mixtures)]
    elif plot_number == 0:
        # If plot_number is zero, plot none
        plot_number = []
    else:
        # plot_number needs to be a list (for looping later)
        plot_number = [plot_number]

    # Number of feature frames
    feature_frames = feature.shape[0]

    # Number of samples per feature
    samples_per_feature = mixdb['feature_samples']

    # Total mixture audio samples
    mixture_samples = feature_frames * samples_per_feature

    # Number of transform frames
    transform_frames = segsnr.shape[0]

    # Number of samples per transform frame
    samples_per_transform = int(mixture_samples / transform_frames)

    # Number of classes
    num_classes = truth.shape[1]

    # Summarize mixture data by noise file, target file, SNR via array mstat:
    # size NNFxNTFxNSNRxNAUGx20
    #  #noise-files, #SNR, #target-files, #augmentations, #param fields.
    # We track all other augmentations in a dimension that auto-increments, so we can support any combinations.
    # param fields:
    #          mi,target_snr,...
    noise_files = mixdb['noises']
    num_noise_files = len(noise_files)
    target_files = mixdb['targets']
    num_target_files = len(target_files)

    # Determine number of SNR cases
    snrs = []
    for target_augmentation in mixdb['target_augmentations']:
        if 'snr' in target_augmentation:
            snrs.append(target_augmentation['snr'])
    snrs = sorted(list(set(snrs)), reverse=True)

    num_snrs = len(snrs)  # Number of SNR cases
    # Detect special noise-only cases, specified by SNR < -96 where genft sets target gain = 0
    np_snrs = []
    for i, x in enumerate(snrs):
        if float(x) < -96:
            np_snrs.append(i)
    # Index of noise performance SNR (should only be 1 of them)
    if len(np_snrs) > 1:
        logger.debug('Error: more than one noise performance SNR < -96 dB detected, proceeding with first one.')
        np_snrs = [np_snrs[0]]

    num_augmentation_types = num_mixtures / (num_noise_files * num_target_files * num_snrs)
    if num_augmentation_types % 1:  # Number of augmentation types should always be integer
        logger.warning('Number of augmentations is fractional.')
    num_augmentation_types = int(np.ceil(num_augmentation_types))

    logger.info(f'Detected {num_augmentation_types} augmentation types beyond noise, target, and SNR.')

    if mixdb['truth_mutex']:
        logger.debug('Detected truth mutex mode')
        truth_is_mutex = True
    else:
        truth_is_mutex = False

    logger.info(
        f'Analyzing performance for {num_mixtures} mixtures, {num_noise_files} noise files, {num_target_files} target files, and {num_snrs} SNR levels.')

    if binary_detection_threshold == 0:
        binary_detection_threshold = 0.5
        cmode = 0
        logger.debug(
            f'Using default argmax() for detection (binary binary_detection_threshold = {binary_detection_threshold:4.2f})')
    else:
        cmode = binary_detection_threshold
        logger.debug(f'Using custom detection threshold of {binary_detection_threshold:4.2f}')

    # Mixture stats
    mstat = np.zeros(shape=(num_noise_files, num_target_files, num_snrs, num_augmentation_types, 23), dtype=np.single)
    # Multiclass stats
    mcmall = np.zeros(shape=(num_noise_files, num_target_files, num_snrs, num_augmentation_types, num_classes, 2, 2),
                      dtype=np.single)
    if num_classes > 1:
        cmall = np.zeros(
            shape=(num_noise_files, num_target_files, num_snrs, num_augmentation_types, num_classes, num_classes),
            dtype=np.single)
    else:
        cmall = np.zeros(shape=(num_noise_files, num_target_files, num_snrs, num_augmentation_types, 2, 2),
                         dtype=np.single)

    # Keep indices in fields [gsnr,HITFA,FPR,TPR,segsnravg,mxst.segsnrpkmed,mxst.NF]
    fnameidx = np.zeros(shape=(num_noise_files, num_target_files, num_snrs, num_augmentation_types, 5), dtype=np.int16)

    # Initial augmentation type
    augi = 0
    sub_predict = []

    miwidth = len(str(num_mixtures - 1))
    tfwidth = max(len(ele) for ele in [Path(x['name']).stem for x in target_files])
    nfwidth = max(len(ele) for ele in [Path(x['name']).stem for x in noise_files])

    if plot_number:
        pdf = PdfPages(f'{output_dir}/evaluate.pdf')

    for mi in range(num_mixtures):
        ni = mixdb['mixtures'][mi]['noise_file_index']
        ti = mixdb['mixtures'][mi]['target_file_index']

        # Get mixture config parameters target gain (and target SNR above)
        target_augmentation_index = mixdb['mixtures'][mi]['target_augmentation_index']
        target_snr = mixdb['target_augmentations'][target_augmentation_index]['snr']

        if 'gain' in mixdb['target_augmentations'][target_augmentation_index]:
            target_gain = mixdb['target_augmentations'][target_augmentation_index]['gain']
        else:
            target_gain = 1

        target_snr_index = snrs.index(target_snr)

        # record the FIRST truth index, provided by genft per mixture. (TBD - change to support multiple tidx??)
        truth_index = mixdb['targets'][mixdb['mixtures'][mi]['target_file_index']]['truth_index'][0][0] - 1
        # store index into filename lists in case we want full filenames
        fnameidx[ni, ti, target_snr_index, augi,] = [ni, ti, truth_index, target_snr_index, augi]

        # For each mixture, get index endpoints (mix,noise,target sample,...)
        i_sample_begin = mixdb['mixtures'][mi]['i_sample_offset']
        i_frame_begin = mixdb['mixtures'][mi]['i_frame_offset']
        o_frame_begin = mixdb['mixtures'][mi]['o_frame_offset']
        if mi == num_mixtures - 1:
            i_sample_end = mixture_samples
            i_frame_end = transform_frames
            o_frame_end = feature_frames
        else:
            i_sample_end = mixdb['mixtures'][mi + 1]['i_sample_offset']
            # in frames are transform
            i_frame_end = mixdb['mixtures'][mi + 1]['i_frame_offset']
            # out frames are possibly decimated/stride-combined
            o_frame_end = mixdb['mixtures'][mi + 1]['o_frame_offset']

        # Select subset of waveforms, if present
        sub_mixture = []
        if mixture is not None:
            sub_mixture = int16_to_float(mixture[i_sample_begin:i_sample_end])
        sub_noise = []
        if noise is not None:
            sub_noise = int16_to_float(noise[i_sample_begin:i_sample_end])
        sub_target = []
        if target is not None:
            sub_target = int16_to_float(target[i_sample_begin:i_sample_end])

        noise_level = get_level(sub_noise)
        target_level = get_level(sub_target)

        mixture_snr = target_level - noise_level

        # Segmental SNR and target stats
        sub_segnsr = segsnr[i_frame_begin:i_frame_end]

        # Replace float('Inf') with weighted filter of 16 past samples, then median filter
        sub_segnsr = segsnr_filter(sub_segnsr)

        # segmental SNR mean = mixture_snr and target_snr
        ssnrmean = 10 * np.log10(np.mean(sub_segnsr + 1e-10))
        # seg SNR max
        ssnrmax = 10 * np.log10(max(sub_segnsr + 1e-10))
        # seg SNR 80% percentile
        ssnrpk80 = 10 * np.log10(np.percentile(sub_segnsr + 1e-10, 80, interpolation='midpoint'))

        # Truth and neural-net prediction data, feature_frames x num_classes
        sub_truth = truth[o_frame_begin:o_frame_end, ]

        if predict is not None:
            sub_predict = predict[o_frame_begin:o_frame_end]
            # don't do this, expect genft to do the right thing w/truth, must be mutex
            # special case for false alarm analysis, set truth to zeros
            # if float(target_snr) < -96:
            #     truth = np.zeros(truth.shape)

            # ACC TPR PPV TNR FPR HITFA F1 MCC NT PT for each class, nclass x 10
            # cm is [TN FP; FN TP]
            (mcm, metrics, cm, cmn, rmse) = one_hot(sub_truth, sub_predict, cmode)
            # mcm2, metrics2, cm2, cmn2, rmse2 = classmetrics(sub_truth, sub_predict, cmode)

            # Save all stats, metrics and TN FP FN TP, but only includes for truth_index class.
            mstat[ni, ti, target_snr_index, augi,] = [mi, target_snr, ssnrmean, ssnrmax, ssnrpk80, target_gain,
                                                      *metrics[truth_index,],
                                                      mcm[truth_index, 0, 0], mcm[truth_index, 0, 1],
                                                      mcm[truth_index, 1, 0],
                                                      mcm[truth_index, 1, 1],
                                                      rmse[truth_index]]
            # metricsall[ni, ti, target_snr_index, augi, ] = metrics
            mcmall[ni, ti, target_snr_index, augi,] = mcm
            cmall[ni, ti, target_snr_index, augi,] = cm
            # cmnall[ni, ti, target_snr_index, augi, ] = cmn

            # Increment augmentation type
            augi += 1
            if augi >= num_augmentation_types:
                augi = 0

        if mi + 1 in plot_number:
            tname = Path(target_files[ti]['name']).stem
            nname = Path(noise_files[ni]['name']).stem
            logger.debug(
                f'{mi:{miwidth}}: Mix spec: SNR: {float(target_snr):4.1f}, target gain: {target_gain:+4.1f}, file: {tname:>{tfwidth}}, {nname:>{nfwidth}}')
            logger.debug(
                f'{mi:{miwidth}}: Measured: SNR: {mixture_snr:4.1f}, target level: {target_level:4.1f}, SegSNR mean, max, peak80%: {ssnrmean:4.1f}, {ssnrmax:4.1f}, {ssnrpk80:4.1f}')

            # Expand number of frames to number of samples (for plotting together with waveforms)
            segsnrex = np.reshape(np.tile(10 * np.log10(sub_segnsr + np.finfo(float).eps), [samples_per_transform, 1]),
                                  len(sub_segnsr) * samples_per_transform,
                                  order='F')
            sub_feature = feature[o_frame_begin:o_frame_end, ]

            # Truth extension to #samples in this mixture, i.e. MixSubSamples x num_classes
            truthex = np.zeros((len(sub_segnsr) * samples_per_transform, num_classes))
            for ntri in range(num_classes):
                truthex[:, ntri] = np.reshape(np.tile(sub_truth[:, ntri], [samples_per_feature, 1]),
                                              len(sub_segnsr) * samples_per_transform, order='F')

            # vector of indices where truth is present
            truth_active = []
            for i, x in enumerate(np.any(sub_truth, axis=0)):
                if x:
                    truth_active.append(i)

            if truth_is_mutex:
                # remove mutex (end), but not when class is always active
                if len(truth_active) > 1:
                    truth_active = np.delete(truth_active, -1)

            if len(truth_active) != 0:
                logger.debug(
                    f'{mi:{miwidth}}: Truth present in {len(truth_active)} of {num_classes} classes. First active category index: {truth_active[0]}')
            else:
                logger.debug(f'{mi:{miwidth}}: Truth not present in {num_classes} classes.')

            fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

            secu = np.arange(len(sub_segnsr) * samples_per_transform, dtype=np.single) / sonusai.mixture.sample_rate
            plots = []
            ymin = [0]

            if mixture is not None:
                mix_plot, = ax1.plot(secu, sub_mixture, 'r', label='Mix')
                plots.append(mix_plot)
                ymin.append(min(sub_mixture))
            if target is not None:
                target_plot, = ax1.plot(secu, sub_target, 'b', label='Target')
                plots.append(target_plot)
                ymin.append(min(sub_target))

            ax1.set_ylim([min(ymin), 1.05])

            if len(truth_active) > 0:
                if len(truth_active) == 1:
                    truthn_plot, = ax1.plot(secu, truthex[:, truth_active[0]], 'g-',
                                            label=f'NN Truth{truth_active[0]}')
                    plots.append(truthn_plot)
                    if truth_is_mutex:
                        trutho_plot, = ax1.plot(secu, truthex[:, -1], 'm-.',
                                                label=f'NN Truth{num_classes} (Other)')
                        plots.append(trutho_plot)
                else:
                    trutha_plot, = ax1.plot(secu, truthex, 'g-', label='NN Truth All')
                    plots.append(trutha_plot)

            if sub_predict is not None:
                nnoex = np.reshape(np.tile(sub_predict, [samples_per_feature, 1]),
                                   len(sub_segnsr) * samples_per_transform)
                nno_plot, = ax1.plot(secu, nnoex, 'k', label='NN Predict All')
                plots.append(nno_plot)

            ax1.legend(handles=plots, bbox_to_anchor=(1.05, 1.0), loc='upper left')

            ax2.plot(secu, segsnrex)
            ax2.set_ylim([-51, max(min(max(segsnrex), 100), -10)])
            ax2.title.set_text(
                f'SegSNR mean={ssnrmean:4.1f} dB, max={ssnrmax:4.1f} dB, Peak80%={ssnrpk80:4.1f} dB')

            if sub_feature.shape[1] < 5:
                tmp = np.reshape(sub_feature, (sub_feature.shape[0], sub_feature.shape[1] * sub_feature.shape[2]))
                titlestr = f'All {sub_feature.shape[0]} features of size {sub_feature.shape[2]}x{sub_feature.shape[1]}'
            else:
                if len(truth_active) != 0:
                    fti = np.nonzero(sub_truth[:, truth_active[0]])[0][0]
                else:
                    fti = 0
                tmp = np.squeeze(sub_feature[fti,])
                titlestr = f'Example feature, frame {fti} of size {sub_feature.shape[2]}x{sub_feature.shape[1]}'
            ax3.imshow(np.transpose(tmp), aspect='auto')
            ax3.invert_yaxis()
            ax3.title.set_text(titlestr)

            fig.suptitle(f'{mi + 1} of {num_mixtures}')
            fig.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

    if plot_number:
        pdf.close()

    if predict is not None:
        save_eval_report(output_dir=output_dir,
                         noise_files=noise_files,
                         target_files=target_files,
                         snrs=snrs,
                         fnameidx=fnameidx,
                         binary_detection_threshold=binary_detection_threshold,
                         np_snrs=np_snrs,
                         truth_is_mutex=truth_is_mutex,
                         mstat=mstat,
                         mcmall=mcmall,
                         cmall=cmall)


def median_filter(x: np.ndarray, n: int) -> np.ndarray:
    assert x.ndim == 1, 'Input must be one-dimensional.'

    n2 = (n - 1) // 2
    if n % 2 == 0:
        n2 += 1

    pad_x = np.zeros(len(x) + n, dtype=x.dtype)
    pad_x[n2:n2 + len(x)] = x

    y = np.zeros((len(x), n), dtype=x.dtype)
    for k in range(len(x)):
        y[k,] = pad_x[k:k + n]

    return np.median(y, axis=1)


def segsnr_filter(segsnr: np.ndarray) -> np.ndarray:
    assert segsnr.ndim == 1, 'Input must be one-dimensional.'

    inf_indices = [i for i, val in enumerate(segsnr) if np.isinf(val)]

    if inf_indices:
        scale = np.arange(16) + 1
        for inf_index in inf_indices:
            # avoid underflow at beginning
            if inf_index > 15:
                i = range(inf_index - 1, inf_index - 17, -1)
                segsnr[inf_index] = np.sum(np.multiply(segsnr[i], scale)) / 136
            else:
                i = range(inf_index + 1)
                segsnr[inf_index] = np.median(segsnr[i])
        segsnr = median_filter(segsnr, 32)
    return segsnr


def save_eval_report(output_dir: str,
                     noise_files: List[Dict],
                     target_files: List[Dict],
                     snrs: dict,
                     fnameidx: np.ndarray,
                     binary_detection_threshold: float,
                     np_snrs: list,
                     truth_is_mutex: bool,
                     mstat: np.ndarray,
                     mcmall: np.ndarray,
                     cmall: np.ndarray,
                     nfacrit: float = 0.05):
    outname = 'evaluate'
    num_noise_files = len(noise_files)
    num_target_files = len(target_files)
    num_snrs = len(snrs)
    num_augmentation_types = mstat.shape[3]
    NCLASS = mcmall.shape[4]  # mcm will = 1 for binary (always be correct)
    NMIX = num_noise_files * num_target_files * num_snrs * num_augmentation_types
    logger.info(
        f'Printing reports in {output_dir} for {NMIX} mixtures, {num_noise_files} noise files, {num_target_files} target files, {num_snrs} SNRs, {num_augmentation_types} augmentations')

    # Target all SNR list index, ordered from highest to lowest SNR
    tasnridx = np.flip(np.argsort(mstat[0, 0, :, 0, 1]))
    # Detect special case SNR
    if len(np_snrs) == 0:
        np_snrs = len(snrs) - 1
        logger.warning(
            f'Did not find low SNR (<-96 dB) case, FA analysis uses lowest SNR of {float(snrs[np_snrs]):3.0f}\n')
    else:
        np_snrs = np_snrs[0]  # In case a list is returned, use 0, TBD list support

    FPSNR = float(snrs[np_snrs])
    # Create list of non-special case SNRs, for some metrics
    if FPSNR < -96:
        sridx = np.arange(0, num_snrs)
        sridx = np.delete(sridx, np_snrs)  # Remove special case SNR
        srsnrlist = list(map(snrs.__getitem__, sridx))  # new list wo fpsnr case
    else:
        FPSNR = 99  # Mark as unused with value 99
        sridx = tasnridx
        srsnrlist = snrs

    snrfloat = np.zeros((num_snrs, 1))
    for i, x in enumerate(snrs):
        snrfloat[i] = float(x)

    if NCLASS == 1:
        bmode = True
    else:
        bmode = False  # TBD might need to detect NCLASS == 2 and truth_is_mutex

    # Total metrics over all data
    metsa, mcmsa, cmsumsa = calculate_metrics(cmall, bmode)  # metric summary all
    metsa_avg = averages(metsa)  # 3 rows: [PPV, TPR, F1, FPR, ACC, TPSUM]
    metsa_avgwo = averages(metsa[0:-1, ])

    # Total metrics over all non-special case SNR
    metsn, mcmsn, cmsumsn = calculate_metrics(cmall[:, :, sridx, ], bmode)
    metsn_avg = averages(metsn)  # 3x6
    metsn_avgwo = averages(metsn[0:-1, ])  # without other (last) class

    # Metric summary by noise and snr per class: 
    # fields: [ACC, TPR, PPV, TNR, FPR, HITFA, F1, MCC, NT, PT, TP, FP]
    metsnr = np.zeros((num_snrs, NCLASS, 12))  # per SNR: nsnr x class x 12
    metsnr_avg = np.zeros((num_snrs, 3, 6))  # per SNR avg over classes: nsnr x 3 x 6
    metsnr_avgwo = np.zeros((num_snrs, 3, 6))  # without other class
    metnsnr = np.zeros((num_noise_files, num_snrs, NCLASS, 12))  # Per Noise & SNR: nnf x nsnr x nclass x 12
    metnsnr_avg = np.zeros((num_noise_files, num_snrs, 3, 6))
    metnsnr_avgwo = np.zeros((num_noise_files, num_snrs, 3, 6))
    for target_snr_index in range(num_snrs):
        metsnr[target_snr_index,], _, _ = calculate_metrics(cmall[:, :, target_snr_index, ])
        metsnr_avg[target_snr_index,] = averages(metsnr[target_snr_index,])
        metsnr_avgwo[target_snr_index,] = averages(metsnr[target_snr_index, 0:-1, ])  # without other class = nclass
        for ni in range(num_noise_files):
            metnsnr[ni, target_snr_index,], _, _ = calculate_metrics(cmall[ni, :, target_snr_index, ])
            metnsnr_avg[ni, target_snr_index,] = averages(metnsnr[ni, target_snr_index,])
            metnsnr_avgwo[ni, target_snr_index,] = averages(metnsnr[ni, target_snr_index, 0:-1, ])

    # mcm: [TN FP; FN TP]
    # Fields in mstat, TargetSNR, TargetGain: 
    FTSNR = 1
    FTGAIN = 5
    # Fields in metrics: 
    FACC = 0
    FF1 = 6
    FTPR = 1
    FFA = 4
    FHITFA = 5

    # FA per noise-file @ lowest SNR, averages over classes:
    fanf_macwo = metnsnr_avgwo[:, np_snrs, 0, 3]  # macro-average wo other class NNFx1
    fanf_micwo = metnsnr_avgwo[:, np_snrs, 1, 3]  # micro-average wo other class NNFx1
    fanf_mac = metnsnr_avg[:, np_snrs, 0, 3]  # macro-average NNFx1
    fanf_mic = metnsnr_avg[:, np_snrs, 1, 3]  # micro-average NNFx1
    nfafail = [i for i, x in enumerate(fanf_mic) if x > nfacrit]

    # Create summary report
    summary_name = f'{output_dir}/nn_perfsummary.txt'
    with open(file=summary_name, mode='w') as f:
        # RMSEmean = np.squeeze(np.mean(np.reshape(mstat[:, :, :, :, 20], (num_noise_files, num_target_files * num_augmentation_types * num_snrs, 1)), 1))

        if bmode:  # -------------- Binary Classification ------------------
            f.write('\n')
            f.write(f'--- Aaware Binary NN Performance Analysis: {outname}\n')
            f.write(f'Performance over {NMIX} mixtures at {num_snrs} SNR cases created from\n')
            f.write(
                f'{num_target_files} target files and {num_noise_files} noise files and {num_augmentation_types} augmentations.\n')
            f.write(f'Binary classification threshold: {binary_detection_threshold:4.2f}.\n')
            f.write('\n')
            # FA Summary, note: for binary *_avg are accurate, although no avg needed (but avgwo is not)
            f.write(f'--- False Alarm Performance over {num_noise_files} noise files  ---\n')
            f.write(f'FA over all mixtures:             {metsa_avg[1, 3] * 100:6.5f}%\n')
            f.write(f'Max FA over SNRs and Noise files: {np.max(metnsnr_avg[:, :, 1, 3]) * 100:6.5f}%\n')
            f.write(f'FA of lowest SNR {FPSNR:2.0f} dB:          {metsnr_avg[np_snrs, 1, 3] * 100:6.5f}%\n')
            if len(nfafail) > 0:
                f.write(f'FAIL: Number of failing noise files with FPR rate > {nfacrit * 100:3.1f}%: {len(nfafail)}\n')
            else:
                f.write(f'PASS: Number of failing noise files with FPR rate > {nfacrit * 100:3.1f}%: {len(nfafail)}\n')

            f.write(generate_snr_summary(mstat, metsnr, snrfloat, tasnridx))

            f.write('\n\n')
            # Failing Noise File List
            if len(nfafail) > 0:
                f.write(
                    f'--- List of {len(nfafail)} failing noise files with FA rate > {nfacrit * 100:3.1f}%:\n')
                for jj in range(len(nfafail)):
                    f.write(f'{noise_files[nfafail[jj]]["name"]:40s}: {100 * fanf_mic[nfafail[jj]]:3.1f}%\n')

            f.write('\n')

        else:  # ----------------- Multiclass Classification -----------------------------
            f.write('\n')
            f.write(f'--- Aaware Multiclass NN Performance Analysis: {outname}\n')
            f.write(f'Performance over {NMIX} mixtures at {num_snrs} SNR cases created from\n')
            f.write(
                f'{num_target_files} target files and {num_noise_files} noise files and {num_augmentation_types} augmentations.\n')
            f.write(f'Number of classes: {NCLASS}.\n')
            f.write(f'Mutex mode (single-label): {truth_is_mutex}\n')
            f.write(f'Classification decision threshold: {binary_detection_threshold:4.2f}.\n')
            f.write('Confusion Matrix over all mixtures:\n')
            f.write(generate_snr_summary(mstat, metsnr, snrfloat, tasnridx))
            f.write('\n')
            # Metrics over all mixtures:
            f.write('Confusion Matrix over all mixtures:\n')
            f.write(format_confusion_matrix(cmsumsa))
            f.write('Metric summary, all mixtures:\n')
            f.write(generate_summary(metsa))
            f.write('\n')
            # Metrics excluding special case SNR
            if FPSNR < -96:
                f.write(
                    f'Metrics excluding special case false-positive SNR (FPSNR) at {FPSNR:2.0f} dB\n')
                f.write('Confusion Matrix for all mixtures except FPSNR:\n')
                f.write(format_confusion_matrix(cmsumsn))

            # FA Summary
            f.write(
                f'False alarm over all mixtures, class micro-avg for all, non-other: {metsa_avg[1, 3] * 100:6.5f}%, {metsa_avgwo[1, 3] * 100:6.5f}%\n')
            f.write(
                f'False alarm summary for lowest SNR at {FPSNR:2.0f} dB, class micro-avg over all, non-other: {metsnr_avg[np_snrs, 1, 3] * 100:6.5f}%, {metsnr_avgwo[np_snrs, 1, 3] * 100:6.5f}%\n')
            if len(nfafail) > 0:
                f.write(
                    f'FAIL: Number of failing noise files with FPR rate > {nfacrit * 100:3.1f}%: {len(nfafail)} (see noise-breakdown report)\n')
            else:
                f.write(f'PASS: Number of failing noise files with FPR rate > {nfacrit * 100:3.1f}%: {len(nfafail)}\n')
            # Print false alarm summary, use micro-avg which tends more pessimistic excluding other class if in mutex mode

            f.write('\n\n')
            f.write('-------- Per SNR Metrics ------------ \n')
            f.write('\n')
            for target_snr_index in range(num_snrs):
                si = tasnridx[target_snr_index]  # sorted list
                f.write('\n')
                f.write(f'--- Confusion Matrix for SNR {float(snrs[si]):3.1f} dB:\n')
                (met, _, cmsum) = calculate_metrics(cmall[:, :, si, ])
                f.write(format_confusion_matrix(cmsum))
                f.write('Metric summary:\n')
                f.write(generate_summary(metsnr[si,]))
                f.write('\n\n')

    # --------------- Create noise breakdown report --------------------------------
    noise_breakdown_name = f'{output_dir}/noise_breakdown.txt'
    with open(file=noise_breakdown_name, mode='w') as f:
        # Calc #frames per noise file, all speech,augm cases at lowSNR case
        f.write('\n')
        f.write(f'--- Aaware sonusai() NN False Alarm Analysis: {outname}\n')
        f.write(f'Performance over {NMIX} mixtures at {num_snrs} SNR cases created from\n')
        f.write(
            f'{num_target_files} target files, {num_noise_files} noise files and {num_augmentation_types} augmentations.\n')
        f.write(f'Classification decision threshold: {binary_detection_threshold:4.2f}.\n')
        f.write(f'Number of classes: {NCLASS}.\n')
        f.write(f'Mutex mode (single-label): {truth_is_mutex}\n')
        f.write('\n')
        f.write(f'--- NN False Alarm Summary over {num_noise_files} noise files ---\n')
        # FA Summary
        # Print false alarm summary, use micro-avg which tends more pessimistic excluding other class if in mutex mode
        f.write(
            f'False alarm over all mixtures, class micro-avg for all, non-other: {metsa_avg[1, 3] * 100:6.5f}%,{metsa_avgwo[1, 3] * 100:6.5f}%\n')
        f.write(
            f'False alarm summary for lowest SNR at {FPSNR:2.0f} dB, class micro-avg over all, non-other: {metsnr_avg[np_snrs, 1, 3] * 100:6.5f}%, {metsnr_avgwo[np_snrs, 1, 3] * 100:6.5f}%\n')

        if len(nfafail) > 0:
            f.write(f'FAIL: Number of failing noise files with FPR rate > {nfacrit * 100:3.1f}%: {len(nfafail)}\n')
        else:
            f.write(f'PASS: Number of failing noise files with FPR rate > {nfacrit * 100:3.1f}%: {len(nfafail)}\n')
        # FA per SNR
        f.write('False alarm per SNR micro-avg (%):\n')
        f.write(f'{np.transpose(snrfloat[tasnridx].astype(int))}\n')
        f.write(f'{np.round(metsnr_avg[tasnridx, 1, 3] * 100, 2)}\n')
        # FA per SNR and Class:
        # f.write(f'False alarm per SNR and Class (%):\n {np.round(metsnr[:,:,FFA]*100,2)}\n')

        f.write('\n')
        NFLOWSNR = int(
            np.sum((metnsnr[:, np_snrs, 0, 8] + metnsnr[:, np_snrs, 0, 9])) / num_noise_files)  # Nframes = NT + PT
        f.write(
            f'--- FA perf. per noise file, over {num_target_files * num_augmentation_types} mixtures, {NFLOWSNR} frames per SNR:\n')

        nfileidx = fnameidx[:, 0, 0, 0, 0]
        for ni in range(num_noise_files):
            # sortni = issnrl[ni]   # TBD figure out how to sort by FA perf
            # FA per SNR
            tmpnfname = splitext(basename(noise_files[nfileidx[ni]]['name']))[0]
            f.write('\n')
            f.write(f'--- NN Perf. for noise file {ni + 1} of {num_noise_files}: {tmpnfname} ---\n')
            f.write('False alarm per SNR micro-avg (%):\n')
            f.write(f'{np.transpose(snrfloat[tasnridx].astype(int))}\n')
            f.write(f'{np.round(metnsnr_avg[ni, tasnridx, 1, 3] * 100, 2)}\n')
            f.write('Confusion Matrix:\n')
            (_, _, cmsum) = calculate_metrics(cmall[ni,])
            f.write(format_confusion_matrix(cmsum))
            f.write(f'Noise file full path: {noise_files[nfileidx[ni]]["name"]}\n')


def get_level(audio: np.ndarray) -> float:
    if audio is not None:
        # level in dB
        return 20 * np.log10(np.sqrt(np.mean(np.square(audio))) + np.finfo(float).eps)
    return float('nan')


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

        feature_name = args['--feature']

        if args['--mixture']:
            mixture_name = args['--mixture']
        else:
            mixture_name = ''

        if args['--predict']:
            predict_name = args['--predict']
        else:
            predict_name = ''

        binary_detection_threshold = float(args['--bthr'])

        plot_number = int(args['--plotnum'])

        # create output directory
        output_dir = f'evaluate-{datetime.now():%Y%m%d-%H%M%S}'
        try:
            mkdir(output_dir)
        except OSError as error:
            logger.error(f'Could not create directory, {output_dir}: {error}')
            raise SystemExit(1)

        log_name = output_dir + '/evaluate.log'
        create_file_handler(log_name)

        mixdb, feature, truth, segsnr = read_feature_data(feature_name)
        mixture, target, noise = read_mixture_data(mixture_name)
        predict = read_predict_data(predict_name, feature.shape[0])

        evaluate(mixdb=mixdb,
                 feature=feature,
                 truth=truth,
                 segsnr=segsnr,
                 output_dir=output_dir,
                 mixture=mixture,
                 target=target,
                 noise=noise,
                 predict=predict,
                 binary_detection_threshold=binary_detection_threshold,
                 plot_number=plot_number,
                 verbose=args['--verbose'])

        logger.info(f'Wrote results to {output_dir}')

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)


if __name__ == '__main__':
    main()
