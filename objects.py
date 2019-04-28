import pygameplus
import pygame
import pytmx


def scale_sprite(sprite, scale):
    return pygame.transform.scale(sprite, [int(x * scale) for x in sprite.get_size()])


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite, scale=1.0):
        super(Tile, self).__init__()
        if scale != 1.0:
            sprite = scale_sprite(sprite, scale)
        self.image = sprite.convert_alpha()
        self.rect = pygame.Rect((x * scale, y * scale), self.image.get_size())


class Arena(pygame.sprite.Group):
    def __init__(self, scale=1.0):
        super(Arena, self).__init__()
        self.scale = scale
        self.tmx_data = pytmx.load_pygame("assets/arena.tmx")

        self.create_arena()

    def create_arena(self):
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        for layer in self.tmx_data.visible_layers:
            for x, y, image in layer.tiles():
                self.add(Tile(x*tw, y*th, image, self.scale))


class Mage(pygameplus.objects.Player):
    def __init__(self, x, y, sprites, scale=1.0):
        super(Mage, self).__init__(x, y, None, scale)

        self.sprites = [scale_sprite(x, scale) for x in sprites]
        self.image = self.sprites[0]
        self.rect = pygame.Rect((x, y), self.image.get_size())
        self.speed = 8

        self.animations = {"Rotate": [0, 7], "Walk Front": [8, 11], "Walk Front-Right": [12, 15],
                           "Walk Right": [16, 19], "Walk Back-Right": [20, 23], "Walk Back": [24, 27],
                           "Walk Back-Left": [28, 31], "Walk Left": [32, 35], "Walk Front-Left": [36, 39],
                           "Attack Front": [40, 41], "Attack Front-Right": [42, 43], "Attack Right": [44, 45],
                           "Attack Back-Right": [46, 47], "Attack Back": [48, 49], "Attack Back-Left": [50, 51],
                           "Attack Left": [52, 53], "Attack Front-Left": [54, 55]}
        self.animation_delay = 10
        self.animation_range = [0, 0]
        self.frame = self.animation_range[0]
        self.play_once = False
        self.last_range = None

        self.cooldown = 200
        
    def next_frame(self, start_frame, end_frame):
        if self.play_once:
            if self.frame < end_frame:
                self.frame += 1
            else:
                self.play_once = False
                self.animation_range = self.last_range
        else:
            self.frame = self.frame + 1 if self.frame < end_frame else start_frame
        self.image = self.sprites[self.frame]

    def update(self, colliders, surface, cam):
        if self.animation_delay <= 0:
            self.next_frame(*self.animation_range)
            self.animation_delay = 10
        else:
            self.animation_delay -= 1

        self.cooldown -= 1
        super(Mage, self).update(colliders, surface, cam)

    def animate_attack(self):
        self.last_range = self.animation_range
        self.play_once = True

        for key in self.animations:
            if self.animation_range == self.animations[key] and not key.startswith("Attack"):
                self.animation_range = self.animations["Attack" + key[4:]]
                self.frame = self.animation_range[0]
                break

    def attack(self):
        if self.cooldown <= 0:
            self.animate_attack()
            self.cooldown = 20

    def move(self, dx, dy, colliders):
        previous_range = self.animation_range
        if dx > 0 and not dy:
            self.animation_range = self.animations["Walk Right"]
        if dx < 0 and not dy:
            self.animation_range = self.animations["Walk Left"]
        if not dx and dy > 0:
            self.animation_range = self.animations["Walk Front"]
        if not dx and dy < 0:
            self.animation_range = self.animations["Walk Back"]
        if dx > 0 and dy > 0:
            self.animation_range = self.animations["Walk Front-Right"]
        if dx > 0 and dy < 0:
            self.animation_range = self.animations["Walk Back-Right"]
        if dx < 0 and dy > 0:
            self.animation_range = self.animations["Walk Front-Left"]
        if dx < 0 and dy < 0:
            self.animation_range = self.animations["Walk Back-Left"]

        if previous_range != self.animation_range:
            self.frame = self.animation_range[0]
        super(Mage, self).move(dx, dy, colliders)


