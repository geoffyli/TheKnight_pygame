#!/usr/bin/env python
import pygame as pg
import constants as c


__author__ = 'Geoff Yulong Li'


class Button(pg.sprite.Sprite):
    def __init__(self, scene, screen, text, func, font, font_size, size, initial_pos, pos, *groups) -> None:
        # Set groups.
        if len(groups) == 0:
            # default case
            self.groups = scene.all_sprites, scene.buttons
        else:
            # customed case
            self.groups = groups
        # self.groups = scene.all_sprites, scene.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.text = text
        self.chosen = False
        self.pos = pos
        self.initial_pos = [initial_pos[0], initial_pos[1]]
        self.screen = screen
        self.func = func
        self.font = font
        self.font_size = font_size
        self.pressed = False
        self.elevation = 6  # height
        self.dynamic_elevation = 0
        self.top_color = (140, 201, 25)
        self.bottom_color = (248, 117, 157)

        self.top_rect = pg.Rect(self.initial_pos, size)
        self.bottom_rect = pg.Rect(
            (self.initial_pos[0], self.initial_pos[1] + self.elevation), size)
        self.text_surf = pg.font.Font(
            font, font_size).render(text, True, c.WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        # collide rect
        self.collide_rect = pg.Rect((self.bottom_rect.x, self.bottom_rect.y -
                                    self.elevation), (self.bottom_rect.width, self.bottom_rect.height))
        # confirm sound
        self.confirm_sound = pg.mixer.Sound(c.CONFIRMSOUND)
        self.confirm_sound.set_volume(c.sound_volume)

    def update_text(self, text):
        # Update text.
        self.text_surf = pg.font.Font(
            self.font, self.font_size).render(text, True,  c.WHITE)
        self.text_rect = self.text_surf.get_rect(topleft=self.initial_pos)

    def update(self, *text):
        """Update the pos of the top rect and text."""
        self.move()
        # Update the confirm sound volume.
        self.confirm_sound.set_volume(c.sound_volume)
        self.top_rect.topleft = (
            self.initial_pos[0], self.initial_pos[1] + self.dynamic_elevation)
        self.bottom_rect.topleft = (
            self.initial_pos[0], self.initial_pos[1] + self.elevation)
        self.collide_rect.topleft = (
            self.bottom_rect.x, self.bottom_rect.y - self.elevation)
        self.text_rect.center = self.top_rect.center
        self.check_click()

    def move(self):
        """the animation of the button"""
        self.initial_pos[0] += (self.pos[0] - self.initial_pos[0]) / 10
        self.initial_pos[1] += (self.pos[1] - self.initial_pos[1]) / 10

    def draw(self):
        """Draw the button on the screen."""
        pg.draw.rect(self.screen, self.bottom_color,
                     self.bottom_rect, border_radius=10)
        pg.draw.rect(self.screen, self.top_color,
                     self.top_rect, border_radius=10)
        self.screen.blit(self.text_surf, self.text_rect)

    def check_click(self):
        if self.chosen:
            self.top_color = (253, 166, 74)
            # If the left button of the mouse is pressed.
            if pg.key.get_pressed()[c.K_RETURN]:
                self.dynamic_elevation = self.elevation
                self.pressed = True
            else:
                self.dynamic_elevation = 0
                if self.pressed == True:
                    self.confirm_sound.play(maxtime=1000)
                    self.func()
                self.pressed = False
        else:
            self.pressed = False
            self.dynamic_elevation = 0
            self.top_color = (140, 201, 25)


class Text(pg.sprite.Sprite):
    def __init__(self, scene, screen, text, font, font_size, color, initial_pos, pos, *groups) -> None:
        # Set groups.
        if len(groups) == 0:
            # default case
            self.groups = scene.all_sprites
        else:
            # customed case
            self.groups = groups
        # self.groups = scene.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.screen = screen
        self.font = font
        self.color = color
        self.font_size = font_size
        self.text_surf = pg.font.Font(
            font, font_size).render(text, True, color)
        self.text_rect = self.text_surf.get_rect(topleft=initial_pos)
        self.initial_pos = [initial_pos[0], initial_pos[1]]
        self.pos = pos

    def update(self, *text):
        """Update the pos of the top rect and text."""
        self.move()
        if len(text) != 0:
            self.text_surf = pg.font.Font(
                self.font, self.font_size).render(str(text[0]), True, self.color)
            self.text_rect = self.text_surf.get_rect(topleft=self.initial_pos)
        self.text_rect.topleft = self.initial_pos

    def update_init_pos(self, init_pos):
        self.initial_pos = [init_pos[0], init_pos[1]]

    def move(self):
        """the animation of the button."""
        self.initial_pos[0] += (self.pos[0] - self.initial_pos[0]) / 10
        self.initial_pos[1] += (self.pos[1] - self.initial_pos[1]) / 10

    def draw(self):
        """Draw the text on the screen."""
        self.screen.blit(self.text_surf, self.text_rect)


class CustomedSurface(pg.sprite.Sprite):
    def __init__(self, scene, screen, size, color, initial_pos, pos, *groups) -> None:
        # Set groups.
        if len(groups) == 0:
            # default case
            self.groups = scene.all_sprites
        else:
            # customed case
            self.groups = groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.screen = screen
        self.surf = pg.Surface(size)
        self.color = color
        self.rect = self.surf.get_rect(topleft=initial_pos)
        self.initial_pos = [initial_pos[0], initial_pos[1]]
        self.pos = pos

    def update(self):
        """Update the pos of the top rect and text."""
        self.move()
        self.rect.topleft = self.initial_pos

    def move(self):
        """the animation of the button."""
        self.initial_pos[0] += (self.pos[0] - self.initial_pos[0]) / 10
        self.initial_pos[1] += (self.pos[1] - self.initial_pos[1]) / 10

    def draw(self):
        """Draw the text on the screen."""
        pg.draw.rect(self.screen, self.color, self.rect, border_radius=12)
