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

    # pair player summary with their game library
    player_summary_and_library = []
    for s in filtered_summaries:
        lib = steam.get_owned_games(s['steamid'])
        player_summary_and_library.append((s, lib))


if __name__ == '__main__':
    main()
