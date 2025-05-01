# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Trenton Stiles
# Licensed under the MIT License. See the LICENSE file in the project root for
# full license text.

'''util.py - contains functions to start logging and parse the sauna config'''

from pathlib import Path
import logging
import tomllib
from itertools import chain
from typing import Any
from sauna.steamapi import SteamAPI
import json

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


def filter_summaries(
        summaries: list[dict[str, Any]],
        config_friends: list[str]) -> list[dict[str, str | int]]:

    '''remove summaries that are not from friends defined in sauna config'''

    filtered = []
    for f in config_friends:
        s = [x for x in summaries if f in x.values()]
        if len(s) > 1:
            logging.warning('filter_summaries: duplicate found: %s', s)

        if len(s) <= 0:
            logging.warning('filter_sumarries: config friend not found: %s', f)

        filtered.append(s)

    # flatten lists inside filtered, returns duplicates and or empty list
    return list(chain.from_iterable(filtered))


def trim_summary_names(summary: dict) -> dict:

    '''trim everything except id, names, avatar, profile'''
    keys = [
        'steamid',
        'personaname',
        'profileurl',
        'avatarfull',
        'realname',
        ]

    trim_summary = {}
    for k in keys:
        try:
            trim_summary[k] = summary[k]
        except KeyError:
            trim_summary[k] = ''
    return trim_summary


def filter_unique_games(libraries: list[list[dict[str, str | int]]]
                        ) -> set[int]:

    '''pass in a list of game libraries and return a set of the games
    app ids that all accounts have'''

    appids: list[set] = []
    for lib in libraries:
        ids = set(game['appid'] for game in lib)
        appids.append(ids)

    # intersection will reduce the elements to ids all sets share,
    common: set = set.intersection(*appids)

    return common


def create_html(player_summaries: list[dict]):

    '''creates a nice formatted way of showing the players profiles
    and they games they all share'''

    player_info = {}

    config = parse_config()
    steam = SteamAPI(config['steamkey'])

    for summary in player_summaries:
        steamid = summary['steamid']
        library = steam.get_owned_games(steamid)

        info = {
            'library': library,
            'summary': summary,
        }

        player_info[steamid] = info

    with open('data.json', 'w') as f:
        w = json.dumps(player_info)
        f.write(w)

    print('finished writing player data')
