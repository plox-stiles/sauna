# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Trenton Stiles
# Licensed under the MIT License. See the LICENSE file in the project root for
# full license text.

'''web.py - for now just handles all operations of serving up a simple
static website to the user to display the data nicely.'''

from pathlib import Path
import json
# import asyncio

from flask import Flask, send_from_directory, jsonify, Response

# from sauna.steamapi import SteamAPI
# from sauna.util import parse_config

# conf = parse_config()
# steam = SteamAPI(conf['steamkey'])
app = Flask(__name__, static_folder='static')
STATIC_SAUNA_LOC = Path(__file__).resolve().parent / 'static' / 'sauna.json'
STATIC_SAUNA_DATA = Response()


@app.route('/')
def serve_index():

    '''serves the home page'''

    if not app.static_folder:
        return ''

    response = send_from_directory(app.static_folder, 'index.html')
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/sauna/v1/pool')
def serve_pool():

    '''API sends json containing static profile info and games owned'''

    if not STATIC_SAUNA_DATA:
        return ''
    return jsonify(STATIC_SAUNA_DATA)


@app.route('/sauna/v1/store/<int:appid>')
def serve_store(appid):

    '''handles proxying the connection between the web page and
    the steam powered server'''
    # TODO need to wrap this in an async wrapper
    # this uses httpx.get() which is IO blocking
    # flask from running properly
    # return jsonify(steam.get_game_info(appid))
    return Response()


def run():

    '''initalizes the flask app to actually start'''
    global STATIC_SAUNA_DATA
    with open(STATIC_SAUNA_LOC, 'r') as f:
        STATIC_SAUNA_DATA = json.load(f)
    app.run(host='0.0.0.0', port=3889, debug=True)


if __name__ == '__main__':
    with open(STATIC_SAUNA_LOC, 'r') as f:
        STATIC_SAUNA_DATA = json.load(f)
    app.run(host='0.0.0.0', port=3889, debug=True)