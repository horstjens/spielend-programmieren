"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: https://github.com/horstjens/
idea: python3/pygame 2d vector dungeon crawl roguelike

"""
import pygame
import random
import os

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


def fight(attacker, defender):
    strike(attacker, defender, 1)
    if defender.hitpoints > 0:
        strike(defender, attacker, -1)
        
def strike(attacker, defender, direction):
    """attacker strikes once against defender"""
    attacker.attack_animation()
    # attack vs defense
    d1 = random.randint(1,6)
    d2 = random.randint(1,6)
    d3 = random.randint(1,6)
    d4 = random.randint(1,6)
    # attack value + d1+d2 > defense value + d3 +d4 ?
    a = attacker.attack + d1 + d2
    d = defender.defense + d3 + d4
    if d >= a:
        Flytext(text="Successful defense {} vs. {}".format(a,d),
                pos = pygame.math.Vector2(defender.pos.x, defender.pos.y),
                move=pygame.math.Vector2(0,15*direction),
                color=(0,200,0))
    else:
        Flytext(text="Successful attack {} vs {}".format(a,d),
                pos = pygame.math.Vector2(attacker.pos.x, attacker.pos.y),
                move=pygame.math.Vector2(0,15*direction),
                color=(0,0,200))
        damage = a-d
        Flytext(text="- {} HP".format(damage),
                pos = pygame.math.Vector2(defender.pos.x, defender.pos.y),
                move=pygame.math.Vector2(0,4*direction),
                color=(255,0,0))
        defender.hitpoints -= damage
    
                
                
    


class VectorSprite(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    numbers = {} # { number, Sprite }

    def __init__(self, **kwargs):
        self._default_parameters(**kwargs)
        self._overwrite_parameters()
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        self.number = VectorSprite.number # unique number for each sprite
        VectorSprite.number += 1
        VectorSprite.numbers[self.number] = self
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
        if "gravity" not in kwargs:
            self.gravity = None
        if "color" not in kwargs:
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

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
        # ---- movement with/without boss ----
        if self.bossnumber is not None:
            if self.kill_with_boss:
                if self.bossnumber not in VectorSprite.numbers:
                    self.kill()
            if self.sticky_with_boss and self.bossnumber in VectorSprite.numbers:
                boss = VectorSprite.numbers[self.bossnumber]
                self.pos = pygame.math.Vector2(boss.pos.x, boss.pos.y)
                self.set_angle(boss.angle)
        self.pos += self.move * seconds
        self.move *= self.friction 
        if self.gravity is not None:
            self.move += self.gravity
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

class Wall(VectorSprite):
    
    def _overwrite_parameters(self):
        self.color = (139, 105, 20)
        self.hitpoints = 200
        
    def crack(self):
        # border point
        border = random.choice(("n","s","w","e"))
        if border == "n":
            x1 = random.randint(0, 50)
            y1 = 0
            x2 = random.randint(20,30)
            y2 = random.randint(15,25)
        if border == "s":
            x1 = random.randint(0, 50)
            y1 = 50
            x2 = random.randint(20,30)
            y2 = random.randint(25,35)
        if border == "w":
            x1 = 0
            y1 = random.randint(0, 50)
            x2 = random.randint(15,25)
            y2 = random.randint(20,30)
        if border == "e":
            x1 = 50
            y1 = random.randint(0, 50)
            x2 = random.randint(25,35)
            y2 = random.randint(20,30)
        # draw crackline
        thick = random.randint(1,3)
        pygame.draw.line(self.image, (0,0,0), (x1,y1), (x2, y2), thick)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
            
        
        
    def create_image(self):
        new = [0,0,0]
        for a in range(3):
            c = self.color[a] + random.randint(-20,20)
            c = min(c, 255)
            c = max(c, 0)
            new[a] = c
        self.color = new
        self.image = pygame.Surface((50,50))
        self.image.fill(self.color)
        pygame.draw.rect(self.image, (0,0,0), (0,0,49,49),1)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        print(self.pos)
            
        
        
        
    

class Wizard(VectorSprite):
    
    def _overwrite_parameters(self):
        self.lookright = True
        self.attacktime = 0
        self._layer = 15
        self.attack = 7
        self.defense = 5
        
        
    def update(self, seconds):
        if self.age < self.attacktime:
            if self.lookright:
                self.image = self.image2
            else:
                self.image = self.image3
        else:
            if self.lookright:
                self.image = self.image0
            else:
                self.image = self.image1
        VectorSprite.update(self, seconds)
        
    def attack_animation(self, duration=0.15):
        self.attacktime = self.age + duration
        if self.lookright:
            self.image = self.image2 
        else:
            self.image = self.image3
        
    
    def create_image(self):
        self.image=Viewer.images["wizard"]        
        self.image0 = self.image.copy()
        self.image1 = pygame.transform.flip(self.image, True, False)
        
        self.image2 = Viewer.images["wizard-a"]
        self.image3 = pygame.transform.flip(self.image2, True, False)
        
        self.rect = self.image.get_rect()


class Lizard(Wizard):
    
    def _overwrite_parameters(self):
        self.attack = 5
        self.defense = 2
        self.attacktime = 0
        self.lookright = True
    
    def create_image(self):
        self.image=Viewer.images["reptile"]        
        self.image0 = self.image.copy()
        self.image1 = pygame.transform.flip(self.image, True, False)
        
        self.image2 = Viewer.images["reptile-a"]
        self.image3 = pygame.transform.flip(self.image2, True, False)
        
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
            
    def fire(self):
        for i in range(1):
            v = pygame.math.Vector2(200,0)
            v.rotate_ip(self.angle + i)
            Bullet(boss=self, mass=500,
                   pos=pygame.math.Vector2(self.pos.x, self.pos.y),
                   angle=self.angle+i, move = v+self.move, color=self.color)
        # --- recoil ----
        v = pygame.math.Vector2(50,0)
        v.rotate_ip(self.angle + 180)
        self.move += v
            
    def launch(self, enemy):
            if self.age < self.ready_to_launch:
                return # not yet ready, wait a bit
            self.ready_to_launch = self.age + 1.5 # wait that time
            v = pygame.math.Vector2(50,0)
            v.rotate_ip(self.angle)
            Rocket(boss=self, target=enemy, mass=50, max_age=7.4,
                   pos=pygame.math.Vector2(self.pos.x, self.pos.y),
                   angle=self.angle, move = v+self.move, color=self.color)
    
    def create_image(self):
        self.image=Viewer.images["cannon"]
        
        self.image0 = self.image.copy()
       # self.image0.set_colorkey((0,0,0))
       # self.image0.convert_alpha()
        self.rect = self.image.get_rect()

    def kill(self):
        Explosion(posvector=self.pos, red=200, red_delta=25, minsparks=500, maxsparks=600, maxlifetime=7)
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
 
 
class Extra(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 9
        self.kill_on_edge = True
        self.pos = pygame.math.Vector2(random.randint(0,Viewer.width),
                                       random.randint(-Viewer.height,0))
        v = pygame.math.Vector2(random.randint(10, 25), 0)
        v.rotate_ip(random.randint(0,360))
        self.move = v
                                              
    
    def create_image(self):
        self.image = pygame.Surface((30,30))
        pygame.draw.circle(self.image, (200,200,200), (15,15), 15)
        pygame.draw.circle(self.image, (200,100,200), (15,15), 12)
        pygame.draw.circle(self.image, (0,0,0), (15,15), 3)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()                          
    
     
   
class Rocket(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 9
        self.kill_on_edge = True
        self.trail = []
    
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        diff = self.target.pos - self.pos
        r = pygame.math.Vector2(1,0)
        a = -diff.angle_to(r)
        # rotate the sprite
        self.set_angle(a)
        #self.move.rotate_ip(a)
        diff.normalize_ip() # diff has lenght 1 now
        self.move *= 0.8   # friction, reduce old move
        self.move += diff * 20  # add new move
        self.trail.insert(0,(self.pos.x, -self.pos.y))
        if len(self.trail) > 255:
            self.trail = self.trail[:256]
    
    def kill(self):
        #Explosion(posvector=self.pos, minsparks=50, maxsparks=150)
        VectorSprite.kill(self)
    
    def create_image(self):
        self.image = pygame.Surface((30,10))
        pygame.draw.circle(self.image, (1,1,1), (25,5), 5)
        pygame.draw.rect(self.image, self.color, (0,0,25,10))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()                          
    

class Bullet(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 9
        self.kill_on_edge = True
        #self.color = (255,255,0) # yellow

    def create_image(self):
        r,g,b = self.color
        self.image = pygame.Surface((10,10))
        
        pygame.draw.circle(self.image, self.color, (5,5), 5)
        
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()                          
    

class Gem(VectorSprite):

    def _overwrite_parameters(self):
        self._layer = 9
        self.kill_on_edge = True

    def create_image(self):
        self.image = pygame.Surface((10,10)) 
        pygame.draw.polygon(self.image, self.color,
             [(5,0), (10,3), (10,7), (5,10), (0,7), (0,3)])
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
                 minsparks=5, maxsparks=20, 
                 shape="spark", gravity = None):
                     
                     
        for s in range(random.randint(minsparks,maxsparks)):
            v = pygame.math.Vector2(1,0) # vector aiming right (0°)
            a = random.randint(minangle,maxangle)
            v.rotate_ip(a)
            speed = random.randint(minspeed, maxspeed)
            duration = random.random() * maxlifetime # in seconds
            red   = randomize_color(red, red_delta)
            green = randomize_color(green, green_delta)
            blue  = randomize_color(blue, blue_delta)
            
            if shape == "spark":
                Spark(pos=pygame.math.Vector2(posvector.x, posvector.y),
                      angle= a, move=v*speed, max_age = duration, 
                      color=(red,green,blue), kill_on_edge = True,
                      gravity=gravity)
            elif shape == "gem":
                Gem(pos=pygame.math.Vector2(posvector.x, posvector.y),
                      angle= a, move=v*speed, max_age = duration, 
                      color=(red,green,blue), kill_on_edge = True,
                      gravity=gravity)


        
    
    

class Viewer(object):
    width = 0
    dungeon = []
    gold = 0
    height = 0
    images = {}
    sounds = {}
    menu =  {"main":            ["resume", "settings", "credits", "cheat","plant tomatoes", "quit" ],
            #main
            # cheatmenu 
            "cheat":           ["back", "shotgun-effect", "double-missles"],
            "settings":        ["back", "video", "difficulty", "reset all values"],
            #settings
            "difficulty":      ["back", "powerups", "bosshealth", "playerhealth"],
            "video":           ["back", "resolution", "fullscreen"],
            #difficulty
            "bosshealth":      ["back", "1000", "2500", "5000", "10000"],
            "playerhealth":    ["back", "100", "250", "500", "1000"],
            "powerups":        ["back", "laser", "bonusrockets", "heal", "shield", "speed"],
            #powerups
            "bonusrockets":    ["back", "bonusrocketincrease", "bonusrocket duration"],
            "laser":           ["back", "laserdamage", "laser duration"],
            "heal":            ["back", "heal effectiveness"],
            "shield":          ["back", "bossrocket deflection", "shield duration"],
            "speed":           ["back", "speed increase", "speed duration"],
            #powerup effects
            "bonusrocketincrease": ["back", "1", "2", "3", "5", "10"],
            "bonusrocket duration": ["back", "10", "30", "60"],
            "laserdamage":     ["back", "3", "5", "10"],
            "laser duration": ["back", "10", "30", "60"],            
            "heal effectiveness": ["back", "50", "100", "250", "full health"],
            "bossrocket deflection": ["back", "true", "false"],
            "shield duration": ["back", "10", "30", "60"],
            "speed increase":  ["back", "3", "5", "10", "15"],
            "speed duration":  ["back", "10", "30", "60"],
            #video
            "resolution":      ["back", "720p", "1080p", "1440p", "4k"],
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
        #self.load_sounds()
        #self.world = World()
        #print(self.world)
        
        
    def load_sounds(self):
        pygame.mixer.music.load(os.path.join("data", "melody.ogg"))
        Viewer.sounds["click"]=  pygame.mixer.Sound(
                 os.path.join("data", "click1.wav"))
        Viewer.sounds["back"] =  pygame.mixer.Sound(
                 os.path.join("data", "click2.wav"))
        return
    
    
    def set_resolution(self):
        if Viewer.fullscreen:
             self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF|pygame.FULLSCREEN)
        else:
             self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.loadbackground()
    
    
    def loadbackground(self):
        
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((64,64,64)) # fill background 
            
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
            Viewer.images["wizard"] = pygame.image.load(os.path.join(
                                      "data", "arch-mage.png"))
            Viewer.images["reptile"] = pygame.image.load(os.path.join(
                                       "data", "fighter.png"))
            Viewer.images["wizard-a"] = pygame.image.load(os.path.join(
                                      "data", "arch-mage-attack.png"))
            Viewer.images["reptile-a"] = pygame.image.load(os.path.join(
                                       "data", "fighter-attack.png"))
            
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
        self.playergroup = pygame.sprite.Group()
        self.rocketgroup = pygame.sprite.Group()
        self.enemygroup = pygame.sprite.Group()
        self.wallgroup = pygame.sprite.Group()
        
        VectorSprite.groups = self.allgroup
        Flytext.groups = self.allgroup, self.flytextgroup
        
        #Cannon.groups = self.allgroup, self.playergroup
        #Bullet.groups = self.allgroup, self.bulletgroup
        #Rocket.groups = self.allgroup, self.rocketgroup
        Lizard.groups = self.allgroup, self.enemygroup
        Wall.groups = self.allgroup, self.wallgroup
        
        #Catapult.groups = self.allgroup,
        #self.player1 =  Player(imagename="player1", warp_on_edge=True, pos=pygame.math.Vector2(Viewer.width/2-100,-Viewer.height/2))
        #self.player2 =  Player(imagename="player2", angle=180,warp_on_edge=True, pos=pygame.math.Vector2(Viewer.width/2+100,-Viewer.height/2))
        #self.cannon1 = Cannon(bounce_on_edge = True)
        #self.cannon2 = Cannon(bounce_on_edge = True)
        self.player1 = Wizard(pos=pygame.math.Vector2(500,-200))
        self.enemy1 = Lizard(pos=pygame.math.Vector2(800,-250))
        
   
    def menu_run(self):
        running = True
        pygame.mouse.set_visible(False)
        
        
        while running:
            
            #pygame.mixer.music.pause()
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1 # running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return -1 # running = False
                    
                    if event.key == pygame.K_d:
                        x = random.randint(0,Viewer.width)
                        y = random.randint(-Viewer.height, 0)
                        g = pygame.math.Vector2(0, -1.5)
                        #Gem(pos=pygame.math.Vector2(x,y),
                        #    max_age = 2)
                        Explosion(posvector=pygame.math.Vector2(x,y),
                                  shape="gem", gravity=g)
                        
                    
                    
                    if event.key == pygame.K_UP:
                        Viewer.cursor -= 1
                        Viewer.cursor = max(0, Viewer.cursor) # not < 0
                        #Viewer.menusound.play()
                        #Viewer.sounds["click"].play()
                    if event.key == pygame.K_DOWN:
                        Viewer.cursor += 1
                        Viewer.cursor = min(len(Viewer.menu[Viewer.name])-1,Viewer.cursor) # not > menu entries
                        #Viewer.menusound.play()
                        #Viewer.sounds["click"].play()
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
                            #Viewer.menucommandsound.play()
                            #pygame.mixer.music.unpause()
                        elif text == "back":
                            Viewer.history = Viewer.history[:-1] # remove last entry
                            Viewer.cursor = 0
                            Viewer.name = Viewer.history[-1] # get last entry
                            #Viewer.menucommandsound.play()
                            
                            # direct action
                        elif text == "credits":
                            Flytext(x=700, y=400, text="by Bigm0 and BakTheBig", fontsize = 100)  

                        elif text == "plant tomatoes":
                            Viewer.gold += 1
                            # ----- Gold Explosion ------
                            Explosion(posvector=pygame.math.Vector2(600,-400))

                        if Viewer.name == "resolution":
                            # text is something like 800x600
                            t = text.find("x")
                            if t != -1:
                                x = int(text[:t])
                                y = int(text[t+1:])
                                Viewer.width = x
                                Viewer.height = y
                                self.set_resolution()
                                #Viewer.menucommandsound.play()
                                    
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
            #self.flytextgroup.update(seconds)
            self.allgroup.update(seconds)

            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)

            # --- paint menu ----
            # ---- name of active menu and history ---
            write(self.screen, text="you are here:", x=200, y=50, color=(0,255,255))
            
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
    
    def paint_dungeon(self):
        # --- paint a 50 x 50 grid ----
        c = (128,128,128) # grey
        for x in range(0, Viewer.width+50, 50):
            pygame.draw.line(self.screen, c, (x-25,0), (x-25, Viewer.height))
        for y in range(0, Viewer.height+50, 50):
            pygame.draw.line(self.screen, c, (0, y-25), (Viewer.width, y-25))
        
    
    def create_level(self):
        for w in self.wallgroup:
            w.kill()
        # --- outer wall ---
        for x in range(0, Viewer.width, 50):
            Wall(pos=pygame.math.Vector2(x, 0))
        for y in range(50, Viewer.height, 50):
            Wall(pos=pygame.math.Vector2(0,-y))
        for x2 in range(0, x, 50):
            Wall(pos=pygame.math.Vector2(x2, -y-50))
        for y2 in range(0, Viewer.height, 50):
            Wall(pos=pygame.math.Vector2(x, -y2-50))
        # -------- random blocks ----------
        for x in range(50, Viewer.width-50, 50):
            for y in range(50, Viewer.height-50, 50):
                if random.random() < 0.15:
                    Wall(pos=pygame.math.Vector2(x,-y))
        # --- no wall on players / enemies -----
        for w in self.wallgroup:
            if w.pos == self.player1.pos:
                w.kill()
            for e in self.enemygroup:
                if w.pos == e.pos:
                    w.kill()
                    
                    
                    
                    
                    
        
        
         
    
    def run(self):
        """The mainloop"""
        
        running = True
        self.menu_run()
        self.create_level()
        pygame.mouse.set_visible(True)
        oldleft, oldmiddle, oldright  = False, False, False
        #pygame.mixer.music.play(loops=-1)
        while running:
            #pygame.display.set_caption("player1 hp: {} player2 hp: {}".format(
            #                     self.player1.hitpoints, self.player2.hitpoints))
            
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            
            
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        
                        #running = False
                        self.menu_run() 
                        
                        
                    # --- move player 1 (wizard) -----
                    dx, dy = 0, 0
                    if event.key == pygame.K_UP:
                        #self.player1.pos.y += 50
                        dy = 50
                        
                    if event.key == pygame.K_DOWN:
                        #self.player1.pos.y -= 50
                        dy = -50
                        
                    if event.key == pygame.K_RIGHT:
                        dx = 50
                        self.player1.lookright = True
                        
                        
                    if event.key == pygame.K_LEFT:
                        dx = -50
                        self.player1.lookright = False
                    
                    # ---- check wall for moving player 1
                    for w in self.wallgroup:
                        if w.pos.x == self.player1.pos.x + dx and w.pos.y==self.player1.pos.y + dy:
                            self.player1.attack_animation()
                            w.crack()
                            w.hitpoints -= random.randint(1,10)
                            Explosion(posvector = pygame.math.Vector2(
                                    self.player1.pos.x + dx//2, self.player1.pos.y + dy//2))
                            dx , dy = 0, 0 # player must stop
                            break
                    # ----- check enemy for moving player 1
                    for e in self.enemygroup:
                        if e.pos.x == self.player1.pos.x + dx and e.pos.y==self.player1.pos.y + dy:
                            
                            ## fight
                            fight(self.player1, e)
                            Explosion(posvector = pygame.math.Vector2(
                                    self.player1.pos.x + dx//2, self.player1.pos.y + dy//2))
                            dx , dy = 0, 0 # player must stop
                            break
                    
                    # ---- move the player -----
                    self.player1.pos.x += dx
                    self.player1.pos.y += dy
                        
                    
                    # --- attack for player1 -----
                    #if event.key == pygame.K_c:
                    #    self.player1.attack()
                        
                    # --- magic for player1 ----
                    if event.key == pygame.K_SPACE:
                        Explosion(posvector = self.player1.pos,
                                  red=255, blue=255, green=0)
                        
                    
                    
            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            # -------- exit game with ctrl + q ? -------
            if pressed_keys[pygame.K_LCTRL] and pressed_keys[pygame.K_q]:
                running = False
        
            # ------ mouse handler ------
            left,middle,right = pygame.mouse.get_pressed()
            oldleft, oldmiddle, oldright = left, middle, right

            # ------ joystick handler -------
            for number, j in enumerate(self.joysticks):
                if number == 0:
                    player = self.cannon1
                else:
                    continue
                x = j.get_axis(0)
                y = j.get_axis(1)
                #if y > 0.2:
                #    player.forward(-1)
                #if y < -0.8:
                #    player.forward(15)
                #elif y < -0.5:
                #    player.forward(10)
                #elif y <  -0.2:
                #    player.forward(5)
                
                #if x > 0.2:
                #    player.rotate(-5)
                #if x < -0.2:
                #    player.rotate(5)
                
                buttons = j.get_numbuttons()
                for b in range(buttons):
                    pushed = j.get_button( b )
                    #if b == 0 and pushed:
                    #     player.fire()
                    #if b == 1 and pushed:
                    #    t = random.choice((self.cannon2,
                    #                       self.cannon3))
                    #    player.launch(t)
                
              
            # =========== delete everything on screen ==============
            self.screen.blit(self.background, (0, 0))
            self.paint_dungeon()
            # ----trails for rockets------
            #for r in self.rocketgroup:
            #    if len(r.trail) > 1:
            #        for rank, (x,y) in enumerate(r.trail):
            #            if rank > 0:
            #                pygame.draw.line(self.screen, r.color,
            #                   (x,y), (old[0], old[1]),(rank // 10))
            #            old = (x,y)
            
            ##self.paint_world()
                       
            # write text below sprites
           
            
            # ----- collision detection between player and Bullet---
            #for p in self.playergroup:
            #    crashgroup=pygame.sprite.spritecollide(p,
            #               self.bulletgroup, False, 
            #               pygame.sprite.collide_mask)
            #    for o in crashgroup:
            #        if o.boss.number == p.number:
            #            continue
            #        elastic_collision(o, p)
            #        Explosion(posvector=o.pos)
            #        o.kill()
            #        # p.hitpoints -= 1
            
                
            
           
            # ================ UPDATE all sprites =====================
            self.allgroup.update(seconds)
            # --- all enemys must look to player ----
            for e in self.enemygroup:
                if e.pos.x < self.player1.pos.x:
                    e.lookright = True
                elif e.pos.x > self.player1.pos.x:
                    e.lookright = False

            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)
            #print(self.allgroup)
            # ----- FPS -----
            write(self.screen, "FPS: {:8.3}".format(
                self.clock.get_fps() ), x=Viewer.width-200, y=10, color=(0,255,0), fontsize=12)
            
           
                
            # -------- next frame -------------
            pygame.display.flip()
        #-----------------------------------------------------
        pygame.mouse.set_visible(True)    
        pygame.quit()

if __name__ == '__main__':
    Viewer(1430,800).run()
