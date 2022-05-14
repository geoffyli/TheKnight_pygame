#!/usr/bin/env python
import time
import pickle
from pygame import display


__author__ = 'Geoff Yulong Li'


archive_path = 'archive.txt'


def load():
    with open(archive_path, 'rb') as f:
        data = pickle.load(f)
        f.close()
        return data


def save(data):
    with open(archive_path, 'wb') as f:
        pickle.dump(data, f)
        f.close()


class Archive:
    def __init__(self, unlock) -> None:
        self.date = time.ctime(time.time())
        self.unlock = unlock  # level unlock

    def update(self, unlock):
        self.date = time.ctime(time.time())
        self.unlock = unlock


class Global:

    def __init__(self) -> None:
        self.next_scene = ['loading_menu', None]
        self.archive_no = None
        self.archive = None
        self.has_loaded_archive = False
        # Whether to play main menu music or not.
        self.ready_to_play_menu_bgm = True
        display.init()
        self.full_display_w = display.Info().current_w
        self.full_display_h = display.Info().current_h
        self.display_width = self.full_display_w
        self.display_height = self.full_display_h
        self.display = display.set_mode(
            (self.display_width, self.display_height))

    def update_archive(self, lv, coin):
        if self.archive is not None:
            self.archive.lv = lv
            self.archive.coin = coin

    def get_archive_info(self, no):
        """Get archive information from the archive.txt file."""
        archives = load()
        if no == 1:
            if archives[0] is None:
                return "empty"
            else:
                return archives[0].date[4:20]
        elif no == 2:
            if archives[1] is None:
                return "empty"
            else:
                return archives[1].date[4:20]
        elif no == 3:
            if archives[2] is None:
                return "empty"
            else:
                return archives[2].date[4:20]
