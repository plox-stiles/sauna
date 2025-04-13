# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Trenton Stiles
# Licensed under the MIT License. See the LICENSE file in the project root for
# full license text.

'''util.py - contains functions to start logging and parse the sauna config'''

from pathlib import Path
import logging
import tomllib

SAUNAROOT = Path(Path(__file__).parent).parent
SAUNACONFIG_FILENAME = 'sauna.toml'
SAUNACONFIG_FILEPATH = SAUNAROOT / SAUNACONFIG_FILENAME


def start_logging():

    '''starts the logging module and configs it'''

    fname = 'sauna.log'
    loglevel = logging.DEBUG
    logging.basicConfig(
        filename=fname,
        level=loglevel,
    )
    logging.debug('started logging')


def parse_config() -> dict:

    ''' reads the sauna toml config and returns it as a python dictionary '''

    conf = None

    logging.debug('SAUNAROOT : %s', SAUNAROOT)
    logging.debug('SAUNACONFIG_FILENAME : %s', SAUNACONFIG_FILENAME)
    logging.debug('SAUNACONFIG_FILEPATH : %s', SAUNACONFIG_FILEPATH)

    try:
        logging.info('loading configuration: %s', SAUNACONFIG_FILEPATH)
        with open(SAUNACONFIG_FILEPATH, 'rb') as f:
            conf = tomllib.load(f)
        logging.info('loaded %s', SAUNACONFIG_FILENAME)
    except Exception as e:
        logging.error("failed to load configuration %s", e)
        raise e

    return conf
