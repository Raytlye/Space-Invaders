import pygame

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

BLACK = [0,0,0]

FPS = 60

SPACESHIP = pygame.image.load('images/spaceship.png')
SPACESHIP = pygame.transform.scale(SPACESHIP, (50,50))

SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 50

class Alien:

    alienImg = pygame.image.load('images/alien.png')
    alienImg = pygame.transform.scale(alienImg, (61, 50))

    def __init__(self, x, y, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.rect = self.alienImg.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.dist_x = 3
        self.dist_y = 0

    def update(self):

        self.rect.x += self.dist_x

        if self.rect.right > self.screen_rect.right:
            self.dist_x *= -1
            self.rect.y += 30
        elif self.rect.left < self.screen_rect.left:
            self.dist_x *= -1
            self.rect.y += 30

    def draw(self, screen):
        screen.blit(self.alienImg, self.rect)

def draw_space_ship(x, y, screen):
    screen.blit(SPACESHIP, (x, y))

pygame.init()

screen = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
screen_rect = screen.get_rect()

aliens = []

alienx = 0
alieny = 0

for i in range(5):
    aliens.append(Alien(alienx, alieny, screen))
    alienx += 60

clock = pygame.time.Clock()

running = True

spaceship_x = (DISPLAY_WIDTH * 0.49)
spaceship_y = (DISPLAY_HEIGHT * 0.9)
spaceship_speed = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceship_speed = -5
            elif event.key == pygame.K_RIGHT:
                spaceship_speed = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceship_speed = 0

    spaceship_x += spaceship_speed
    screen.fill(BLACK)
    draw_space_ship(spaceship_x, spaceship_y, screen)

    if spaceship_x > DISPLAY_WIDTH - SPACESHIP_WIDTH:
        spaceship_x = DISPLAY_WIDTH - SPACESHIP_WIDTH
    elif spaceship_x < 0:
        spaceship_x = 0

    for alien in aliens:
        alien.update()

    for alien in aliens:
        alien.draw(screen)

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
