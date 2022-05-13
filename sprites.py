#!/usr/bin/env python
import pygame as pg
from constants import *
import constants as c
from random import randint
from tilemap import collide_rect, collide_body_rect


__author__ = 'Geoff Yulong Li'


class HorizontalPlayer(pg.sprite.Sprite):
    def __init__(self, scene, x, y, speed, hv, fire_ball_amount, size_multiplier) -> None:
        # super().__init__(scene, x, y, speed, size_multiplier)
        self.groups = scene.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size_multiplier = size_multiplier
        self.sprite_sheet = pg.image.load(FIGHTER)  # Load sprite sheet image.
        self.load_images_from_sheet()  # Load sprite sheet.
        self.scene = scene
        # Get rects
        self.rect = pg.Rect(x - 21 * self.size_multiplier, y - 12 * self.size_multiplier,
                            53 * self.size_multiplier, 29 * self.size_multiplier)
        self.body_rect = pg.Rect(
            x, y, 11 * self.size_multiplier, 17 * self.size_multiplier)
        self.attack_rect = None
        # Set player attributes.
        self.g = 30  # gravity
        self.player_speed = speed
        self.jump_height = -700  # jump height
        self.state = FACING_RIGHT
        self.attack_dir = None
        self.hv = hv
        self.fire_ball_amount = fire_ball_amount
        self.vel = [0, 0]   # Use the vector instead of the vx, vy.
        self.pos = [x, y]   # Use the position instead of the x, y.
        self.state = FACING_RIGHT  # Set the initial state.
        # img and rect
        self.image = self.all_images[0][0]  # Set the initial image.
        # animation settings
        self.image_index = 0  # It's used to traverse the animation images.
        self.image_interval = 50
        self.last_update = 0
        self.invincible_last_update = 0
        self.invincible_interval = 500
        # Set fire ball
        self.fire_ball_settings()
        # Set booleans.
        self.set_booleans()
        # Set sounds
        self.set_sounds()

    def set_sounds(self):
        self.slash_sound = pg.mixer.Sound(SLASHSOUND)
        self.slash_sound.set_volume(c.sound_volume)
        self.throw_fire_ball_sound = pg.mixer.Sound(THROWFIREBALLSOUND)
        self.throw_fire_ball_sound.set_volume(c.sound_volume)

    def fire_ball_settings(self):
        self.press_key_l = False
        self.press_key_l_begin = 0  # the beginning time of the press
        self.press_key_l_duration = 0  # the duration of the press
        # If it's true, the player will throw a new fire ball.
        self.throw_fire_ball = False

    def set_booleans(self):
        """Set up player booleans."""
        self.jumping = False
        self.invincible = False
        self.attacking = False
        self.begin_attack_animation = True

    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()
        # Cut the image.
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        image = pg.transform.scale(image,
                                   (int(rect.width * self.size_multiplier),
                                    int(rect.height * self.size_multiplier)))
        return image

    def load_images_from_sheet(self):
        """Load player animation frame by get_image() method."""
        self.right_frame = []
        self.left_frame = []
        self.facing_right_frame = []
        self.facing_left_frame = []
        self.attack_right_frame = []
        self.attack_left_frame = []
        # Images for the player
        right_images = [self.get_image(6, 82, 53, 29),
                        self.get_image(70, 82, 53, 29),
                        self.get_image(134, 83, 53, 29),
                        self.get_image(198, 83, 53, 29),
                        self.get_image(262, 81, 53, 29),
                        self.get_image(326, 81, 53, 29)]
        attack_right_images = [self.get_image(6, 275, 53, 29),
                               self.get_image(69, 275, 53, 29),
                               self.get_image(134, 275, 53, 29),
                               self.get_image(199, 275, 53, 29),
                               self.get_image(262, 275, 53, 29),
                               self.get_image(325, 275, 53, 29),
                               ]
        facing_right_images = [self.get_image(6, 19, 53, 29),
                               self.get_image(70, 19, 53, 29),
                               self.get_image(134, 19, 53, 29),
                               self.get_image(198, 19, 53, 29),
                               self.get_image(262, 19, 53, 29)]

        # left
        self.left_frame.append(pg.transform.flip(right_images[0], True, False))
        self.left_frame.append(pg.transform.flip(right_images[1], True, False))
        self.left_frame.append(pg.transform.flip(right_images[2], True, False))
        self.left_frame.append(pg.transform.flip(right_images[3], True, False))
        self.left_frame.append(pg.transform.flip(right_images[4], True, False))
        self.left_frame.append(pg.transform.flip(right_images[5], True, False))
        # right
        self.right_frame.append(right_images[0])
        self.right_frame.append(right_images[1])
        self.right_frame.append(right_images[2])
        self.right_frame.append(right_images[3])
        self.right_frame.append(right_images[4])
        self.right_frame.append(right_images[5])
        # facing left
        self.facing_left_frame.append(pg.transform.flip(
            facing_right_images[0], True, False))
        self.facing_left_frame.append(pg.transform.flip(
            facing_right_images[1], True, False))
        self.facing_left_frame.append(pg.transform.flip(
            facing_right_images[2], True, False))
        self.facing_left_frame.append(pg.transform.flip(
            facing_right_images[3], True, False))
        self.facing_left_frame.append(pg.transform.flip(
            facing_right_images[4], True, False))
        # facing right
        self.facing_right_frame.append(facing_right_images[0])
        self.facing_right_frame.append(facing_right_images[1])
        self.facing_right_frame.append(facing_right_images[2])
        self.facing_right_frame.append(facing_right_images[3])
        self.facing_right_frame.append(facing_right_images[4])
        # attack right
        self.attack_right_frame.append(attack_right_images[0])
        self.attack_right_frame.append(attack_right_images[1])
        self.attack_right_frame.append(attack_right_images[2])
        self.attack_right_frame.append(attack_right_images[3])
        self.attack_right_frame.append(attack_right_images[4])
        self.attack_right_frame.append(attack_right_images[5])
        # attack left
        self.attack_left_frame.append(
            pg.transform.flip(attack_right_images[0], True, False))
        self.attack_left_frame.append(
            pg.transform.flip(attack_right_images[1], True, False))
        self.attack_left_frame.append(
            pg.transform.flip(attack_right_images[2], True, False))
        self.attack_left_frame.append(
            pg.transform.flip(attack_right_images[3], True, False))
        self.attack_left_frame.append(
            pg.transform.flip(attack_right_images[4], True, False))
        self.attack_left_frame.append(
            pg.transform.flip(attack_right_images[5], True, False))

        # all images
        self.all_images = [
            self.right_frame,
            self.left_frame,
            self.facing_right_frame,
            self.facing_left_frame,
            self.attack_right_frame,
            self.attack_left_frame]

    def update_animation(self):
        """Update the animation."""
        if self.attacking:
            self.animate_attack()
        else:
            if self.state == LEFT or self.state == RIGHT:
                self.animate_moving()
            if self.state == FACING_RIGHT or self.state == FACING_LEFT:
                self.animate_facing()

    def animate_facing(self):
        """Set up the facing images."""
        images = None
        if self.state == FACING_LEFT:
            images = self.all_images[3]
        elif self.state == FACING_RIGHT:
            images = self.all_images[2]
        if self.image_index >= len(images):
            self.image_index = 0
        else:
            self.image = images[self.image_index]
            self.image_index += 1

    def animate_moving(self):
        """Set up the images while moving."""
        images = None
        if self.state == LEFT:
            images = self.all_images[1]
        elif self.state == RIGHT:
            images = self.all_images[0]
        if self.image_index >= len(images):
            self.image_index = 0
        else:
            self.image = images[self.image_index]
            self.image_index += 1

    def animate_attack(self):
        """Set up the attack animation."""
        images = None
        # Load images by attack direction.
        if self.attack_dir == 'attack_right':
            images = self.all_images[4]
        elif self.attack_dir == 'attack_left':
            images = self.all_images[5]
        # If it's the beginning of the attack animation, set the image index 0.
        if self.begin_attack_animation:
            self.image_index = 0

        if self.image_index == 0:
            # Record that it's not the beginning of the animation any more.
            self.begin_attack_animation = False
            self.image = images[self.image_index]
            self.image_index += 1
        elif self.image_index == 1:
            self.image = images[self.image_index]
            self.image_index += 1
        elif self.image_index == 2:
            # Set up the attack rect.
            if self.attack_dir == 'attack_right':
                self.attack_rect = pg.Rect(
                    self.rect.centerx, self.rect.top, self.rect.width / 2, self.rect.height)
            elif self.attack_dir == 'attack_left':
                self.attack_rect = pg.Rect(
                    self.rect.x, self.rect.top, self.rect.width / 2, self.rect.height)
            self.image = images[self.image_index]
            self.image_index += 1
            # Play slash sound.
            self.slash_sound.play(maxtime=1000)
        elif 2 < self.image_index < len(images):
            self.image = images[self.image_index]
            self.image_index += 1
        # the end of the attack animation
        elif self.image_index >= len(images):
            self.attacking = False  # Set player attacking state false.
            self.begin_attack_animation = True
            self.attack_rect = None
            self.attack_dir = None

    def stand(self):
        """Set up the static state of the player."""
        self.vel[0] -= self.vel[0] / 10
        if self.state == LEFT:
            self.state = FACING_LEFT
        elif self.state == RIGHT:
            self.state = FACING_RIGHT

    def get_keys(self):
        """This method is called once each game loop.
            It checks keys and sets corresponding state of the player."""
        keys = pg.key.get_pressed()
        if keys[K_a] or keys[K_d]:
            self.move(keys)
        if keys[K_k] and not self.jumping:
            self.jump()
        if keys[K_a] == keys[K_d] == 0:
            self.stand()
        if keys[K_j] and not (self.attacking or self.invincible):
            self.attack_dir = self.detect_attack()

    def detect_throw_fire_ball(self):
        """etect wheather to throw the fire ball the initial state of the fire ball that will be thrown."""
        if self.fire_ball_amount > 0:
            if self.throw_fire_ball:
                fire_ball_vel = [0, 0]  # the velocity of the fire ball
                # Adjust the duration.
                if self.press_key_l_duration < 200:
                    self.press_key_l_duration = 200
                elif self.press_key_l_duration > 500:
                    self.press_key_l_duration = 600
                # Adjust the fire ball direction by the player state.
                if self.state == RIGHT or self.state == FACING_RIGHT:
                    fire_ball_vel[0] = self.press_key_l_duration
                elif self.state == LEFT or self.state == FACING_LEFT:
                    fire_ball_vel[0] = -self.press_key_l_duration
                fire_ball_vel[1] = -self.press_key_l_duration
                # Create a new fire ball.
                FireBall(
                    self.scene, self.pos[0], self.pos[1], fire_ball_vel, self.size_multiplier)
                self.throw_fire_ball = False
                # Minus the fire ball amount.
                self.fire_ball_amount -= 1
                # Play throw fire ball sound.
                self.throw_fire_ball_sound.play(fade_ms=500, maxtime=1000)
        else:
            self.throw_fire_ball = False

    def detect_attack(self):
        """The player will begin attack when this method is called.
            This method detect the direction the player will attack."""
        self.attacking = True
        if self.state == RIGHT or self.state == FACING_RIGHT:
            return 'attack_right'
        elif self.state == LEFT or self.state == FACING_LEFT:
            return 'attack_left'

    def move(self, keys):
        """Set the state and velocity of the player according to the pressed keys."""
        if keys[K_a]:
            self.state = LEFT
            if self.vel[0] != -self.player_speed:
                self.vel[0] += (-self.player_speed - self.vel[0]) / 5
        if keys[K_d]:
            self.state = RIGHT
            if self.vel[0] != self.player_speed:
                self.vel[0] += (self.player_speed - self.vel[0]) / 5

    def fall(self):
        """The gravity makes the player fall."""
        self.vel[1] += self.g * self.scene.dt * 60
        if self.vel[1] > 2 * self.g:
            self.jumping = True

    def jump(self):
        """Change the velocity of y direction to make player jump."""
        self.vel[1] += self.jump_height - self.vel[1]
        self.jumping = True

    def update_pos(self):
        '''Update the position of the player.'''
        # Update the player position.
        self.pos[0] += self.vel[0] * self.scene.dt
        self.pos[1] += self.vel[1] * self.scene.dt
        # Update the rect and the body rect.
        self.body_rect.x = self.pos[0]
        self.rect.x = self.pos[0] - 21 * self.size_multiplier
        self.collide_with_walls(self, self.scene.walls, 'x')
        self.body_rect.y = self.pos[1]
        self.rect.y = self.pos[1] - 12 * self.size_multiplier
        self.collide_with_walls(self, self.scene.walls, 'y')

    def update(self):
        """Update the player."""
        # Update the animation.
        if pg.time.get_ticks() - self.last_update > self.image_interval:
            self.update_animation()
            self.last_update = pg.time.get_ticks()
        # If the player is invincible, make the player alternate transparent.
        if self.invincible:
            if pg.time.get_ticks() - self.invincible_last_update > self.invincible_interval:
                self.invincible = False
        self.update_image_alpha()
        self.get_keys()
        self.detect_throw_fire_ball()
        self.fall()
        self.update_pos()

    def update_image_alpha(self):
        """Update the alpha of the image.
            If player is invincible, set image the alternate alpha.
            If player is vincible, set image normal."""
        if self.invincible:
            if self.image.get_alpha() != 0:
                self.image.set_alpha(0)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

    def is_hit(self):
        """This method will be called if the player is hit."""
        # Minus the hv.
        self.hv -= 1
        # Set the player invincible.
        if self.invincible == False:
            self.invincible = True
            self.invincible_last_update = pg.time.get_ticks()

    def collide_with_walls(self, sprite, group, dir):
        """This method detects if the play collides with walss or not."""
        if dir == 'x':
            hits = pg.sprite.spritecollide(
                sprite, group, False, collide_body_rect)
            if hits:
                # That means we are colliding the left of the wall.
                if sprite.vel[0] > 0:
                    sprite.pos[0] = hits[0].rect.left - sprite.body_rect.width
                # That means we are colliding the right of the wall.
                if sprite.vel[0] < 0:
                    sprite.pos[0] = hits[0].rect.right
                sprite.vel[0] = 0
                sprite.body_rect.x = sprite.pos[0]
                sprite.rect.x = sprite.pos[0] - 21 * self.size_multiplier
        if dir == 'y':
            hits = pg.sprite.spritecollide(
                sprite, group, False, collide_body_rect)
            if hits:
                if sprite.vel[1] > 0:
                    sprite.pos[1] = hits[0].rect.top - sprite.body_rect.height
                    self.jumping = False  # back to ground
                if sprite.vel[1] < 0:
                    sprite.pos[1] = hits[0].rect.bottom
                sprite.vel[1] = 0
                sprite.body_rect.y = sprite.pos[1]
                sprite.rect.y = sprite.pos[1] - 12 * self.size_multiplier


