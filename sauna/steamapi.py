# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Trenton Stiles
# Licensed under the MIT License. See the LICENSE file in the project root for
# full license text.

''' steamapi.py - all related work to calling the steam API is here'''
import time
import logging
import httpx
from typing import Any, cast
import sauna.steamapi_error


class SteamAPI:

    '''handles interactions with the steam api'''

    def __init__(self, steam_key: str):
        self.steam_key = steam_key
        self.format = 'json'

    def verify_account_data_public(self, steamid):

        '''ensures the steamid has a profile thats public'''

        pass

    def send_api_request_rate_limited(
            self,
            url: str,
            params: dict) -> httpx.Response:

        '''When being rate limited attempt to retry the request'''
        retrys = 5
        resp = httpx.Response(429)
        for i in range(retrys):
            wait_time = i * 5
            logging.info('rate-limited: waiting %d seconds', wait_time)
            time.sleep(wait_time)
            resp = httpx.get(url, params=params)
            if resp.status_code == 200:
                break
        return resp

    def send_api_request(
            self,
            url: str,
            params: dict) -> dict[str, Any]:

        '''wraps all the get requests for api calls to steam'''

        logging.debug('sending get request: %s', url)
        resp = httpx.get(url, params=params)
        logging.debug('response status code: %d', resp.status_code)

        if resp.status_code == 429:
            logging.warning('rate limit hit, retrying slowly...')
            resp = self.send_api_request_rate_limited(url, params)

        if resp.status_code != 200:
            logging.debug('response code: %s', resp.status_code)
            logging.debug('url : %s', resp.url)
            logging.debug('url : %s', resp.headers)
            raise sauna.steamapi_error.InvalidStatusCodeError()

        try:
            data: dict = resp.json()
            logging.debug('send_api_request data: %s', data)
        except Exception as e:
            logging.error('failed to parse json from request')
            raise e

        return data

    def get_friend_list(self, steamid) -> list[dict[str, str | int]]:

        '''returns a list of friends from the associated steam id'''

        # API Reference:
        # https://developer.valvesoftware.com/wiki/Steam_Web_API#GetFriendList_(v0001)

        logging.info('requesting friends list')

        url = (
            'http://api.steampowered.com/'
            'ISteamUser/GetFriendList/v0001/'
        )

        params = {
            'key': self.steam_key,
            'steamid': steamid,
            'relationship': 'friend',
            'format': self.format,
        }

        friends = self.send_api_request(url, params)
        friends = friends['friendslist']['friends']

        logging.info('retrieved %d friends', len(friends))
        logging.debug('friends : %s', friends)

        return cast(list[dict[str, str | int]], friends)

    def get_player_summaries(
            self,
            steamids: list[str] | str
            ) -> list[dict[str, str | int]]:

        '''Get a steam players summary'''

        # API Reference:
        # https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_(v0002)

        logging.info('requesting player summaries')

        url = (
            'http://api.steampowered.com/'
            'ISteamUser/GetPlayerSummaries/v0002/'
        )

        if type(steamids) is not str:

            if len(steamids) > 100:
                raise sauna.steamapi_error.ExceedSteamIDQueryError

            steamids = ','.join(steamids)

        params = {
            'key': self.steam_key,
            'steamids': steamids,
            'format': self.format,
        }

        summaries = self.send_api_request(url, params)

        summaries = summaries['response']['players']
        summary_list = cast(list[dict[str, str | int]], summaries)

        logging.info('retrieved player summaries')
        logging.debug('summaries : %s', summaries)

        return summary_list

    def get_owned_games(self, steamid: str) -> list[dict[str, str | int]]:

        '''returns a list of games a player owns'''

        params = {
            'steamid': steamid,
            'include_appinfo': 1,
            'include_played_free_games': 1,
            'key': self.steam_key,
        }

        url = (
            'http://api.steampowered.com/'
            'IPlayerService/GetOwnedGames/v0001/'
        )

        resp = self.send_api_request(url, params)
        games = resp['response']['games']
        return games

    def get_game_info(self, appid: str) -> dict:

        '''pass in an appid and return the json as a dict'''

        url = (
            f"https://store.steampowered.com/"
            f"api/appdetails?appids={appid}"
        )

        params = {'appids': appid}
        resp = self.send_api_request(url, params)

        # if bad request like invalid appid comes in
        # we will still get a success on response
        if not resp[appid]['success']:
            return {}

        return resp[appid]['data']


class PlayerSummary():

    '''Represents a steam player'''

    def __init__(self):

        # public data
        self.steamid = ''
        self.personaname = ''
        self.profileurl = ''
        self.avatar = ''
        self.avatarmedium = ''
        self.avatarfull = ''
        self.personastate = ''
        self.communityvisibilitystate = ''
        self.profilestate = ''
        self.lastlogoff = ''
        self.commentpermission = ''

        # private data
        self.realname = ''
        self.primaryclanid = ''
        self.timecreated = ''
        self.gameid = ''
        self.gameserverip = ''
        self.gameextrainfo = ''
        self.cityid = ''
        self.loccountrycode = ''
        self.locstatecode = ''
        self.loccityid = ''
