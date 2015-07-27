#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
name: pyrogue
descr: rogue game using python + pygame. graphics from dungeon crawl stone soup
URL:
Author:  Horst JENS
Licence: gpl, see http://www.gnu.org/licenses/gpl.html
"""

####
import pygame
import random
####


class Spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error:
            print ('Unable to load spritesheet image:'), filename
            raise #SystemExit, message
    # Load a specific image from a specific rectangle

    def image_at(self, rectangle, colorkey = None):
        """Loads image from x,y,x+offset,y+offset"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        """Loads multiple images, supply a list of coordinates"""
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        """Loads a strip of images and returns them as a list"""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

#import spritesheet
#...
#ss = spritesheet.spriteshee('somespritesheet.png')
## Sprite is 16x16 pixels at location 0,0 in the file...
#image = ss.image_at((0, 0, 16, 16))
#images = []
## Load two images into an array, their transparent bit is (255, 255, 255)
#images = ss.images_at((0, 0, 16, 16),(17, 0, 16,16), colorkey=(255, 255, 255))
#...

SIDE = 32


class Monster(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.hitpoints = random.randint(10,20)
        self.name = "Monster"


class Player(Monster):
    def __init__(self,bild):
        Monster.__init__(self,1,1)
        self.name="Player"
        self.bild = bild
        self.z = 0
        

class PygView(object):

    def __init__(self, width=640, height=400):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.fps = 30  # frames per second
        pygame.display.set_caption("Press ESC to quit")
        self.walls = Spritesheet("wall.png")
        self.floors = Spritesheet("floor.png")
        self.figuren = Spritesheet("player.png")
        self.wall = self.walls.image_at((0, 0, SIDE, SIDE))
        self.floor = self.floors.image_at((160, SIDE*2 ,SIDE, SIDE))
        self.playerbild = self.figuren.image_at((0, 0, SIDE, SIDE), (0, 0, 0))
        self.player = Player(self.playerbild)
        self.level = ["##########",
                      "#........#",
                      "#........#",
                      "#........#",
                      "#........#",
                      "#........#",
                      "##########"]
                      
    def paint(self):
        y = 0
        for line in self.level:
            x = 0
            for char in line:
                if x == self.player.x * SIDE and y == self.player.y * SIDE:
                    self.screen.blit(self.player.bild,(x,y))
                elif char == "#":
                    self.screen.blit(self.wall, (x,y))
                elif char == ".":
                    self.screen.blit(self.floor, (x,y))
                x += SIDE
            y += SIDE

    def run(self):
        """The mainloop
        """
        self.clock = pygame.time.Clock() 
        running = True
        while running:
            self.seconds = self.clock.tick(self.fps)/1000.0  # seconds since last frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_UP:
                        self.player.y -= 1
                    if event.key == pygame.K_DOWN:
                        self.player.y += 1
                    if event.key == pygame.K_LEFT:
                        self.player.x -= 1
                    if event.key == pygame.K_RIGHT:
                        self.player.x += 1
                        
            #pressedkeys = pygame.key.get_pressed() 
            

            pygame.display.set_caption("press Esc to quit. Fps: %.2f (%i x %i)"%(self.clock.get_fps(), self.width, self.height))
            
            
            self.paint()
            pygame.display.flip()          
        pygame.quit()

####

if __name__ == '__main__':

    PygView().run()
