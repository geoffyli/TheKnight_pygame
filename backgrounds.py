#!/usr/bin/env python
import pygame as pg
from constants import SCREENHEIGHT, SCREENWIDTH


__author__ = 'Geoff Yulong Li'


class Background:
    def __init__(self, screen, camera, image, vel_multiplier, pos, scale_multiplier) -> None:
        self.pos = pos
        self.screen = screen
        self.camera = camera
        self.vel_multiplier = vel_multiplier
        self.scale_multiplier = scale_multiplier
        self.image = pg.image.load(image)
        self.rect = self.image.get_rect(
            topleft=(self.pos[0] * SCREENWIDTH, self.pos[1] * SCREENHEIGHT))
        self.surf = pg.transform.scale(
            self.image, (int(self.scale_multiplier[0] * SCREENWIDTH), int(self.scale_multiplier[1] * SCREENHEIGHT)))
        self.width = self.rect.width
        self.height = self.rect.height

    def draw(self):
        self.screen.blit(self.surf, self.camera.customed_apply(
            self, self.vel_multiplier))
