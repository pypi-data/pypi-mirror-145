from copy import deepcopy
from typing import List
from typing import Union

from sonusai import SonusAIError
from sonusai.mixture import get_mixtures_from_mixid


def new_mixdb_from_mixid(mixdb: dict,
                         mixid: Union[str, List[int]]) -> dict:
    mixdb_out = deepcopy(mixdb)
    mixdb_out['mixtures'] = get_mixtures_from_mixid(mixdb_out, mixid)

    if not mixdb_out['mixtures']:
        raise SonusAIError(f'Error processing mixid: {mixid}; resulted in empty list of mixtures')

    return mixdb_out
