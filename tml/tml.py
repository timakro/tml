#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    The TeeworldsMapLib is a python tool which makes it possible to read,
    modify and write teeworlds map files easily without using the original
    teeworlds client, allowing to built teewor on top of it

    :copyright: 2010-2013 by the TML Team, see AUTHORS for more details.
    :license: GNU GPL, see LICENSE for more details.
"""
import sys

from PIL import Image

from .constants import *
from .datafile import DataFileReader, DataFileWriter
from .items import TileLayer
from .utils import get_next_tile_coords, add_tile_image_to_final_png, get_image_from_mapres

class MapError(BaseException):
    """Raised when your map is not a valid teeworlds map.

    For example, it will be raised when there is no gamelayer or more than one.

    """

class LayerError(MapError):
    pass

class Teemap(object):
    """Representation of a teeworlds map.

    All information about the map can be accessed through this class.

    :param map_path: Path to the teeworlds mapfile.
    """

    def __init__(self, map_path=None):
        self.name = ''

        if map_path:
            self._load(map_path)
        else:
            # default item types
            for type_ in ITEM_TYPES:
                if type_ not in ('version', 'layer', 'info'):
                    setattr(self, ''.join([type_, 's']), [])
            self.info = None

    @property
    def layers(self):
        """Returns a list of all layers, collected from the groups."""
        layers = []
        for group in self.groups:
            layers.extend(group.layers)
        return layers

    @property
    def gamelayer(self):
        """Returns the gamelayer."""
        for layer in self.layers:
            if layer.is_gamelayer:
                return layer

    @property
    def telelayer(self):
        """Returns the telelayer. Only for race modification."""
        for layer in self.layers:
            if layer.is_telelayer:
                return layer

    @property
    def speeduplayer(self):
        """Returns the speeduplayer. Only for race modification."""
        for layer in self.layers:
            if layer.is_speeduplayer:
                return layer

    @property
    def frontlayer(self):
        """Returns the frontlayer. Only for DDrace modification."""
        for layer in self.layers:
            if layer.is_frontlayer:
                return layer

    @property
    def switchlayer(self):
        """Returns the switchlayer. Only for DDrace modification."""
        for layer in self.layers:
            if layer.is_switchlayer:
                return layer

    @property
    def tunelayer(self):
        """Returns the tunelayer. Only for DDrace modification."""
        for layer in self.layers:
            if layer.is_tunelayer:
                return layer

    @property
    def gamegroup(self):
        for group in self.groups:
            if group.is_gamegroup:
                return group

    @property
    def width(self):
        return self.gamelayer.width

    @property
    def height(self):
        return self.gamelayer.height

    def validate(self):
        """Check if the map is a valid teeworlds map.

        Returns ``True`` or raises an exception.

        """
        gamelayers = 0
        for layer in self.layers:
            if layer.type == 'tilelayer':
                if len(layer.tiles) != layer.width * layer.height:
                    raise LayerError('Layer width and height does not fit to '
                                     'the number of tiles')
            if layer.is_gamelayer:
                gamelayers += 1
        if gamelayers < 1:
            raise MapError('This map contains no gamelayer.')
        if gamelayers > 1:
            raise MapError('This map contains {0} gamelayers.'.format(gamelayers))
        if len(self.gamelayer.tiles) == 0:
            raise MapError('The gamelayer does not contain any tiles')

        return True

    def _load(self, map_path):
        """Load a new teeworlds map from `map_path`.

        Should only be called by __init__.
        """
        datafile = DataFileReader(map_path)
        self.envelopes = datafile.envelopes
        self.envpoints = datafile.envpoints
        self.groups = datafile.groups
        self.images = datafile.images
        self.info = datafile.info

    def save(self, map_path):
        """Saves the current map to `map_path`."""
        DataFileWriter(self, map_path)

    def _create_default(self):
        """Creates the default map.

        The default map consists out of two groups containing a quadlayer
        with the background and the game layer. Should only be called by
        __init__.

        """
        self.info = items.Info()
        self.groups = []
        background_group = items.Group()
        self.groups.append(background_group)
        background_group.default_background()
        background_layer = items.QuadLayer()
        background_layer.add_background_quad()
        background_group.layers.append(background_layer)
        game_group = items.Group()
        self.groups.append(game_group)
        game_layer = items.TileLayer(game=1)
        game_group.layers.append(game_layer)

    def export_to_png(self, output_file_path, progress_bar=False):
        """Create a png file based on the map."""

        # For each group
        for group in self.groups:
            # Keep only the groups where there is a game layer
            if [l for l in group.layers if l.is_gamelayer]:
                # Get map size
                image_width = max([l.width for l in group.layers if isinstance(l, TileLayer)])
                image_height = max([l.height for l in group.layers if isinstance(l, TileLayer)])
                # Create a new empty image
                layer_image = Image.new('RGBA', (image_width * 64, image_height * 64))

                # For each group layer
                tile_layers = [l for l in group.layers if isinstance(l, TileLayer)]
                for layer_index, layer in enumerate(tile_layers):
                    mapres = None
                    if not layer.is_gamelayer:
                        # If It's not a gamelayer, get the mapres
                        mapres = self.images[layer.image_id]

                    # Progress bar
                    if progress_bar:
                        sys.stdout.write("\nLayer {}/{}".format(layer_index + 1, len(tile_layers)))
                        sys.stdout.write("\nTiles in this layer: {}\n".format(len(layer.tiles)))
                        toolbar_width = 100
                        sys.stdout.write("[%s]" % (" " * toolbar_width))
                        sys.stdout.flush()
                        sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

                    # For each cell on the layer grid
                    coord_y = 0
                    coord_x = 0
                    for tile_index, tile in enumerate(layer.tiles):
                        empty_tile = False
                        if not layer.is_gamelayer:
                            # If it's not a game layer, we get the tile from the mapres
                            tile_image = get_image_from_mapres(mapres, tile.coords, tile.flags)
                        else:
                            # If it's a game layer, we get the tile from the entities mapres
                            tile_type = R_TILEINDEX.get(tile.index)
                            if not tile_type:
                                empty_tile = True
                            else:
                                tile_image = get_image_from_mapres(None, tile.coords, None, True)

                        if not empty_tile:
                            # Add the tile_image to the final png image
                            add_tile_image_to_final_png(layer_image, tile_image, (coord_x, coord_y))
                            if progress_bar and tile_index * toolbar_width / len(layer.tiles) % 1 == 0:
                                sys.stdout.write("-")
                                sys.stdout.flush()

                        # Get the next tile coords
                        coord_x, coord_y = get_next_tile_coords(layer, coord_x, coord_y)
                        # Repeat the tile on the final png image if it's needed
                        for x in range(tile.skip):
                            if not empty_tile:
                                # Add the tile_image to the final png image
                                add_tile_image_to_final_png(layer_image, tile_image, (coord_x, coord_y))
                                if progress_bar and tile_index * toolbar_width / len(layer.tiles) % 1 == 0:
                                    sys.stdout.write("-")
                                    sys.stdout.flush()

                            # Get the next tile coords
                            coord_x, coord_y = get_next_tile_coords(layer, coord_x, coord_y)

                # Save image
                layer_image.save(output_file_path)

    def __repr__(self):
        return '<Teemap ({0})>'.format(self.name or 'new')
