import pygame
import random

pygame.init()

display_width = 800
display_height = 600

black = [0,0,0]
white = [255,255,255]

spaceship_width = 50
spaceship_height = 50

alien_width = 61
alien_height = 50

bullet_width = 10
bullet_height = 10

bulletstate = "ready"

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

spaceshipImg = pygame.image.load('images/spaceship.png')
spaceshipImg = pygame.transform.scale(spaceshipImg, (50,50))

def drawSpaceShip(x,y):
    gameDisplay.blit(spaceshipImg,(x,y))

class Alien(object):

    def __init__(self, startX = 0, startY = 0, speed = 3):
        self.x = startX
        self.y = startY
        self.speed = speed
        self.alienImg = pygame.image.load('images/alien.png')
        self.alienImg = pygame.transform.scale(self.alienImg, (61, 50))

    def move(self):
        self.x += self.speed

def shoot(x,y):
    pygame.draw.rect(gameDisplay, white, (x + 20,y,10,10))

def game_loop():

    global bulletstate
    x = (display_width * 0.49)
    y = (display_height * 0.9)
    x_change = 0


    enemylist = [5]

    bullet_speed = 5

    while True:

        if bulletstate == "ready":
            bulletx = x
            bullety = y
        gameDisplay.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_SPACE:
                    shoot(bulletx,bullety)
                    bulletstate = "shoot"

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        if bulletstate == "shoot":
            bullety -= bullet_speed
            shoot(bulletx, bullety)
        drawSpaceShip(x,y)
        for alien in enemylist:
            alien.move()
            gameDisplay.blit(alien.alienImg, alien.x, alien.y)

        if x > display_width - spaceship_width:
            x = display_width - spaceship_width
        elif x < 0:
            x = 0

        # if alien_startx > display_width - alien_width:
        #     alien_speed *= -1
        #     alien_starty += 40
        # elif alien_startx < 0:
        #     alien_speed *= -1
        #     alien_starty += 40

        # if bullety < alien_starty + alien_height:
        #
        #     if bulletx + bullet_width > alien_startx and bulletx < alien_startx + alien_width:
        #         print("Hit")

        if bullety < 0:
            bulletstate = "ready"


        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
