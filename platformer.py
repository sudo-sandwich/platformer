import pygame
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 768
HEIGHT = 512

GRAVITY = .5

LEFT = -1
RIGHT = 1

class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, color):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):

    vspeed = 0
    platformsGroup = None

    def __init__(self, x, y, platformsGroup):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((32, 32))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.platformsGroup = platformsGroup

    def jump(self):

        self.rect.y += 1
        if pygame.sprite.spritecollideany(self, self.platformsGroup):
            self.vspeed -= 14
        self.rect.y -= 1

    def move(self, direction):

        self.rect.x += 5 * direction

        while direction == LEFT and pygame.sprite.spritecollideany(self, self.platformsGroup):
            self.rect.x += 1
        while direction == RIGHT and pygame.sprite.spritecollideany(self, self.platformsGroup):
            self.rect.x -= 1

    def update(self):

        self.rect.y += self.vspeed
        self.vspeed += GRAVITY

        if pygame.sprite.spritecollideany(self, self.platformsGroup):
            if self.vspeed > 0:
                self.vspeed = 0
                while pygame.sprite.spritecollideany(self, self.platformsGroup):
                    self.rect.y -= 1
            if not self.vspeed > 0:
                self.vspeed = 0
                while pygame.sprite.spritecollideany(self, self.platformsGroup):
                    self.rect.y += 1

class Controller():

    def __init__(self):

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("platformer")
        clock = pygame.time.Clock()

        platformsGroup = pygame.sprite.Group()
        allSpritesGroup = pygame.sprite.Group()

        player = Player(64, 350, platformsGroup)
        allSpritesGroup.add(player)

        self.makeLevel(platformsGroup, allSpritesGroup)

        oldKeys = pygame.key.get_pressed()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and not oldKeys[pygame.K_UP]:
                player.jump()
            if keys[pygame.K_SPACE] and not oldKeys[pygame.K_SPACE]:
                player.jump()
            if not keys[pygame.K_UP] and oldKeys[pygame.K_UP] and player.vspeed < 0:
                player.vspeed /= 2
            if not keys[pygame.K_SPACE] and oldKeys[pygame.K_SPACE] and player.vspeed < 0:
                player.vspeed /= 2
            if keys[pygame.K_RIGHT]:
                player.move(RIGHT)
            if keys[pygame.K_LEFT]:
                player.move(LEFT)
            oldKeys = keys
            
            player.update()

            screen.fill(BLACK)
            allSpritesGroup.draw(screen)
            pygame.display.flip()

            clock.tick(60)

    def makeLevel(self, platformsGroup, allSpritesGroup):

        platform = Platform(0, 0, 32, 512, BLUE)
        platformsGroup.add(platform)
        allSpritesGroup.add(platform)
        platform = Platform(0, 480, 768, 32, BLUE)
        platformsGroup.add(platform)
        allSpritesGroup.add(platform)
        platform = Platform(736, 0, 32, 512, BLUE)
        platformsGroup.add(platform)
        allSpritesGroup.add(platform)
        platform = Platform(256, 384, 128, 32, BLUE)
        platformsGroup.add(platform)
        allSpritesGroup.add(platform)

game = Controller()
