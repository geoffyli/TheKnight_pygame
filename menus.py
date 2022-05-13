#!/usr/bin/env python
import sys
import constants as c
from buttons import *
from globals import load, save, Archive
from copy import deepcopy


__author__ = 'Geoff Yulong Li'


class Menu:
    """This class represents a general menu."""

    def __init__(self, clock, screen, display, glo) -> None:
        self.pressed_keys = None
        self.main_loop_running = True
        self.next_scene = None
        self.clock = clock
        self.screen = screen
        self.display = display
        self.glo = glo

    def new(self):
        """Initialize components of the menu."""
        pass

    def fade_in(self):
        '''Fade in effect.'''
        fade = pg.Surface((c.SCREENWIDTH, c.SCREENHEIGHT))
        fade.fill(c.BLACK)
        for alpha in range(255, 0, -5):
            fade.set_alpha(alpha)  # accumulative
            self.dt = self.clock.tick(c.FPS) / 1000
            self.event_loop()
            # Update
            self.update()
            # Draw components
            self.fade_draw(fade)
            # Update the screen.
            pg.display.update()

    def fade_out(self):
        """fade out effect"""
        fade = pg.Surface((c.SCREENWIDTH, c.SCREENHEIGHT))
        fade.fill(c.BLACK)
        for alpha in range(0, 255, 5):
            fade.set_alpha(alpha)  # accumulative
            self.dt = self.clock.tick(c.FPS) / 1000
            self.event_loop()
            # Update
            self.update()
            # Draw components
            self.fade_draw(fade)
            # Update the screen.
            pg.display.update()

    def go_to(self):
        """Stop the main loop and set the global variable next_scene."""
        self.main_loop_running = False
        self.glo.next_scene = self.next_scene

    def update(self):
        """Update all components of the menu."""
        pass

    def fade_draw(self, fade):
        # Draw black surf.
        self.screen.blit(fade, (0, 0))
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), (0, 0))

    def draw(self):
        """Draw all components of the menu."""
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), (0, 0))

    def event_loop(self):
        """Set the event loop of the menu."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def main_loop(self):
        """the main loop of the menu"""
        while self.main_loop_running:
            self.dt = self.clock.tick(c.FPS) / 1000
            # event loop
            self.event_loop()
            # update items
            self.update()
            # draw items
            self.draw()
            # update screen
            pg.display.update()
            # go to
            if self.next_scene is not None:
                self.go_to()

    def main(self):
        self.new()
        self.fade_in()
        self.main_loop()
        self.fade_out()


class LoadingMenu(Menu):
    def __init__(self, clock, screen, display, glo) -> None:
        super().__init__(clock, screen, display, glo)
        self.timer_interval = 500
        self.counter = 5

    def new(self):
        """Initialize components of the menu."""
        self.demo_font = pg.font.Font(c.KA1, 40)
        self.author_text = self.demo_font.render(
            "AUTHOR_YULONG LI", True, (255, 255, 255))
        self.author_text_rect = self.author_text.get_rect(
            center=(c.SCREENWIDTH / 2, c.SCREENHEIGHT / 2))
        self.timer_event = pg.USEREVENT + 1
        pg.time.set_timer(self.timer_event, self.timer_interval)

    def event_loop(self):
        """Set the event loop of the menu."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == self.timer_event:
                self.counter -= 1
                if self.counter == 0:
                    # Exit the loading menu.
                    self.next_scene = ['main_menu', 'press_key']

    def draw(self):
        """Draw all components of the menu."""
        self.screen.fill(c.BLACK)
        self.screen.blit(self.author_text, self.author_text_rect)
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), (0, 0))

    def fade_draw(self, fade):
        # Draw black surf.
        self.screen.fill(c.BLACK)
        self.screen.blit(self.author_text, self.author_text_rect)
        self.screen.blit(fade, (0, 0))
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), (0, 0))


