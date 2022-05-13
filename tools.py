#!/usr/bin/env python
import pygame as pg
from constants import *
from scenes import *
from menus import *
from globals import Global


__author__ = 'Geoff Yulong Li'

next_scene = ['outside', 'player01']


class Control:
    def __init__(self) -> None:
        self.clock = None
        self.screen = None
        self.pressed_keys = None

    def pygame_init(self):
        """Initialize the pygame module."""
        # Init pygame module.
        pg.init()
        self.clock = pg.time.Clock()
        self.display = self.glo.display
        self.display.fill(BLACK)
        self.screen = pg.Surface((SCREENWIDTH, SCREENHEIGHT))
        pg.display.set_caption(TITLE)
        pg.key.set_repeat(200)  # If we hold it 0.2 sec, it would repeat.
        pg.mouse.set_visible(False)

    def global_init(self):
        self.glo = Global()

    def main(self):
        """The main skeleton of the game process."""
        self.global_init()
        self.pygame_init()

        # loading_menu = LoadingMenu(
        #     self.clock, self.screen, self.display, self.glo)
        # loading_menu.main()
        self.glo.next_scene = ['main_menu', 'press_key']
        while True:
            if self.glo.next_scene[0] == 'main_menu':
                self.detect_has_loaded_archive()
                main_menu = MainMenu(
                    self.clock, self.screen, self.display, self.glo)
                main_menu.main()
            elif self.glo.next_scene[0] == 'settings_menu':
                self.detect_has_loaded_archive()
                settings_menu = SettingsMenu(
                    self.clock, self.screen, self.glo.display, self.glo)
                settings_menu.main()
            elif self.glo.next_scene[0] == 'scene_selection_menu':
                self.detect_has_loaded_archive()
                # Save game automatically when entering the scene selection menu.
                self.auto_save()
                menu = SceneSelectionMenu(
                    self.clock, self.screen, self.display, self.glo)
                menu.main()
            elif self.glo.next_scene[0] == 'cliff':
                # Get ready to play menu bgm.
                self.glo.ready_to_play_menu_bgm = True
                self.detect_has_loaded_archive()
                cliff = Cliff(self.clock, self.screen,
                              self.glo.display, self.glo, 1.5)
                cliff.main()
            elif self.glo.next_scene[0] == 'string_star':
                # Get ready to play menu bgm.
                self.glo.ready_to_play_menu_bgm = True
                self.detect_has_loaded_archive()
                stringstar = StringStar(self.clock, self.screen,
                                        self.glo.display, self.glo, 1.5)
                stringstar.main()
            elif self.glo.next_scene[0] == 'infinite_mode_cliff':
                # Get ready to play menu bgm.
                self.glo.ready_to_play_menu_bgm = True
                self.detect_has_loaded_archive()
                infinite_mode = InfiniteModeCliff(
                    self.clock, self.screen, self.display, self.glo, 1.5)
                infinite_mode.main()

    def auto_save(self):
        """Save the game automatically."""
        archives = load()
        # Overwrite the current archive.
        self.glo.archive.update(self.glo.archive.unlock)
        archives[self.glo.archive_no - 1] = self.glo.archive
        save(archives)

    def detect_has_loaded_archive(self):
        """Detect if it has loaded the archive."""
        scene = self.glo.next_scene[0]
        if scene == 'cliff' or scene == 'string_star' or scene == 'infinite_mode_cliff':
            self.glo.has_loaded_archive = True
        else:
            self.glo.has_loaded_archive = False