class Knight(pg.sprite.Sprite):
    def __init__(self, scene, type, x, y, speed, hv, size_multiplier) -> None:
        self.groups = scene.all_sprites, scene.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size_multiplier = size_multiplier
        self.type = {'01': KNIGHT01, '02': KNIGHT02, '03': KNIGHT03}
        # Load sprite_sheet image.
        self.sprite_sheet = pg.image.load(self.type[type])
        self.load_images_from_sheet()  # Load player sprite sheet.
        self.scene = scene
        # Set up knight attributes.
        self.g = 30  # gravity
        self.type = type  # 01 or 02 or 03
        self.jump_height = -700  # jump height
        self.speed = speed
        self.move_dir = 'r'  # Movement direction.
        self.vel = [0, 0]
        self.pos = [x, y]  # body pos
        self.state = RIGHT  # Set the initial state.
        self.hv = hv
        # Set up knight image and rects.
        self.image = self.all_images[1][0]  # Set the initial image.
        self.rect = pg.Rect(x - 21 * self.size_multiplier, y - 12 * self.size_multiplier,
                            53 * self.size_multiplier, 29 * self.size_multiplier)
        self.body_rect = pg.Rect(
            x, y, 11 * self.size_multiplier, 17 * self.size_multiplier)
        self.attack_rect = None
        # Set up animation
        self.image_index = 0  # It's used to traverse the animation images.
        self.image_interval = 50
        self.last_update = 0
        self.invincible_last_update = 0
        self.invincible_interval = 500
        # Set up knight booleans.
        self.set_booleans()
        # Set sounds.
        self.set_sounds()

    def set_sounds(self):
        """Set up sounds."""
        self.slash_sound = pg.mixer.Sound(SLASHSOUND)
        self.slash_sound.set_volume(c.sound_volume)
        self.be_hit_sound = pg.mixer.Sound(BEHITSOUND)
        self.be_hit_sound.set_volume(c.sound_volume * 2)

    def set_booleans(self):
        """Set up booleans."""
        self.attacking = False  # Set attack state.
        # Get ready to show attack animation.
        self.begin_attack_animation = True
        self.slain = False
        self.begin_slain_animation = True  # Get ready to show slain animation.
        self.exists = True  # It the knight is slain, he won't exist any more.
        self.invincible = False

    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()
        # Cut the image.
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        image = pg.transform.scale(image,
                                   (int(rect.width * self.size_multiplier),
                                    int(rect.height * self.size_multiplier)))
        return image

    def load_images_from_sheet(self):
        """Extracts Mario images from the sprite sheet(1 image)."""
        self.right_frame = []
        self.left_frame = []
        self.attack_left_frame = []
        self.attack_right_frame = []
        self.slain_right_frame = []
        self.slain_left_frame = []

        # Images for the player
        right_images = [self.get_image(6, 82, 53, 29),
                        self.get_image(70, 82, 53, 29),
                        self.get_image(134, 83, 53, 29),
                        self.get_image(198, 83, 53, 29),
                        self.get_image(262, 81, 53, 29),
                        self.get_image(326, 81, 53, 29)]
        attack_right_images = [self.get_image(6, 275, 53, 29),
                               self.get_image(69, 275, 53, 29),
                               self.get_image(134, 275, 53, 29),
                               self.get_image(199, 275, 53, 29),
                               self.get_image(262, 275, 53, 29),
                               self.get_image(325, 275, 53, 29),
                               ]
        slain_right_images = [self.get_image(6, 403, 53, 29),
                              self.get_image(71, 403, 53, 29),
                              self.get_image(135, 403, 53, 29),
                              self.get_image(197, 403, 53, 29),
                              self.get_image(262, 403, 53, 29),
                              self.get_image(326, 403, 53, 29)]

        # left
        self.left_frame.append(pg.transform.flip(right_images[0], True, False))
        self.left_frame.append(pg.transform.flip(right_images[1], True, False))
        self.left_frame.append(pg.transform.flip(right_images[2], True, False))
        self.left_frame.append(pg.transform.flip(right_images[3], True, False))
        self.left_frame.append(pg.transform.flip(right_images[4], True, False))
        self.left_frame.append(pg.transform.flip(right_images[5], True, False))
        # right
        self.right_frame.append(right_images[0])
        self.right_frame.append(right_images[1])
        self.right_frame.append(right_images[2])
        self.right_frame.append(right_images[3])
        self.right_frame.append(right_images[4])
        self.right_frame.append(right_images[5])
        # attack right
        self.attack_right_frame.append(attack_right_images[0])
        self.attack_right_frame.append(attack_right_images[1])
        self.attack_right_frame.append(attack_right_images[2])
        self.attack_right_frame.append(attack_right_images[3])
        self.attack_right_frame.append(attack_right_images[4])
        self.attack_right_frame.append(attack_right_images[5])
        # attack left
        self.attack_left_frame.append(
            pg.transform.flip(attack_right_images[0], True, False))
        self.attack_left_frame.append(
            pg.transform.flip(attack_right_images[1], True, False))
        self.attack_left_frame.append(
            pg.transform.flip(attack_right_images[2], True, False))
        self.attack_left_frame.append(
            pg.transform.flip(attack_right_images[3], True, False))
        self.attack_left_frame.append(
            pg.transform.flip(attack_right_images[4], True, False))
        self.attack_left_frame.append(
            pg.transform.flip(attack_right_images[5], True, False))
        # slain right
        self.slain_right_frame.append(slain_right_images[0])
        self.slain_right_frame.append(slain_right_images[1])
        self.slain_right_frame.append(slain_right_images[2])
        self.slain_right_frame.append(slain_right_images[3])
        self.slain_right_frame.append(slain_right_images[4])
        self.slain_right_frame.append(slain_right_images[5])
        # slain left
        self.slain_left_frame.append(pg.transform.flip(
            slain_right_images[0], True, False))
        self.slain_left_frame.append(pg.transform.flip(
            slain_right_images[1], True, False))
        self.slain_left_frame.append(pg.transform.flip(
            slain_right_images[2], True, False))
        self.slain_left_frame.append(pg.transform.flip(
            slain_right_images[3], True, False))
        self.slain_left_frame.append(pg.transform.flip(
            slain_right_images[4], True, False))
        self.slain_left_frame.append(pg.transform.flip(
            slain_right_images[5], True, False))

        # all images
        self.all_images = [self.right_frame,
                           self.left_frame,
                           self.attack_right_frame,
                           self.attack_left_frame,
                           self.slain_right_frame,
                           self.slain_left_frame]

    def update_animation(self):
        """Update the animation."""
        if self.slain:
            self.animate_slain()
        elif self.attacking:
            self.animate_attack()
        else:
            if self.state == LEFT or self.state == RIGHT:
                self.animate_moving(self.state)

    def animate_slain(self):
        images = None
        if self.state == RIGHT:
            images = self.all_images[4]
        elif self.state == LEFT:
            images = self.all_images[5]

        if self.begin_slain_animation:
            self.image_index = 0

        if self.image_index == 0:
            self.begin_slain_animation = False
            self.image = images[self.image_index]
            self.image_index += 1
        elif 0 < self.image_index < len(images):
            self.image = images[self.image_index]
            self.image_index += 1
        elif self.image_index >= len(images):
            self.exists = False
            self.begin_slain_animation = True

    def animate_attack(self):
        images = None
        if self.attack_dir == 'attack_right':
            images = self.all_images[2]
        elif self.attack_dir == 'attack_left':
            images = self.all_images[3]

        if self.begin_attack_animation:
            self.image_index = 0

        if self.image_index == 0:
            self.begin_attack_animation = False
            self.image = images[self.image_index]
            self.image_index += 1
        elif self.image_index == 1:
            self.image = images[self.image_index]
            self.image_index += 1
        elif self.image_index == 2:
            if self.attack_dir == 'attack_right':
                self.attack_rect = pg.Rect(
                    self.rect.centerx, self.rect.top, self.rect.width / 2, self.rect.height)
            elif self.attack_dir == 'attack_left':
                self.attack_rect = pg.Rect(
                    self.rect.x, self.rect.top, self.rect.width / 2, self.rect.height)
            self.image = images[self.image_index]
            self.image_index += 1
            # Play slash sound.
            self.slash_sound.play(maxtime=1000)
        elif 2 < self.image_index < len(images):
            self.image = images[self.image_index]
            self.image_index += 1
        elif self.image_index >= len(images):
            self.attacking = False
            self.begin_attack_animation = True
            self.attack_rect = None
            self.attack_dir = None

    def animate_moving(self, state):
        """Set the images while moving."""
        images = None
        if self.state == LEFT:
            images = self.all_images[1]
        elif self.state == RIGHT:
            images = self.all_images[0]

        if self.image_index >= len(images):
            self.image_index = 0
        else:
            self.image = images[self.image_index]
            self.image_index += 1

    def is_slain(self):
        """This method will be called if the knight is slain."""
        self.slain = True

    def is_hit(self):
        """This mdthod will be called if the knight is hit."""
        # Minus the hv.
        self.hv -= 1
        # Play be hit sound.
        self.be_hit_sound.play(fade_ms=700)
        # Set the knight invincible.
        if self.invincible == False:
            self.invincible = True
            self.invincible_last_update = pg.time.get_ticks()

    def fall(self):
        self.vel[1] += self.g * self.scene.dt * 60
        if self.vel[1] > 2 * self.g:
            self.jumping = True

    def move(self, dir):
        """Set the state and velocity of the player according to the pressed keys."""
        if dir == 'r':
            self.state = RIGHT
            self.vel[0] += (self.speed - self.vel[0])
        elif dir == 'l':
            self.state = LEFT
            self.vel[0] += (-self.speed - self.vel[0])

    def stand(self):
        self.vel[0] = 0

    def update(self):
        # Update knight animation.
        if pg.time.get_ticks() - self.last_update > self.image_interval:
            self.update_animation()
            self.last_update = pg.time.get_ticks()
        # If set the knight vincible.
        if self.invincible:
            if pg.time.get_ticks() - self.invincible_last_update > self.invincible_interval:
                self.invincible = False
        # If the hv is less than 1, it shows the knight is slain.
        if self.hv < 1:
            self.is_slain()
        # If the knight has not been slain yet, update the knight.
        if not self.slain:
            self.fall()
            if self.attacking:
                self.stand()
            else:
                self.attack_dir = self.detect_player()
                self.move(self.move_dir)
            self.update_pos()

    def detect_player(self):
        """Detect wheather to attack and the direction of the attack."""
        if self.state == RIGHT:
            if 0 < self.scene.player.rect.centerx - self.body_rect.centerx < 45 and abs(self.scene.player.rect.centery - self.body_rect.centery) < 20:
                self.attacking = True
                return 'attack_right'
        elif self.state == LEFT:
            if 0 < self.body_rect.centerx - self.scene.player.rect.centerx < 45 and abs(self.scene.player.rect.centery - self.body_rect.centery) < 20:
                self.attacking = True
                return 'attack_left'

    def update_pos(self):
        '''Update the position of the player.'''
        # Update pos according to the vel.
        self.pos[0] += self.vel[0] * self.scene.dt
        self.pos[1] += self.vel[1] * self.scene.dt

        self.body_rect.x = self.pos[0]
        self.rect.x = self.pos[0] - 21 * self.size_multiplier
        self.collide_with_walls(self, self.scene.walls, 'x')
        self.collide_with_walls(self, self.scene.invisible_walls, 'x')
        self.body_rect.y = self.pos[1]
        self.rect.y = self.pos[1] - 12 * self.size_multiplier
        self.collide_with_walls(self, self.scene.walls, 'y')
        self.collide_with_walls(self, self.scene.invisible_walls, 'y')

    def collide_with_walls(self, sprite, group, dir):
        """This method detects if the play collides with walss or not."""
        if dir == 'x':
            hits = pg.sprite.spritecollide(
                sprite, group, False, collide_body_rect)
            if hits:
                # That means we are colliding the left of the wall.
                if sprite.vel[0] > 0:
                    sprite.pos[0] = hits[0].rect.left - sprite.body_rect.width
                    self.move_dir = 'l'
                # That means we are colliding the right of the wall.
                if sprite.vel[0] < 0:
                    sprite.pos[0] = hits[0].rect.right
                    self.move_dir = 'r'
                sprite.vel[0] = -sprite.vel[0]
                sprite.body_rect.x = sprite.pos[0]
                sprite.rect.x = sprite.pos[0] - 21 * self.size_multiplier

        if dir == 'y':
            hits = pg.sprite.spritecollide(
                sprite, group, False, collide_body_rect)
            if hits:
                if sprite.vel[1] > 0:
                    sprite.pos[1] = hits[0].rect.top - sprite.body_rect.height
                if sprite.vel[1] < 0:
                    sprite.pos[1] = hits[0].rect.bottom
                sprite.vel[1] = 0
                sprite.body_rect.y = sprite.pos[1]
                sprite.rect.y = sprite.pos[1] - 12 * self.size_multiplier


