'''
    Author: Cristian Mosqueda
    Purpose: Practice making space invaders in Python..
'''
# importing pygame + random (rand num generator)
import pygame
import random
import math
from pygame import mixer
# initialize the pygame
pygame.init()

#creating a screen
'''
    tuple
    set_mode takes two parameters width pixel, height pixels
'''
screen = pygame.display.set_mode((800,600)) # (width x, height y)

# Background
background = pygame.image.load('background.png')

# # Background Sound
# mixer.music.load('background.wav')
# mixer.music.play(-1) # plays music in a infinite loop


# Title & Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('alien.png') # loading png into icon var
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font('ARCADE_I.ttf', 32)
# score coordinates
score_X = 10
score_Y = 10

# Game over code
over_font = pygame.font.Font('ARCADE_I.ttf', 64)

# Player
player_Img = pygame.image.load('player.png')
player_X = 370  # player x & y coordinates
player_Y = 520
player_X_Dir_Change = 0

# Enemy code create a list of enemies
enemy_Img = []
enemy_X = []
enemy_Y = []
enemy_X_Dir_Change = []
enemy_Y_Dir_Change = []
num_of_aliens = 10

for i in range(num_of_aliens):
    enemy_Img.append(pygame.image.load('enemy.png'))
    enemy_X.append(random.randint(0, 735)) #generating a random x coordinate b/w 0 - 800
    enemy_Y.append(random.randint(30, 150))
    enemy_X_Dir_Change.append(4)
    enemy_Y_Dir_Change.append(40) # move alien down by 40 pixels

# Bullet code
# ready - cant see the bullet on the screen
# fire - bullet is currently moving
bullet_Img = pygame.image.load('bomb.png')
bullet_X = 370
bullet_Y = 520 # bullet should start at same position as spaceship
bullet_X_Dir_Change = 0
bullet_Y_Dir_Change = 10
bullet_State = "ready"

# bullet count for validity
bullet_count = 0

# functions
def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_display = over_font.render("Game OVER", True, (255, 255, 255))
    screen.blit(over_display, (145, 250))

def draw_player(x, y):
    # blit takes two parameters the mage and the coordinates
    screen.blit(player_Img,(x, y)) # blit = means to draw on screen

def draw_enemy(x, y, j):
    screen.blit(enemy_Img[j], (x, y))

def fire_bullet(x, y):
    global bullet_State # needs to be global so function can use it
    bullet_State = "fire" # change in bullet state
    screen.blit(bullet_Img, (x + 15.7, y + 10)) # drawing the bullet to the screen

# function to see if missile/bullet has hit the alien/enemy
def is_Collison(enemyX, enemyY, bulletX, bulletY):
    # get distance b/w the missile and enemy
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# event is anything happening in your game window ex: moving mouse, pressing arrow key
# game loop -> infinite loop
running = True
while running:

    # change color of background screen
    # RGB - RED, GREEN, BLUE 0-255 in TUPLE
    screen.fill((0, 0, 0)) # ((RED,GREEN,BLUE))

    # drawing the background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # will close out if player wants to exit
        # if a keystroke is pressed check whether its left/right arrow
        if event.type == pygame.KEYDOWN: # KEYDOWN -> any key on keyboard
            if event.key == pygame.K_LEFT:
                player_X_Dir_Change = -5 # move space 0.5 to the left
            if event.key == pygame.K_RIGHT:
                player_X_Dir_Change = 5 # move spaceship 0.5 to right while key is being pressed
            # space key to fire a bullet
            if event.key == pygame.K_SPACE and bullet_State == "ready":
                bullet_X = player_X # bullet now has its original trjectory of where spaceship shot it
                fire_bullet(bullet_X, bullet_Y)
                bullet_count += 1 # current bullet being shot
        # releasing the keystroke
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_X_Dir_Change = 0 # key is no longer being pressed so dont move space ship

    # updating spaceship coordinates in case of movement
    player_X += player_X_Dir_Change

    # creating boundaries for spaceship depending on its width or x
    if player_X <= 0:
        player_X = 0
    elif player_X >= 736:
        player_X = 736

    # Enemies CODE
    for j in range(num_of_aliens):

        # GAME OVER CODE
        if enemy_Y[j] >= 500:
            for k in range(num_of_aliens):
                enemy_Y[k] = 2000 # removing aliens from screen completely
                # calling the game over function
            game_over_text()
            break


        # updating enemies coordinates && checking for boundaries
        enemy_X[j] += enemy_X_Dir_Change[j]
        if enemy_X[j] <= 0:
            enemy_X_Dir_Change[j] = 4
            enemy_Y[j] += enemy_Y_Dir_Change[j] # moving down in y direction with each boundary encounter
        elif enemy_X[j] >= 736:
            enemy_X_Dir_Change[j] = -4
            enemy_Y[j] += enemy_Y_Dir_Change[j]
        # Collision code
        collision = is_Collison(enemy_X[j],enemy_Y[j], bullet_X, bullet_Y) #if the missile has hit the alien then
        if collision:
            # reset the missiles position to where the spaceship is at
            bullet_Y = 520
            bullet_State = "ready"
            # next increase the score since missile has hit the alien
            score_value += 1
            # enemy respawns after getting hit
            enemy_X[j] = random.randint(0, 735) #generating a random x coordinate b/w 0 - 800
            enemy_Y[j] = random.randint(30, 150)
        # drawing the given
        draw_enemy(enemy_X[j], enemy_Y[j], j)



    # BULLET MOVEMENT CODE
    # resetting bullets after one has escaped y boundary
    if bullet_Y <= 0:
        bullet_Y = 520 # reset bullet to spaceships bound y-axis
        bullet_State = "ready"
    if bullet_State == "fire":
        fire_bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Y_Dir_Change

    #calling draw_player & draw_enemy methods
    draw_player(player_X, player_Y)
    show_score(score_X, score_Y)
    pygame.display.update() # want to update your screen always
