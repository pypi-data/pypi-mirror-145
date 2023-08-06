from typing import List
from typing import Union


def convert_mixid_to_list(mixdb: dict, mixid: Union[str, List[int]]) -> List[int]:
    if isinstance(mixid, str):
        try:
            return list(eval(f'range(len({mixdb["mixtures"]}))[{mixid}]'))
        except NameError:
            return []
    return mixid


def get_mixtures_from_mixid(mixdb: dict, mixid: Union[str, List[int]]) -> list:
    mixid_out = convert_mixid_to_list(mixdb, mixid)

    if not all(isinstance(x, int) and x < len(mixdb['mixtures']) for x in mixid_out):
        return []

    return [mixdb['mixtures'][i] for i in mixid_out]
