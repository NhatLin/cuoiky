import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

(screen_width,screen_height)= (700,700)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Our game")

#Define game variable
tile_size = 35

#Load img
bg_img = pygame.image.load('img/sky.png')
sun_img = pygame.image.load('img/sun.png')

def draw_grid():
    for line in range(20):
        pygame.draw.line(screen, (255,255,255), (0, line * tile_size ), (screen_width, line * tile_size) )
        pygame.draw.line(screen, (255,255,255), (line * tile_size, 0 ), (line * tile_size, screen_height) )

class CPlayer:
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for i in range(1,7):
            img_right = pygame.image.load(f'img/guy{i}.png')
            img_right = pygame.transform.scale(img_right, (35,60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0


    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 5

        #Get ketpresses
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.jumped == False:
            self.vel_y -= 15
            self.jumped = True
        if key[pygame.K_UP] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 3.5
            self.counter +=1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 3.5
            self.counter +=1
            self.direction = 1
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
            if self.direction ==1:
                self.image = self.images_right[self.index]
            if self.direction ==-1:
                self.image = self.images_left[self.index]

        #Handle animation
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction ==1:
                self.image = self.images_right[self.index]
            if self.direction ==-1:
                self.image = self.images_left[self.index]


        #Add gravity
        self.vel_y +=1
        if self.vel_y > 5:
            self.vel_y = 5
        dy += self.vel_y
        #Check for collision



        #Update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        #Draw player onto screen
        screen.blit(self.image, self.rect)

class CWorld:
    def __init__(self,data):
        self.tile_list = []

        #Load img
        land_img = pygame.image.load('img/land.png')
        grass_img = pygame.image.load('img/grass.png')


        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(land_img,(tile_size, tile_size))
                    img_react = img.get_rect()
                    img_react.x = col_count * tile_size
                    img_react.y = row_count * tile_size
                    tile = (img, img_react)
                    self.tile_list.append(tile)
                col_count +=1
            row_count +=1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

world_data = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]


player = CPlayer(70, screen_height - 91)
world = CWorld(world_data)

run = True
while run:

    clock.tick(fps)

    screen.blit(bg_img, (0,0))
    screen.blit(sun_img, (35,35))
                

    world.draw()

    player.update()
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()