class MainMenu(Menu):
    """2 Phases: not_enter: ['main_menu', 'press_key'], enter: ['main_menu']
       Called by loading menu or settings."""

    def __init__(self, clock, screen, display, glo) -> None:
        super().__init__(clock, screen, display, glo)
        self.winkle_interval = 500
        self.load_component_interval = 100
        if self.glo.next_scene[1] == 'press_key':
            self.enter = False
        elif self.glo.next_scene[1] == 'main':
            self.enter = True
        self.chosen_button = 0
        # out of game

    def new(self):
        self.activite_components = []  # a boolean list
        self.all_sprites = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        # Add wallpaper.
        self.wall_paper = pg.transform.scale(
            pg.image.load(c.MAINMENUWALLPAPER), (c.SCREENWIDTH, c.SCREENHEIGHT))
        # Add enter font.
        self.enter_font = pg.font.Font(c.KA1, 20)
        self.enter_text = self.enter_font.render(
            "Press Any Key", True, (255, 255, 255))
        self.enter_rect = self.enter_text.get_rect(
            center=(c.SCREENWIDTH / 2, c.SCREENHEIGHT * 4 / 5))
        # Define customed events.
        self.winkle_event = pg.USEREVENT + 2
        pg.time.set_timer(self.winkle_event, self.winkle_interval)
        self.load_component_event = pg.USEREVENT + 3
        pg.time.set_timer(self.load_component_event,
                          self.load_component_interval)
        # Add components.
        Text(self, self.screen, 'The', c.KA1, 60, c.BLUE, (
            c.SCREENWIDTH / 2, -c.SCREENHEIGHT / 4), (c.SCREENWIDTH / 2, c.SCREENHEIGHT / 5))
        Text(self, self.screen, 'Knight', c.KA1, 60, c.BLUE, (
            c.SCREENWIDTH / 2, -c.SCREENHEIGHT / 4), (c.SCREENWIDTH / 2, c.SCREENHEIGHT * 2 / 5))
        Button(self, self.screen, 'Load Game', self.load_game, c.ARCADE, 20, (
            c.SCREENWIDTH / 5, c.SCREENHEIGHT / 15), (-c.SCREENWIDTH / 4, c.SCREENHEIGHT / 5), (c.SCREENWIDTH / 8, c.SCREENHEIGHT / 5))
        Button(self, self.screen, 'New Game', self.new_game, c.ARCADE, 20, (
            c.SCREENWIDTH / 5, c.SCREENHEIGHT / 15), (-c.SCREENWIDTH / 4, c.SCREENHEIGHT * 2 / 5), (c.SCREENWIDTH / 8, c.SCREENHEIGHT * 2 / 5))
        Button(self, self.screen, 'Settings', self.set_game, c.ARCADE, 20, (
            c.SCREENWIDTH / 5, c.SCREENHEIGHT / 15), (-c.SCREENWIDTH / 4, c.SCREENHEIGHT * 3 / 5), (c.SCREENWIDTH / 8, c.SCREENHEIGHT * 3 / 5))
        Button(self, self.screen, 'Quit', self.quit, c.ARCADE, 20, (
            c.SCREENWIDTH / 5, c.SCREENHEIGHT / 15), (-c.SCREENWIDTH / 4, c.SCREENHEIGHT * 4 / 5), (c.SCREENWIDTH / 8, c.SCREENHEIGHT * 4 / 5))
        # Set the activite_components list.
        for i in range(0, len(self.all_sprites)):
            if i == 0:
                self.activite_components.append(True)
            else:
                self.activite_components.append(False)
        # Set chosen button.
        self.buttons.sprites()[self.chosen_button].chosen = True
        # Set bgm and sounds
        if self.glo.ready_to_play_menu_bgm:
            pg.mixer.music.load(c.MAINMENUBGM)
            pg.mixer.music.set_volume(c.bgm_volume)
        self.choose_sound = pg.mixer.Sound(c.CHOOSESOUND)
        self.choose_sound.set_volume(c.sound_volume)

    def load_game(self):
        """Get archive menu with load mode.
           If user choose an entry, the main menu will stop running, the next scene is chosen in archive menu."""
        load_menu = ArchiveMenu(self.clock, self.screen,
                                self.display, 'load', self.glo)
        next_scene = load_menu.main()
        if next_scene is not None:
            self.next_scene = next_scene

    def new_game(self):
        """Get archive menu with new (archives) mode.
           If user choose an entry, the main menu will stop running, the next scene is chosen in archive menu."""
        new_menu = ArchiveMenu(self.clock, self.screen,
                               self.display, 'new', self.glo)
        next_scene = new_menu.main()
        if next_scene is not None:
            self.next_scene = next_scene

    def set_game(self):
        """Get the settings menu."""
        self.next_scene = ['settings_menu', None]

    def quit(self):
        """Quit game."""
        pg.quit()
        sys.exit()

    def event_loop(self):
        """Set the event loop of the menu."""
        for event in pg.event.get():
            # Quit game.
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                # Query
                sb = SelectionBox(self.clock, self.screen, self.display,
                                  'Quit game?', c.PIXEL, 30, self.glo)
                if sb.main():
                    self.quit()
            # not enter
            if not self.enter:
                # winkle effect
                if event.type == self.winkle_event:
                    if self.enter_text.get_alpha() == 0:
                        self.enter_text.set_alpha(255)
                    else:
                        self.enter_text.set_alpha(0)
                # Display the main menu.
                elif event.type == pg.KEYDOWN:
                    self.enter = True
            # enter
            elif self.enter:
                # Load components.
                if event.type == self.load_component_event:
                    for i in range(0, len(self.activite_components)):
                        if not self.activite_components[i]:
                            self.activite_components[i] = True
                            break
                # Choose button according to the key.
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w or event.key == pg.K_UP:
                        # Play choose sound.
                        self.choose_sound.play(maxtime=1000)
                        self.buttons.sprites()[
                            self.chosen_button].chosen = False
                        self.chosen_button = (
                            self.chosen_button - 1) % len(self.buttons)
                        self.buttons.sprites()[
                            self.chosen_button].chosen = True
                    if event.key == pg.K_s or event.key == pg.K_DOWN:
                        # Play choose sound.
                        self.choose_sound.play(maxtime=1000)
                        self.buttons.sprites()[
                            self.chosen_button].chosen = False
                        self.chosen_button = (
                            self.chosen_button + 1) % len(self.buttons)
                        self.buttons.sprites()[
                            self.chosen_button].chosen = True
                if self.glo.ready_to_play_menu_bgm:
                    # Play bgm
                    pg.mixer.music.play(loops=-1, fade_ms=1000)
                    self.glo.ready_to_play_menu_bgm = False

    def draw(self):
        self.screen.blit(self.wall_paper, (0, 0))
        if not self.enter:
            self.screen.blit(self.enter_text, self.enter_rect)
        else:
            for sprite in self.all_sprites:
                sprite.draw()
        # Avoid screen flickering.
        if self.next_scene is not None and self.next_scene[0] == 'scene_selection_menu':
            # Draw screen black.
            pg.draw.rect(self.screen, c.BLACK, self.screen.get_rect())
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), (0, 0))

    def update(self):
        if self.enter:
            # Update all components.
            for i in range(0, len(self.all_sprites)):
                if self.activite_components[i]:
                    self.all_sprites.sprites()[i].update()

    def fade_draw(self, fade):
        """Draw components while fading in."""
        self.screen.blit(self.wall_paper, (0, 0))
        if not self.enter:
            self.screen.blit(self.enter_text, self.enter_rect)
        else:
            for sprite in self.all_sprites:
                sprite.draw()
        # Draw black surf.
        self.screen.blit(fade, (0, 0))
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), (0, 0))

    def main(self):
        self.new()
        self.fade_in()
        self.main_loop()


