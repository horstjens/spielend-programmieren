import pygame
import random
import os
import sys


class Ball(object):
    def __init__(self, radius = 50, color=(0,0,255), x=320, y=240, friction=0.999, targets=[None,None], image=None, wallsound=None, walldamage=True):
        self.radius = radius
        self.hitpoints =100
        self.wallsound = wallsound
        self.targets = targets
        self.walldamage = walldamage
        self.color = color
        self.image = image
        self.x = x
        self.friction = friction
        self.dy=0
        self.dx=0
        self.y = y
        if self.image is None:
            self.surface = pygame.Surface((2*self.radius,2*self.radius))
            pygame.draw.circle(self.surface, color, (radius, radius), radius)
            self.surface.set_colorkey((0,0,0)) # black is transparent
        else:
            self.surface = self.image
            self.surface = pygame.transform.scale(self.surface, (self.radius*2, self.radius*2))
        self.surface = self.surface.convert_alpha()
        self.liste= []
        for i in range(11):
            self.liste.append((self.x,self.y))
        
    def update(self,seconds):
        self.ai()  # calculate where to move: new dx and dy 
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        if self.x<0:
            if self.walldamage:
                self.hitpoints-=1
                self.wallsound.play()
            self.x = 0
            self.dx *= -0.3
        if self.x > PygView.width:
            if self.walldamage:
                self.hitpoints-=1
                self.wallsound.play()
            self.x = PygView.width
            self.dx *= -0.3
        if self.y < 0:
            if self.walldamage:
                self.hitpoints-=1
                self.wallsound.play()
            self.y = 0
            self.dy *= -0.3
        if self.y>PygView.height:
            if self.walldamage:
                self.hitpoints-=1
                self.wallsound.play()
            self.y = PygView.height
            self.dy *= -0.3
        self.dx *= self.friction
        self.dy *= self.friction
        
    def ai(self):
         # coose the nearest of targets and move into this direction
         # verfolger1,  wo will ich hin?
         distances = {} # key is distance, value is target
         for target in self.targets:
             if target is None:
                 continue
             if target.hitpoints < 1:
                 continue
             distance_x = abs(target.x - self.x)
             distance_y = abs(target.y - self.y)
             distance = (distance_x**2 + distance_y**2)**0.5 # pythagoras!
             distances[distance] = target
         # what is the nearest target?
         self.target = None
         if len(distances) == 0:
             return
         distances_sorted = list(distances.keys())
         distances_sorted.sort()
         self.target = distances[distances_sorted[0]]
         # change dx, dy
         if self.x > self.target.x:
             self.dx -= 1
         elif self.x < self.target.x:
             self.dx += 1
         if self.y > self.target.y:
             self.dy -= 1
         elif self.y < self.target.y:
             self.dy += 1

        
    def blit(self, background):
        background.blit(self.surface, (self.x-self.radius, self.y-self.radius))