class FireBall(pg.sprite.Sprite):
    def __init__(self, scene, x, y, vel, size_multiplier) -> None:
        self.groups = scene.all_sprites, scene.fire_balls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size_multiplier = size_multiplier
        self.sprite_sheet = pg.image.load(FIREBALL)
        self.load_images_from_sheet()
        self.scene = scene
        # fire ball attributes
        self.g = 30  # gravity
        self.init_vel = (vel[0], vel[1])
        self.vel = [vel[0], vel[1]]
        self.pos = [x, y]  # body pos
        # surf and rect
        self.image = self.all_images[0][0]
        self.rect = pg.Rect(x, y, 15,
                            15)
        # animation settings
        self.image_index = 0  # It's used to traverse the animation images.
        self.image_interval = 50
        self.last_update = 0
        self.set_booleans()

    def set_booleans(self):
        self.hit = False  # If the fire ball hits the enemy.
        self.exists = True  # If the fire ball exists.

    def get_image(self, x, y, width, height):
        """Extracts image from sprite sheet"""
        image = pg.Surface([width, height])
        rect = image.get_rect()
        # Cut the image.
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        image = pg.transform.scale(image,
                                   (int(rect.width * self.size_multiplier),
                                    int(rect.height * self.size_multiplier)))
        return image

    def load_images_from_sheet(self):
        """Extracts Mario images from the sprite sheet(1 image)."""
        self.spin_frame = []

        # spin
        self.spin_frame.append(pg.transform.scale(self.get_image(
            94, 95, 305, 305), (15, 15)))
        self.spin_frame.append(pg.transform.scale(self.get_image(
            816, 94, 305, 305), (15, 15)))
        self.spin_frame.append(pg.transform.scale(self.get_image(
            1478, 110, 305, 305), (15, 15)))
        self.spin_frame.append(pg.transform.scale(self.get_image(
            2215, 111, 305, 305), (15, 15)))
        self.spin_frame.append(pg.transform.scale(self.get_image(
            2849, 101, 305, 305), (15, 15)))

        # all images
        self.all_images = [self.spin_frame]

    def animate_spin(self):
        """Set the images while moving."""
        images = self.all_images[0]

        if self.image_index >= len(images):
            self.image_index = 0
        else:
            self.image = images[self.image_index]
            self.image_index += 1

    def fall(self):
        self.vel[1] += self.g * self.scene.dt * 60

    def update_existence(self):
        if abs(self.vel[0]) < abs(self.init_vel[0] / 10) and abs(self.vel[1]) < abs(self.init_vel[1] / 10):
            self.exists = False

    # def detect_hit(self):
    #     hits = pg.sprite.spritecollide(
    #         self, self.scene.enemies, False, collide_another_body_rect)
    #     if hits:
    #         self.hit = True
    #         self.exists = False

    def update(self):
        # Update knight animation.
        if pg.time.get_ticks() - self.last_update > self.image_interval:
            self.animate_spin()
            self.last_update = pg.time.get_ticks()
        self.update_existence()
        # self.detect_hit()
        if self.exists:
            self.fall()
            self.update_pos()
            self.draw()

    def update_pos(self):
        '''Update the position of the player.'''
        # Update pos according to the vel.
        self.pos[0] += self.vel[0] * self.scene.dt
        self.pos[1] += self.vel[1] * self.scene.dt

        self.rect.x = self.pos[0]
        self.collide_with_walls(self, self.scene.walls, 'x')
        self.rect.y = self.pos[1]
        self.collide_with_walls(self, self.scene.walls, 'y')

    def collide_with_walls(self, sprite, group, dir):
        """This method detects if the play collides with walls or not."""
        if dir == 'x':
            hits = pg.sprite.spritecollide(sprite, group, False, collide_rect)
            if hits:
                # That means we are colliding the left of the wall.
                if sprite.vel[0] > 0:
                    sprite.pos[0] = hits[0].rect.left - sprite.rect.width
                # That means we are colliding the right of the wall.
                if sprite.vel[0] < 0:
                    sprite.pos[0] = hits[0].rect.right
                sprite.vel[0] = -sprite.vel[0] * 4 / 5
                sprite.vel[1] = sprite.vel[1] * 4 / 5
                sprite.rect.x = sprite.pos[0]
        if dir == 'y':
            hits = pg.sprite.spritecollide(sprite, group, False, collide_rect)
            if hits:
                if sprite.vel[1] > 0:
                    sprite.pos[1] = hits[0].rect.top - sprite.rect.height
                if sprite.vel[1] < 0:
                    sprite.pos[1] = hits[0].rect.bottom
                sprite.vel[1] = -sprite.vel[1] * 4 / 5
                sprite.vel[0] = sprite.vel[0] * 4 / 5
                sprite.rect.y = sprite.pos[1]

    def draw(self):
        self.scene.screen.blit(self.image, self.scene.camera.apply(self))