class ArchiveMenu(Menu):
    """Archive menu is built on another menu or scene.(ArchiveMenu can be called in other menus or scenes only.)
       4 modes(new, save, load, delete) should be specified when creating the instance of ArchiveMenu class.
       Creating or loading an new archive will change the current scene or menu to the game birthplace(home_level_2),
            while deleting or saving or doing nothing won't.
       """

    def __init__(self, clock, screen, display, mode, glo) -> None:
        super().__init__(clock, screen, display, glo)
        self.chosen_button = 0
        self.mode = mode
        # Set it true when loading or creating an archive.
        self.quit_scene = False

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        # Add wallpaper.
        self.wall_paper = pg.transform.scale(
            pg.image.load(c.ARCHIVEMENUWALLPAPER), (c.SCREENWIDTH, c.SCREENHEIGHT))
        # Get button text and tip text.
        if self.mode == 'load':
            button_func = [self.load_01, self.load_02, self.load_03]
            tip_text = 'load game'.center(15, '-')
        elif self.mode == 'new':
            button_func = [self.new_01, self.new_02, self.new_03]
            tip_text = 'new game'.center(15, '-')
        elif self.mode == 'delete':
            button_func = [self.del_01, self.del_02, self.del_03]
            tip_text = 'delete game'.center(15, '-')
        elif self.mode == 'save':
            button_func = [self.save_01, self.save_02, self.save_03]
            tip_text = 'save game'.center(15, '-')
        # Add Tip text
        Text(self, self.screen, tip_text, c.PIXEL, 40, c.DARKGREY, (c.SCREENWIDTH /
             5.8, -2 * c.SCREENHEIGHT), (c.SCREENWIDTH / 5.8, c.SCREENHEIGHT / 15))
        # Add archive buttons.
        self.archive_buttons = []
        self.archive_buttons.append(Button(self, self.screen, self.glo.get_archive_info(1), button_func[0], c.PIXEL,
                                           30, (c.SCREENWIDTH * 2 / 3, c.SCREENHEIGHT / 5), (c.SCREENWIDTH / 6, -2 * c.SCREENHEIGHT), (c.SCREENWIDTH / 6, c.SCREENHEIGHT / 4)))
        self.archive_buttons.append(Button(self, self.screen, self.glo.get_archive_info(2), button_func[1], c.PIXEL,
                                           30, (c.SCREENWIDTH * 2 / 3, c.SCREENHEIGHT / 5), (c.SCREENWIDTH / 6, -2 * c.SCREENHEIGHT), (c.SCREENWIDTH / 6, c.SCREENHEIGHT / 2)))
        self.archive_buttons.append(Button(self, self.screen, self.glo.get_archive_info(3), button_func[2], c.PIXEL,
                                           30, (c.SCREENWIDTH * 2 / 3, c.SCREENHEIGHT / 5), (c.SCREENWIDTH / 6, -2 * c.SCREENHEIGHT), (c.SCREENWIDTH / 6, c.SCREENHEIGHT * 3 / 4)))
        # Add back button.
        Button(self, self.screen, "Back", self.back, c.ARCADE, 20, (c.SCREENWIDTH / 12, c.SCREENHEIGHT / 10),
               (c.SCREENWIDTH * 21 / 24, -2 * c.SCREENHEIGHT), (c.SCREENWIDTH * 21 / 24, c.SCREENHEIGHT * 17 / 20))

        # Set chosen button.
        self.buttons.sprites()[self.chosen_button].chosen = True
        # Set bgm and sounds
        self.choose_sound = pg.mixer.Sound(c.CHOOSESOUND)
        self.choose_sound.set_volume(c.sound_volume)
        self.confirm_sound = pg.mixer.Sound(c.CONFIRMSOUND)
        self.confirm_sound.set_volume(c.sound_volume)
        # Fade in effect
        self.screen_pos = (0, 0)
        self.screen_rect = self.screen.get_rect(
            topleft=(0, -1.5 * c.SCREENHEIGHT))
        self.initial_screen_pos = [self.screen_rect.x, self.screen_rect.y]

    def load_archive(self, i):
        archive = load()[i - 1]
        if archive is not None:
            self.next_scene = ['scene_selection_menu', None]
            self.quit_scene = True
            self.glo.archive = deepcopy(archive)
            self.glo.archive_no = i

    def delete_archive(self, i):
        if load()[i - 1] is not None:
            sb = SelectionBox(self.clock, self.screen, self.display,
                              'Delete?', c.PIXEL, 30, self.glo)
            if sb.main():
                # Delete archive.
                archives = load()
                archives[i - 1] = None
                save(archives)
                # Update text
                self.archive_buttons[i - 1].update_text('empty')

    def save_archive(self, i):
        archives = load()
        if archives[i - 1] is None:
            # Update archive time
            self.glo.archive.update(self.glo.archive.unlock)
            archives[i - 1] = self.glo.archive
            save(archives)
            self.archive_buttons[i - 1].update_text(
                self.glo.get_archive_info(i))
        else:
            sb = SelectionBox(self.clock, self.screen, self.display,
                              'Overwrite?', c.PIXEL, 30, self.glo)
            if sb.main():
                # Overwrite.
                # Update archive time
                self.glo.archive.update(self.glo.archive.unlock)
                archives[i - 1] = self.glo.archive
                save(archives)
                self.archive_buttons[i - 1].update_text(
                    self.glo.get_archive_info(i))

    def new_archive(self, i):
        archives = load()
        if archives[i - 1] is None:
            self.glo.archive = Archive([True, False, False])
            self.glo.archive_no = i
            archives[i - 1] = self.glo.archive
            save(archives)
            self.archive_buttons[i - 1].update_text(
                self.glo.get_archive_info(i))
            self.next_scene = ['scene_selection_menu', None]
            self.quit_scene = True
        else:
            sb = SelectionBox(self.clock, self.screen, self.display,
                              'Overwrite?', c.PIXEL, 30, self.glo)
            if sb.main():
                # Overwrite.
                self.glo.archive = Archive([True, False, False])
                self.glo.archive_no = i
                archives[i - 1] = self.glo.archive
                save(archives)
                self.archive_buttons[i - 1].update_text(
                    self.glo.get_archive_info(i))
                self.next_scene = ['scene_selection_menu', None]
                self.quit_scene = True

    def load_01(self):
        self.load_archive(1)

    def load_02(self):
        self.load_archive(2)

    def load_03(self):
        self.load_archive(3)

    def del_01(self):
        self.delete_archive(1)

    def del_02(self):
        self.delete_archive(2)

    def del_03(self):
        self.delete_archive(3)

    def save_01(self):
        self.save_archive(1)

    def save_02(self):
        self.save_archive(2)

    def save_03(self):
        self.save_archive(3)

    def new_01(self):
        self.new_archive(1)

    def new_02(self):
        self.new_archive(2)

    def new_03(self):
        self.new_archive(3)

    def back(self):
        self.next_scene = [None, None]

    def event_loop(self):
        """Set the event loop of the menu."""
        for event in pg.event.get():
            # Quit game.
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Choose button according to the key.
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w or event.key == pg.K_UP:
                    self.choose_sound.play(maxtime=1000)  # Play choose sound.
                    self.buttons.sprites()[self.chosen_button].chosen = False
                    self.chosen_button = (
                        self.chosen_button - 1) % len(self.buttons)
                    self.buttons.sprites()[self.chosen_button].chosen = True
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    self.choose_sound.play(maxtime=1000)  # Play choose sound.
                    self.buttons.sprites()[self.chosen_button].chosen = False
                    self.chosen_button = (
                        self.chosen_button + 1) % len(self.buttons)
                    self.buttons.sprites()[self.chosen_button].chosen = True
                if event.key == pg.K_ESCAPE or event.key == pg.K_BACKSPACE:
                    self.confirm_sound.play(maxtime=1000)
                    self.back()

    def draw(self):
        """Draw all components."""
        self.screen.blit(self.wall_paper, (0, 0))
        for sprite in self.all_sprites:
            sprite.draw()
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), self.screen_rect)

    def update(self):
        # Update the pos of the screen rect.
        self.initial_screen_pos[0] += (self.screen_pos[0] -
                                       self.initial_screen_pos[0]) / 20
        self.initial_screen_pos[1] += (self.screen_pos[1] -
                                       self.initial_screen_pos[1]) / 20
        self.screen_rect.x = self.initial_screen_pos[0]
        self.screen_rect.y = self.initial_screen_pos[1]
        # Update all sprites.
        self.all_sprites.update()

    def change_scene(self):
        if self.quit_scene:
            return self.next_scene
        else:
            return None

    def main(self):
        self.new()
        self.main_loop()
        # Quit current menu or scene.
        return self.change_scene()


