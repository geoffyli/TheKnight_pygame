#!/usr/bin/env python
import sys
import constants as c
from sprites import *
from tilemap import *
from buttons import Text
from menus import SettingsMenu, SelectionBox
from backgrounds import Background


class Scene:
    """Scene class describes a scene.
       new(), event_loop(), main(), etc. should be customized by subclasses."""

    def __init__(self, clock, screen, display, glo, size_multiplier) -> None:
        self.pressed_keys = None
        self.main_loop_running = True
        self.size_multiplier = size_multiplier
        self.enter_rects = {}
        self.next_scene = None
        self.clock = clock
        self.screen = screen
        self.display = display
        self.glo = glo
        self.player_pos = glo.next_scene[1]

    def load_data(self, map_path):
        """Load data from files, tile map for instance."""
        self.map = TiledMap(map_path)
        self.map_img = self.map.make_map()
        # Scaled
        self.map_rect = self.map_img.get_rect()
        self.map_img = pg.transform.scale(
            self.map_img, (int(self.size_multiplier * self.map_rect.width), int(self.size_multiplier * self.map_rect.height)))
        self.map_rect = self.map_img.get_rect()

    def new(self):
        """Ininialize all componenets in the scene."""
        pass

    def fade_in(self):
        '''Fade in effect.'''
        fade = pg.Surface((c.SCREENWIDTH, c.SCREENHEIGHT))
        fade.fill(c.BLACK)
        for alpha in range(255, 0, -10):
            fade.set_alpha(alpha)  # accumulative
            self.dt = self.clock.tick(FPS) / 1000
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
        """Update all sprites and let the camera track the player."""
        self.all_sprites.update()
        self.camera.update(self.player)

    def fade_draw(self, fade):
        """Draw components."""
        self.screen.blit(
            self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # Draw black surf.
            self.screen.blit(fade, (0, 0))
        # Blit the screen to the display.
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), (0, 0))

    def draw(self):
        self.screen.blit(
            self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), (0, 0))

    def event_loop(self):
        '''the event loop of this scene'''
        pass

    def main_loop(self):
        """the main loop of the scene"""
        while self.main_loop_running:
            self.dt = self.clock.tick(c.FPS) / 1000
            # event loop
            self.event_loop()
            # Make sure the game won't crash when moving the game window.
            if self.dt < 0.1:
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
        pass


