#!/usr/bin/env python
import pygame as pg
from constants import *
import pytmx


__author__ = 'Geoff Yulong Li'


def collide_rect(one, two):
    return one.rect.colliderect(two.rect)


def collide_body_rect(o, t):
    return o.body_rect.colliderect(t.rect)


def collide_another_body_rect(o, t):
    return o.rect.colliderect(t.body_rect)


class TiledMap:
    def __init__(self, filename) -> None:
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        # tm.width is the num of blocks, tm.tilewidth is the num of pixels of one tile.
        # self.width is the num of pixels of the tiled map.
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm  # type: pytmx.TiledMap

    def render(self, surface):
        """This method traverses the layers in the tiled map and 
            blits the images of tiles to the tiled map surface."""
        # ti() returns the image according to the gid.
        ti = self.tmxdata.get_tile_image_by_gid
        # from bottom to top layer.
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)  # tile is the image of the specific tile.
                    if tile:  # If tile isn't null, blit it to the tiled map surface.
                        surface.blit(
                            tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        """Create the surface of the tiled map."""
        # Create a surface the same size of the tiled map.
        temp_surface = pg.Surface((self.width, self.height))
        # Render the surface.
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height) -> None:
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width  # map width
        self.height = height  # map height
        # self.camera = None  # It's a rect.
        self.x = 0
        self.y = 0

    def apply(self, entity):
        """Apply the camera to the entity."""
        return entity.rect.move(self.x, self. y)

    def customed_apply(self, entity, multiplier):
        """Apply the camera to the entity with the multiplier."""
        return entity.rect.move((multiplier * self.x, multiplier * self. y))

    def apply_rect(self, rect):
        return rect.move((self.x, self.y))

    def update(self, target):
        """Follow the target sprite.
           self.x, self.y are offset variables."""
        self.x = -target.rect.x - target.rect.width + int(SCREENWIDTH / 2)
        self.y = -target.rect.y - target.rect.height + int(SCREENHEIGHT / 2)
        # limit scrolling to map size
        self.x = min(0, self.x)  # left
        self.y = min(0, self.y)  # top
        self.x = max(-(self.width - SCREENWIDTH), self.x)  # right
        self.y = max(-(self.height - SCREENHEIGHT), self.y)  # bottom

    def delayed_update(self, target):
        """Follow the target sprite and make a little lag."""
        self.x += (int(SCREENWIDTH / 2) - target.rect.x -
                   target.rect.width - self.x) / 20
        self.y += (int(SCREENHEIGHT * 2 / 3) - target.rect.y -
                   target.rect.height - self.y) / 20
        # limit scrolling to map size
        self.x = min(0, self.x)  # left
        self.y = min(0, self.y)  # top
        self.x = max(-(self.width - SCREENWIDTH), self.x)  # right
        self.y = max(-(self.height - SCREENHEIGHT), self.y)  # bottom