class SettingsMenu(Menu):
    """A menu for settings. It can be called by main menu and scenes."""

    def __init__(self, clock, screen, display, glo) -> None:
        super().__init__(clock, screen, display, glo)
        self.load_component_interval = 100
        self.initial_chosen_button = 0
        self.volume_chosen_button = 0
        self.resolution_chosen_button = 0
        self.archive_chosen_button = 0
        self.submenu_boolean = {'keyboard': False,
                                'volume': False, 'archive': False, 'resolution': False}
        self.quit_scene = False  # Whether to quit current scene or not.

    def new(self):
        # a boolean list for the initial components animation.
        self.activite_components = []
        # Create groups.
        self.initial_group = pg.sprite.Group()
        self.initial_buttons_group = pg.sprite.Group()
        self.keyboard_group = pg.sprite.Group()
        self.volume_group = pg.sprite.Group()
        self.volume_buttons_group = pg.sprite.Group()
        self.resolution_group = pg.sprite.Group()
        self.resolution_buttons_group = pg.sprite.Group()
        self.archive_group = pg.sprite.Group()
        self.archive_buttons_group = pg.sprite.Group()
        # Add wallpaper and its cover.
        self.wall_paper = pg.transform.scale(
            pg.image.load(c.SETTINGSWALLPAPER), (c.SCREENWIDTH, c.SCREENHEIGHT))
        self.wall_paper_cover = pg.Surface((c.SCREENWIDTH, c.SCREENHEIGHT))
        self.wall_paper_cover.set_alpha(125)
        # Define the customed event.
        self.load_component_event = pg.USEREVENT + 4
        pg.time.set_timer(self.load_component_event,
                          self.load_component_interval)
        # Add initial sprites.
        Text(self, self.screen, 'SETTINGS', c.KA1, 40, c.WHITE, (
            -c.SCREENWIDTH / 4, c.SCREENHEIGHT / 25), (c.SCREENWIDTH / 16, c.SCREENHEIGHT / 25), self.initial_group)
        CustomedSurface(self, self.screen,
                        (c.SCREENWIDTH / 2, c.SCREENHEIGHT * 2 / 3), c.DARKPURPLE, (c.SCREENWIDTH * 2 / 5, -2 * c.SCREENHEIGHT), (c.SCREENWIDTH * 2 / 5, c.SCREENHEIGHT / 5), self.initial_group)
        Button(self, self.screen, 'keyboard', self.show_keyboard, c.ARCADE, 20, (
            c.SCREENWIDTH / 5, c.SCREENHEIGHT / 15), (-c.SCREENWIDTH / 4, c.SCREENHEIGHT / 5), (c.SCREENWIDTH / 8, c.SCREENHEIGHT / 5), self.initial_group, self.initial_buttons_group)
        Button(self, self.screen, 'volumn', self.show_volume, c.ARCADE, 20, (
            c.SCREENWIDTH / 5, c.SCREENHEIGHT / 15), (-c.SCREENWIDTH / 4, c.SCREENHEIGHT * 19 / 60), (c.SCREENWIDTH / 8, c.SCREENHEIGHT * 19 / 60), self.initial_group, self.initial_buttons_group)
        Button(self, self.screen, 'resolution', self.show_resolution, c.ARCADE, 20, (
            c.SCREENWIDTH / 5, c.SCREENHEIGHT / 15), (-c.SCREENWIDTH / 4, c.SCREENHEIGHT * 26 / 60), (c.SCREENWIDTH / 8, c.SCREENHEIGHT * 26 / 60), self.initial_group, self.initial_buttons_group)
        Button(self, self.screen, 'archive', self.show_archive, c.ARCADE, 20, (
            c.SCREENWIDTH / 5, c.SCREENHEIGHT / 15), (-c.SCREENWIDTH / 4, c.SCREENHEIGHT * 33 / 60), (c.SCREENWIDTH / 8, c.SCREENHEIGHT * 33 / 60), self.initial_group, self.initial_buttons_group)
        Button(self, self.screen, 'back', self.back, c.ARCADE, 20, (
            c.SCREENWIDTH / 5, c.SCREENHEIGHT / 15), (-c.SCREENWIDTH / 4, c.SCREENHEIGHT * 40 / 60), (c.SCREENWIDTH / 8, c.SCREENHEIGHT * 40 / 60), self.initial_group, self.initial_buttons_group)
        Button(self, self.screen, 'main menu', self.back_to_main_menu, c.ARCADE, 20, (
            c.SCREENWIDTH / 5, c.SCREENHEIGHT / 15), (-c.SCREENWIDTH / 4, c.SCREENHEIGHT * 47 / 60), (c.SCREENWIDTH / 8, c.SCREENHEIGHT * 47 / 60), self.initial_group, self.initial_buttons_group)
        # Add keyboard group sprites.
        Text(self, self.screen, 'keboard', c.PIXEL, 40, c.WHITE, (c.SCREENWIDTH / 2,
             c.SCREENHEIGHT / 4), (c.SCREENWIDTH / 2, c.SCREENHEIGHT / 4), self.keyboard_group)
        Text(self, self.screen, 'move: w, a, s, d', c.TICKETING, 40, c.WHITE, (c.SCREENWIDTH * 17 / 40,
             c.SCREENHEIGHT * 7 / 18), (c.SCREENWIDTH * 17 / 40, c.SCREENHEIGHT * 7 / 18), self.keyboard_group)
        Text(self, self.screen, 'interact: e', c.TICKETING, 40, c.WHITE, (c.SCREENWIDTH * 17 / 40,
             c.SCREENHEIGHT * 9 / 18), (c.SCREENWIDTH * 17 / 40, c.SCREENHEIGHT * 9 / 18), self.keyboard_group)
        Text(self, self.screen, 'jump: k', c.TICKETING, 40, c.WHITE, (c.SCREENWIDTH * 17 / 40,
             c.SCREENHEIGHT * 11 / 18), (c.SCREENWIDTH * 17 / 40, c.SCREENHEIGHT * 11 / 18), self.keyboard_group)
        Text(self, self.screen, 'attack: j & l', c.TICKETING, 40, c.WHITE, (c.SCREENWIDTH * 17 / 40,
             c.SCREENHEIGHT * 13 / 18), (c.SCREENWIDTH * 17 / 40, c.SCREENHEIGHT * 13 / 18), self.keyboard_group)
        # Add volume group sprites.
        Text(self, self.screen, 'volume', c.PIXEL, 40, c.WHITE, (c.SCREENWIDTH * 21 / 40,
                                                                 c.SCREENHEIGHT / 4), (c.SCREENWIDTH * 21 / 40, c.SCREENHEIGHT / 4), self.volume_group)
        Text(self, self.screen, 'BGM: ', c.TICKETING, 40, c.WHITE, (c.SCREENWIDTH * 17 / 40,
             c.SCREENHEIGHT * 8 / 18), (c.SCREENWIDTH * 17 / 40, c.SCREENHEIGHT * 8 / 18), self.volume_group)
        Text(self, self.screen, 'effect: ', c.TICKETING, 40, c.WHITE, (c.SCREENWIDTH * 17 / 40,
             c.SCREENHEIGHT * 10 / 18), (c.SCREENWIDTH * 17 / 40, c.SCREENHEIGHT * 10 / 18), self.volume_group)
        self.dynamic_text01 = Text(self, self.screen, '{0:2}'.format(str(round(c.bgm_volume * 10))), c.TICKETING, 40, c.WHITE, (c.SCREENWIDTH * 19 / 30,
                                                                                                                                c.SCREENHEIGHT * 8 / 18), (c.SCREENWIDTH * 19 / 30, c.SCREENHEIGHT * 8 / 18), self.volume_group)
        self.dynamic_text02 = Text(self, self.screen, '{0:2}'.format(str(round(c.sound_volume * 10))), c.TICKETING, 40, c.WHITE, (c.SCREENWIDTH * 19 / 30,
                                                                                                                                  c.SCREENHEIGHT * 10 / 18), (c.SCREENWIDTH * 19 / 30, c.SCREENHEIGHT * 10 / 18), self.volume_group)
        Button(self, self.screen, '<', self.turn_down_bgm, c.TICKETING, 40, (c.SCREENWIDTH / 15, c.SCREENHEIGHT / 10), (c.SCREENWIDTH *
               22 / 30, c.SCREENHEIGHT * 15 / 36), (c.SCREENWIDTH * 22 / 30, c.SCREENHEIGHT * 15 / 36), self.volume_group, self.volume_buttons_group)
        Button(self, self.screen, '>', self.turn_up_bgm, c.TICKETING, 40, (c.SCREENWIDTH / 15, c.SCREENHEIGHT / 10), (c.SCREENWIDTH *
               49 / 60, c.SCREENHEIGHT * 15 / 36), (c.SCREENWIDTH * 49 / 60, c.SCREENHEIGHT * 15 / 36), self.volume_group, self.volume_buttons_group)
        Button(self, self.screen, '<', self.turn_down_effect, c.TICKETING, 40, (c.SCREENWIDTH / 15, c.SCREENHEIGHT / 10), (c.SCREENWIDTH *
               22 / 30, c.SCREENHEIGHT * 20 / 36), (c.SCREENWIDTH * 22 / 30, c.SCREENHEIGHT * 20 / 36), self.volume_group, self.volume_buttons_group)
        Button(self, self.screen, '>', self.turn_up_effect, c.TICKETING, 40, (c.SCREENWIDTH / 15, c.SCREENHEIGHT / 10), (c.SCREENWIDTH *
               49 / 60, c.SCREENHEIGHT * 20 / 36), (c.SCREENWIDTH * 49 / 60, c.SCREENHEIGHT * 20 / 36), self.volume_group, self.volume_buttons_group)
        # Add resolution group sprites.
        Button(self, self.screen, 'FULL', self.set_full_screen, c.TICKETING, 40, (c.SCREENWIDTH / 4, c.SCREENHEIGHT / 10), (c.SCREENWIDTH *
               21 / 40, c.SCREENHEIGHT * 19 / 75), (c.SCREENWIDTH * 21 / 40, c.SCREENHEIGHT * 19 / 75), self.resolution_group, self.resolution_buttons_group)
        Button(self, self.screen, '640x360', self.set_640x360, c.TICKETING, 40, (c.SCREENWIDTH / 4, c.SCREENHEIGHT / 10), (c.SCREENWIDTH *
               21 / 40, c.SCREENHEIGHT * 30 / 75), (c.SCREENWIDTH * 21 / 40, c.SCREENHEIGHT * 30 / 75), self.resolution_group, self.resolution_buttons_group)
        Button(self, self.screen, '800x450', self.set_800x450, c.TICKETING, 40, (c.SCREENWIDTH / 4, c.SCREENHEIGHT / 10), (c.SCREENWIDTH *
               21 / 40, c.SCREENHEIGHT * 41 / 75), (c.SCREENWIDTH * 21 / 40, c.SCREENHEIGHT * 41 / 75), self.resolution_group, self.resolution_buttons_group)
        Button(self, self.screen, '1280x720', self.set_1280x720, c.TICKETING, 40, (c.SCREENWIDTH / 4, c.SCREENHEIGHT / 10), (c.SCREENWIDTH *
               21 / 40, c.SCREENHEIGHT * 52 / 75), (c.SCREENWIDTH * 21 / 40, c.SCREENHEIGHT * 52 / 75), self.resolution_group, self.resolution_buttons_group)
        # Add archive group sprites.
        Button(self, self.screen, 'save', self.save_archive, c.TICKETING, 40, (c.SCREENWIDTH / 4, c.SCREENHEIGHT / 10), (c.SCREENWIDTH *
               21 / 40, c.SCREENHEIGHT * 19 / 75), (c.SCREENWIDTH * 21 / 40, c.SCREENHEIGHT * 19 / 75), self.archive_group, self.archive_buttons_group)
        Button(self, self.screen, 'load', self.load_archive, c.TICKETING, 40, (c.SCREENWIDTH / 4, c.SCREENHEIGHT / 10), (c.SCREENWIDTH *
               21 / 40, c.SCREENHEIGHT * 30 / 75), (c.SCREENWIDTH * 21 / 40, c.SCREENHEIGHT * 30 / 75), self.archive_group, self.archive_buttons_group)
        Button(self, self.screen, 'new', self.new_archive, c.TICKETING, 40, (c.SCREENWIDTH / 4, c.SCREENHEIGHT / 10), (c.SCREENWIDTH *
               21 / 40, c.SCREENHEIGHT * 41 / 75), (c.SCREENWIDTH * 21 / 40, c.SCREENHEIGHT * 41 / 75), self.archive_group, self.archive_buttons_group)
        Button(self, self.screen, 'delete', self.del_archive, c.TICKETING, 40, (c.SCREENWIDTH / 4, c.SCREENHEIGHT / 10), (c.SCREENWIDTH *
               21 / 40, c.SCREENHEIGHT * 52 / 75), (c.SCREENWIDTH * 21 / 40, c.SCREENHEIGHT * 52 / 75), self.archive_group, self.archive_buttons_group)

        # Set activite_componenets list.
        for i in range(0, len(self.initial_group)):
            if i == 0:
                self.activite_components.append(True)
            else:
                self.activite_components.append(False)
        # Set chosen button.
        self.initial_buttons_group.sprites(
        )[self.initial_chosen_button].chosen = True
        self.volume_buttons_group.sprites(
        )[self.volume_chosen_button].chosen = True
        self.resolution_buttons_group.sprites(
        )[self.resolution_chosen_button].chosen = True
        self.archive_buttons_group.sprites(
        )[self.archive_chosen_button].chosen = True
        # Set bgm and sounds
        self.choose_sound = pg.mixer.Sound(c.CHOOSESOUND)
        self.confirm_sound = pg.mixer.Sound(c.CONFIRMSOUND)
        self.choose_sound.set_volume(c.sound_volume)
        self.confirm_sound.set_volume(c.sound_volume)
        # Fade in effect
        self.screen_pos = (0, 0)
        self.screen_rect = self.screen.get_rect(
            topleft=(0, -c.SCREENHEIGHT))
        self.initial_screen_pos = [self.screen_rect.x, self.screen_rect.y]

    def set_full_screen(self):
        self.glo.display_width = self.glo.full_display_w
        self.glo.display_height = self.glo.full_display_h
        self.glo.display = pg.display.set_mode(
            (self.glo.display_width, self.glo.display_height), pg.FULLSCREEN)
        self.next_scene = ['settings_menu']

    def set_640x360(self):
        self.glo.display_width = 640
        self.glo.display_height = 360
        self.glo.display = pg.display.set_mode(
            (self.glo.display_width, self.glo.display_height))
        self.next_scene = ['settings_menu']

    def set_800x450(self):
        self.glo.display_width = 800
        self.glo.display_height = 450
        self.glo.display = pg.display.set_mode(
            (self.glo.display_width, self.glo.display_height))
        self.next_scene = ['settings_menu']

    def set_1280x720(self):
        self.glo.display_width = 1280
        self.glo.display_height = 720
        self.glo.display = pg.display.set_mode(
            (self.glo.display_width, self.glo.display_height))
        self.next_scene = ['settings_menu']

    def show_submenu(self, submenu):
        for key in self.submenu_boolean.keys():
            if key == submenu:
                self.submenu_boolean[key] = True
            else:
                self.submenu_boolean[key] = False

    def show_keyboard(self):
        self.show_submenu('keyboard')

    def show_volume(self):
        self.show_submenu('volume')

    def show_resolution(self):
        self.show_submenu('resolution')

    def show_archive(self):
        self.show_submenu('archive')

    def del_archive(self):
        archive = ArchiveMenu(
            self.clock, self.screen, self.display, 'delete', self.glo)
        archive.main()

    def load_archive(self):
        archive = ArchiveMenu(
            self.clock, self.screen, self.display, 'load', self.glo)
        next_scene = archive.main()
        if next_scene is not None:
            # Quit the current game scene.
            self.quit_scene = True
            self.next_scene = next_scene

    def new_archive(self):
        archive = ArchiveMenu(
            self.clock, self.screen, self.display, 'new', self.glo)
        next_scene = archive.main()
        if next_scene is not None:
            # Quit the current game scene.
            self.quit_scene = True
            self.next_scene = next_scene

    def save_archive(self):
        # In game
        if self.glo.has_loaded_archive:
            archive = ArchiveMenu(
                self.clock, self.screen, self.display, 'save', self.glo)
            archive.main()
        # In menu
        else:
            mb = MessageBox(self.clock, self.screen, self.display,
                            'Not in game.',  c.PIXEL, 30, self.glo)
            mb.main()

    def back(self):
        self.next_scene = ['main_menu', 'main']

    def back_to_main_menu(self):
        self.next_scene = ['main_menu', 'main']
        self.quit_scene = True

    # inappropriate code here
    def turn_up_bgm(self):
        if c.bgm_volume < 0.9:
            c.bgm_volume += 0.1

    def turn_down_bgm(self):
        if c.bgm_volume > 0.1:
            c.bgm_volume -= 0.1

    def turn_up_effect(self):
        if c.sound_volume < 0.9:
            c.sound_volume += 0.1

    def turn_down_effect(self):
        if c.sound_volume > 0.1:
            c.sound_volume -= 0.1

    def event_loop(self):
        """Set the event loop of the menu."""

        def change_active_button(group, index, step):
            """Change the chosen button.
                    group: The target button group
                    index: current chosen button index
                    step: the length of offset"""
            group.sprites()[index].chosen = False
            index = (index + step) % len(group)
            group.sprites()[index].chosen = True
            return index

        for event in pg.event.get():
            # Quit game.
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Load components.
            if event.type == self.load_component_event:
                for i in range(0, len(self.activite_components)):
                    if not self.activite_components[i]:
                        self.activite_components[i] = True
                        break
            # Choose button according to the key.
            if event.type == pg.KEYDOWN:
                # main menu of settings menu.
                if all(_ == False for _ in self.submenu_boolean.values()):
                    # Back to the main menu.
                    if (event.key == pg.K_ESCAPE or event.key == pg.K_BACKSPACE):
                        self.confirm_sound.play(maxtime=1000)
                        self.back()
                    # Select button in main setting menu.
                    if (event.key == pg.K_w or event.key == pg.K_UP):
                        # Play choose sound.
                        self.choose_sound.play(maxtime=1000)
                        self.initial_chosen_button = change_active_button(
                            self.initial_buttons_group, self.initial_chosen_button, -1)
                    if (event.key == pg.K_s or event.key == pg.K_DOWN):
                        # Play choose sound.
                        self.choose_sound.play(maxtime=1000)
                        self.initial_chosen_button = change_active_button(
                            self.initial_buttons_group, self.initial_chosen_button, 1)
                # submenu of settings menu
                if not(all(_ == False for _ in self.submenu_boolean.values())):
                    # Back to the main menu of the settings menu.
                    if (event.key == pg.K_ESCAPE or event.key == pg.K_BACKSPACE):
                        self.confirm_sound.play(maxtime=1000)
                        for key in self.submenu_boolean.keys():
                            self.submenu_boolean[key] = False
                # volume submenu
                if self.submenu_boolean['volume']:
                    if (event.key == pg.K_w or event.key == pg.K_UP):
                        # Play choose sound.
                        self.choose_sound.play(maxtime=1000)
                        self.volume_chosen_button = change_active_button(
                            self.volume_buttons_group, self.volume_chosen_button, -2)
                    if (event.key == pg.K_s or event.key == pg.K_DOWN):
                        # Play choose sound.
                        self.choose_sound.play(maxtime=1000)
                        self.volume_chosen_button = change_active_button(
                            self.volume_buttons_group, self.volume_chosen_button, 2)
                    if (event.key == pg.K_a or event.key == pg.K_LEFT):
                        # Play choose sound.
                        self.choose_sound.play(maxtime=1000)
                        self.volume_chosen_button = change_active_button(
                            self.volume_buttons_group, self.volume_chosen_button, -1)
                    if (event.key == pg.K_d or event.key == pg.K_RIGHT):
                        # Play choose sound.
                        self.choose_sound.play(maxtime=1000)
                        self.volume_chosen_button = change_active_button(
                            self.volume_buttons_group, self.volume_chosen_button, 1)
                # resolution submenu
                elif self.submenu_boolean['resolution']:
                    if (event.key == pg.K_w or event.key == pg.K_UP):
                        # Play choose sound.
                        self.choose_sound.play(maxtime=1000)
                        self.resolution_chosen_button = change_active_button(
                            self.resolution_buttons_group, self.resolution_chosen_button, -1)
                    if (event.key == pg.K_s or event.key == pg.K_DOWN):
                        # Play choose sound.
                        self.choose_sound.play(maxtime=1000)
                        self.resolution_chosen_button = change_active_button(
                            self.resolution_buttons_group, self.resolution_chosen_button, 1)
                # archive submenu
                elif self.submenu_boolean['archive']:
                    if (event.key == pg.K_w or event.key == pg.K_UP):
                        # Play choose sound.
                        self.choose_sound.play(maxtime=1000)
                        self.archive_chosen_button = change_active_button(
                            self.archive_buttons_group, self.archive_chosen_button, -1)
                    if (event.key == pg.K_s or event.key == pg.K_DOWN):
                        # Play choose sound.
                        self.choose_sound.play(maxtime=1000)
                        self.archive_chosen_button = change_active_button(
                            self.archive_buttons_group, self.archive_chosen_button, 1)

    def update(self):
        # Update the pos of the screen rect.
        self.initial_screen_pos[0] += (self.screen_pos[0] -
                                       self.initial_screen_pos[0]) / 20
        self.initial_screen_pos[1] += (self.screen_pos[1] -
                                       self.initial_screen_pos[1]) / 20
        self.screen_rect.x = self.initial_screen_pos[0]
        self.screen_rect.y = self.initial_screen_pos[1]
        # Update initial sprites.
        if all(_ == False for _ in self.submenu_boolean.values()):
            for i in range(0, len(self.initial_group)):
                if self.activite_components[i]:
                    self.initial_group.sprites()[i].update()
        # Update volume group sprites.
        if self.submenu_boolean['volume']:
            for sprite in self.volume_group:
                # Update dynamic text.
                if sprite is self.dynamic_text01:
                    sprite.update('{0:2}'.format(
                        str(round(c.bgm_volume * 10))))
                elif sprite is self.dynamic_text02:
                    sprite.update('{0:2}'.format(
                        str(round(c.sound_volume * 10))))
                # Update other bolume group sprites.
                else:
                    sprite.update()
        # Update resolution group sprites.
        if self.submenu_boolean['resolution']:
            self.resolution_group.update()
        # Update archive group sprites.
        if self.submenu_boolean['archive']:
            self.archive_group.update()
        # Update volume
        pg.mixer.music.set_volume(c.bgm_volume)
        self.choose_sound.set_volume(c.sound_volume)
        self.confirm_sound.set_volume(c.sound_volume)

    def draw(self):
        """Draw all components."""
        # Draw wallpaper and wallpaper cover.
        self.screen.blit(self.wall_paper, (0, 0))
        self.screen.blit(self.wall_paper_cover, (0, 0))
        # Draw initial sprites group.
        for sprite in self.initial_group:
            sprite.draw()
        # Draw keyboard sprites.
        if self.submenu_boolean['keyboard']:
            for sprite in self.keyboard_group:
                sprite.draw()
        # Draw volume sprites.
        elif self.submenu_boolean['volume']:
            for sprite in self.volume_group:
                sprite.draw()
        # Draw resolution sprites.
        elif self.submenu_boolean['resolution']:
            for sprite in self.resolution_group:
                sprite.draw()
        # Draw archive sprites.
        elif self.submenu_boolean['archive']:
            for sprite in self.archive_group:
                sprite.draw()
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), self.screen_rect)

    def main(self):
        self.new()
        self.main_loop()
        # Quit current scene.
        return self.change_scene()

    def change_scene(self):
        if self.quit_scene:
            return self.next_scene
        else:
            return None


