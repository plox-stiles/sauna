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

    # start logging
    util.start_logging()
    config = util.parse_config()

    # check flag to redirect control flow to
    # run the webserver instead if asset was
    # created already
    if config['web-static']:
        pass

    # get config and prepare steamapi caller
    owner = config['owner']
    steamkey = config['steamkey']
    steam = SteamAPI(steamkey)

    # TODO ensure the owners profile is public so we can read friends lists

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

    # from here we have most data and we can send the collection
    # of summaries to an output convertor or send it off to process
    # more data locally since the actual game info has not been populated

    # for now its just going to convert data the data into json and place it
    # in a static assets folder to be served by a web client.

    # doing this in order to have a pause on the project but at least show
    # have a way to nicely show the data

    util.convert_summary_web_asset(trimmed_summaries)
    print('web asset sauna.json created.')


if __name__ == '__main__':
    main()
