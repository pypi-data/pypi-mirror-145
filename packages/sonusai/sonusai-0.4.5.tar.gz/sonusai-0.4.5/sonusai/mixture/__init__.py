# SonusAI mixture utilities

import os
import re

import sonusai

valid_augmentations = ['normalize', 'gain', 'pitch', 'tempo', 'eq1', 'eq2', 'eq3', 'lpf', 'snr', 'count']
rand_pattern = re.compile(r'rand\(([-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+)),\s*([-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+))\)')
sample_rate = 16000
bit_depth = 16
channel_count = 1
sample_bytes = int(bit_depth / 8)
float_bytes = 4
excessive_size = 6 * 1024 * 1024 * 1024

default_noise = os.path.join(sonusai.basedir, 'data', 'whitenoise.wav')
default_config = os.path.join(sonusai.basedir, 'data', 'genmixdb.yml')
default_snr = 80

from sonusai.mixture.segment import Segment  # noqa: E402
from sonusai.mixture.load_mixid import load_mixid  # noqa: E402
from sonusai.mixture.load_mixdb import load_mixdb  # noqa: E402
from sonusai.mixture.apply_augmentation import apply_augmentation  # noqa: E402
from sonusai.mixture.read_audio import read_audio  # noqa: E402
from sonusai.mixture.audio_db import build_noise_audio_db  # noqa: E402
from sonusai.mixture.audio_db import build_target_audio_db  # noqa: E402
from sonusai.mixture.audio_db import get_noise_audio_from_db  # noqa: E402
from sonusai.mixture.audio_db import get_target_audio_from_db  # noqa: E402
from sonusai.mixture.audio_db import check_audio_files_exist  # noqa: E402
from sonusai.mixture.get_class_weights_threshold import get_class_weights_threshold  # noqa: E402
from sonusai.mixture.get_default_config import get_default_config  # noqa: E402
from sonusai.mixture.update_truth_settings import update_truth_settings  # noqa: E402
from sonusai.mixture.update_config_from_file import update_config_from_file  # noqa: E402
from sonusai.mixture.get_config_from_file import get_config_from_file  # noqa: E402
from sonusai.mixture.update_config_from_hierarchy import update_config_from_hierarchy  # noqa: E402
from sonusai.mixture.get_next_noise import get_next_noise  # noqa: E402
from sonusai.mixture.get_offsets import get_offsets  # noqa: E402
from sonusai.mixture.get_mixtures_from_mixid import convert_mixid_to_list  # noqa: E402
from sonusai.mixture.get_mixtures_from_mixid import get_mixtures_from_mixid  # noqa: E402
from sonusai.mixture.class_count import get_class_count  # noqa: E402
from sonusai.mixture.class_count import get_total_class_count  # noqa: E402
from sonusai.mixture.truth_reduction import truth_reduction  # noqa: E402
from sonusai.mixture.estimate_audio_length import estimate_audio_length  # noqa: E402
from sonusai.mixture.generate_segsnr import generate_segsnr  # noqa: E402
from sonusai.mixture.generate_truth import generate_truth  # noqa: E402
from sonusai.mixture.generate_truth import truth_function  # noqa: E402
from sonusai.mixture.generate_truth import get_truth_indices  # noqa: E402
from sonusai.mixture.mixture_data import get_audio_and_truth_t  # noqa: E402
from sonusai.mixture.mixture_data import get_target_noise_audio  # noqa: E402
from sonusai.mixture.mixture_data import set_mixture_offsets  # noqa: E402
from sonusai.mixture.mixture_data import get_samples_in_mixture  # noqa: E402
from sonusai.mixture.mixture_data import get_transform_frames_in_mixture  # noqa: E402
from sonusai.mixture.mixture_data import get_feature_frames_in_mixture  # noqa: E402
from sonusai.mixture.mixture_data import get_sample_offsets_in_mixture  # noqa: E402
from sonusai.mixture.mixture_data import get_transform_frame_offsets_in_mixture  # noqa: E402
from sonusai.mixture.mixture_data import get_feature_frame_offsets_in_mixture  # noqa: E402
from sonusai.mixture.new_mixdb_from_mixid import new_mixdb_from_mixid  # noqa: E402
from sonusai.mixture.get_ft_from_file import get_ft_from_file  # noqa: E402
