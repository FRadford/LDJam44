import pygame
import pygameplus
import objects

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Game(object):
    def __init__(self, width, height):
        # pygame setup / screen init
        pygame.init()
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))

        # "camera" to control view of game world
        self.camera = pygameplus.objects.Camera(pygameplus.objects.simple_camera, (self.width, self.height))

        # state variables
        self.clock = pygame.time.Clock()
        self.target_fps = 60
        self.keys = None
        self.running = True

        # spritesheets
        self.mage = pygameplus.helpers.SpriteSheet("assets/sprites/Bloodmage.png")
        self.mage_list = self.mage.split_sheet(pygame.Rect(0, 0, 16, 16))
        self.skeleton = pygameplus.helpers.SpriteSheet("assets/sprites/Skeleboi.png")

        # group setup
        self.all_sprites = pygame.sprite.Group()
        self.colliders = pygame.sprite.Group()
        self.arena = objects.Arena(6)

        self.player = objects.Mage(432, 432, self.mage_list, scale=6)
        self.player.add(self.all_sprites, self.colliders)

        self.diagonal_factor = 1.8

        self.main_loop()

    def main_loop(self):
        while self.running:
            self.update()
            self.event_loop()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.target_fps)

    def update(self):
        self.keys = pygame.key.get_pressed()
        self.all_sprites.update(self.colliders, self.screen, self.camera)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.running = False

        # There's got to be a better way!
        # Seperate state for each of 8 directions, mostly so that the animation can be changed
        if self.keys[pygame.K_w] and not self.keys[pygame.K_a] and not self.keys[pygame.K_s] and not self.keys[pygame.K_d]:
            self.player.move(0, -self.player.speed, self.colliders)
        if not self.keys[pygame.K_w] and self.keys[pygame.K_a] and not self.keys[pygame.K_s] and not self.keys[pygame.K_d]:
            self.player.move(-self.player.speed, 0, self.colliders)
        if not self.keys[pygame.K_w] and not self.keys[pygame.K_a] and self.keys[pygame.K_s] and not self.keys[pygame.K_d]:
            self.player.move(0, self.player.speed, self.colliders)
        if not self.keys[pygame.K_w] and not self.keys[pygame.K_a] and not self.keys[pygame.K_s] and self.keys[pygame.K_d]:
            self.player.move(self.player.speed, 0, self.colliders)
        if self.keys[pygame.K_w] and not self.keys[pygame.K_a] and not self.keys[pygame.K_s] and self.keys[pygame.K_d]:
            self.player.move(self.player.speed / self.diagonal_factor, -(self.player.speed / self.diagonal_factor), self.colliders)
        if self.keys[pygame.K_w] and self.keys[pygame.K_a] and not self.keys[pygame.K_s] and not self.keys[pygame.K_d]:
            self.player.move(-(self.player.speed / self.diagonal_factor), -(self.player.speed / self.diagonal_factor), self.colliders)
        if not self.keys[pygame.K_w] and not self.keys[pygame.K_a] and self.keys[pygame.K_s] and self.keys[pygame.K_d]:
            self.player.move(self.player.speed / self.diagonal_factor, self.player.speed / self.diagonal_factor, self.colliders)
        if not self.keys[pygame.K_w] and self.keys[pygame.K_a] and self.keys[pygame.K_s] and not self.keys[pygame.K_d]:
            self.player.move(-(self.player.speed / self.diagonal_factor), self.player.speed / self.diagonal_factor, self.colliders)
        if self.keys[pygame.K_SPACE]:
            self.player.attack()

    def draw(self):
        self.screen.fill(WHITE)
        self.arena.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))


if __name__ == "__main__":
    game = Game(960, 960)