class PygView(object):
    width = 0
    height = 0
    def __init__(self, width=640, height=400, fps=100, walldamage=False):
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.walldamage = walldamage
        self.width = width
        PygView.width = width
        self.height = height
        PygView.height = height
        self.font = pygame.font.SysFont("mono", 24, bold=True)
        self.screen = pygame.display.set_mode((self.width, self.height),pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255,255,255))
        self.paint_background()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        try:
            self.wall1 = pygame.mixer.Sound(os.path.join('data','bump1.wav'))  #load sound
            self.wall2 = pygame.mixer.Sound(os.path.join('data','bump2.wav'))  #load sound
            self.wall3 = pygame.mixer.Sound(os.path.join('data','bump3.wav'))  #load sound
            self.wall4 = pygame.mixer.Sound(os.path.join('data','bump4.wav'))  #load sound
            self.wall5 = pygame.mixer.Sound(os.path.join('data','bump5.wav'))  #load sound
            self.wall6 = pygame.mixer.Sound(os.path.join('data','bump6.wav'))  #load sound
            self.tooclose = pygame.mixer.Sound(os.path.join('data','evil3.wav'))  #load sound
            print("loading sounds o.k.")
            
        except:
            print("error while loading sounds from data folder")
            pygame.quit()
            sys.exit()
        try:
            self.img1 = pygame.image.load(os.path.join("data", "player1.png"))
            self.img2 = pygame.image.load(os.path.join("data", "player2.png"))
            self.evilimg1 = pygame.image.load(os.path.join("data", "evil1.png"))
            self.evilimg2 = pygame.image.load(os.path.join("data", "evil2.png"))
            print("loading images o.k.")
        except:
            print("error while loading images from data folder")
            pygame.quit()
            sys.exit()
            
        
    
    def paint_background(self):
        self.draw_text("steer players with w,a,s,d and cursor keys", x= 20, y=0, color=(100,100,100), screen=self.background)
        self.draw_text("aviod evils, lure them into walls", x=20, y=20, color=(100,100,100), screen=self.background)
           
        self.draw_text("      Hitpoints, dx,  dy",y=60, screen=self.background)
        self.draw_text("Player1:", y=100, screen=self.background)
        self.draw_text("Player2:", y=150, screen=self.background)
        self.draw_text("Evil1:", y=200, screen=self.background)
        self.draw_text("Evil2:", y=250, screen=self.background)
        self.draw_text("Evil3:", y=300, screen=self.background)
        self.draw_text("Evil4:", y=350, screen=self.background)
        #pygame.draw.line(self.background, (11,11,235), (10,10), (50,100)) 
        #pygame.draw.rect(self.background, (255,230,48), (45,45,100,45))
        #pygame.draw.rect(self.background, (184,255,48), (40,40,80,35))
        #pygame.draw.rect(self.background, (61,255,48), (35,35,60,25))
        #pygame.draw.rect(self.background, (48,255,200), (30,30,40,15))
        #pygame.draw.rect(self.background, (255,230,48), (45,195,100,45))
        #pygame.draw.rect(self.background, (184,255,48), (40,220,80,35))
        #pygame.draw.rect(self.background, (61,255,48), (35,245,60,25))
        #pygame.draw.rect(self.background, (48,255,200), (30,260,40,15))
        #pygame.draw.circle(self.background, (11,11,225), (205, 35),45)
        #pygame.draw.circle(self.background, (255,72,48), (205, 35),40)
        #pygame.draw.circle(self.background, (255,48,203), (205, 35),35)
        #pygame.draw.circle(self.background, (198,255,48), (205, 35),30)
        #pygame.draw.circle(self.background, (111,255,48), (205, 35),25)
        #pygame.draw.circle(self.background, (48,255,75), (205, 35),20)
        #pygame.draw.circle(self.background, (48,255,192), (205, 35),15)
        #pygame.draw.polygon(self.background, (11,11,215),((250,100),(300,0),(350,50)))
        #pygame.draw.arc(self.background, (11,11,205),(400,10,150,100), 0, 3.14)

    def run(self):
       #self.paint()
       running = True
       myball1 = Ball(radius=15,walldamage = self.walldamage, color=(0,128,255), x=self.width//2 - 100, y=self.height//2, wallsound=self.wall1, image=self.img1 )
       myball2=Ball(radius=15,walldamage= self.walldamage, color=(255,128,0), x=self.width//2 + 100, y=self.height//2, wallsound=self.wall2, image=self.img2)
       verfolger1=Ball(radius=20,color=(0,0,255), x=0, y=0,friction=0.99, targets = [myball1, myball2],wallsound=self.wall3, image=self.evilimg1 )
       verfolger2=Ball(radius=22,color=(0,255,255), x=self.width, y=0, friction=0.98,  targets = [myball1, myball2, verfolger1], wallsound=self.wall4, image=self.evilimg2)
       verfolger3=Ball(radius=24,color=(200,200,200), x= 0, y=self.height, friction=0.97, targets = [myball1, myball2, verfolger1, verfolger2], wallsound=self.wall5) # not white
       verfolger4=Ball(radius=28,color=(255,255,0), x=self.width, y=self.height, friction=0.96, targets = [myball1, myball2, verfolger1, verfolger2, verfolger3], wallsound=self.wall6)
       
       sprites = [verfolger4, verfolger3, verfolger2, verfolger1, myball2, myball1] # order of blitting
       
       clock=pygame.time.Clock()
       gameovertime = 0
       while running:
           #pygame.display.set_caption("hitpoints: myball1: {} myball2: {} verfolger1: {}".format(myball1.hitpoints, myball2.hitpoints, #verfolger1.hitpoints))
           milliseconds= clock.tick(self.fps)
           seconds=milliseconds /1000.0
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   running = False
               elif event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_ESCAPE:
                       running = False
                   if event.key == pygame.K_LCTRL:
                       myball1.x =random.randint(0,self.width)
                       myball1.y =random.randint(0,self.height)
                   if event.key == pygame.K_q:
                       myball1.x =self.width//2     
                       myball1.y =self.height//2
                       myball1.dx=0
                       myball1.dy=0
                      
                   if event.key == pygame.K_RCTRL:
                       myball2.x =random.randint(0,self.width)
                       myball2.y =random.randint(0,self.height)
                   if event.key == pygame.K_p:
                       myball2.x =self.width//3     
                       myball2.y =self.height//3
                       myball2.dx=0
                       myball2.dy=0   
                   if event.key == pygame.K_F9:
                       myball2.hitpoints *=10
                   if event.key == pygame.K_F10:
                       myball2.hitpoints +=20
                   if event.key == pygame.K_F1:
                       myball1.hitpoints *=10
                   if event.key == pygame.K_F2:
                       myball1.hitpoints +=20
                   if event.key == pygame.K_F3:
                       myball1.hitpoints =100
                   if event.key == pygame.K_F8:
                       myball2.hitpoints =100 
                   if event.key == pygame.K_F6:
                       verfolger1.x=0
                       verfolger1.y=0
                       verfolger2.x=self.width
                       verfolger2.y=0
                       verfolger3.x=0
                       verfolger3.y=self.height
                       verfolger4.x=self.width
                       verfolger4.y=self.height
                   if event.key == pygame.K_F7:
                       x,y = myball1.x, myball1.y
                       myball1.x = myball2.x
                       myball1.y = myball2.y
                       myball2.x = x
                       myball2.y = y
                   if event.key == pygame.K_F5:
                       myball1.hitpoints =100    
                       myball2.hitpoints =100
                       verfolger1.hitpoints =100
                       verfolger2.hitpoints =100
                       verfolger3.hitpoints =100
                       verfolger4.hitpoints =100
                       
                       
                       verfolger1.x=0
                       verfolger1.y=0
                       verfolger2.x=self.width
                       verfolger2.y=0
                       verfolger3.x=0
                       verfolger3.y=self.height
                       verfolger4.x=self.width
                       verfolger4.y=self.height
                       
                        
                          
                       
                           
                   
                    
           pressedkeys = pygame.key.get_pressed()
           if myball2.hitpoints > 0:
               if pressedkeys[pygame.K_UP]:
                   myball2.dy-=1
               if pressedkeys[pygame.K_DOWN]:
                   myball2.dy+=1
               if pressedkeys[pygame.K_LEFT]:
                   myball2.dx-=1
               if pressedkeys[pygame.K_RIGHT]:
                   myball2.dx+=1            
                       
           #pressedkeys = pygame.key.get_pressed()
           if myball1.hitpoints > 0:
               if pressedkeys[pygame.K_w]:
                   myball1.dy-=1
               if pressedkeys[pygame.K_s]:
                   myball1.dy+=1
               if pressedkeys[pygame.K_a]:
                   myball1.dx-=1
               if pressedkeys[pygame.K_d]:
                   myball1.dx+=1
          
           milliseconds = self.clock.tick(self.fps)
           self.playtime += milliseconds / 1000.0
           
           # check if player is touching evil
           for evil in [verfolger1, verfolger2, verfolger3, verfolger4]:
               if evil.hitpoints > 0:
                   for player in [myball1, myball2]:
                       if player.hitpoints > 0:
                            distance_x = abs(player.x - evil.x)
                            distance_y = abs(player.y - evil.y)
                            distance = (distance_x**2 + distance_y**2)**0.5 # pythagoras!
                            if distance < (evil.radius + player.radius):
                                player.hitpoints -= 1
                                self.tooclose.play()
                                #self.screen.fill(random.choice((player.color, evil.color, (0,0,0), (255,255,255))))
                                for krach in range(5):
                                     pygame.draw.line(self.screen, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), (player.x, player.y), (player.x + random.randint(-50,50), player.y+random.randint(-50,50)), 6)
           
                    
           
           #self.draw_text("FPS: {:5.3f}{}PLAYTIME: {:6.3} SECONDS".format(
           #               self.clock.get_fps(), " "*5, self.playtime))
           

           pygame.display.flip()
           self.screen.blit(self.background, (0, 0))
           self.draw_text("{} {:5.2f} {:5.2f}".format(myball1.hitpoints, myball1.dx, myball1.dy), y=100, x = 200)
           self.draw_text("{} {:5.2f} {:5.2f}".format(myball2.hitpoints, myball1.dx, myball1.dy), y=150, x = 200)
           self.draw_text("{}".format(verfolger1.hitpoints), y=200, x = 200)
           self.draw_text("{}".format(verfolger2.hitpoints), y=250, x = 200)
           self.draw_text("{}".format(verfolger3.hitpoints), y=300, x = 200)
           self.draw_text("{}".format(verfolger4.hitpoints), y=350, x = 200)
           # glittering line between players
           if myball1.hitpoints > 0 and myball2.hitpoints > 0:
               pygame.draw.line(self.screen, (random.randint(0,255),random.randint(0,255),random.randint(0,255)),
                                (myball1.x, myball1.y), (myball2.x, myball2.y), 1)
           
           for sprite in sprites:
               if sprite.hitpoints > 0:
                   sprite.update(seconds)
                   if sprite.target is not None:
                       pygame.draw.line(self.screen, sprite.color, (sprite.x, sprite.y), (sprite.target.x, sprite.target.y), 2) 
                   sprite.blit(self.screen)
           # game over
           if myball1.hitpoints < 1 and myball2.hitpoints < 1:
               self.draw_text("Game Over", x = 300, y = 300, color=(255,0,0))
               self.draw_text("both players loose", x = 300, y = 330, color=(0,255,0))
               gameovertime += seconds
           if verfolger1.hitpoints < 1 and verfolger2.hitpoints < 1 and verfolger3.hitpoints < 1 and verfolger4.hitpoints < 1:
               self.draw_text("Game Over", x = 300, y = 300, color=(255,0,0))
               self.draw_text("both player win!", x = 300, y = 330, color=(0,0,255))
               gameovertime += seconds
               
            
           if gameovertime > 5:
               break # display game over message for 5 seconds    
           
       pygame.quit()
       
    def draw_text(self, text, x=50, y=150, color=(0,0,0), screen=None):
        if screen is None:
            screen = self.screen
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, color)
        screen.blit(surface, (x,y))

if __name__ == "__main__":
    PygView(width=1024, height=800).run()
