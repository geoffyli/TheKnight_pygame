#!/usr/bin/env python
import pygame as pg
from constants import BLACK, SCREENHEIGHT, SCREENWIDTH


__author__ = 'Geoff Yulong Li'


class Background:
    def __init__(self, screen, camera, image, vel_multiplier, pos, scale_multiplier, *convert) -> None:
        self.pos = pos
        self.screen = screen
        self.camera = camera
        self.vel_multiplier = vel_multiplier
        self.scale_multiplier = scale_multiplier
        # if convert arg is True, convert image surface.
        if len(convert) != 0 and convert[0]:
            self.image = pg.image.load(image).convert()
        else:
            self.image = pg.image.load(image)
        self.image.set_colorkey(BLACK)
        self.surf = pg.transform.scale(
            self.image, (int(self.scale_multiplier[0] * SCREENWIDTH), int(self.scale_multiplier[1] * SCREENHEIGHT)))
        self.rect = self.surf.get_rect(
            topleft=(self.pos[0] * SCREENWIDTH, self.pos[1] * SCREENHEIGHT))

    def draw(self):
        self.screen.blit(self.surf, self.camera.customed_apply(
            self, self.vel_multiplier))
