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

    # main entry point
    '''saunas entry point'''

    # print title to screen
    print('sauna - version 0.0.1')

    # dtart logging
    util.start_logging()
    config = util.parse_config()

    # get config and prepare steamapi caller
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

    # pipe player summaries to here and it will aggregate all the
    # data to create a nice html page for you to share
    util.create_html(trimmed_summaries)


if __name__ == '__main__':
    main()
