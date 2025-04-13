# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Trenton Stiles
# Licensed under the MIT License. See the LICENSE file in the project root for
# full license text.

'''steamapi_error.py - contains all the exceptions that can be raised by the
steamAPI class'''


class SteamAPIError(Exception):

    '''Base class for all SteamAPI errors'''


class InvalidStatusCodeError(SteamAPIError):

    '''The HTTP request for friends list was not 200'''


class ExceedSteamIDQueryError(SteamAPIError):

    '''The amount of steam ids placed in the query exceeded the limit of 100'''
