#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from tml import Header, Teemap
from items import Layer, QuadLayer, TileLayer

class TestHeader(unittest.TestCase):

    def setUp(self):
        pass

    def test_signature(self):
        with open('tml/maps/dm1.map') as f:
            header = Header(f)

    def test_load(self):
        assert Teemap('tml/maps/dm1.map')
        assert Teemap('tml/maps/dm1')
        t = Teemap()
        t.load('tml/maps/dm1.map')
        t = Teemap()
        t.load('tml/maps/dm1')

class TestTeemap(unittest.TestCase):

    def setUp(self):
        pass

    def test_groups(self):
        t = Teemap('tml/test_maps/vanilla')
        self.assertEqual(len(t.groups), 7)
        names = [None, None, 'Game', 'NamedGroup', None, None, 'OtherGroup']
        for i, group in enumerate(t.groups):
            self.assertEqual(group.name, names[i])

    def test_layers(self):
        t = Teemap('tml/test_maps/vanilla')
        self.assertEqual(len(t.layers), 6)
        for i, num in enumerate([1,2,1,0,2,0,0]):
            self.assertEqual(len(t.groups[i].layers), num)

        self.assertIs(t.groups[0].layers[0], t.layers[0])
        self.assertIs(t.groups[1].layers[0], t.layers[1])
        self.assertIs(t.groups[1].layers[1], t.layers[2])
        self.assertIs(t.groups[2].layers[0], t.layers[3])
        self.assertIs(t.groups[4].layers[0], t.layers[4])
        self.assertIs(t.groups[4].layers[1], t.layers[5])

        names = ['TestQuads', 'Quads', 'TestTiles', 'Game', None, 'LastTiles']
        classes = [QuadLayer, QuadLayer, TileLayer, TileLayer, TileLayer,
                   TileLayer]
        for i, layer in enumerate(t.layers):
            self.assertIsInstance(layer, classes[i])
            self.assertEqual(layer.name, names[i])

        for layer in t.layers:
            if isinstance(layer, TileLayer):
                if layer.name == 'TestTiles':
                    self.assertEqual(layer.width, 42)
                    self.assertEqual(layer.height, 84)
                else:
                    self.assertEqual(layer.width, 50)
                    self.assertEqual(layer.height, 50)

    def test_envelopes(self):
        t = Teemap('tml/test_maps/vanilla')
        self.assertEqual(len(t.envelopes), 2)
        self.assertEqual(t.envelopes[0].name, 'PosEnv')
        self.assertEqual(t.envelopes[1].name, 'ColorEnv')

    def test_envpoints(self):
        t = Teemap('tml/test_maps/vanilla')
        self.assertEqual(len(t.envpoints), 9)
        self.assertEqual(len(t.envelopes[0].envpoints), 4)
        self.assertEqual(len(t.envelopes[1].envpoints), 5)

        for i, envpoint in enumerate(t.envelopes[0].envpoints):
            self.assertIs(envpoint, t.envpoints[i])
        for i, envpoint in enumerate(t.envelopes[1].envpoints):
            self.assertIs(envpoint, t.envpoints[i+4])

if __name__ == '__main__':
    unittest.main()