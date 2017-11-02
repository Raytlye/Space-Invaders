import pygame
import inputbox

#constants
DISPLAY_WIDTH = 1366
DISPLAY_HEIGHT = 768

BLACK = [0, 0, 0]
BLUE = [135, 206, 250]
WHITE = [255, 255, 255]

FPS = 60

SPACESHIP = pygame.image.load('images/spaceship.png')
SPACESHIP = pygame.transform.scale(SPACESHIP, (50,50))

SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 50

ALIEN_WIDTH = 50
ALIEN_HEIGHT = 50

BULLET_WIDTH = 10
BULLET_HEIGHT = 10

#global variables
bullet_state = "Ready"
level = 0
score = 0
adventure = False
infinite = False

#initialising pygame and screen resolution
pygame.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
screen_rect = screen.get_rect()

#Class Alien
class Alien:

    alienImg = pygame.image.load('images/invader.png')
    alienImg = pygame.transform.scale(alienImg, (50, 50))

    def __init__(self, x, y, speed, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.rect = self.alienImg.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.dist_x = speed
        self.dist_y = 37

    #move the object on the screen
    def update(self):

        self.rect.x += self.dist_x

        if self.rect.right > self.screen_rect.right:
            self.dist_x *= -1
            self.rect.y += self.dist_y
        elif self.rect.left < self.screen_rect.left:
            self.dist_x *= -1
            self.rect.y += self.dist_y

    #draw the alien object onto the screen
    def draw(self, screen):
        screen.blit(self.alienImg, self.rect)

    #check if bullet hit an alien-object
    def check_bullet_collision(self, bullet_x, bullet_y):
        global bullet_state, score
        if bullet_y < self.rect.y + ALIEN_HEIGHT:
            if bullet_x + BULLET_WIDTH > self.rect.x and bullet_x < self.rect.x + ALIEN_WIDTH:
                print("Hit")
                score += 1
                bullet_state = "Ready"
                return True
        else: return False

    #check if alien-object hit the user
    def check_user_collision(self, spaceship_x, spaceship_y):
        if spaceship_y < self.rect.y + ALIEN_HEIGHT:
            if spaceship_x + SPACESHIP_WIDTH > self.rect.x and spaceship_x < self.rect.x + ALIEN_WIDTH:
                print("Gotcha")
                return True
        else: return False

def current_score(name):
    font = pygame.font.SysFont(None, 25)
    text = font.render(name + ": " + str(score), True, BLACK)
    screen.blit(text, (0, 0))

def draw_space_ship(x, y, screen):
    screen.blit(SPACESHIP, (x, y))

def draw_bullet(x, y, screen):
    pygame.draw.rect(screen, BLUE, (x + 20, y, 10, 10))

#create text_objects for the screen
def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()

#intro screen before the game starts
def game_intro():
    global adventure, infinite
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    adventure = True
                    intro = False
                if event.key == pygame.K_i:
                    infinite = True
                    intro = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        screen.fill(WHITE)
        large_text = pygame.font.Font('freesansbold.ttf', 75)
        text_surf, text_rect = text_objects("Space Invaders", large_text)
        text_rect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))
        screen.blit(text_surf, text_rect)

        small_text = pygame.font.Font('freesansbold.ttf', 35)
        text_surf, text_rect = text_objects("Press a for Advendture, i for Infinite and escape to quit game", small_text)
        text_rect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2 + 50))

        screen.blit(text_surf, text_rect)
        pygame.display.update()

#end screen after each level
def game_exit(text, won):

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_RETURN:
                    game_loop()

        screen.fill(WHITE)
        large_text = pygame.font.Font('freesansbold.ttf', 45)
        text_surf, text_rect = text_objects(text, large_text)
        text_rect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))
        screen.blit(text_surf, text_rect)

        if not won:
            small_text = pygame.font.Font('freesansbold.ttf', 35)
            text_surf, text_rect = text_objects("Press ENTER to restart or ESCAPE to exit", small_text)
            text_rect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2 + 50))
        else:
            small_text = pygame.font.Font('freesansbold.ttf', 35)
            text_surf, text_rect = text_objects("Press ENTER to proceed or ESCAPE to exit", small_text)
            text_rect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2 + 50))

        screen.blit(text_surf, text_rect)
        pygame.display.update()

#switches level if one completes one
def switch_levels(alienx, alieny):

    global level
    if level == 0:
        return level_generator(5, 3, alienx, alieny, 60, 0)
    elif level == 1:
        return level_generator(7, 3, alienx, alieny, 60, 37)
    elif level == 2:
        return level_generator(8, 4, alienx, alieny, 8, 60)
    elif level == 3:
        return level_generator(12, 3, alienx, alieny, 50, 37)
    elif level == 4:
        return level_generator(3, 10, alienx, alieny, 51, 37)
    elif level == 5:
        return level_generator(25, 4, alienx, alieny, 50, 20)
    else:
        pygame.quit()
        quit()


#generates level and reduces hardcoding
def level_generator(size, speed, alienx, alieny, alienx_add, alieny_add):
    aliens = []
    for i in range(size):
        aliens.append(Alien(alienx, alieny, speed, screen))
        alienx += alienx_add
        alieny += alieny_add
    return aliens


#main method
def game_loop():

    global bullet_state, level
    alienx = 0
    alieny = 0

    aliens = switch_levels(alienx, alieny)

    clock = pygame.time.Clock()

    running = True

    spaceship_x = (DISPLAY_WIDTH * 0.49)
    spaceship_y = (DISPLAY_HEIGHT * 0.9)
    spaceship_speed = 0
    bullet_speed = 5

    while running:
        if bullet_state == "Ready":
            bullet_x = spaceship_x
            bullet_y = spaceship_y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

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
        screen.fill(WHITE)
        draw_space_ship(spaceship_x, spaceship_y, screen)

        if bullet_state == "Shoot":
            bullet_y -= bullet_speed
            draw_bullet(bullet_x, bullet_y, screen)

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
                game_exit("You lost...", False)

        if not aliens:
            level += 1
            game_exit("Winner winner chicken dinner", True)

        pygame.display.update()

        clock.tick(FPS)

def infinite_game():

    global bullet_state, level
    alienx = 0
    alieny = 0

    aliens = switch_levels(alienx, alieny)

    clock = pygame.time.Clock()

    running = True

    spaceship_x = (DISPLAY_WIDTH * 0.49)
    spaceship_y = (DISPLAY_HEIGHT * 0.9)
    spaceship_speed = 0
    bullet_speed = 5

    size = 5
    speed = 3

    name = inputbox.ask(screen, "Your name")

    while running:
        if bullet_state == "Ready":
            bullet_x = spaceship_x
            bullet_y = spaceship_y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

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
        screen.fill(WHITE)
        draw_space_ship(spaceship_x, spaceship_y, screen)
        current_score(name)

        if bullet_state == "Shoot":
            bullet_y -= bullet_speed
            draw_bullet(bullet_x, bullet_y, screen)

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
                game_exit("You lost...", False)

        if not aliens:
            size += 1
            speed += 1
            aliens = level_generator(size, speed, alienx, alieny, 60, 0)

        pygame.display.update()

        clock.tick(FPS)

game_intro()
if adventure:
    game_loop()
if infinite:
    infinite_game()
pygame.quit()
quit()
