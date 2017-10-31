import pygame

#--constants--
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

FPS = 60

SPACESHIP = pygame.image.load('images/spaceship.png')
SPACESHIP = pygame.transform.scale(SPACESHIP, (50,50))

SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 50

ALIEN_WIDTH = 61
ALIEN_HEIGHT = 50

BULLET_WIDTH = 10
BULLET_HEIGHT = 10

#--Class Alien--
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

    def check_bullet_collision(self, bullet_x, bullet_y):
        if bullet_y < self.rect.y + ALIEN_HEIGHT:
            if bullet_x + BULLET_WIDTH > self.rect.x and bullet_x < self.rect.x + ALIEN_WIDTH:
                print("Hit")
                return True
        else: return False

    def check_user_collision(self, spaceship_x, spaceship_y):
        if spaceship_y < self.rect.y + ALIEN_HEIGHT:
            if spaceship_x + SPACESHIP_WIDTH > self.rect.x and spaceship_x < self.rect.x + ALIEN_WIDTH:
                print("Gotcha")
                return True
        else: return False



def draw_space_ship(x, y, screen):
    screen.blit(SPACESHIP, (x, y))

def draw_bullet(x, y):
    pygame.draw.rect(screen, WHITE, (x + 20, y, 10, 10))

pygame.init()

screen = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
screen_rect = screen.get_rect()

aliens = []

alienx = 0
alieny = 500

for i in range(5):
    aliens.append(Alien(alienx, alieny, screen))
    alienx += 60

clock = pygame.time.Clock()

running = True
bullet_state = "Ready"

spaceship_x = (DISPLAY_WIDTH * 0.49)
spaceship_y = (DISPLAY_HEIGHT * 0.9)
spaceship_speed = 0
BULLET_SPEED = 5

while running:
    if bullet_state == "Ready":
        bullet_x = spaceship_x
        bullet_y = spaceship_y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceship_speed = -5
            elif event.key == pygame.K_RIGHT:
                spaceship_speed = 5
            elif event.key == pygame.K_SPACE:
                bullet_state = "Shoot"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                spaceship_speed = 0

    spaceship_x += spaceship_speed
    screen.fill(BLACK)
    draw_space_ship(spaceship_x, spaceship_y, screen)

    if bullet_state == "Shoot":
        bullet_y -= BULLET_SPEED
        draw_bullet(bullet_x, bullet_y)

    if spaceship_x > DISPLAY_WIDTH - SPACESHIP_WIDTH:
        spaceship_x = DISPLAY_WIDTH - SPACESHIP_WIDTH
    elif spaceship_x < 0:
        spaceship_x = 0

    if bullet_y < 0:
        bullet_state = "Ready"

    for alien in aliens:
        alien.update()

    for alien in aliens:
        alien.draw(screen)
        aliens = [alien for alien in aliens if not alien.check_bullet_collision(bullet_x, bullet_y)]
        if alien.check_user_collision(spaceship_x, spaceship_y):
            pygame.quit()
            quit()

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
