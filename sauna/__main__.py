#!/usr/bin/env python3

# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Trenton Stiles
# Licensed under the MIT License. See the LICENSE file in the project root for
# full license text.

# NAME        : sauna
# AUTHOR      : Trenton Stiles
# DESCRIPTION : a tool to produce a list of multiplayer games that you share
# with friends.

'''__main__.py : module handles all high level core logic of running sauna'''

from sauna import util
from sauna.steamapi import SteamAPI
import json


def main():

    '''saunas entry point'''

    print('sauna - version 0.0.1')

    util.start_logging()
    config = util.parse_config()

    owner = config['owner']
    steamkey = config['steamkey']
    steam = SteamAPI(steamkey)

    # TODO ensure the owners profile is public

    # get the users entire friend list
    friends = steam.get_friend_list(owner)
    friend_ids = []
    for friend in friends:
        friend_ids.append(friend['steamid'])

    # query all friends player summaries
    summaries = steam.get_player_summaries(friend_ids)

    # remove summaries that are not from friends defined in sauna config
    filtered_summaries = util.filter_summaries(summaries, config['friends'])
    trimmed_summaries = []
    for s in filtered_summaries:
        s = util.trim_summary_names(s)
        trimmed_summaries.append(s)

    # pair player summary with their game library
    player_summary_and_library = []
    for s in trimmed_summaries:
        id = str(s['steamid'])
        lib = steam.get_owned_games(id)
        player_summary_and_library.append((s, lib))

    # get a list of games that all friends own
    libraries = [x[1] for x in player_summary_and_library]
    unique_appids = util.filter_unique_games(libraries)

    out = {
        'players': [],
        'shared': [],
    }

    for player_data in player_summary_and_library:
        out['players'].append(player_data)

    # convert set to regular list
    out['shared'] = [x for x in unique_appids]

    with open('games.json', 'w', encoding='utf-8') as f:
        j = json.dumps(out)
        f.write(j)

    print('complete')


if __name__ == '__main__':
    main()
