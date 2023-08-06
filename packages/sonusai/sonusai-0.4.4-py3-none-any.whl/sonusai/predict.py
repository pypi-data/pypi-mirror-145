"""predict

usage: predict [-hvnlas] (-m MODEL) (-i INPUT) [-o OUTPUT] [-e EXPECT] [-r RESET]

options:
   -h, --help
   -v, --verbose                Be verbose.
   -n, --no_progress            Do not show the progress bar.
   -m MODEL, --model MODEL      Trained model file.
   -i INPUT, --input INPUT      Input feature file.
   -o OUTPUT, --output OUTPUT   Optional output directory.
   -e EXPECT, --expect EXPECT   Optional expected results file.
   -l, --legacy                 Use legacy AawareRT.
   -a, --accelerate             Use acceleration if possible (only in legacy mode).
   -r RESET, --reset RESET      Reset model after RESET frames (only in legacy mode).
   -s, --sonusai_ep             Use the ONNX runtime SonusAI execution provider (only in non-legacy mode).

The predict command runs predictions on a trained model using genft generated data
and optionally compares the results to expected results.

"""
from datetime import datetime
from os import mkdir
from subprocess import run

from docopt import docopt

import sonusai
from sonusai import SonusAIError
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import update_console_handler
from sonusai.utils import trim_docstring


def predict(model: str,
            feature: str,
            output: str = None,
            expect: str = None,
            legacy: bool = False,
            accelerate: bool = False,
            reset: int = None,
            sonusai_ep: bool = True,
            verbose: bool = False,
            show_progress: bool = False):
    # TODO
    #  Return predict result
    update_console_handler(verbose)
    initial_log_messages('predict')

    # create output directory
    if output is None:
        output = f'predict-{datetime.now():%Y%m%d-%H%M%S}'

    try:
        mkdir(output)
    except OSError as e:
        raise SonusAIError(f'Could not create directory, {output}: {e}')

    log_name = output + '/predict.log'
    create_file_handler(log_name)

    logger.info(f'Writing results to {output}')

    # create command
    predict_type = ''
    if legacy:
        predict_type = '-art'

    command = ['sonusai-helper-predict' + predict_type, '-m', model, '-i', feature, '-o', output]

    if expect is not None:
        command.extend(['-e', expect])

    if legacy and accelerate:
        command.append('-a')

    if legacy and reset is not None:
        command.extend(['-r', reset])

    if not legacy and sonusai_ep:
        command.extend(['-s'])

    if verbose:
        command.append('-v')

    if not show_progress:
        command.extend(['-n'])

    try:
        run(command, check=True)
    except Exception as e:
        raise SonusAIError(f'Error running predict: {e}')


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

        predict(model=args['--model'],
                feature=args['--input'],
                output=args['--output'],
                expect=args['--expect'],
                legacy=args['--legacy'],
                accelerate=args['--accelerate'],
                reset=args['--reset'],
                sonusai_ep=args['--sonusai_ep'],
                verbose=args['--verbose'],
                show_progress=not args['--no_progress'])

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)


if __name__ == '__main__':
    main()
