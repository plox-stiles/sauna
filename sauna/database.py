# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Trenton Stiles
# Licensed under the MIT License. See the LICENSE file in the project root for
# full license text.

'''database.py : module handles functionality for all database transactions'''

import peewee as pwe

DB_NAME = 'sauna.db'
DB = pwe.SqliteDatabase(DB_NAME)


class Base(pwe.Model):

    '''base pwe model that the rest inherit from, module syntax sugar'''

    class Meta:

        '''defined by peewee library'''

        database = DB


class Users(Base):

    '''represents the data you would get from GetPlayerSummaries API call
    https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_(v0002)'''

    steamid = pwe.TextField(primary_key=True)
    communityvisibilitystate = pwe.IntegerField()
    profilestate = pwe.IntegerField()
    personaname = pwe.TextField()
    profileurl = pwe.TextField()
    avatar = pwe.TextField()
    avatarmedium = pwe.TextField()
    avatarfull = pwe.TextField()
    avatarhash = pwe.TextField()
    lastlogoff = pwe.IntegerField()
    personastate = pwe.IntegerField()
    realname = pwe.TextField()
    primaryclanid = pwe.TextField()
    timecreated = pwe.IntegerField()
    personastateflags = pwe.TextField()


class Games(Base):

    '''Represents the most important data for a steam game'''

    name = pwe.TextField()
    appid = pwe.IntegerField(primary_key=True)
    is_free = pwe.TextField()
    detailed_description = pwe.TextField()
    header_image = pwe.TextField()
    website = pwe.TextField()
    movies = pwe.TextField()  # space seperated field of movie urls
    screenshots = pwe.TextField()  # space seperated field of screenshots
    json = pwe.TextField()

def initalize():

    '''creates the tables and the database'''

    DB.connect()
    DB.create_tables([Users, Games])