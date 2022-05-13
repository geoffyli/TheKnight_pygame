#!/usr/bin/env python
from pygame.locals import (
    K_w,
    K_s,
    K_d,
    K_a,
    K_k,
    K_f,
    K_j,
    K_l,
    K_RETURN
)


__author__ = 'Geoff Yulong Li'


# FPS
FPS = 60
# caption
TITLE = 'The Knight'
# screen size
SCREENWIDTH = 640
SCREENHEIGHT = 360
# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 128, 255)
AQUA = (50, 206, 223)
ORANGE = (255, 206, 43)
PURPLE = (151, 60, 255)
PAPERYELLOW = (227, 232, 188)
DARKPURPLE = (59, 12, 112)
FIRBALLCOLOR01 = (190, 74, 47)
FIRBALLCOLOR02 = (247, 118, 34)
FIRBALLCOLOR03 = (254, 231, 97)
KNIGHTCOLOR0101 = (58, 68, 102)
KNIGHTCOLOR0102 = (90, 105, 136)
KNIGHTCOLOR0103 = (192, 203, 220)
KNIGHTCOLOR0104 = (18, 78, 137)
KNIGHTCOLOR0201 = (228, 59, 68)
KNIGHTCOLOR0202 = (24, 20, 37)
KNIGHTCOLOR0203 = (139, 155, 180)
KNIGHTCOLOR0204 = (63, 40, 50)
KNIGHTCOLOR0301 = (24, 20, 37)
KNIGHTCOLOR0302 = (38, 43, 68)
KNIGHTCOLOR0303 = (192, 203, 220)
KNIGHTCOLOR0304 = (158, 40, 53)


# sprite sheet
KNIGHT01 = 'gameArts/images/knight01.png'
KNIGHT02 = 'gameArts/images/knight02.png'
KNIGHT03 = 'gameArts/images/knight03.png'
FIGHTER = 'gameArts/images/fighter.png'
FIREBALL = 'gameArts/images/fireball.png'
# player state
RIGHT = 'right'
LEFT = 'left'
FACING_LEFT = 'facing_left'
FACING_RIGHT = 'facing_right'
# previews
CLIFFPREVIEW = 'gameArts/images/cliff_preview.png'
STRINGSTARPREVIEW = 'gameArts/images/string_star_preview.png'
INFINITEMODEPREVIEW = 'gameArts/images/infinite_mode_preview.png'
# maps
CLIFF = 'gameArts/maps/cliff.tmx'
STRINGSTAR = 'gameArts/maps/stringstar.tmx'
INFINITEMODECLIFF = 'gameArts/maps/infinite_mode_cliff.tmx'
# background imgs
MAINMENUWALLPAPER = 'gameArts/images/main_menu_wallpaper.jpg'
ARCHIVEMENUWALLPAPER = 'gameArts/images/archive_menu_wallpaper.jpg'
SETTINGSWALLPAPER = 'gameArts/images/settings_menu_wallpaper.jpg'
SCENESELECTIONWALLPAPER = 'gameArts/images/scene_selection_menu_wallpaper.jpg'
CLIFFBACKGROUND = 'gameArts/images/cliff_background.png'
STRINGSTARBACKGROUND = 'gameArts/images/stringstar_background.png'
CLIFFCLOUDS = 'gameArts/images/cliff_clouds.png'
CLIFFSEA = 'gameArts/images/cliff_sea.png'
CLIFFGROUND = 'gameArts/images/cliff_ground.png'
STRINGSTARBLUECLOUD = 'gameArts/images/stringstar_blue_cloud.png'
STRINGSTARPURPLECLOUD = 'gameArts/images/stringstar_purple_cloud.png'
# fonts
KA1 = 'gameArts/fonts/ka1.ttf'
BACKTO1982 = 'gameArts/fonts/BACKTO1982.TTF'
ARCADE = 'gameArts/fonts/ARCADECLASSIC.TTF'
PIXEL = 'gameArts/fonts/Pixel.ttf'
TICKETING = 'gameArts/fonts/Ticketing.ttf'
# bgm
MAINMENUBGM = 'gameArts/music/bgm/main_menu.wav'
CLIFFBGM = 'gameArts/music/bgm/cliff.wav'
STRINGSTARBGM = 'gameArts/music/bgm/stringstar.wav'
INFINITEMODEBGM = 'gameArts/music/bgm/infinite_mode.wav'
# sounds
CHOOSESOUND = 'gameArts/music/sounds/choose.wav'
CONFIRMSOUND = 'gameArts/music/sounds/confirm.wav'
SLASHSOUND = 'gameArts/music/sounds/slash.wav'
BEHITSOUND = 'gameArts/music/sounds/be_hit.wav'
THROWFIREBALLSOUND = 'gameArts/music/sounds/throw_fire_ball.wav'
EXPLOSIONSOUND = 'gameArts/music/sounds/explosion.wav'
HEALSOUND = 'gameArts/music/sounds/heal.wav'
# volume
sound_volume = 0.5
bgm_volume = 0.5
