# -*- coding: utf-8 -*-
"""
    Important constants.

    :copyright: 2010-2013 by the TML Team, see AUTHORS for more details.
    :license: GNU GPL, see LICENSE for more details.
"""

import os

ITEM_VERSION, ITEM_INFO, ITEM_IMAGE, ITEM_ENVELOPE, ITEM_GROUP, ITEM_LAYER, \
    ITEM_ENVPOINT = range(7)

LAYERTYPE_INVALID, LAYERTYPE_GAME, LAYERTYPE_TILES, LAYERTYPE_QUADS, \
    LAYERTYPE_FRONT, LAYERTYPE_TELE, LAYERTYPE_SPEEDUP, LAYERTYPE_SWITCH, \
    LAYERTYPE_TUNE, LAYERTYPE_SOUNDS_DEPRECATED, LAYERTYPE_SOUNDS = range(11)

# TODO: do we need this?
ITEM_TYPES = ('version', 'info', 'image', 'envelope', 'group', 'layer',
              'envpoint')

TML_DIR = os.path.dirname(os.path.abspath(__file__))

TILEFLAG_VFLIP = 1
TILEFLAG_HFLIP = 2
TILEFLAG_OPAQUE = 4
TILEFLAG_ROTATE = 8

LAYERFLAG_DETAIL = 1

EXTERNAL_MAPRES = ['bg_cloud1', 'bg_cloud2', 'bg_cloud3', 'desert_doodads',
        'desert_main', 'desert_mountains', 'desert_mountains2', 'desert_sun',
        'generic_deathtiles', 'generic_unhookable', 'grass_doodads', 'grass_main',
        'jungle_background', 'jungle_deathtiles', 'jungle_doodads', 'jungle_main',
        'jungle_midground', 'jungle_unhookables', 'moon', 'mountains', 'snow',
        'stars', 'sun', 'winter_doodads', 'winter_main', 'winter_mountains',
        'winter_mountains2', 'winter_mountains3']

TILEINDEX  = {
    'air': 0,
    'solid': 1,
    'death': 2,
    'nohook': 3,
    'start': 33,
    'finish': 34,
    'cp_first': 35,
    'cp_last': 59,
    'stopper': 60,
    'stopper_twoway': 61,
    'stopper_allway': 62,
    'spawn': 192,
    'spawn_red': 193,
    'spawn_blue': 194,
    'flagstand_red': 195,
    'flagstand_blue': 196,
    'armor': 197,
    'health': 198,
    'shotgun': 199,
    'grenade': 200,
    'ninja': 201,
    'rifle': 202,
}

TELEINDEX = {
    'air': 0,
    'from_evil': 10,
    'weapon': 14,
    'hook': 15,
    'from': 26,
    'to': 27,
    'cp': 29,
    'cp_to': 30,
    'cp_from': 31,
    'cp_from_evil': 63,
}

SPEEDUPINDEX = 28
