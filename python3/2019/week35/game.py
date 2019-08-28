"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: https://github.com/horstjens/catapults3d
idea: python3/pygame 3d vector rts game
"""

import pygame
import random
import os
#import winsound

def mouseVector():
    return pygame.math.Vector2(pygame.mouse.get_pos()[0],
                               - pygame.mouse.get_pos()[1])
def randomize_color(color, delta=50):
    d=random.randint(-delta, delta)
    color = color + d
    color = min(255,color)
    color = max(0, color)
    return color

def make_text(msg="pygame is cool", fontcolor=(255, 0, 255), fontsize=42, font=None):
    """returns pygame surface with text. You still need to blit the surface."""
    myfont = pygame.font.SysFont(font, fontsize)
    mytext = myfont.render(msg, True, fontcolor)
    mytext = mytext.convert_alpha()
    return mytext

def write(background, text="bla", pos=None, color=(0,0,0),
          fontsize=None, center=False, x=None, y=None):
        """write text on pygame surface. pos is a 2d Vector """
        if pos is None and (x is None or y is None):
            print("Error with write function: no pos argument given and also no x and y:", pos, x, y)
            return
        if pos is not None:
            # pos has higher priority than x or y
            x = pos.x
            y = -pos.y
        if fontsize is None:
            fontsize = 24
        font = pygame.font.SysFont('mono', fontsize, bold=True)
        fw, fh = font.size(text)
        surface = font.render(text, True, color)
        if center: # center text around x,y
            background.blit(surface, (x-fw//2, y-fh//2))
        else:      # topleft corner is x,y
            background.blit(surface, (x,y))

def elastic_collision(sprite1, sprite2):
        """elasitc collision between 2 VectorSprites (calculated as disc's).
           The function alters the dx and dy movement vectors of both sprites.
           The sprites need the property .mass, .radius, pos.x pos.y, move.x, move.y
           by Leonard Michlmayr"""
        if sprite1.static and sprite2.static:
            return 
        dirx = sprite1.pos.x - sprite2.pos.x
        diry = sprite1.pos.y - sprite2.pos.y
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.move.x * sprite1.mass + sprite2.move.x * sprite2.mass) / sumofmasses
        sy = (sprite1.move.y * sprite1.mass + sprite2.move.y * sprite2.mass) / sumofmasses
        bdxs = sprite2.move.x - sx
        bdys = sprite2.move.y - sy
        cbdxs = sprite1.move.x - sx
        cbdys = sprite1.move.y - sy
        distancesquare = dirx * dirx + diry * diry
        if distancesquare == 0:
            dirx = random.randint(0,11) - 5.5
            diry = random.randint(0,11) - 5.5
            distancesquare = dirx * dirx + diry * diry
        dp = (bdxs * dirx + bdys * diry) # scalar product
        dp /= distancesquare # divide by distance * distance.
        cdp = (cbdxs * dirx + cbdys * diry)
        cdp /= distancesquare
        if dp > 0:
            if not sprite2.static:
                sprite2.move.x -= 2 * dirx * dp
                sprite2.move.y -= 2 * diry * dp
            if not sprite1.static:
                sprite1.move.x -= 2 * dirx * cdp
                sprite1.move.y -= 2 * diry * cdp


class VectorSprite(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    numbers = {} # { number, Sprite }

    def __init__(self, **kwargs):
        self._default_parameters(**kwargs)
        VectorSprite.number += 1
        VectorSprite.numbers[self.number] = self
        self.number = VectorSprite.number # unique number for each sprite
        self._overwrite_parameters()
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        
       
        self.create_image()
        self.distance_traveled = 0 # in pixel
        #self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        if self.angle != 0:
            self.set_angle(self.angle)
        self.tail = [] 

    def _overwrite_parameters(self):
        """change parameters before create_image is called""" 
        pass

    def _default_parameters(self, **kwargs):    
        """get unlimited named arguments and turn them into attributes
           default values for missing keywords"""

        for key, arg in kwargs.items():
            setattr(self, key, arg)
        if "layer" not in kwargs:
            self._layer = 4
        else:
            self._layer = self.layer
        if "side" not in kwargs:
            self.side = 0 # 1 for player1, 2 for player2
        if "static" not in kwargs:
            self.static = False
        if "selected" not in kwargs:
            self.selected = False
        if "pos" not in kwargs:
            self.pos = pygame.math.Vector2(random.randint(0, Viewer.width),-50)
        if "move" not in kwargs:
            self.move = pygame.math.Vector2(0,0)
        if "fontsize" not in kwargs:
            self.fontsize = 22
        if "friction" not in kwargs:
            self.friction = 1.0 # no friction
        if "radius" not in kwargs:
            self.radius = 5
        if "width" not in kwargs:
            self.width = self.radius * 2
        if "height" not in kwargs:
            self.height = self.radius * 2
        
        if "hitpoints" not in kwargs:
            self.hitpoints = 100
        self.hitpointsfull = self.hitpoints # makes a copy
        if "mass" not in kwargs:
            self.mass = 10
        if "damage" not in kwargs:
            self.damage = 10
        if "bounce_on_edge" not in kwargs:
            self.bounce_on_edge = False
        if "kill_on_edge" not in kwargs:
            self.kill_on_edge = False
        if "angle" not in kwargs:
            self.angle = 0 # facing right?
        if "max_age" not in kwargs:
            self.max_age = None
        if "max_distance" not in kwargs:
            self.max_distance = None
        if "picture" not in kwargs:
            self.picture = None
        if "bossnumber" not in kwargs:
            self.bossnumber = None
        if "kill_with_boss" not in kwargs:
            self.kill_with_boss = False
        if "sticky_with_boss" not in kwargs:
            self.sticky_with_boss = False
        if "mass" not in kwargs:
            self.mass = 15
        if "upkey" not in kwargs:
            self.upkey = None
        if "downkey" not in kwargs:
            self.downkey = None
        if "rightkey" not in kwargs:
            self.rightkey = None
        if "leftkey" not in kwargs:
            self.leftkey = None
        if "speed" not in kwargs:
            self.speed = None
        if "age" not in kwargs:
            self.age = 0 # age in seconds
        if "warp_on_edge" not in kwargs:
            self.warp_on_edge = False
        if "gravity" not in kwargs:
            self.gravity = None
        if "survive_north" not in kwargs:
            self.survive_north = False
        if "survive_south" not in kwargs:
            self.survive_south = False
        if "survive_west" not in kwargs:
            self.survive_west = False
        if "survive_east" not in kwargs:
            self.survive_east = False
        if "speed" not in kwargs:
            self.speed = 0
        if "color" not in kwargs:
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if "always_calculate_image" not in kwargs:
            self.always_calculate_image = False

    def kill(self):
        if self.number in self.numbers:
           del VectorSprite.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)
    
   
    
    def create_image(self):
        if self.picture is not None:
            self.image = self.picture.copy()
        else:
            self.image = pygame.Surface((self.width,self.height))
            self.image.fill((self.color))
        self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
    
    def rotate_to(self, final_degree):
        if final_degree < self.angle:
            self.rotate(- self.turnspeed)
        elif final_degree > self.angle:
            self.rotate(self.turnspeed)
        else:
            return
        
    def forward(self, speed=10):
        m = pygame.math.Vector2(speed, 0)
        m.rotate_ip(self.angle)
        self.move += m
        
    def rotate(self, by_degree):
        """rotates a sprite and changes it's angle by by_degree"""
        self.angle += by_degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def set_angle(self, degree):
        """rotates a sprite and changes it's angle to degree"""
        self.angle = degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        #self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        # ----- kill because... ------
        if self.hitpoints <= 0:
            self.kill()
        if self.max_age is not None and self.age > self.max_age:
            self.kill()
        if self.max_distance is not None and self.distance_traveled > self.max_distance:
            self.kill()
        # ---- new image calculating ? ---
        if self.always_calculate_image:
            self.create_image()
        # ---- movement with/without boss ----
        if self.bossnumber is not None:
            if self.kill_with_boss:
                if self.bossnumber not in VectorSprite.numbers:
                    self.kill()
            if self.sticky_with_boss and self.bossnumber in VectorSprite.numbers:
                boss = VectorSprite.numbers[self.bossnumber]
                self.pos = pygame.math.Vector2(boss.pos.x, boss.pos.y+self.ydistance)
                self.set_angle(boss.angle)
                #print(self.number, self.bossnumber, boss)
        self.pos += self.move * seconds
        self.move *= self.friction 
        self.distance_traveled += self.move.length() * seconds
        self.age += seconds
        self.wallbounce()
        self.rect.center = ( round(self.pos.x, 0), -round(self.pos.y, 0) )

    def wallbounce(self):
        # ---- bounce / kill on screen edge ----
        # ------- left edge ----
        if self.pos.x < 0:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = 0
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = Viewer.width 
        # -------- upper edge -----
        if self.pos.y  > 0:
            if self.kill_on_edge and not self.survive_north:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = 0
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = -Viewer.height
        # -------- right edge -----                
        if self.pos.x  > Viewer.width:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = Viewer.width
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = 0
        # --------- lower edge ------------
        if self.pos.y   < -Viewer.height:
            if self.kill_on_edge:
                self.hitpoints = 0
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = -Viewer.height
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = 0


class Wolf(VectorSprite):
    
    def _overwrite_parameters(self):
        #print("ich bin wolf nummer", self.number)
        Hitpointbar(bossnumber=self.number, kill_with_boss = True,
                    sticky_with_boss = True, ydistance=50, width=72,
                    always_calculate_image = True)
    
    def create_image(self):
        self.image=Viewer.images["wolf"]
        self.image0 = self.image.copy()
        # self.image0.set_colorkey((0,0,0))
        # self.image0.convert_alpha()
        self.rect = self.image.get_rect()
        

class Player(VectorSprite):
    
    def _overwrite_parameters(self):
        Hitpointbar(bossnumber=self.number, kill_with_boss = True,
                    sticky_with_boss = True, ydistance=50, width=72,
                    always_calculate_image = True)
    
    def create_image(self):
        if self.lookleft:
            self.image = Viewer.images["player"]
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image=Viewer.images["player"]
        self.image0 = self.image.copy()
        # self.image0.set_colorkey((0,0,0))
        # self.image0.convert_alpha()
        self.rect = self.image.get_rect()

class Cannon(VectorSprite):
    
    def _overwrite_parameters(self):
        self.kill_on_edge = False
        self.survive_north = True
        #self.pos.y = -Viewer.height //2
        #self.pos.x = Viewer.width //2
       
        #self.imagenames = ["cannon"]
        self.speed  = 7
        self.turnspeed = 0.5
        self.ready_to_launch = 0
                
    def wallbounce(self):
        # ---- bounce / kill on screen edge ----
        # ------- left edge ----
        if self.pos.x < self.left_border:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = self.left_border
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = self.right_border 
        # -------- upper edge -----
        if self.pos.y  > self.upper_border:
            if self.kill_on_edge and not self.survive_north:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = self.upper_border
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = self.upper_border
        # -------- right edge -----                
        if self.pos.x  > self.right_border:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = self.right_border
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = self.left_border
        # --------- lower edge ------------
        if self.pos.y   < self.lower_border:
            if self.kill_on_edge:
                self.hitpoints = 0
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y =self.lower_border
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = 0
            
    def fire(self):
        v = pygame.math.Vector2(200,0)
        v.rotate_ip(self.angle)
        Bullet(boss=self, pos=pygame.math.Vector2(self.pos.x, self.pos.y), angle=self.angle,
                    move = v)
        if Viewer.shotgun == 2:
            if self.number == 0:
                print("Fired Shotgun")
                for i in range(5):
                    v = pygame.math.Vector2(random.randint (80,120),0)
                    a = random.randint(-10,10)
                    v.rotate_ip(self.angle+ a)
                    Bullet(boss=self, max_age=10, mass=20000, pos=pygame.math.Vector2(self.pos.x, self.pos.y), angle=self.angle+a,
                        move = v)
                  
        #---- recoil ----
        #v= pygame.math.Vector2(10,0)
        #v.rotate_ip(self.angle + 180)
        #self.move += v
     
    def launch(self):
        if self.age < self.ready_to_launch:
            return # not yet ready
        self.ready_to_launch = self.age + 0.1
        v = pygame.math.Vector2(50,0)
        v.rotate_ip(self.angle)
        # chose an enemy wisely
        e = []
        for sprite in VectorSprite.numbers.values():
             if sprite.number == self.number:
                 continue
             if sprite.bossnumber == self.number:
                 continue
             if sprite.__class__.__name__ == "Cannon":
                 e.append(sprite)
             if sprite.__class__.__name__ == "Rocket":
                 e.append(sprite)
             if sprite.__class__.__name__ == "Castle":
                 e.append(sprite)
        
        if Viewer.double_rocket == 1:
            for i in range(2):
                enemy = random.choice(e)     
                Rocket(boss=self, target=enemy, max_age=30, mass=50, pos=pygame.math.Vector2(self.pos.x, self.pos.y), angle=self.angle,
                    move = v+ self.move)
        else:
            enemy = random.choice(e)     
            Rocket(boss=self, target=enemy, max_age=30, mass=50, pos=pygame.math.Vector2(self.pos.x, self.pos.y), angle=self.angle,
                    move = v+ self.move)          
               
    def create_image(self):
        self.image=Viewer.images["cannon"]
        
        self.image0 = self.image.copy()
       # self.image0.set_colorkey((0,0,0))
       # self.image0.convert_alpha()
        self.rect = self.image.get_rect()

    def kill(self):
        #Explosion(posvector=self.pos, red=200, red_delta=25, minsparks=50, maxsparks=60, maxlifetime=7)
        VectorSprite.kill(self)
   
   
    def update(self,seconds):
        VectorSprite.update(self,seconds)
        # - - - - - - go to mouse cursor ------ #
        target = mouseVector()
        dist =target - self.pos
        try:
            dist.normalize_ip() #schrupmft ihn zur länge 1
        except:
            print("i could not normalize", dist)
            return
        dist *= self.speed  
        rightvector = pygame.math.Vector2(1,0)
        angle = -dist.angle_to(rightvector)
        #print(angle)
        #if self.angle == round(angle, 0):
        if self.selected:
            self.move = dist
            self.set_angle(angle)
            pygame.draw.rect(self.image, (0,200,0), (0,0,self.rect.width, self.rect.height),1)



class Flytext(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 7  # order of sprite layers (before / behind other sprites)
        self.r, self.g, self.b = self.color
        
    def create_image(self):
        self.image = make_text(self.text, (self.r, self.g, self.b), self.fontsize)  # font 22
        self.rect = self.image.get_rect()
 
class Guardian(VectorSprite):
    def _overwrite_parameters(self):
          self._layer = 9
          self.kill_on_edge = True
          self.pos = pygame.math.Vector2(random.randint(0, Viewer.width),
                                                            random.randint(-Viewer.height,0))
          self. max_age = 15
          
          v = pygame.math.Vector2(random.randint(2, 2), 0)
          v.rotate_ip(random.randint(0, 360))
          self.move = v
                            
          
    def create_image(self):
          self.image = pygame.Surface((50,50))
          pygame.draw.circle(self.image, (139, 105, 20) , (25, 25), 20)
          pygame.draw.circle(self.image, (223, 21,44) , (25,25), 13)
          self.image.set_colorkey((0,0,0))
          self.image.convert_alpha()
          self.rect= self.image.get_rect()
          self.image0 = self.image.copy() 
 
 
class PowerUp(VectorSprite):
    def _overwrite_parameters(self):
          self._layer = 9
          self.kill_on_edge = True
          self.pos = pygame.math.Vector2(random.randint(0, Viewer.width),
                                                            random.randint(-Viewer.height,0))
          self. max_age = 15
          
          v = pygame.math.Vector2(random.randint(10, 25), 0)
          v.rotate_ip(random.randint(0, 360))
          self.move = v
                            
          
    def create_image(self):
          self.image = pygame.Surface((30,30))
          pygame.draw.circle(self.image, (200, 200, 200) , (15,15), 15)
          pygame.draw.circle(self.image, (255, 64, 0) , (15,15), 10)
          self.image.set_colorkey((0,0,0))
          self.image.convert_alpha()
          self.rect= self.image.get_rect()
          self.image0 = self.image.copy()
 
 
class Castle(VectorSprite):
        
    def create_image(self):
        self.image=Viewer.images["castle"]
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        

class Tower(VectorSprite):

    def create_image(self):
        self.image=Viewer.images["tower"]
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()

    
class Rocket(VectorSprite):
    
       def _overwrite_parameters(self):
          self._layer = 9
          self.kill_on_edge = True
          self.trail = []
          self.max_age = 5
        
       def create_image(self):
          self.image = pygame.Surface((30,10))
          pygame.draw.circle(self.image, self.boss.color , (25,5), 5)
          pygame.draw.rect(self.image, self.boss.color, (0,0,25,10))
          self.image.set_colorkey((0,0,0))
          self.image.convert_alpha()
          self.rect= self.image.get_rect()
          self.image0 = self.image.copy()
       
       def update(self, seconds):
           if self.target not in VectorSprite.numbers.values():
               self.kill()
        
           VectorSprite.update(self, seconds)
           diff = self.target.pos - self.pos
           r = pygame.math.Vector2(1,0)
           a = diff.angle_to(r)
           #rotate sprite
           self.set_angle(-a)
           #self.move.rotate_ip(a)
           diff.normalize_ip()
           self.move *= 0.8
           self.move += diff * 25
           
           self.trail.insert (0, (self.pos.x, -self.pos.y))
           if len(self.trail) > 255:
               self.trail = self.trail[:256]
       
       def kill(self):
           #Explosion (posvector=self.pos, minsparks=20, maxsparks=30)
           VectorSprite.kill(self)
       
class Hitpointbar(VectorSprite):
    
     def _overwrite_parameters(self):
         print("ich bin hitpointbar", self.number, "my bossnumber is", self.bossnumber)
         #print("my boss is a ", VectorSprite.numbers[self.bossnumber])
          
          
     def create_image(self):
         boss = VectorSprite.numbers[self.bossnumber]
         width = self.width
         self.image = pygame.Surface((width,10)) # size of rect
         #pygame.draw.circle(self.image, self.color, (5,5), 5)
         
         percent = boss.hitpoints / boss.hitpointsfull
         #print(percent, boss.hitpoints, boss.hitpointsfull)
         w2 = int(width * percent)
         # moving inside filling
         if boss.side == 1:
             c = (200,0,0)
         elif boss.side == 2:
             c = (0,0,200)
         else:
             c = (200,200,200)
         pygame.draw.rect(self.image,c, (1,1,w2,8)) 
         # static outside border
         pygame.draw.rect(self.image, (200,200,200), (0,0,width,10),1)
         self.image.set_colorkey((0,0,0))
         self.image.convert_alpha()
         self.rect= self.image.get_rect()
         self.image0 = self.image.copy()
         #self.rect.centerx = boss.rect.centerx
         #self.rect.centerx = boss.rect.centerx
         #self.rect.centery = boss.rect.centery - 100

    
    
class Bullet (VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 9
        self.kill_on_edge = False
        self.bounce_on_edge= True
        self.max_age = 10
        self.color = self.boss.color
        
        
    def create_image(self):
        self.image = pygame.Surface((10,10))
        pygame.draw.circle(self.image, self.color, (5,5), 5)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()

class Spark(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 9
        self.kill_on_edge = True
        
    def create_image(self):
        r,g,b = self.color
        r = randomize_color(r,50)
        g = randomize_color(g,50)
        b = randomize_color(b,50)
        self.image = pygame.Surface((10,10))
        pygame.draw.line(self.image, (r,g,b), 
                         (10,5), (5,5), 3)
        pygame.draw.line(self.image, (r,g,b),
                          (5,5), (2,5), 1)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()                          
        

class Explosion():
    """emits a lot of sparks, for Explosion or Player engine"""
    def __init__(self, posvector, minangle=0, maxangle=360, maxlifetime=3,
                 minspeed=5, maxspeed=150, red=255, red_delta=0, 
                 green=225, green_delta=25, blue=0, blue_delta=0,
                 minsparks=5, maxsparks=20):
        for s in range(random.randint(minsparks,maxsparks)):
            v = pygame.math.Vector2(1,0) # vector aiming right (0°)
            a = random.randint(minangle,maxangle)
            v.rotate_ip(a)
            speed = random.randint(minspeed, maxspeed)
            duration = random.random() * maxlifetime # in seconds
            red   = randomize_color(red, red_delta)
            green = randomize_color(green, green_delta)
            blue  = randomize_color(blue, blue_delta)
            Spark(pos=pygame.math.Vector2(posvector.x, posvector.y),
                  angle= a, move=v*speed, max_age = duration, 
                  color=(red,green,blue), kill_on_edge = True)
    



        
    
    

class Viewer():
    credits="learn to code python at spielend-programmieren.at " 
    width = 0
    height = 0
    border_x=500
    border_y= -500
    shotgun = 1
    double_rocket = 0
    disablecheat = False
    v_fullscreen = False
    missles = 1
    images = {}
    sounds = {}
    menu =  {"main":            ["resume", "settings", "credits", "help", "quit" ],
            #main
            "settings":        ["back", "video", "grid size", "influence radius"],
            #settings
            "influence radius":["back", "25", "50", "75", "100", "125", "150", "175", "200", "225", "250", "300", "350", "400"],  
            "grid size":       ["back", "25", "50", "75", "100", "125", "150", "175", "200"  ],
            
            "video":           ["back", "resolution", "fullscreen"],
            #keys
            "help":            ["back", "", "player1 movement: WASD", "player1 action: left CTRL",
                                            "player2 movement: Cursor", "player2 action: <not yet>"],
         
            #video
            "resolution":      ["back", ],
            "fullscreen":      ["back", "true", "false"]
            }
    
    
    #Viewer.menu["resolution"] = pygame.display.list_modes()
    history = ["main"]
    cursor = 0
    name = "main"
    fullscreen = False

    def __init__(self, width=640, height=400, fps=60):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.mixer.pre_init(44100,-16, 2, 2048)   
        pygame.init()
        Viewer.width = width    # make global readable
        Viewer.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        # -- menu --
        li = ["back"]
        for i in pygame.display.list_modes():
            # li is something like "(800, 600)"
            pair = str(i)
            comma = pair.find(",")
            x = pair[1:comma]
            y = pair[comma+2:-1]
            li.append(str(x)+"x"+str(y))
        Viewer.menu["resolution"] = li
        self.set_resolution()
        self.gridsize = 100
        self.influence_radius = 50
        self.calculate_grid() # to have default values for the menu
        self.convert_rate = 2 # how much color value (128=neutral, 0/255=full) changes per second
        
        # ------ background images ------
        #self.backgroundfilenames = [] # every .jpg file in folder 'data'
        #try:
        #    for root, dirs, files in os.walk("data"):
        #        for file in files:
        #            if file[-4:] == ".jpg" or file[-5:] == ".jpeg":
        #                self.backgroundfilenames.append(file)
        #    random.shuffle(self.backgroundfilenames) # remix sort order
        #except:
        #    print("no folder 'data' or no jpg files in it")

        self.age = 0
        # ------ joysticks ----
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()
        self.prepare_sprites()
        self.loadbackground()
        self.load_sounds()
        #self.world = World()
        #print(self.world)
        
        
    def load_sounds(self):
        #pygame.mixer.music.load(os.path.join("data", "Caketown.ogg"))
        Viewer.sounds["click1"]=  pygame.mixer.Sound(
                 os.path.join("data", "click1.wav"))
        Viewer.sounds["click2"] = pygame.mixer.Sound(
                 os.path.join("data", "click2.wav"))
        Viewer.sounds["menu"] = pygame.mixer.Sound(
                 os.path.join("data", "menu_ogg.ogg")) 
               
         
        Viewer.sounds["explosion_rocket1"] = pygame.mixer.Sound(
                 os.path.join("data", "explosion_rocket1.wav"))
        Viewer.sounds["explosion_rocket2"] = pygame.mixer.Sound(
                 os.path.join("data", "explosion_rocket2.wav"))
        Viewer.sounds["explosion_rocket3"] = pygame.mixer.Sound(
                 os.path.join("data", "explosion_rocket3.wav"))
        Viewer.sounds["explosion_rocket4"] = pygame.mixer.Sound(
                 os.path.join("data", "explosion_rocket3.wav"))
        return
    
    
    def set_resolution(self):
        if Viewer.fullscreen:
             self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF|pygame.FULLSCREEN)
        else:
             self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.loadbackground()
    
    
    def loadbackground(self):
        
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0,0,128)) # fill background white
            
        self.background = pygame.transform.scale(self.background,
                          (Viewer.width,Viewer.height))
        self.background.convert()
        
    
  
    
    def load_sprites(self):
            """ all sprites that can rotate MUST look to the right. Edit Image files manually if necessary!"""
            print("loading sprites from 'data' folder....")
            #Viewer.images["catapult1"]= pygame.image.load(
            #     os.path.join("data", "catapultC1.png")).convert_alpha()
            
            ##self.create_selected("catapult1")
            
            Viewer.images["cannon"] = pygame.image.load(os.path.join("data", "cannon.png"))
            Viewer.images["wolf"] = pygame.image.load(os.path.join("data", "wolf.png"))
            Viewer.images["player"] = pygame.image.load(os.path.join("data", "arch-mage.png"))
            Viewer.images["castle"] = pygame.image.load(os.path.join("data", "keep-tile.png"))
            Viewer.images["tower"] = pygame.image.load(os.path.join("data", "keep-convex-bl.png"))
            
            # --- scalieren ---
            #for name in Viewer.images:
            #    if name == "bossrocket":
            #        Viewer.images[name] = pygame.transform.scale(
            #                        Viewer.images[name], (60, 60))
            
     
    def prepare_sprites(self):
        """painting on the surface and create sprites"""
        self.load_sprites()
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.flytextgroup = pygame.sprite.Group()
        #self.mousegroup = pygame.sprite.Group()
        self.bulletgroup = pygame.sprite.Group()
        self.playergroup= pygame.sprite.Group()
        self.rocketgroup = pygame.sprite.Group()
        
        #self.powerupgroup = pygame.sprite.Group()
        #self.guardiangroup = pygame.sprite.Group()
        self.castlegroup = pygame.sprite.Group()
        self.towergroup = pygame.sprite.Group()
        self.bargroup = pygame.sprite.Group()
        self.wolfgroup = pygame.sprite.Group()
        #self.group1=pygame.sprite.Group()
        #self.group2=pygame.sprite.Group()
        self.targetgroup = pygame.sprite.Group()
        VectorSprite.groups = self.allgroup
        Flytext.groups = self.allgroup, self.flytextgroup
        
        #Cannon.groups = self.allgroup, self.playergroup
        
        Bullet.groups = self.allgroup, self.bulletgroup
        Rocket.groups = self.allgroup, self.rocketgroup, self.targetgroup
        
        #PowerUp.groups = self.allgroup, self.powerupgroup
        #Guardian.groups = self.allgroup, self.guardiangroup
        Castle.groups = self.allgroup, self.castlegroup, self.targetgroup
        Wolf.groups = self.allgroup, self.wolfgroup
        Hitpointbar.groups = self.allgroup, self.bargroup
        Tower.groups = self.allgroup, self.towergroup, self.targetgroup
    
    
    def place_sprites(self):    
        """create the sprite instances and set them on the correct place on the grid,
           depending on screen resolution and gridsize"""
        # VectorSprite.numbers[0]
        self.player1 = Player(pos = pygame.math.Vector2(self.gridsize//2+self.gridsize,
                              -self.gridsize//2-self.gridsize), lookleft=False,
                              side=1)
        # VectorSprite.numbers[1]
        self.player2 = Player(pos = pygame.math.Vector2(self.gridsize//2+self.gridsize*(self.maxx-1),
                              -self.gridsize//2 - self.gridsize*(self.maxy-1)), angle = 0, lookleft=True,
                              side=2)
        # VectorSprite.numbers[2]                      
        self.castle1 = Castle(pos=pygame.math.Vector2(self.gridsize//2, -self.gridsize//2), bossnumber = self.player1.number, side=1)
        # VectorSprite.numbers[3]
        self.castle2 = Castle(pos=pygame.math.Vector2(self.gridsize//2 + self.gridsize* self.maxx,
                                                      -self.gridsize//2-self.gridsize*self.maxy), bossnumber = self.player2.number, side=2)
        
        self.wolf1 = Wolf(pos= pygame.math.Vector2(600, -400),
                          move=pygame.math.Vector2(0,30),
                          bounce_on_edge=True )
        
        
    def menu_run(self):
        running = True
        pygame.mouse.set_visible(True)
        secret_text = ""
        
        #pygame.mixer.music.load(os.path.join("data", "menu_ogg.ogg"))
        #pygame.mixer.music.play()
        
        while  running:
            
            #pygame.mixer.music.pause()
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1 # running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c and  secret_text == "":
                        secret_text = "c"
                    if event.key == pygame.K_h and secret_text == "c":
                        secret_text = "ch"
                    if event.key == pygame.K_e and secret_text == "ch":
                        secret_text = "che"
                    if event.key == pygame.K_a and secret_text == "che":
                        secret_text = "chea"
                    if event.key == pygame.K_t and secret_text == "chea":
                        secret_text = "cheat"
                        print("cheat activated")
                        Viewer.menu["cheat"] = ["back", "double-rocket", "shotgun", "power-up-and-rocket", "disable cheat"]
                        Viewer.menu["cheat"].append("sound")
                        Viewer.menu["sound"] = ["back", "enable sound", "disable sound"]
                        Viewer.menu["main"].append("cheat")
                        
           
                   # if event.key == pygame.K_ESCAPE:
                       # return -1 # running = False
                    if event.key == pygame.K_UP:
                        text = Viewer.menu[Viewer.name][Viewer.cursor]
                        if text == "back to main menu":
                            continue
                        else:
                            Viewer.cursor -= 1
                            Viewer.cursor = max(0, Viewer.cursor) # not < 0
                            Viewer.sounds["click2"].play()
                    if event.key == pygame.K_DOWN:
                        text = Viewer.menu[Viewer.name][Viewer.cursor]
                        if text == "back to main menu":
                            continue
                        else:
                            Viewer.cursor += 1
                            Viewer.cursor = min(len(Viewer.menu[Viewer.name])-1,Viewer.cursor) # not > menu entries
                            Viewer.sounds["click2"].play()
                    if event.key == pygame.K_RETURN:
                        text = Viewer.menu[Viewer.name][Viewer.cursor]
                        if text == "quit":
                            return -1
                            #Viewer.menucommandsound.play()
                        elif text in Viewer.menu:
                            # changing to another menu
                            Viewer.history.append(text) 
                            Viewer.name = text
                            Viewer.cursor = 0
                            #Viewer.menuselectsound.play()
                        elif text == "resume":
                            return
                            #pygame.mixer.music.load(os.path.join("data", "Caketown.ogg"))
                            #Viewer.menucommandsound.play()
                            #pygame.mixer.music.unpause()
                        elif text == "back":
                            Viewer.sounds["click1"].play()
                            Viewer.history = Viewer.history[:-1] # remove last entry
                            Viewer.cursor = 0
                            Viewer.name = Viewer.history[-1] # get last entry
                            #Viewer.play()
                            # direct action
                      
                        elif text == "credits":
                            Flytext(pos=pygame.math.Vector2(Viewer.width, -50),
                                    text=Viewer.credits, fontsize = 100, max_age=10,
                                    move=pygame.math.Vector2(-50,0), color=(200,200,0))  
                        
                       
                        if Viewer.name == "grid size" and text != "grid size":
                            self.gridsize = int(text)
                            Flytext(pos=pygame.math.Vector2(Viewer.width//2,-400),
                                    move=pygame.math.Vector2(0,25),
                                    max_age=4,color=(200,200,0),fontsize=44,
                                    text="grid size is now {}".format(self.gridsize))
                            self.calculate_grid()
                                    
                                     
                        
                        elif Viewer.name == "influence radius" and text != "influence radius":
                            self.influence_radius = int(text)
                            Flytext(pos=pygame.math.Vector2(Viewer.width//2,-400),
                                    move=pygame.math.Vector2(0,25),
                                    max_age=4,color=(200,200,0),fontsize=44,
                                    text="the influence radius is now {}".format(self.gridsize))
                            
                            
                        if Viewer.name == "resolution" and text != "resolution":
                            # text is something like "800x600"
                            t = text.find("x")
                            if t != -1:
                                x = int(text[:t])
                                y = int(text[t+1:])
                                Viewer.width = x
                                Viewer.height = y
                                self.set_resolution()
                                #Viewer.menucommandsound.play()
                            self.calculate_grid()
                            Flytext(pos=pygame.math.Vector2(Viewer.width//2,-400),
                                    move=pygame.math.Vector2(0,25),
                                    max_age=4,color=(200,200,0),fontsize=44,
                                    text="screen resolution is now {}x{}".format(Viewer.width, Viewer.height))
                            
                                    
                        if Viewer.name == "fullscreen":
                            if text == "true":
                                #Viewer.menucommandsound.play()
                                Viewer.fullscreen = True
                                self.set_resolution()
                            elif text == "false":
                                #Viewer.menucommandsound.play()
                                Viewer.fullscreen = False
                                self.set_resolution()
                       
                        
            # ------delete everything on screen-------
            self.screen.blit(self.background, (0, 0))
            
            
         
            # -------------- UPDATE all sprites -------             
            self.flytextgroup.update(seconds)

            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)

            # --- paint menu ----
            # ---- name of active menu and history ---
            write(self.screen, text="you are here:", x=200, y=50, color=(0,255,255))
            # display of grid size. grid must be at last 4x4
            if len(self.cells) > 3 and len(self.cells[0]) > 3:
                text1 = "grid ok"
                c1 = (0,128,0)
            else:
                text1 = "Error: grid must be at last 4x4"
                c1 = (128,0,0)
            write(self.screen, text1, x=20, y=Viewer.height-30, color=c1, fontsize = 16)
            text2 = "grid is {}x{}, grid size: {}, screen resolution: {} x {}".format(
                     self.maxx, self.maxy, self.gridsize, Viewer.width, Viewer.height)
            write(self.screen, text2, x=20, y=Viewer.height-15, color=c1, fontsize = 16)
            
            t = "main"
            for nr, i in enumerate(Viewer.history[1:]):
                #if nr > 0:
                t+=(" > ")
                t+=(i)
                #
            
            #t+=Viewer.name
            write(self.screen, text=t, x=200,y=70,color=(0,255,255))
            # --- menu items ---
            menu = Viewer.menu[Viewer.name]
            for y, item in enumerate(menu):
                write(self.screen, text=item, x=200, y=100+y*20, color=(255,255,255))
            # --- cursor ---
            write(self.screen, text="-->", x=100, y=100+ Viewer.cursor * 20, color=(255,255,255))
                        
                
            # -------- next frame -------------
            pygame.display.flip()
        #----------------------------------------------------- 
    
    def select_target(self):
        """choose the closer on of cannon1 or cannon2 as target for cannon3"""
        pass 
        #distance1 = self.cannon3.pos - self.cannon1.pos
        #distance2 = self.cannon3.pos - self.cannon2.pos
        
        #if distance1.length() < distance2.length():
        #    self.cannon3.target = self.cannon1
        #else:
        #    self.cannon3.target = self.cannon2
    
            
    
    
    def draw_grid(self):
        """draw self.gridsize=100 x 100? grid"""
        for y in range(0, Viewer.height, self.gridsize):
            pygame.draw.line(self.screen, (200,200,200),
                (0,y), (Viewer.width,y))
        for x in range(0, Viewer.width, self.gridsize):
            pygame.draw.line(self.screen, (200,200,200),
                (x, 0), (x, Viewer.height))
        
    
    def calculate_grid(self):
        """ makes (self.gridsze=100) x 100 grid, each grid cell 
            has a color value from 0 to 255
            and an radius value"""
        self.cells = []
        for y in range(0, Viewer.height, self.gridsize):
            pass
        self.maxy = y
        for x in range(0, Viewer.width, self.gridsize):
            pass
        self.maxx = x
        #print("maxx, maxy", self.maxx, self.maxy)
        if Viewer.height % self.gridsize != 0 and Viewer.height % self.gridsize < self.gridsize * 0.85 :
            self.maxy -= 1
        self.maxx = x // self.gridsize
        if Viewer.width % self.gridsize != 0 and Viewer.width % self.gridsize < self.gridsize * 0.85 :
            self.maxx -= 1
        self.maxy = y // self.gridsize
        print("maxx, maxy", self.maxx, self.maxy)
        
        for y in range(0, Viewer.height, self.gridsize):
            line = []
            for x in range(0, Viewer.width, self.gridsize):
                #c = random.randint(96,160)
                c = 128
                line.append([c,0])
            self.cells.append(line)
            
        
    def paint_cells(self):
        for y, line in enumerate(self.cells):
            for x, (color, radius) in enumerate(line):
                if color == 128:
                    c = (128,128,128)
                elif color < 128:
                    c = (color,0,0)
                else:
                    c = (0,0, color)
                pygame.draw.rect(self.screen, c,
                     (x*self.gridsize, y*self.gridsize, self.gridsize, self.gridsize))
                    
        
    def pos_to_grid(self, posvector):
        """get posvector (negative y coordinate!) and returns the (x,y)
           index of the corresponding grid cell (x and y are both positive)
        """
        try:
            px = posvector.x
            py = -posvector.y
        except:
            print("problem extracting x,y from posvector:", posvector)
        x = min(self.maxx, px // self.gridsize)
        y = min(self.maxy, py // self.gridsize)
        return x, y
        
    
    def run(self):
        """The mainloop"""
        
        running = True
        
        
        end = self.menu_run()
        if end == -1:
            running = False
        self.calculate_grid()
        self.place_sprites()
        pygame.mouse.set_visible(True)
        oldleft, oldmiddle, oldright  = False, False, False
        #self.select_target()
        
        
        minimum_sparks = 0
  
  
        #lives_cannon3 = 5
  
        count_powerup = 0
   
        #fps_warnung = False
        #pygame.mixer.music.load(os.path.join("data", "8BitMetal.ogg"))
        #pygame.mixer.music.play(loops=-1)
        
        
        while running:
            #pygame.display.set_caption("player1 hp: {} player2 hp: {}".format(
            #                     self.player1.hitpoints, self.player2.hitpoints))
            
            milliseconds = self.clock.tick(self.fps) 
            seconds = milliseconds / 1000
            self.playtime += seconds
            
            
            fps = self.clock.get_fps()
            
            # ... friction ....       
            #for p in self.playergroup:
            #    p.move *= 0.99
            
            
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
              
                        pygame.mixer.music.load(os.path.join("data", "menu_ogg.ogg"))
                        end = Viewer.menu_run(self)
                        if end == -1:
                            running = False
                        #pygame.mixer.music.load(os.path.join("data", "8BitMetal.ogg"))
                        #pygame.mixer.music.play(loops=-1)
                    
                    # ----- player 1------
                    if event.key == pygame.K_a:
                        self.player1.pos.x -= self.gridsize # left
                    if event.key == pygame.K_d:
                        self.player1.pos.x += self.gridsize # right
                    if event.key == pygame.K_w:
                        self.player1.pos.y += self.gridsize # up
                    if event.key == pygame.K_s:
                        self.player1.pos.y -= self.gridsize # down
                    
                    # --- player1 build tower -----
                    if event.key == pygame.K_LCTRL:
                        Tower(pos=pygame.math.Vector2(
                              self.player1.pos.x, self.player1.pos.y))
                    
                    
                    # ----- player 2------
                    if event.key == pygame.K_LEFT:
                        self.player2.pos.x -= self.gridsize # left
                    if event.key == pygame.K_RIGHT:
                        self.player2.pos.x += self.gridsize # right
                    if event.key == pygame.K_UP:
                        self.player2.pos.y += self.gridsize # up
                    if event.key == pygame.K_DOWN:
                        self.player2.pos.y -= self.gridsize # down
                      
                      
            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            
  
            # ------ mouse handler ------
            left,middle,right = pygame.mouse.get_pressed()
            oldleft, oldmiddle, oldright = left, middle, right

           
            # ------ joystick handler -------
            for number, j in enumerate(self.joysticks):
                if number == 0:
                    player = self.cannon1
                else:
                    continue
                x = j.get_axis(2)
                y = j.get_axis(1)
                if y > 0.2:
                    player.forward(-1)
                if y < -0.8:
                    player.forward(15)
                elif y < -0.5:
                    player.forward(10)
                elif y < -0.2:
                    player.forward(5)
                if x > 0.2:
                    player.rotate(7)
                if x < -0.2:
                    player.rotate(-7)
                
                buttons = j.get_numbuttons()
                for b in range(buttons):
                    pushed = j.get_button( b )
                    if b == 0 and pushed:
                        player.fire()
                    if b == 1 and pushed:
                        t = random.choice((self.cannon3, self.cannon2))
                        player.launch(t)
                        #if b == 5 and pushed:
                            #player.strafe_right()                
                
            # ---- tower launch rocket ----
            for t in self.towergroup:
                if random.random() < 0.01 :   # 1% chance, 30x pro sec
                    victim = random.choice((self.player2, self.castle2))
                    Rocket(pos=pygame.math.Vector2(t.pos.x, t.pos.y),
                           boss=t, target=victim, color=(3,3,3))
              
            # =========== delete everything on screen ==============
            self.screen.blit(self.background, (0, 0))
            

            #---- draw vertical border ------
            ##pygame.draw.line(self.screen, (255, 255, random.randint(200,255)), (Viewer.border_x, 0), (Viewer.border_x, Viewer.height), 5)
            # ----- draw horizontal border 
            ##pygame.draw.line(self.screen, (255, 255, random.randint(200,255)), (0, -Viewer.border_y), (Viewer.width, -Viewer.border_y),5)         
            
            self.paint_cells()
            self.draw_grid()
            
            # ------ update cells -----
            for y, line in enumerate(self.cells):
                for x, (color, radius) in enumerate(line):
                    if color  == 0 or color == 255:
                        continue
                    cellvector = pygame.math.Vector2(x*self.gridsize+self.gridsize//2, -y*self.gridsize-self.gridsize//2)
                    for p in self.playergroup:
                        distance = p.pos - cellvector
                        if distance.length() < self.influence_radius:
                            #print("blubb", x, y, radius, color)
                            radius += 1
                            if radius > 70:
                                radius = 1
                                if p.number == 0:
                                    delta = -1
                                elif p.number == 1:
                                    delta = 1
                                else:
                                    delta = 0
                                color += delta * self.convert_rate
                                color = min(255, color)
                                color = max(0, color)
                                if color == 0 or color == 255:
                                    radius = 0
                                self.cells[y][x][0] = color
                            self.cells[y][x][1] = radius
                            pygame.draw.circle(self.screen, (random.randint(128,255), random.randint(128,255), random.randint(128,255)),
                                (x*self.gridsize+self.gridsize//2, y*self.gridsize+self.gridsize//2), radius+1, 1)
                
                            break
                    else:
                        self.cells[y][x][1] = 0
              
            
            #--- trails for rockets ----
            for r in self.rocketgroup:
                if len(r.trail) > 1:
                    for rank, (x,y) in enumerate(r.trail):
                        if rank > 0:
                            pygame.draw.line(self.screen, r.color, 
                                        (x,y), (old[0], old [1]), (rank // 10))
                        old = (x,y)
            
            ##self.paint_world()
                       
            # write text below sprites (fps, sparks)
            write(self.screen, "FPS: {:8.3}".format(
                self.clock.get_fps() ), x=Viewer.width-200, y=10, color=(200,200,200))
            write(self.screen, "Sparks: " + str(minimum_sparks), x=300, y=10, color=(200,200,200))
            write(self.screen, str(len(self.bulletgroup)), x=Viewer.width-100, y=Viewer.height-30, color=(200,200,200))
            # ----- collision detection between player and bullets---
            for p in self.playergroup:
                crashgroup=pygame.sprite.spritecollide(p,
                           self.bulletgroup, False, 
                           pygame.sprite.collide_mask)
                for o in crashgroup:
                      if o.boss.number == p.number:
                          continue
                      
                      
                      elastic_collision(o, p)
                      
                      
                      o.kill()
                      
            #---- collision with rocket? ----          
            for p in self.playergroup:
                crashgroup=pygame.sprite.spritecollide(p,
                           self.rocketgroup, False, 
                           pygame.sprite.collide_mask)
                           
                           
                for o in crashgroup:
                    if o.boss.number == p.number:
                        continue
                    else: 
                        Explosion(posvector=p.pos, minsparks=50, maxsparks=60)
                        select_sound = random.choice((1, 2, 3, 4))
                        if select_sound == 1:
                            Viewer.sounds["explosion_rocket1"].play()
                        if select_sound == 2:
                            Viewer.sounds["explosion_rocket2"].play()
                        if select_sound == 3:
                            Viewer.sounds["explosion_rocket3"].play()
                        if select_sound == 4:
                            Viewer.sounds["explosion_rocket4"].play()
                        o.kill()
                        p.lives -= 1
                        
                        if p.number == 0:
                            Viewer.border_x += 5
                            self.update_border()
                        if p.number == 1:
                            Viewer.border_x -= 5
                            self.update_border()

                        
                #... between rocket and rocket?
                 
                for r1 in self.rocketgroup:
                    crashgroup=pygame.sprite.spritecollide(r1,
                           self.rocketgroup, False, 
                           pygame.sprite.collide_mask)
                           
                           
                    for r2 in crashgroup:
                        if r2.number <= r1.number:
                            continue
                        if r1.boss.number == r2.boss.number:
                            continue
                        else: 
                            Explosion(posvector=r2.pos, minsparks=10, maxsparks=20)
                            select_sound = random.choice((1, 2, 3, 4))
                            if select_sound == 1:
                                Viewer.sounds["explosion_rocket1"].play()
                            if select_sound == 2:
                                Viewer.sounds["explosion_rocket2"].play()
                            if select_sound == 2:
                                Viewer.sounds["explosion_rocket3"].play()
                            if select_sound == 2:
                                Viewer.sounds["explosion_rocket4"].play()
                            r1.kill()
                            r2.kill()      
              
            #---- collision between player and PowerUp? ----
            
            for p in self.playergroup:
                crashgroup=pygame.sprite.spritecollide(p,
                           self.powerupgroup, False, 
                           pygame.sprite.collide_mask)
                for o in crashgroup:
                    o.kill()
                    p.lives += 1
            
       
                   
            # ================ UPDATE all sprites =====================
            self.allgroup.update(seconds)

            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)

            
           
                
            # -------- next frame -------------
            pygame.display.flip()
        #-----------------------------------------------------
        pygame.mouse.set_visible(True)    
        pygame.quit()

if __name__ == '__main__':
    Viewer(1430,800).run()
