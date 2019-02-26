#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    A library which makes it possible to read teeworlds map files.

    :copyright: 2010-2013 by the TML Team, see AUTHORS for more details.
    :license: GNU GPL, see LICENSE for more details.
"""
import os

from PIL import Image

from .constants import TML_DIR


def int32(x):
    if x>0xFFFFFFFF:
        raise OverflowError
    if x>0x7FFFFFFF:
        x=int(0x100000000-x)
        if x<2147483648:
            return -x
        else:
            return -2147483648
    return x

def safe_ord(char):
    num = ord(char)
    if num > 0x7F:
        num = 0x100 - num
        if num < 128:
            return -num
        else:
            return -128
    return num

def safe_chr(i):
    return chr(max(0, min(i if i >= 0 else 256 + i, 256)))

def string_to_ints(in_string, length=8):
    ints = []
    for i in range(length):
        string = ''
        for j in range(i*4, i*4+4):
            if in_string and j < len(in_string):
                string += in_string[j]
            else:
                string += chr(0)
        ints.append(int32(((safe_ord(string[0])+128)<<24)|((safe_ord(string[1])+128)<<16)|((safe_ord(string[2])+128)<<8)|(safe_ord(string[3])+128)))
    ints[-1] &= int32(0xffffff00)
    return ints

def ints_to_string(num):
    return ''.join([''.join([
        safe_chr(((val>>24)&0xff)-128),
        safe_chr(((val>>16)&0xff)-128),
        safe_chr(((val>>8)&0xff)-128),
        safe_chr((val&0xff)-128),
    ]) for val in num]).partition('\x00')[0]


def get_next_tile_coords(layer, coord_x, coord_y):
    """Check if we are at the end of the line."""
    coord_x += 1
    if coord_x == layer.width:
        coord_x = 0
        coord_y += 1
    return coord_x, coord_y


def add_tile_image_to_final_png(layer_image, tile_image, coords):
    """Add tile png image to the final png image."""
    # Get the tile image coords
    box = (coords[0] * 64,  # left
           coords[1] * 64,  # top
           (coords[0] + 1) * 64,  # right
           (coords[1] + 1) * 64,  # bottom
           )
    # Paste the tile in the final png image
    layer_image.paste(tile_image, box, tile_image)


def get_image_from_mapres(mapres, coords, flags=None, entities=False):
    """Get tile png image from mapres."""
    # Get from entities mapres
    if entities:
        src = os.sep.join([TML_DIR, 'mapres', 'entities.png'])
        mapres_image = Image.open(src)
    # If the mapres is embedded in the map file
    elif not mapres.external:
        mapres_image = Image.frombytes(mode='RGBA', size=(mapres.width, mapres.height), data=mapres.data)
    # If the mapres is externale
    else:
        src = os.sep.join([TML_DIR, 'mapres', mapres.name +'.png'])
        mapres_image = Image.open(src)
    # Get the tile image coords
    box = (coords[0] * 64,  # left
           coords[1] * 64,  # top
           (coords[0] + 1) * 64,  # right
           (coords[1] + 1) * 64,  # bottom
           )
    # Copy only the tile image
    tile_image = mapres_image.crop(box)
    # Transform the image if needed
    if flags:
        if flags['rotation']:
            tile_image = tile_image.rotate(-90)
        if flags['vflip']:
            tile_image = tile_image.transpose(Image.FLIP_LEFT_RIGHT)
        if flags['hflip']:
            tile_image = tile_image.transpose(Image.FLIP_TOP_BOTTOM)
    return tile_image
