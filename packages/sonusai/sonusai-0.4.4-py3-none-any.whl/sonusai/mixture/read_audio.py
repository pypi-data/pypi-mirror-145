from os.path import expandvars

import numpy as np
import sox

from sonusai import SonusAIError
from sonusai import logger
from sonusai import mixture


def read_audio(name: str, dither: bool = True) -> np.ndarray:
    expanded_name = expandvars(name)

    try:
        # Read in and convert to desired format
        inp = sox.Transformer()
        inp.set_output_format(rate=mixture.sample_rate, bits=mixture.bit_depth, channels=mixture.channel_count)
        inp.set_globals(dither=dither)
        return inp.build_array(input_filepath=expanded_name,
                               sample_rate_in=int(sox.file_info.sample_rate(expanded_name)))

    except Exception as e:
        if name != expanded_name:
            logger.error(f'Error reading {name} (expanded: {expanded_name}): {e}')
        else:
            raise SonusAIError(f'Error reading {name}: {e}')