class SelectionBox(Menu):
    def __init__(self, clock, screen, display, text, font, font_size, glo, *button_text) -> None:
        super().__init__(clock, screen, display, glo)
        self.select = None
        if len(button_text) == 0:
            self.button_text = (('NO', 20), ('YES', 20))
        else:
            self.button_text = button_text
        self.bottom_color = c.PURPLE
        self.chosen_button = 0
        self.size = (c.SCREENWIDTH / 2, c.SCREENHEIGHT / 2)
        self.bottom_rect = pg.Rect(
            (c.SCREENWIDTH / 2 - self.size[0] / 2, c.SCREENHEIGHT / 2 - self.size[1] / 2), self.size)

        self.text_surf = self.text_surf = pg.font.Font(
            font, font_size).render(text, True, c.WHITE)
        self.text_rect = self.text_surf.get_rect(
            center=(self.bottom_rect.centerx, self.bottom_rect.y + self.bottom_rect.height / 4))

    def new(self):
        # sprite groups
        self.all_sprites = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        # Set up background.
        self.bg_surf = pg.Surface((c.SCREENWIDTH, c.SCREENHEIGHT))
        self.bg_surf.set_alpha(125)
        self.bg_rect = self.bg_surf.get_rect(topleft=(0, 0))
        # Blit background surface to the screen.
        self.screen.blit(self.bg_surf, self.bg_rect)
        # Set buttons.
        confirm_button_pos = (self.bottom_rect.x + self.bottom_rect.width *
                              5 / 9, self.bottom_rect.y + self.bottom_rect.height / 2)
        deny_button_pos = (self.bottom_rect.x + self.bottom_rect.width / 9,
                           self.bottom_rect.y + self.bottom_rect.height / 2)
        Button(self, self.screen, self.button_text[0][0], self.deny, c.ARCADE, self.button_text[0][1], (self.bottom_rect.width /
               3, self.bottom_rect.height / 3), deny_button_pos, deny_button_pos)
        Button(self, self.screen, self.button_text[1][0], self.confirm, c.ARCADE, self.button_text[1][1], (self.bottom_rect.width /
               3, self.bottom_rect.height / 3), confirm_button_pos, confirm_button_pos)
        # Set chosen button.
        self.buttons.sprites()[self.chosen_button].chosen = True
        # Set bgm and sounds
        self.choose_sound = pg.mixer.Sound(c.CHOOSESOUND)
        self.choose_sound.set_volume(c.sound_volume)

    def confirm(self):
        self.select = True

    def deny(self):
        self.select = False

    def event_loop(self):
        """Set the event loop of the menu."""
        for event in pg.event.get():
            # Quit game.
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Choose button according to the key.
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w or event.key == pg.K_UP or event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.choose_sound.play(maxtime=1000)  # Play choose sound.
                    self.buttons.sprites()[self.chosen_button].chosen = False
                    self.chosen_button = (
                        self.chosen_button - 1) % len(self.buttons)
                    self.buttons.sprites()[self.chosen_button].chosen = True
                if event.key == pg.K_s or event.key == pg.K_DOWN or event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.choose_sound.play(maxtime=1000)  # Play choose sound.
                    self.buttons.sprites()[self.chosen_button].chosen = False
                    self.chosen_button = (
                        self.chosen_button + 1) % len(self.buttons)
                    self.buttons.sprites()[self.chosen_button].chosen = True

    def update(self):
        """Update all components."""
        for sprite in self.all_sprites:
            sprite.update()

    def draw(self):
        """Draw all components of the menu."""
        pg.draw.rect(self.screen, self.bottom_color,
                     self.bottom_rect, border_radius=12)
        # Draw buttons.
        for button in self.buttons:
            button.draw()
        # Draw text.
        self.screen.blit(self.text_surf, self.text_rect)
        # Scale the screen.
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), (0, 0))

    def main_loop(self):
        """the main loop of the menu"""
        while self.main_loop_running:
            self.dt = self.clock.tick(c.FPS) / 1000
            # event loop
            self.event_loop()
            # update items
            self.update()
            # draw items
            self.draw()
            # update screen
            pg.display.update()
            # go to
            if self.select is not None:
                return self.select

    def main(self):
        self.new()
        return self.main_loop()


