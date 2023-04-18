import pygame
from pygame.locals import *
import pickle
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60

(screen_width,screen_height)= (700,700)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Our game")

#Define game variable
tile_size = 35
game_over = 0
main_menu = True
level = 1
max_levels = 3

#Load img
bg_img = pygame.image.load('img/sky.png')
sun_img = pygame.image.load('img/sun.png')
restart_img = pygame.image.load('img/restart.png')
start_img = pygame.image.load('img/start.png')
exit_img = pygame.image.load('img/exit.png')

#reset level
def reset_level(level):
    player.restart(70, screen_height - 91)
    enemy_group.empty()
    poison_group.empty()
    exit_group.empty()

    if path.exists(f'level{level}.pickle'):
        pickle_in = open(f'level{level}.pickle ', 'rb')
        world_data = pickle.load(pickle_in)
    world = CWorld(world_data)

    return world
# def draw_grid():
#     for line in range(20):
#         pygame.draw.line(screen, (255,255,255), (0, line * tile_size ), (screen_width, line * tile_size) )
#         pygame.draw.line(screen, (255,255,255), (line * tile_size, 0 ), (line * tile_size, screen_height) )


class CButton:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        #Get mouse position
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0]:
            self.clicked = False


        #Draw button
        screen.blit(self.image, self.rect)

        return action

class CPlayer:
    def __init__(self, x, y):
        self.restart(x,y)


    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over ==0: 
            #Get ketpresses
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.jumped == False and self.in_air == False:
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
            self.in_air = True
            for tile in world.tile_list:
            #Check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height): 
                        dx = 0
                #Check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): 
                        #check if below the ground jumping
                        if self.vel_y<0:
                            dy = tile[1].bottom - self.rect.top
                            self.vel_y = 0
                            #check if above the ground falling
                        elif self.vel_y>=0:
                            dy = tile[1].top - self.rect.bottom
                            self.vel_y = 0
                            self.in_air = False
            #Check for collision with ghost
            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = -1

            #Check for collision with poison
            if pygame.sprite.spritecollide(self, poison_group, False):
                game_over = -1
                

            #Check for collision with exit
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1


            #Update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = pygame.transform.scale(self.dead_image, (35, 50))
        
        #Draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (183,223,253), self.rect,2)
        return game_over
    
    def restart(self, x, y):
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
        self.dead_image = pygame.image.load('img/tomb.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


class CWorld:
    def __init__(self,data):
        self.tile_list = []

        #Load img
        land_img = pygame.image.load('img/land.png')

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
                if tile ==2:
                    enemy = CEnemy(col_count * tile_size + 5, row_count * tile_size + 10)
                    enemy_group.add(enemy)
                if tile ==3:
                    poison = CPoison(col_count * tile_size, row_count * tile_size + 13)
                    poison_group.add(poison)
                if tile ==4:
                    exit = CExit(col_count * tile_size, row_count * tile_size + 15)
                    exit_group.add(exit)
                col_count +=1
            row_count +=1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255,255,255), tile[1], 2)

class CEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/ghost.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0


    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 42:
            self.move_direction *= -1
            self.move_counter *= -1

class CPoison(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('img/poison.png')
        self.image = pygame.transform.scale(image,(tile_size, tile_size/1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class CExit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('img/gate.png')
        self.image = pygame.transform.scale(image,(tile_size, tile_size*1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y





player = CPlayer(70, screen_height - 91)

enemy_group = pygame.sprite.Group()
poison_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#Load in level data and create world

if path.exists(f'level{level}.pickle'):
	pickle_in = open(f'level{level}.pickle', 'rb')
	world_data = pickle.load(pickle_in)
world = CWorld(world_data)

#Create button
restart_button = CButton(screen_width //2 - 50, screen_height //2 + 100, restart_img)
start_button = CButton(screen_width //2 - 260, screen_height //2 , start_img)
exit_button = CButton(screen_width //2 + 90, screen_height//2, exit_img)





run = True
while run:

    clock.tick(fps)

    screen.blit(bg_img, (0,0))
    screen.blit(sun_img, (35,35))


    if main_menu:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False  
               
    else:
        world.draw()

        if game_over == 0:
            enemy_group.update()

        enemy_group.draw(screen)
        poison_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over)


        #If player has died
        if game_over == -1:
            if restart_button.draw():
                player.restart(70, screen_height - 91)
                game_over = 0

        #Player has completed level
        if game_over == 1:
            level += 1
            if level <= max_levels:
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                if restart_button.draw():
                    level = 1
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
    # draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()