class BattleScene(Scene):
    def __init__(self, clock, screen, display, glo, size_multiplier) -> None:
        super().__init__(clock, screen, display, glo, size_multiplier)
        # It determins whether to show tips or not.
        self.activate_tips_text = False
        self.activate_exit_text = False

    def new_groups(self):
        """Create scene groups."""
        self.all_sprites = pg .sprite.Group()
        self.walls = pg.sprite.Group()
        self.invisible_walls = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.fire_balls = pg.sprite.Group()
        self.tips_text_group = pg.sprite.Group()
        self.exit_text_group = pg.sprite.Group()
        self.player_info_text_group = pg.sprite.Group()

    def new_background(self):
        """Add background wallpaper, background images and camera."""
        pass

    def new_objs_from_map(self):
        """Traverse the objects in the map and create sprites and rects."""
        pass

    def new_text(self):
        """Create scene text."""
        pass

    def new_music(self):
        """Add and set bgm and sounds."""
        pass

    def new(self):
        """Initialize all varis and do all the setup for a new game."""
        # Create groups.
        self.new_groups()
        # Create background stuff.
        self.new_background()
        # Load sprites and rects from the map.
        self.new_objs_from_map()
        # Create scene text.
        self.new_text()
        # Set sounds and music.
        self.new_music()

    def load_data(self, map_path):
        """Load tile map from files."""
        self.map = TiledMap(map_path)
        self.map_img = self.map.make_map()
        self.map_img.set_colorkey((0, 0, 0))
        # Scale the map.
        self.map_rect = self.map_img.get_rect()
        self.map_img = pg.transform.scale(
            self.map_img, (int(self.size_multiplier * self.map_rect.width), int(self.size_multiplier * self.map_rect.height)))
        self.map_rect = self.map_img.get_rect()

    def show_settings_menu(self):
        """Show settings menu and reset the sound volume."""
        self.confirm_sound.play(maxtime=1000)
        settings_menu = SettingsMenu(
            self.clock, self.screen, self.display, self.glo)
        next_scene = settings_menu.main()
        if next_scene is not None:
            # Go back to the main menu.
            self.next_scene = next_scene
        else:
            # Set sound volume and return to the scene.
            for sound in self.sounds:
                sound.set_volume(c.sound_volume)
            for sprite in self.enemies:
                sprite.slash_sound.set_volume(c.sound_volume)
                sprite.be_hit_sound.set_volume(c.sound_volume)

    def press_key_l(self):
        """Begin to record the pressed time of key l."""
        self.player.press_key_l = True
        self.player.press_key_l_begin = pg.time.get_ticks()

    def release_key_l(self):
        """Release key l and get ready to throw a fire ball and get the pressed time."""
        self.player.press_key_l = False
        self.player.throw_fire_ball = True
        self.player.press_key_l_duration = pg.time.get_ticks() - \
            self.player.press_key_l_begin

    def fire_ball_hits_enemy(self, sprite):
        """Detect if there is a fire ball hits the enemy.
            If there is, the enemy will be slain and particles will be drawn."""
        for fire_ball in self.fire_balls:
            if fire_ball.rect.colliderect(sprite.body_rect) and not sprite.invincible:
                sprite.is_slain()
                fire_ball.exists = False
                # Play explosion sound.
                self.explosion_sound.play()
                # Create explosion particles.
                for _ in range(20):
                    SquareParticle(
                        self, self.camera, fire_ball.rect.centerx, fire_ball.rect.centery, [c.FIRBALLCOLOR01, c.FIRBALLCOLOR02, c.FIRBALLCOLOR03], [randint(2000, 4000)/10 - 300, randint(0, 8000) / 10 - 600], 20)

    def player_slashes_enemy(self, sprite):
        """Detect if the player slashes the enemy.
            If it does, set the enemy velocity and minus its hv.
            If the enemy is slashed to death, the player will get a fire ball."""
        if self.player.attack_rect is not None:
            # If player attack rect overlapes with the enemy body rect and the enemy is vincible, begin to slash.
            if self.player.attack_rect.colliderect(sprite.body_rect) and not sprite.invincible:
                if self.player.body_rect.centerx < sprite.body_rect.centerx:
                    sprite.vel[1] = sprite.jump_height / 2
                elif self.player.body_rect.centerx >= sprite.body_rect.centerx:
                    sprite.vel[1] = sprite.jump_height / 2
                sprite.is_hit()
                # If the player slashes the enemy to his death, the player will get a fire ball.
                if sprite.hv < 1:
                    self.player.fire_ball_amount += 1

    def player_collides_enemy(self, sprite):
        """Detect if player collides with the enemy."""
        if self.player.body_rect.colliderect(sprite.body_rect) and not self.player.invincible:
            if self.player.body_rect.x + self.player.body_rect.width > sprite.body_rect.x and self.player.body_rect.centerx < sprite.body_rect.centerx:
                self.player.vel[0] = -2 * self.player.player_speed
                self.player.vel[1] = self.player.jump_height / 2
            elif self.player.body_rect.x < sprite.body_rect.x + sprite.body_rect.width and self.player.body_rect.centerx > sprite.body_rect.centerx:
                self.player.vel[0] = 2 * self.player.player_speed
                self.player.vel[1] = self.player.jump_height / 2
            self.player.is_hit()

    def enemy_slashes_player(self, sprite):
        """Detect if the enemy slashes the player.
            If it does, set the player velocity and minus his hv."""
        if sprite.attack_rect is not None and self.player.body_rect.colliderect(sprite.attack_rect) and not self.player.invincible:
            if sprite.attack_dir == 'attack_left':
                self.player.vel[0] = -3 * self.player.player_speed
                self.player.vel[1] = self.player.jump_height / 2
            elif sprite.attack_dir == 'attack_right':
                self.player.vel[0] = 3 * self.player.player_speed
                self.player.vel[1] = self.player.jump_height / 2
            self.player.is_hit()

    def new_enemy_killed_particles(self, sprite):
        """Create 1 particle when the enemy is killed."""
        particle_color = []  # The color depends on the type of the enemy.
        if sprite.type == '01':
            particle_color = [
                c.KNIGHTCOLOR0101, c.KNIGHTCOLOR0102, c.KNIGHTCOLOR0103, c.KNIGHTCOLOR0104]
        elif sprite.type == '02':
            particle_color = [
                c.KNIGHTCOLOR0201, c.KNIGHTCOLOR0202, c.KNIGHTCOLOR0203, c.KNIGHTCOLOR0204]
        elif sprite.type == '03':
            particle_color = [
                c.KNIGHTCOLOR0301, c.KNIGHTCOLOR0302, c.KNIGHTCOLOR0303, c.KNIGHTCOLOR0304]
        for _ in range(1):
            SquareParticle(
                self, self.camera, sprite.body_rect.centerx, sprite.body_rect.centery, particle_color, [randint(2000, 4000)/10 - 300, randint(1000, 5000)/10 - 400], 30)

    def show_tips(self):
        """Detect if to show tips."""
        if self.player.rect.colliderect(self.enter_rects['tips']):
            self.activate_tips_text = True
        else:
            self.activate_tips_text = False
            # Set the text to the original position.
            for text in self.tips_text_group:
                text.update_init_pos((-30, self.map_rect.height / 2))

    def show_exit_text(self):
        if self.player.rect.colliderect(self.enter_rects['exit']):
            self.activate_exit_text = True
        else:
            self.activate_exit_text = False
            # Set the text to the original position.
            for text in self.exit_text_group:
                text.update_init_pos(
                    (self.map_rect.width + 30, self.map_rect.height / 2))

    def show_exit_selection_box(self):
        """Show selection box and update the archive. Unlock the next level."""
        sb = SelectionBox(self.clock, self.screen, self.display, 'Enemies: '+str(self.total_enemy_amount -
                                                                                 len(self.enemies))+'/'+str(self.total_enemy_amount), c.BACKTO1982, 20, self.glo, ('restart', 15), ('exit', 15))
        if sb.main():
            self.next_scene = ['scene_selection_menu', None]
        else:
            self.next_scene = ['cliff', 'player01']

    def show_fail_selection_box(self):
        sb = SelectionBox(self.clock, self.screen, self.display, 'failed',
                          c.BACKTO1982, 20, self.glo, ('restart', 15), ('exit', 15))
        if sb.main():
            self.next_scene = ['scene_selection_menu', None]
        else:
            self.next_scene = ['cliff', 'player01']

    def event_loop(self):
        """the event loop of the game"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                # Display the settings menu.
                if event.key == pg.K_ESCAPE:
                    self.show_settings_menu()
                # Detect the length of pressed key l.
                if event.key == pg.K_l and not self.player.press_key_l:
                    self.press_key_l()
                # Detect if to exit the scene.
                if event.key == pg.K_e and self.activate_exit_text:
                    self.show_exit_selection_box()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_l and self.player.press_key_l:
                    self.release_key_l()
        # Detect the event of the enemies.
        for sprite in self.enemies:
            # Detect if the fire ball attacks the enemy.
            self.fire_ball_hits_enemy(sprite)
            # Detect if the player slashes the enemy.
            self.player_slashes_enemy(sprite)
            # If the enemy has not been slain, the player may be hit.
            if not sprite.slain:
                # Detect if the player collides the body of the enemy.
                self.player_collides_enemy(sprite)
                # Detect if the enemy slashes the player.
                self.enemy_slashes_player(sprite)
            # if the enemy is slain
            else:
                # Draw particles.
                self.new_enemy_killed_particles(sprite)
            # Find if the enemy still exists.
            if not sprite.exists:
                # If the enemy doesn't exist any longer, remove it from all the groups it belongs
                self.all_sprites.remove(sprite)
                self.enemies.remove(sprite)
        # Detect if the player still exists.
        if self.player.hv < 1:
            self.show_fail_selection_box()
        # Detect if the fire ball still exists.
        for fire_ball in self.fire_balls:
            if not fire_ball.exists:
                self.fire_balls.remove(fire_ball)
                self.all_sprites.remove(fire_ball)
        # Detect whether to show tips or not.
        self.show_tips()
        # Detect whether to show exit text or not.
        self.show_exit_text()

    def draw_components(self):
        """Draw components of the scene."""
        # Draw background picture.
        self.screen.blit(self.screen_background, (0, 0))
        # Draw background images.
        for bg in self.backgrounds:
            bg.draw()
        # Draw map.
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # Draw sprites.
        for sprite in self.all_sprites:
            # Blit the sprite image.
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # Draw tips.
        if self.activate_tips_text:
            for text in self.tips_text_group:
                self.screen.blit(
                    text.text_surf, self.camera.apply_rect(text.text_rect))
        # Draw exit text.
        if self.activate_exit_text:
            for text in self.exit_text_group:
                self.screen.blit(
                    text.text_surf, self.camera.apply_rect(text.text_rect))
        # Draw particles
        for sprite in self.particles:
            sprite.draw()
        # Draw player info text.
        for text in self.player_info_text_group:
            text.draw()
        # Avoid screen flickering.
        if self.next_scene is not None and self.next_scene[0] == 'scene_selection_menu':
            # Draw screen black.
            pg.draw.rect(self.screen, c.BLACK, self.screen.get_rect())

    def scale_screen(self):
        """Scale the scene surface to the game window size."""
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), (0, 0))

    def draw(self):
        """Draw everything in the scene."""
        self.draw_components()
        # Scale the screen.
        self.scale_screen()

    def main(self):
        """The main skeleton of the game process."""
        self.load_data(None)
        self.new()
        self.fade_in()
        self.main_loop()

    def update_particles(self):
        """Update particles in the scene."""
        for sprite in self.particles:
            sprite.update()
            if sprite.timer < 0:
                self.particles.remove(sprite)

    def update_tips(self):
        """Update the tips text in the scene."""
        for text in self.tips_text_group:
            if self.activate_tips_text == True:
                text.update()

    def update_exit_text(self):
        """Update the exit text in the scene."""
        for text in self.exit_text_group:
            if self.activate_exit_text == True:
                text.update()

    def update_player_info(self):
        """Update the player info in the scene."""
        self.player_info_text_group.sprites()[0].update(
            'Hv: '+str(self.player.hv))
        self.player_info_text_group.sprites()[1].update(
            'FireBall: '+str(self.player.fire_ball_amount))
        self.player_info_text_group.sprites()[2].update(
            'Enemies: '+str(self.total_enemy_amount -
                            len(self.enemies))+'/'+str(self.total_enemy_amount))

    def update(self):
        """Update all sprites and let the camera track the player."""
        self.all_sprites.update()
        # Update particles.
        self.update_particles()
        # Update tips text.
        self.update_tips()
        # Update exit text.
        self.update_exit_text()
        # Update player information.
        self.update_player_info()
        # Update camera by the player.
        self.camera.delayed_update(self.player)

    def fade_draw(self, fade):
        """Draw components."""
        self.draw_components()
        # Draw black surf.
        self.screen.blit(fade, (0, 0))
        # Blit the screen to the display.
        self.scale_screen()


class Cliff(BattleScene):
    def __init__(self, clock, screen, display, glo, size_multiplier) -> None:
        super().__init__(clock, screen, display, glo, size_multiplier)

    def new_background(self):
        # Create screen wallpaper.
        self.screen_background = pg.transform.scale(
            pg.image.load(c.CLIFFBACKGROUND), (SCREENWIDTH, SCREENHEIGHT))
        # Create and add backgrouds
        self.backgrounds = []
        # Create the camera.
        self.camera = Camera(self.map.width * self.size_multiplier,
                             self.map.height * self.size_multiplier)
        # Append background images.
        self.backgrounds.append(Background(
            self.screen, self.camera, CLIFFCLOUDS, 0.1, (-0.1, 0.1), (0.6, 1)))
        self.backgrounds.append(Background(
            self.screen, self.camera, CLIFFCLOUDS, 0.1, (0.5, 0.1), (0.6, 1)))
        self.backgrounds.append(Background(
            self.screen, self.camera, CLIFFCLOUDS, 0.1, (1.1, 0.1), (0.6, 1)))
        self.backgrounds.append(Background(
            self.screen, self.camera, CLIFFSEA, 0.25, (-0.1, 0.8), (1.2, 0.5)))
        self.backgrounds.append(Background(
            self.screen, self.camera, CLIFFSEA, 0.25, (1.1, 0.8), (1.2, 0.5)))
        self.backgrounds.append(Background(
            self.screen, self.camera, CLIFFGROUND, 0.5, (-0.1, 0.9), (1.2, 0.5)))
        self.backgrounds.append(Background(
            self.screen, self.camera, CLIFFGROUND, 0.5, (0.7, 0.9), (1.2, 0.5)))

    def new_objs_from_map(self):
        for tile_object in self.map.tmxdata.objects:
            # Each object is a dict. Keys are properties.
            if tile_object.type == 'player':
                if tile_object.name == self.player_pos:
                    self.player = HorizontalPlayer(
                        self, tile_object.x * self.size_multiplier, tile_object.y * self.size_multiplier, 250, 5, 5, self.size_multiplier)
            elif tile_object.type == 'knight':
                if tile_object.name == 'knight01':
                    Knight(self, '01', tile_object.x * self.size_multiplier,
                           tile_object.y * self.size_multiplier, randint(60, 80), 1, self.size_multiplier)
                elif tile_object.name == 'knight02':
                    Knight(self, '02', tile_object.x * self.size_multiplier,
                           tile_object.y * self.size_multiplier, randint(80, 100), 2, self.size_multiplier)
                elif tile_object.name == 'knight03':
                    Knight(self, '03', tile_object.x * self.size_multiplier,
                           tile_object.y * self.size_multiplier, randint(100, 120), 3, self.size_multiplier)
            if tile_object.name == 'obstacle':
                Obstacle(self, tile_object.x * self.size_multiplier, tile_object.y * self.size_multiplier,
                         tile_object.width * self.size_multiplier, tile_object.height * self.size_multiplier)
            elif tile_object.name == 'invisible_obstacle':
                InvisibleObstacle(self, tile_object.x * self.size_multiplier, tile_object.y * self.size_multiplier,
                                  tile_object.width * self.size_multiplier, tile_object.height * self.size_multiplier)
            elif tile_object.name == 'tips':
                self.enter_rects['tips'] = pg.Rect(self.size_multiplier * tile_object.x, self.size_multiplier * tile_object.y,
                                                   self.size_multiplier * tile_object.width, self.size_multiplier * tile_object.height)
            elif tile_object.name == 'exit':
                self.enter_rects['exit'] = pg.Rect(self.size_multiplier * tile_object.x, self.size_multiplier * tile_object.y,
                                                   self.size_multiplier * tile_object.width, self.size_multiplier * tile_object.height)
        # total enemy amount
        self.total_enemy_amount = len(self.enemies)

    def new_text(self):
        # tips text
        Text(self, self.map_img, 'Tips:', c.TICKETING, 20, c.DARKPURPLE, (-30,
             self.map_rect.height * 3 / 5), (170, self.map_rect.height * 3 / 5), self.tips_text_group)
        Text(self, self.map_img, '  J: slash', c.TICKETING, 20, c.DARKPURPLE, (-30,
             self.map_rect.height * 3 / 5), (170, self.map_rect.height * 25 / 40), self.tips_text_group)
        Text(self, self.map_img, '  L: throw a fire ball', c.TICKETING, 20, c.DARKPURPLE, (-30,
             self.map_rect.height * 3 / 5), (170, self.map_rect.height * 26 / 40), self.tips_text_group)
        Text(self, self.map_img, '    Hold L longer to throw farther!', c.TICKETING, 20, c.DARKPURPLE, (-30,
             self.map_rect.height * 3 / 5), (170, self.map_rect.height * 27 / 40), self.tips_text_group)
        Text(self, self.map_img, '    Slash enemies to get fire balls!', c.TICKETING, 20, c.DARKPURPLE, (-30,
             self.map_rect.height * 3 / 5), (170, self.map_rect.height * 28 / 40), self.tips_text_group)
        Text(self, self.map_img, '  Don\'t bump into the enemies!', c.TICKETING, 20, c.DARKPURPLE, (-30,
             self.map_rect.height * 3 / 5), (170, self.map_rect.height * 29 / 40), self.tips_text_group)
        # exit text
        Text(self, self.map_img, 'Press E to exit.', c.TICKETING, 20, c.WHITE, (self.map_rect.width + 30,
             self.map_rect.height * 3 / 5), (self.map_rect.width - 150, self.map_rect.height * 3 / 5), self.exit_text_group)
        # player info text
        Text(self, self.screen, 'Hv:'+str(self.player.hv), c.BACKTO1982, 15,
             c.DARKPURPLE, (30, -30), (30, 30), self.player_info_text_group)
        Text(self, self.screen, 'FireBall:'+str(self.player.fire_ball_amount), c.BACKTO1982, 15,
             c.DARKPURPLE, (120, -30), (120, 30), self.player_info_text_group)
        Text(self, self.screen, 'Enemies: 0/'+str(self.total_enemy_amount), c.BACKTO1982, 15,
             c.DARKPURPLE, (280, -30), (280, 30), self.player_info_text_group)  # enemies killed

    def new_music(self):
        self.sounds = []
        self.confirm_sound = pg.mixer.Sound(c.CONFIRMSOUND)
        self.confirm_sound.set_volume(c.sound_volume)
        self.explosion_sound = pg.mixer.Sound(c.EXPLOSIONSOUND)
        self.explosion_sound.set_volume(c.sound_volume * 8)
        # Append all sounds to the list.
        self.sounds.append(self.confirm_sound)
        self.sounds.append(self.explosion_sound)
        self.sounds.append(self.player.slash_sound)
        self.sounds.append(self.player.throw_fire_ball_sound)

        # Set up bgm.
        pg.mixer.music.load(c.CLIFFBGM)
        pg.mixer.music.set_volume(c.bgm_volume)
        # Play bgm.
        pg.mixer.music.play(loops=-1, fade_ms=2000)

    def show_exit_selection_box(self):
        """Show selection box and update the archive. Unlock the next level."""
        sb = SelectionBox(self.clock, self.screen, self.display, 'Enemies: '+str(self.total_enemy_amount -
                                                                                 len(self.enemies))+'/'+str(self.total_enemy_amount), c.BACKTO1982, 20, self.glo, ('restart', 20), ('exit', 20))
        if sb.main():
            self.next_scene = ['scene_selection_menu', None]
        else:
            self.next_scene = ['cliff', 'player01']
        self.glo.archive.unlock[1] = True

    def show_fail_selection_box(self):
        sb = SelectionBox(self.clock, self.screen, self.display, 'failed',
                          c.BACKTO1982, 20, self.glo, ('restart', 20), ('exit', 20))
        if sb.main():
            self.next_scene = ['scene_selection_menu', None]
        else:
            self.next_scene = ['cliff', 'player01']

    def main(self):
        """The main skeleton of the game process."""
        self.load_data(c.CLIFF)
        self.new()
        self.fade_in()
        self.main_loop()

    def update_player_info(self):
        self.player_info_text_group.sprites()[0].update(
            'Hv: '+str(self.player.hv))
        self.player_info_text_group.sprites()[1].update(
            'FireBall: '+str(self.player.fire_ball_amount))
        self.player_info_text_group.sprites()[2].update(
            'Enemies: '+str(self.total_enemy_amount -
                            len(self.enemies))+'/'+str(self.total_enemy_amount))


class StringStar(BattleScene):
    def __init__(self, clock, screen, display, glo, size_multiplier) -> None:
        super().__init__(clock, screen, display, glo, size_multiplier)

    def new_background(self):
        self.screen_background = pg.transform.scale(
            pg.image.load(c.STRINGSTARBACKGROUND), (SCREENWIDTH, SCREENHEIGHT))
        # Create and add backgrouds
        self.backgrounds = []
        # Create the camera.
        self.camera = Camera(self.map.width * self.size_multiplier,
                             self.map.height * self.size_multiplier)
        # Append background images.
        self.backgrounds.append(Background(
            self.screen, self.camera, STRINGSTARBLUECLOUD, 0.25, (-0.1, -0.65), (1.2, 1.8)))
        self.backgrounds.append(Background(
            self.screen, self.camera, STRINGSTARBLUECLOUD, 0.25, (1.1, -0.65), (1.2, 1.8)))
        self.backgrounds.append(Background(
            self.screen, self.camera, STRINGSTARBLUECLOUD, 0.25, (2.3, -0.65), (1.2, 1.8)))
        self.backgrounds.append(Background(
            self.screen, self.camera, STRINGSTARPURPLECLOUD, 0.5, (-0.1, -0.5), (1.2, 1.8)))
        self.backgrounds.append(Background(
            self.screen, self.camera, STRINGSTARPURPLECLOUD, 0.5, (1.1, -0.5), (1.2, 1.8)))
        self.backgrounds.append(Background(
            self.screen, self.camera, STRINGSTARPURPLECLOUD, 0.5, (2.3, -0.5), (1.2, 1.8)))
        self.backgrounds.append(Background(
            self.screen, self.camera, STRINGSTARPURPLECLOUD, 0.5, (3.5, -0.5), (1.2, 1.8)))

    def new_objs_from_map(self):
        # Create sprites.
        for tile_object in self.map.tmxdata.objects:
            # Each object is a dict. Keys are properties.
            if tile_object.type == 'player':
                if tile_object.name == self.player_pos:
                    self.player = HorizontalPlayer(
                        self, tile_object.x * self.size_multiplier, tile_object.y * self.size_multiplier, 250, 5, 5, self.size_multiplier)
            elif tile_object.type == 'knight':
                if tile_object.name == 'knight01':
                    Knight(self, '01', tile_object.x * self.size_multiplier,
                           tile_object.y * self.size_multiplier, randint(60, 80), 1, self.size_multiplier)
                elif tile_object.name == 'knight02':
                    Knight(self, '02', tile_object.x * self.size_multiplier,
                           tile_object.y * self.size_multiplier, randint(80, 100), 2, self.size_multiplier)
                elif tile_object.name == 'knight03':
                    Knight(self, '03', tile_object.x * self.size_multiplier,
                           tile_object.y * self.size_multiplier, randint(100, 120), 3, self.size_multiplier)
            if tile_object.name == 'obstacle':
                Obstacle(self, tile_object.x * self.size_multiplier, tile_object.y * self.size_multiplier,
                         tile_object.width * self.size_multiplier, tile_object.height * self.size_multiplier)
            elif tile_object.name == 'invisible_obstacle':
                InvisibleObstacle(self, tile_object.x * self.size_multiplier, tile_object.y * self.size_multiplier,
                                  tile_object.width * self.size_multiplier, tile_object.height * self.size_multiplier)
            elif tile_object.name == 'tips':
                self.enter_rects['tips'] = pg.Rect(self.size_multiplier * tile_object.x, self.size_multiplier * tile_object.y,
                                                   self.size_multiplier * tile_object.width, self.size_multiplier * tile_object.height)
            elif tile_object.name == 'exit':
                self.enter_rects['exit'] = pg.Rect(self.size_multiplier * tile_object.x, self.size_multiplier * tile_object.y,
                                                   self.size_multiplier * tile_object.width, self.size_multiplier * tile_object.height)
        # total enemy amount
        self.total_enemy_amount = len(self.enemies)

    def new_text(self):
        # tips text
        Text(self, self.map_img, 'Enemies could be stronger.', c.TICKETING, 20, c.WHITE, (-30,
             self.map_rect.height * 3 / 5), (20, self.map_rect.height * 22 / 40), self.tips_text_group)
        Text(self, self.map_img, 'BE CAREFUL!', c.TICKETING, 20, c.WHITE, (-30,
             self.map_rect.height * 3 / 5), (20, self.map_rect.height * 23 / 40), self.tips_text_group)
        # exit text
        Text(self, self.map_img, 'Press E to exit.', c.TICKETING, 20, c.WHITE, (self.map_rect.width + 30,
             self.map_rect.height * 3 / 5), (self.map_rect.width - 150, self.map_rect.height * 23 / 40), self.exit_text_group)
        # player info text
        Text(self, self.screen, 'Hv:'+str(self.player.hv), c.BACKTO1982, 15,
             c.WHITE, (30, -30), (30, 30), self.player_info_text_group)
        Text(self, self.screen, 'FireBall:'+str(self.player.fire_ball_amount), c.BACKTO1982, 15,
             c.WHITE, (120, -30), (120, 30), self.player_info_text_group)
        Text(self, self.screen, 'Enemies: 0/'+str(self.total_enemy_amount), c.BACKTO1982, 15,
             c.WHITE, (280, -30), (280, 30), self.player_info_text_group)  # enemies killed

    def new_music(self):
        self.sounds = []
        # Set sounds and music.
        self.confirm_sound = pg.mixer.Sound(c.CONFIRMSOUND)
        self.confirm_sound.set_volume(c.sound_volume)
        self.explosion_sound = pg.mixer.Sound(c.EXPLOSIONSOUND)
        self.explosion_sound.set_volume(c.sound_volume * 8)
        # Append all sounds to the list.
        self.sounds.append(self.confirm_sound)
        self.sounds.append(self.explosion_sound)
        self.sounds.append(self.player.slash_sound)
        self.sounds.append(self.player.throw_fire_ball_sound)
        pg.mixer.music.load(c.STRINGSTARBGM)
        pg.mixer.music.set_volume(c.bgm_volume)
        # Play bgm.
        pg.mixer.music.play(loops=-1, fade_ms=2000)

    def show_exit_selection_box(self):
        """Show selection box and update the archive. Unlock the next level."""
        sb = SelectionBox(self.clock, self.screen, self.display, 'Enemies: '+str(self.total_enemy_amount -
                                                                                 len(self.enemies))+'/'+str(self.total_enemy_amount), c.BACKTO1982, 20, self.glo, ('restart', 20), ('exit', 20))
        if sb.main():
            self.next_scene = ['scene_selection_menu', None]
        else:
            self.next_scene = ['string_star', 'player01']
        self.glo.archive.unlock[2] = True

    def show_fail_selection_box(self):
        sb = SelectionBox(self.clock, self.screen, self.display, 'failed',
                          c.BACKTO1982, 20, self.glo, ('restart', 20), ('exit', 20))
        if sb.main():
            self.next_scene = ['scene_selection_menu', None]
        else:
            self.next_scene = ['string_star', 'player01']

    def main(self):
        """The main skeleton of the game process."""
        self.load_data(c.STRINGSTAR)
        self.new()
        self.fade_in()
        self.main_loop()

    def update_player_info(self):
        # Update player info
        self.player_info_text_group.sprites()[0].update(
            'Hv: '+str(self.player.hv))
        self.player_info_text_group.sprites()[1].update(
            'FireBall: '+str(self.player.fire_ball_amount))
        self.player_info_text_group.sprites()[2].update(
            'Enemies: '+str(self.total_enemy_amount -
                            len(self.enemies))+'/'+str(self.total_enemy_amount))


class InfiniteModeCliff(BattleScene):
    def __init__(self, clock, screen, display, glo, size_multiplier) -> None:
        super().__init__(clock, screen, display, glo, size_multiplier)
        self.set_up_booleans()  # Set up booleans.
        self.set_up_timers()
        self.set_up_enemy_generation_counter()
        self.game_round = 0  # game round

    def set_up_booleans(self):
        """Set up booleans in the scene."""
        self.game_begin = False
        self.show_round_text = False
        self.generate_enemies = False
        self.ready_to_heal_player = True  # Heal player every 5 rounds.

    def set_up_timers(self):
        """Set up round text timer and enemy generation timer."""
        self.round_text_last_update = 0
        self.round_text_interval = 2000  # the time interval of the round text.
        self.generate_enemies_interval = 500
        self.generate_enemies_last_update = 0

    def set_up_enemy_generation_counter(self):
        """Set up the attributes about enemy generation."""
        self.generation_amount = 0
        self.enemy_generation_counter = 0

    def new_groups(self):
        super().new_groups()
        self.round_text_group = pg.sprite.Group()

    def new_background(self):
        # Create screen background.
        self.screen_background = pg.transform.scale(
            pg.image.load(c.CLIFFBACKGROUND), (SCREENWIDTH, SCREENHEIGHT))
        # Create and add backgrouds
        self.backgrounds = []
        # Create the camera.
        self.camera = Camera(self.map.width * self.size_multiplier,
                             self.map.height * self.size_multiplier)
        # Append background images.
        self.backgrounds.append(Background(
            self.screen, self.camera, CLIFFCLOUDS, 0.1, (-0.1, 0.1), (0.6, 1)))
        self.backgrounds.append(Background(
            self.screen, self.camera, CLIFFCLOUDS, 0.1, (0.5, 0.1), (0.6, 1)))
        self.backgrounds.append(Background(
            self.screen, self.camera, CLIFFCLOUDS, 0.1, (1.1, 0.1), (0.6, 1)))
        self.backgrounds.append(Background(
            self.screen, self.camera, CLIFFSEA, 0.25, (-0.1, 0.8), (1.2, 0.5)))
        self.backgrounds.append(Background(
            self.screen, self.camera, CLIFFSEA, 0.25, (1.1, 0.8), (1.2, 0.5)))
        self.backgrounds.append(Background(
            self.screen, self.camera, CLIFFGROUND, 0.5, (0.2, 1.1), (1.2, 0.5)))

    def new_objs_from_map(self):
        self.knights_pos = []  # Record the knight generation site position.
        # Create sprites.
        for tile_object in self.map.tmxdata.objects:
            # Each object is a dict. Keys are properties.
            if tile_object.type == 'player':
                if tile_object.name == self.player_pos:
                    self.player = HorizontalPlayer(
                        self, tile_object.x * self.size_multiplier, tile_object.y * self.size_multiplier, 250, 5, 5, self.size_multiplier)
            if tile_object.name == 'obstacle':
                Obstacle(self, tile_object.x * self.size_multiplier, tile_object.y * self.size_multiplier,
                         tile_object.width * self.size_multiplier, tile_object.height * self.size_multiplier)
            elif tile_object.name == 'invisible_obstacle':
                InvisibleObstacle(self, tile_object.x * self.size_multiplier, tile_object.y * self.size_multiplier,
                                  tile_object.width * self.size_multiplier, tile_object.height * self.size_multiplier)
            elif tile_object.name == 'knight':
                self.knights_pos.append(
                    (tile_object.x * self.size_multiplier, tile_object.y * self.size_multiplier))
            elif tile_object.name == 'tips':
                self.enter_rects['tips'] = pg.Rect(self.size_multiplier * tile_object.x, self.size_multiplier * tile_object.y,
                                                   self.size_multiplier * tile_object.width, self.size_multiplier * tile_object.height)
            elif tile_object.name == 'game_begin':
                self.enter_rects['game_begin'] = pg.Rect(self.size_multiplier * tile_object.x, self.size_multiplier * tile_object.y,
                                                         self.size_multiplier * tile_object.width, self.size_multiplier * tile_object.height)

    def new_text(self):
        # tips text
        Text(self, self.map_img, 'Infinite mode.', c.TICKETING, 20, c.WHITE, (-30,
             self.map_rect.height / 2), (20, self.map_rect.height * 16 / 40), self.tips_text_group)
        Text(self, self.map_img, 'You will be healed every 5 rounds.', c.TICKETING, 20, c.WHITE, (-30,
             self.map_rect.height / 2), (20, self.map_rect.height * 17 / 40), self.tips_text_group)
        Text(self, self.map_img, 'Try to survive!', c.TICKETING, 20, c.WHITE, (-30,
             self.map_rect.height / 2), (20, self.map_rect.height * 18 / 40), self.tips_text_group)
        # player info text
        Text(self, self.screen, 'Hv:'+str(self.player.hv), c.BACKTO1982, 15,
             c.AQUA, (30, -30), (30, 30), self.player_info_text_group)
        Text(self, self.screen, 'FireBall:'+str(self.player.fire_ball_amount), c.BACKTO1982, 15,
             c.AQUA, (120, -30), (120, 30), self.player_info_text_group)
        Text(self, self.screen, 'Enemies: 0/0', c.BACKTO1982, 15,
             c.AQUA, (280, -30), (280, 30), self.player_info_text_group)  # enemies killed
        # round text
        self.round_text = Text(self, self.screen, 'ROUND:'+str(self.game_round), c.TICKETING, 40,
                               c.AQUA, (220, -30), (220, 170), self.round_text_group)

    def new_music(self):
        self.sounds = []
        # Set sounds and music.
        self.confirm_sound = pg.mixer.Sound(c.CONFIRMSOUND)
        self.confirm_sound.set_volume(c.sound_volume)
        self.explosion_sound = pg.mixer.Sound(c.EXPLOSIONSOUND)
        self.explosion_sound.set_volume(c.sound_volume * 8)
        self.heal_sound = pg.mixer.Sound(c.HEALSOUND)
        self.heal_sound.set_volume(c.sound_volume)
        # Append all sounds to the list.
        self.sounds.append(self.confirm_sound)
        self.sounds.append(self.explosion_sound)
        self.sounds.append(self.player.slash_sound)
        self.sounds.append(self.player.throw_fire_ball_sound)
        self.sounds.append(self.heal_sound)
        pg.mixer.music.load(c.INFINITEMODEBGM)
        pg.mixer.music.set_volume(c.bgm_volume)

    def begin_game(self):
        """Begin the game, start the game round and play the bgm."""
        if self.player.rect.colliderect(self.enter_rects['game_begin']) and not self.game_begin:
            self.game_begin = True  # Begin game.
            # Play bgm.
            pg.mixer.music.play(loops=-1, fade_ms=2000)
            self.game_round += 1  # Begin round 1.
            # Update round text.
            self.round_text.update('ROUND: '+str(self.game_round))
            self.show_round_text = True  # Show round text.
            self.round_text_last_update = pg.time.get_ticks()

    def begin_next_round(self):
        """Plus the game ground and get ready to show the game round text."""
        if self.game_begin and not (self.show_round_text or self.generate_enemies) and len(self.enemies) == 0:
            self.game_round += 1
            self.round_text.update('ROUND: '+str(self.game_round))
            self.show_round_text = True
            self.round_text_last_update = pg.time.get_ticks()

    def heal_player(self):
        """Heal player every 5 rounds."""
        if self.game_round % 5 == 0 and self.game_begin:
            if self.ready_to_heal_player:
                self.ready_to_heal_player = False
                self.player.hv += 5
                if self.player.hv > 5:
                    self.player.hv = 5
                self.heal_sound.play()
        else:
            self.ready_to_heal_player = True

    def show_exit_selection_box(self):
        """Show selection box and information."""
        sb = SelectionBox(self.clock, self.screen, self.display, 'You reached: '+str(
            self.game_round), c.BACKTO1982, 20, self.glo, ('restart', 15), ('exit', 15))
        if sb.main():
            self.next_scene = ['scene_selection_menu', None]
        else:
            self.next_scene = ['infinite_mode_cliff', 'player01']

    def event_loop(self):
        """the event loop of the game"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                # Display the settings menu.
                if event.key == pg.K_ESCAPE:
                    self.show_settings_menu()
                # Detect the length of pressed key l.
                if event.key == pg.K_l and not self.player.press_key_l:
                    self.press_key_l()

            elif event.type == pg.KEYUP:
                if event.key == pg.K_l and self.player.press_key_l:
                    self.release_key_l()
        # Detect the event of the enemies.
        for sprite in self.enemies:
            # Fire ball attacks the enemy.
            self.fire_ball_hits_enemy(sprite)
            # Player attacks the enemy.
            self.player_slashes_enemy(sprite)

            # If the enemy has not been slain, the player may be hit.
            if not sprite.slain:
                # If player collides the body of the enemy, player would be hit.
                self.player_collides_enemy(sprite)
                # The enemy attacks the player.
                self.enemy_slashes_player(sprite)
            # if the enemy is slain
            else:
                self.new_enemy_killed_particles(sprite)
            # Find if the enemy still exists.
            if not sprite.exists:
                # If the enemy doesn't exist any longer, remove it from all the groups it belongs
                self.all_sprites.remove(sprite)
                self.enemies.remove(sprite)
        # Detect if the fire ball still exists.
        for fire_ball in self.fire_balls:
            if not fire_ball.exists:
                self.fire_balls.remove(fire_ball)
                self.all_sprites.remove(fire_ball)
        # Detect if the player still exists.
        if self.player.hv < 1:
            self.show_exit_selection_box()
        # Detect whether to show tips or not.
        self.show_tips()
        # Detect whether to begin the game or not.
        self.begin_game()
        # If all enemies have been killed, begin the next round.
        self.begin_next_round()
        # Heal player every 5 rounds.
        self.heal_player()
        # Detect if to create enemies.
        self.new_enemies()

    def new_enemies(self):
        """If it's the time to generate enemies, new enemies by the game round."""
        if self.generate_enemies:
            # Determine enemy generation amount.
            if 0 < self.game_round <= 3:
                self.generation_amount = 3
            elif 4 <= self.game_round <= 10:
                self.generation_amount = self.game_round
            else:
                self.generation_amount = 10
            # Choose the enemy position.(random)
            knight_pos = self.knights_pos[randint(
                0, len(self.knights_pos) - 1)]
            # Generate an enemy half a sec.
            if pg.time.get_ticks() - self.generate_enemies_last_update > self.generate_enemies_interval:
                # Generate different kinds of enemy by the game round.
                if 0 < self.game_round <= 2:
                    Knight(self, '01', knight_pos[0],
                           knight_pos[1], randint(30, 40), 1, self.size_multiplier)
                elif 3 <= self.game_round <= 6:
                    Knight(self, '02', knight_pos[0],
                           knight_pos[1], randint(40, 60), 2, self.size_multiplier)
                elif self.game_round >= 7:
                    Knight(self, '03', knight_pos[0],
                           knight_pos[1], randint(60, 80), 3, self.size_multiplier)
                # Update the enemy generation counter.
                self.enemy_generation_counter += 1
                self.generate_enemies_last_update = pg.time.get_ticks()
            # If the counter reaches the amount, stop generating enemies.
            if self.enemy_generation_counter == self.generation_amount:
                self.generate_enemies = False
                # Reset the counter.
                self.enemy_generation_counter = 0

    def draw_round_text(self):
        """If it's the time to show round text, Update and draw the round text.
            Otherwise do nothing."""
        # If it's the time to show round text.
        if self.show_round_text:
            if pg.time.get_ticks() - self.round_text_last_update < self.round_text_interval:
                self.round_text.update()
                self.round_text.draw()
            else:
                self.show_round_text = False
                # Put the round text to initial position.
                self.round_text.update_init_pos((300, -30))
                # Generate enemies.
                self.generate_enemies = True

    def draw(self):
        """Draw components."""
        self.draw_components()
        # Draw round text.
        self.draw_round_text()
        # Scale the scene surf to the game window size.
        self.display.blit(pg.transform.scale(
            self.screen, (self.glo.display_width, self.glo.display_height)), (0, 0))

    def main(self):
        """The main skeleton of the game process."""
        self.load_data(c.INFINITEMODECLIFF)
        self.new()
        self.fade_in()
        self.main_loop()

    def update_player_info(self):
        # Update player info
        self.player_info_text_group.sprites()[0].update(
            'Hv: '+str(self.player.hv))
        self.player_info_text_group.sprites()[1].update(
            'FireBall: '+str(self.player.fire_ball_amount))
        if self.game_begin and not self.generate_enemies:
            self.player_info_text_group.sprites()[2].update(
                'Enemies: '+str(self.generation_amount -
                                len(self.enemies))+'/'+str(self.generation_amount))