class SceneSelectionMenu(Menu):
    def __init__(self, clock, screen, display, glo) -> None:
        super().__init__(clock, screen, display, glo)
        self.chosen_button = 0

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        # Add wallpaper.
        self.wall_paper = pg.transform.scale(
            pg.image.load(c.SCENESELECTIONWALLPAPER), (c.SCREENWIDTH, c.SCREENHEIGHT))
        # Add previews.
        self.previews = []
        self.previews.append(pg.transform.scale(pg.image.load(
            c.CLIFFPREVIEW), (int(c.SCREENWIDTH / 4), int(c.SCREENHEIGHT * 2 / 5))))
        self.previews.append(pg.transform.scale(pg.image.load(
            c.STRINGSTARPREVIEW), (int(c.SCREENWIDTH / 4), int(c.SCREENHEIGHT * 2 / 5))))
        self.previews.append(pg.transform.scale(pg.image.load(
            c.INFINITEMODEPREVIEW), (int(c.SCREENWIDTH / 4), int(c.SCREENHEIGHT * 2 / 5))))
        # Add selecton buttons.
        Button(self, self.screen, 'cliff', self.level01, c.BACKTO1982,
               15, (c.SCREENWIDTH / 4, c.SCREENHEIGHT / 5), (c.SCREENWIDTH * -1 / 4, 2.5 * c.SCREENHEIGHT), (c.SCREENWIDTH / 16, c.SCREENHEIGHT * 3 / 4))
        Button(self, self.screen, 'stringstar', self.level02, c.BACKTO1982,
               15, (c.SCREENWIDTH / 4, c.SCREENHEIGHT / 5), (c.SCREENWIDTH * 6 / 16, 3 * c.SCREENHEIGHT), (c.SCREENWIDTH * 6 / 16, c.SCREENHEIGHT * 3 / 4))
        Button(self, self.screen, 'infinite', self.level03, c.BACKTO1982,
               15, (c.SCREENWIDTH / 4, c.SCREENHEIGHT / 5), (c.SCREENWIDTH, 2.5 * c.SCREENHEIGHT), (c.SCREENWIDTH * 11 / 16, c.SCREENHEIGHT * 3 / 4))
        # Add back button.
        Button(self, self.screen, "Back", self.back, c.ARCADE, 20, (c.SCREENWIDTH / 12, c.SCREENHEIGHT / 10),
               (c.SCREENWIDTH * 21 / 24, -2 * c.SCREENHEIGHT), (c.SCREENWIDTH * 21 / 24, c.SCREENHEIGHT / 15))

        # Set chosen button.
        self.buttons.sprites()[self.chosen_button].chosen = True
        # Set bgm and sounds
        if self.glo.ready_to_play_menu_bgm:
            pg.mixer.music.load(c.MAINMENUBGM)
            pg.mixer.music.set_volume(c.bgm_volume)
            pg.mixer.music.play(loops=-1)
            self.glo.ready_to_play_menu_bgm = False
        self.choose_sound = pg.mixer.Sound(c.CHOOSESOUND)
        self.choose_sound.set_volume(c.sound_volume)
        self.confirm_sound = pg.mixer.Sound(c.CONFIRMSOUND)
        self.confirm_sound.set_volume(c.sound_volume)

    def level01(self):
        if self.glo.archive.unlock[0]:
            self.next_scene = ['cliff', 'player01']
        else:
            mb = MessageBox(self.clock, self.screen, self.display,
                            'LOCKED', c.BACKTO1982, 30, self.glo)
            mb.main()

    def level02(self):
        if self.glo.archive.unlock[1]:
            self.next_scene = ['string_star', 'player01']
        else:
            mb = MessageBox(self.clock, self.screen, self.display,
                            'LOCKED', c.BACKTO1982, 30, self.glo)
            mb.main()

    def level03(self):
        if self.glo.archive.unlock[2]:
            self.next_scene = ['infinite_mode_cliff', 'player01']
        else:
            mb = MessageBox(self.clock, self.screen, self.display,
                            'LOCKED', c.BACKTO1982, 30, self.glo)
            mb.main()

    def back(self):
        self.next_scene = ['main_menu', 'main']

    def event_loop(self):
        """Set the event loop of the menu."""
        for event in pg.event.get():
            # Quit game.
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Choose button according to the key.
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w or event.key == pg.K_UP or event.key == pg.K_a or event.key == pg.K_LEFT:
                    self.choose_sound.play(maxtime=1000)  # Play choose sound.
                    self.buttons.sprites()[self.chosen_button].chosen = False
                    self.chosen_button = (
                        self.chosen_button - 1) % len(self.buttons)
                    self.buttons.sprites()[self.chosen_button].chosen = True
                if event.key == pg.K_s or event.key == pg.K_DOWN or event.key == pg.K_d or event.key == pg.K_RIGHT:
                    self.choose_sound.play(maxtime=1000)  # Play choose sound.
                    self.buttons.sprites()[self.chosen_button].chosen = False
                    self.chosen_button = (
                        self.chosen_button + 1) % len(self.buttons)
                    self.buttons.sprites()[self.chosen_button].chosen = True
                if event.key == pg.K_ESCAPE or event.key == pg.K_BACKSPACE:
                    self.confirm_sound.play(maxtime=1000)
                    self.back()

    def draw(self):
        """Draw all components."""
        self.screen.blit(self.wall_paper, (0, 0))
        for sprite in self.all_sprites:
            sprite.draw()
        # Draw previews
            self.screen.blit(
                self.previews[0], (c.SCREENWIDTH / 16, c.SCREENHEIGHT / 4))
            self.screen.blit(
                self.previews[1], (c.SCREENWIDTH * 6 / 16, c.SCREENHEIGHT / 4))
            self.screen.blit(
                self.previews[2], (c.SCREENWIDTH * 11 / 16, c.SCREENHEIGHT / 4))

        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), (0, 0))

    def fade_draw(self, fade):
        self.screen.blit(self.wall_paper, (0, 0))
        for sprite in self.all_sprites:
            sprite.draw()
        # Draw previews
            self.screen.blit(
                self.previews[0], (c.SCREENWIDTH / 16, c.SCREENHEIGHT / 4))
            self.screen.blit(
                self.previews[1], (c.SCREENWIDTH * 6 / 16, c.SCREENHEIGHT / 4))
            self.screen.blit(
                self.previews[2], (c.SCREENWIDTH * 11 / 16, c.SCREENHEIGHT / 4))
        # Draw black surf.
        self.screen.blit(fade, (0, 0))
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), (0, 0))

    def update(self):
        # Update all sprites.
        self.all_sprites.update()

    def main(self):
        self.new()
        self.fade_in()
        self.main_loop()


