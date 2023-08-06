"""

queries - set of functions that generate mixids based on search criteria
    Each returns a dictionary where:
        - keys are the found criteria
        - values are lists of the mixids that match that criteria
    * get_mixids_from_noise(mixdb: dict, mixid: list, index: list = None) -> dict
    * get_mixids_from_noise_augmentation(mixdb: dict, mixid: list, index: list = None) -> dict
    * get_mixids_from_target(mixdb: dict, mixid: list, index: list = None) -> dict
    * get_mixids_from_target_augmentation(mixdb: dict, mixid: list, index: list = None) -> dict
    * get_mixids_from_snr(mixdb: dict, mixid: list, snr: regex = None) -> dict
    * get_mixids_from_truth_index(mixdb: dict, mixid: list, index: regex = None) -> dict
    * get_mixids_from_truth_function(mixdb: dict, mixid: list, index: regex = None) -> dict

metrics - set of functions that generate metrics data based on mixids
    * SNR summary
    * Class summary
    * Confusion matrix
        func(mixdb: dict, mixid: list) -> Pandas?

reports - set of functions that generate reports presentation based on metrics
    * SNR summary
    * Class summary
    * Confusion matrix

"""