class Obstacle(pg.sprite.Sprite):
    def __init__(self, scene, x, y, width, height) -> None:
        self.groups = scene.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = scene
        self.rect = pg.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y


class InvisibleObstacle(pg.sprite.Sprite):
    def __init__(self, scene, x, y, width, height) -> None:
        # Obstacles are invisible. They don't have images.
        self.groups = scene.invisible_walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = scene
        self.rect = pg.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y


class SquareParticle(pg.sprite.Sprite):
    def __init__(self, scene, camera, x, y, color, vel, gravity) -> None:
        self.groups = scene.particles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.pos = [x, y]
        self.vel = vel
        self.timer = randint(10, 20)  # The time the particle would exist.
        self.ts = 0.2  # timer speed
        self.scene = scene
        self.camera = camera
        self.size = randint(3, 10)
        self.surf = pg.Surface((self.size, self.size))
        self.color_index = randint(0, len(color) - 1)
        self.surf.fill(color[self.color_index])
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.g = gravity

    def fall(self):
        self.vel[1] += self.g * self.scene.dt * 60

    def update_pos(self):
        self.pos[0] += self.vel[0] * self.scene.dt
        self.pos[1] += self.vel[1] * self.scene.dt
        self.rect.x = self.pos[0]
        self.collide_with_walls(self, self.scene.walls, 'x')
        self.rect.y = self.pos[1]
        self.collide_with_walls(self, self.scene.walls, 'y')

    def update(self):
        self.fall()
        self.update_pos()

    def collide_with_walls(self, sprite, group, dir):
        """This method detects if the play collides with walss or not."""
        if dir == 'x':
            hits = pg.sprite.spritecollide(sprite, group, False, collide_rect)
            if hits:
                # That means we are colliding the left of the wall.
                if sprite.vel[0] > 0:
                    sprite.pos[0] = hits[0].rect.left - sprite.rect.width
                # That means we are colliding the right of the wall.
                if sprite.vel[0] < 0:
                    sprite.pos[0] = hits[0].rect.right
                sprite.vel[0] = -sprite.vel[0]
                sprite.rect.x = sprite.pos[0]
        if dir == 'y':
            hits = pg.sprite.spritecollide(sprite, group, False, collide_rect)
            if hits:
                if sprite.vel[1] > 0:
                    sprite.pos[1] = hits[0].rect.top - sprite.rect.height
                if sprite.vel[1] < 0:
                    sprite.pos[1] = hits[0].rect.bottom
                sprite.vel[1] = -sprite.vel[1]
                sprite.rect.y = sprite.pos[1]

    def draw(self):
        self.scene.screen.blit(self.surf, self.camera.apply(self))
        self.timer -= self.ts