class MessageBox(Menu):
    def __init__(self, clock, screen, display, text, font, font_size, glo) -> None:
        super().__init__(clock, screen, display, glo)
        self.select = False
        self.bottom_color = c.PURPLE
        self.size = (c.SCREENWIDTH / 2, c.SCREENHEIGHT / 2)
        self.bottom_rect = pg.Rect(
            (c.SCREENWIDTH / 2 - self.size[0] / 2, c.SCREENHEIGHT / 2 - self.size[1] / 2), self.size)
        self.text_surf = self.text_surf = pg.font.Font(
            font, font_size).render(text, True, c.WHITE)
        self.text_rect = self.text_surf.get_rect(
            center=(self.bottom_rect.centerx, self.bottom_rect.y + self.bottom_rect.height / 4))

    def new(self):
        # sprite groups
        self.all_sprites = pg.sprite.Group()
        # Set up background.
        self.bg_surf = pg.Surface((c.SCREENWIDTH, c.SCREENHEIGHT))
        self.bg_surf.set_alpha(125)
        self.bg_rect = self.bg_surf.get_rect(topleft=(0, 0))
        # Blit background surface to the screen.
        self.screen.blit(self.bg_surf, self.bg_rect)
        # Set buttons.
        confirm_button_pos = (self.bottom_rect.x + self.bottom_rect.width / 4,
                              self.bottom_rect.y + self.bottom_rect.height / 2)
        self.confirm_button = Button(self, self.screen, 'OK', self.confirm, c.ARCADE, 20, (
            self.bottom_rect.width / 2, self.bottom_rect.height / 3), confirm_button_pos, confirm_button_pos, self.all_sprites)
        # Set chosen button.
        self.confirm_button.chosen = True
        # Set bgm and sounds
        self.choose_sound = pg.mixer.Sound(c.CHOOSESOUND)
        self.choose_sound.set_volume(c.sound_volume)

    def confirm(self):
        self.select = True

    def event_loop(self):
        """Set the event loop of the menu."""
        for event in pg.event.get():
            # Quit game.
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def update(self):
        """Update all components."""
        for sprite in self.all_sprites:
            sprite.update()

    def draw(self):
        """Draw all components of the menu."""
        pg.draw.rect(self.screen, self.bottom_color,
                     self.bottom_rect, border_radius=12)
        # Draw buttons.
        self.confirm_button.draw()
        # Draw text.
        self.screen.blit(self.text_surf, self.text_rect)
        # Scale the screen.
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), (0, 0))

    def main_loop(self):
        """the main loop of the menu"""
        while self.main_loop_running:
            self.dt = self.clock.tick(c.FPS) / 1000
            # event loop
            self.event_loop()
            # update items
            self.update()
            # draw items
            self.draw()
            # update screen
            pg.display.update()
            # go to
            if self.select:
                return

    def main(self):
        self.new()
        self.main_loop()
