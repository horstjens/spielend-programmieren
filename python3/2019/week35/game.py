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
            self.damage = 1
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
        if self.number in VectorSprite.numbers:
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


class Soldier(VectorSprite):
    
     def _overwrite_parameters(self):
        self._layer = 5
        self.hitpoints = 50
        self.hitpointsfull = 50
        self.weaponrange = 200
        Hitpointbar(bossnumber=self.number, kill_with_boss = True,
                    sticky_with_boss = True, ydistance=50, width=72,
                    always_calculate_image = True)
        if self.side == 2:
            self.color = (0,0,255)
        elif self.side == 1:
            self.color = (255,0,0)
                    
     def create_image(self):
        self.image=Viewer.images["soldier"]
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        

    

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
        self._layer = 6
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


class Flytext(VectorSprite):
    
    def _overwrite_parameters(self):
        self._layer = 7  # order of sprite layers (before / behind other sprites)
        self.r, self.g, self.b = self.color
        
    def create_image(self):
        self.image = make_text(self.text, (self.r, self.g, self.b), self.fontsize)  # font 22
        self.rect = self.image.get_rect()
 


 
class Castle(VectorSprite):
        
    def _overwrite_parameters(self):
        self.hitpoints = 1000
        self.hitpointsfull = 1000
        self.max_army = 4
        Hitpointbar(bossnumber=self.number, kill_with_boss = True,
                    sticky_with_boss = True, ydistance=50, width=72,
                    always_calculate_image = True)
        
    
    def create_image(self):
        self.image=Viewer.images["castle"]
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        

class Tower(VectorSprite):

    def _overwrite_parameters(self):
        Hitpointbar(bossnumber=self.number, kill_with_boss = True,
                    sticky_with_boss = True, ydistance=50, width=72,
                    always_calculate_image = True)
        self.weaponrange = 300
        if self.side == 2:
            self.color = (0,0,255)
        elif self.side == 1:
            self.color = (255,0,0)

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
           try:
               diff.normalize_ip()
               self.move += diff * 25
           except:
               print("problem with normalizing diffvector", diff)
           self.move *= 0.8
           
           
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
         try:
             boss = VectorSprite.numbers[self.bossnumber]
         except:
             return
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
        damage = 1
        #self.color = self.boss.color
        
        
    def create_image(self):
        self.image = pygame.Surface((10,2))
        if self.side == 1:
            self.image.fill((255,0,255))
        elif self.side == 2:
            self.image.fill((255,255,0))
        else:
            self.image.fill((255,255,255))
        #pygame.draw.circle(self.image, self.color, (5,5), 5)
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
        #r = randomize_color(r,50)
        #g = randomize_color(g,50)
        #b = randomize_color(b,50)
        self.image = pygame.Surface((10,10))
        pygame.draw.line(self.image, (r,g,b), 
                         (10,5), (5,5), 3)
        pygame.draw.line(self.image, (r,g,b),
                          (5,5), (2,5), 1)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()                          
        
class Ring(VectorSprite):
    
     def _overwrite_parameters(self):
        self._layer = 9
        self.kill_on_edge = True
        
     def create_image(self):
        r,g,b = self.color
        #r = randomize_color(r,50)
        #g = randomize_color(g,50)
        #b = randomize_color(b,50)
        self.image = pygame.Surface((16,16))
        r1 = random.randint(2,8)
        pygame.draw.circle(self.image, (r,g,b), 
                         (15,15), r1)
        r2 = random.randint(1, r1-1)
        pygame.draw.circle(self.image, (r,g,b), 
                         (15,15), r2)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect= self.image.get_rect()
        self.image0 = self.image.copy()  
        self.rect.centerx, self.rect.centery = self.pos.x, self.pos.y

class Explosion():
    """emits a lot of sparks, for Explosion or Player engine"""
    def __init__(self, posvector, minangle=0, maxangle=360, maxlifetime=3,
                 minspeed=5, maxspeed=150, red=255, red_delta=0, 
                 green=225, green_delta=25, blue=0, blue_delta=0,
                 minsparks=5, maxsparks=20, shape="spark"):
        for s in range(random.randint(minsparks,maxsparks)):
            v = pygame.math.Vector2(1,0) # vector aiming right (0°)
            a = random.uniform(minangle,maxangle)
            v.rotate_ip(a)
            speed = random.uniform(minspeed, maxspeed)
            duration = random.random() * maxlifetime # in seconds
            red   = randomize_color(red, red_delta)
            green = randomize_color(green, green_delta)
            blue  = randomize_color(blue, blue_delta)
            if shape=="spark":
                Spark(pos=pygame.math.Vector2(posvector.x, posvector.y),
                      angle= a, move=v*speed, max_age = duration, 
                      color=(red,green,blue), kill_on_edge = True)
            elif shape == "ring":
                Ring(pos=pygame.math.Vector2(posvector.x, posvector.y),
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
        self.convert_rate = 8.6 # how much color value (128=neutral, 0/255=full) changes per second
        self.convert_rate_back = 0.2 # how fast an "alone", not fully converted field changes per second back to neutral
        #self.convert_rate_slow = 1.5 # how much color value changes per second if already full converted to opponent
        
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
            Viewer.images["soldier"] = pygame.image.load(os.path.join("data", "scout-ranged-1.png"))
            Viewer.images["farm1"] = pygame.image.load(os.path.join("data", "farm-veg-spring.png"))
            Viewer.images["farm2"] = pygame.image.load(os.path.join("data", "farm-veg-spring2.png"))
            Viewer.images["fire1"] = pygame.image.load(os.path.join("data", "fire1.png"))
            Viewer.images["forest1"] = pygame.image.load(os.path.join("data", "mixed-summer.png"))
            Viewer.images["water1"] = pygame.image.load(os.path.join("data", "ocean-A08.png"))
            Viewer.images["water1"] = pygame.image.load(os.path.join("data", "ocean-A09.png"))
            Viewer.images["forest2"] = pygame.image.load(os.path.join("data", "pine.png"))
            Viewer.images["swamp1"] = pygame.image.load(os.path.join("data", "reed.png"))
            Viewer.images["swamp1"] = pygame.image.load(os.path.join("data", "reed2.png"))
            Viewer.images["rocks1"] = pygame.image.load(os.path.join("data", "rocks.png"))
            Viewer.images["rocks2"] = pygame.image.load(os.path.join("data", "rocks2.png"))
            Viewer.images["windmill"] = pygame.image.load(os.path.join("data", "windmill-01.png"))
            
            
            
            
            
            
            
            
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
        self.armygroup = pygame.sprite.Group()
        self.movementblockgroup = pygame.sprite.Group()
        #self.powerupgroup = pygame.sprite.Group()
        #self.guardiangroup = pygame.sprite.Group()
        self.castlegroup = pygame.sprite.Group()
        self.towergroup = pygame.sprite.Group()
        self.bargroup = pygame.sprite.Group()
        self.wolfgroup = pygame.sprite.Group()
        #self.group1=pygame.sprite.Group()
        #self.group2=pygame.sprite.Group()
        self.targetgroup = pygame.sprite.Group()
        self.targetgroup2 = pygame.sprite.Group()
        VectorSprite.groups = self.allgroup
        Flytext.groups = self.allgroup, self.flytextgroup
        
        #Cannon.groups = self.allgroup, self.playergroup
        
        Bullet.groups = self.allgroup, self.bulletgroup
        Rocket.groups = self.allgroup, self.rocketgroup, self.targetgroup2
        Player.groups = self.allgroup, self.playergroup, self.movementblockgroup, self.targetgroup, self.targetgroup2
        #PowerUp.groups = self.allgroup, self.powerupgroup
        #Guardian.groups = self.allgroup, self.guardiangroup
        Soldier.groups = self.allgroup, self.armygroup, self.targetgroup, self.targetgroup2
        Castle.groups = self.allgroup, self.castlegroup, self.movementblockgroup, self.targetgroup, self.targetgroup2
        Wolf.groups = self.allgroup, self.wolfgroup, self.targetgroup, self.targetgroup2
        Hitpointbar.groups = self.allgroup, self.bargroup
        Tower.groups = self.allgroup, self.towergroup, self.movementblockgroup, self.targetgroup, self.targetgroup2
    
    
    def place_sprites(self):    
        """create the sprite instances and set them on the correct place on the grid,
           depending on screen resolution and gridsize"""
        # VectorSprite.numbers[0]
        self.player1 = Player(pos = pygame.math.Vector2(self.gridsize//2+self.gridsize,
                              -self.gridsize//2-self.gridsize), lookleft=False,
                              side=1, gold=0, gold_per_grid = 1.0)
        # VectorSprite.numbers[1]
        self.player2 = Player(pos = pygame.math.Vector2(self.gridsize//2+self.gridsize*(self.maxx-1),
                              -self.gridsize//2 - self.gridsize*(self.maxy-1)), angle = 0, lookleft=True,
                              side=2, gold=0, gold_per_grid = 1.0)
        # VectorSprite.numbers[2]                      
        self.castle1 = Castle(pos=pygame.math.Vector2(self.gridsize//2, -self.gridsize//2), bossnumber = self.player1.number, side=1)
        # VectorSprite.numbers[3]
        self.castle2 = Castle(pos=pygame.math.Vector2(self.gridsize//2 + self.gridsize* self.maxx,
                                                      -self.gridsize//2-self.gridsize*self.maxy), bossnumber = self.player2.number, side=2)
        
        self.wolf1 = Wolf(pos= pygame.math.Vector2(600, -400),
                          move=pygame.math.Vector2(0,30),
                          bounce_on_edge=True )
        Tower(side=0, pos=pygame.math.Vector2(Viewer.width//2,
            -Viewer.height//2))
        for t in range(5):
            x = random.randint(0, Viewer.width)
            y = -random.randint(0, Viewer.height)
            Tower(side=0, pos=pygame.math.Vector2(x,y))
                                              
        
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
        
        for y in range(0, self.maxy+1):
            line = []
            for x in range(0, self.maxx+1):
                #c = random.randint(96,160)
                c = 128
                # ============== values in cell ================
                # 0: color, 1: age, 2: terrain
                # ==============================================
                line.append([c,0, random.choice(("forest", "water", "farm", "rock","swamp"))])
            self.cells.append(line)
        #--- new terrain ---
        self.calculate_terrain()
            
        
    def paint_cells(self):
        for y, line in enumerate(self.cells):
            for x, (color, radius, terrain) in enumerate(line):
                if color == 128:
                    c = (128,128,128)
                elif color > 128:
                    #red
                    c = (int(color),255-int(color),255-int(color))
                else:
                    c = (int(color),int(color), 255-int(color))
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
        return int(x), int(y)
    
    def calculate_terrain(self):
        """creates an image with terrain graphic, like the background"""
        if len(Viewer.images) == 0:
            return
        self.terrain_layer = pygame.Surface((Viewer.width, Viewer.height))
        for y in range(0, self.maxy+1):
            for x in range(0, self.maxx+1):
                what = self.cells[y][x][2]
                # ("forest", "water", "farm", "rock","swamp")
                #if what == "forest":
                #--- force castle corners to be a farm
                if (x==0 and y==0) or (x ==self.maxx and y==self.maxy):
                    what = "farm"
                pic = random.choice([Viewer.images[p] for p in Viewer.images.keys() if what in p])
                self.terrain_layer.blit(pic, (x * self.gridsize, y*self.gridsize))
        self.terrain_layer.set_colorkey((0,0,0))
        self.terrain_layer.convert_alpha()
                
                
                
    def update_cells(self, seconds):
        """change color value of cells if player is nearby, paint raindrop"""
        # ------ update cells -----
        # ---- back to neutral ----
        for y in range(self.maxy+1):
            for x in range(self.maxx+1):
                cvalue = self.cells[y][x][0]
                if cvalue == 0 or cvalue == 255 or cvalue == 128:
                    continue
                if cvalue < 128:
                    sign = 1
                else:
                    sign = -1
                self.cells[y][x][0] += sign * seconds * self.convert_rate_back
                
                
        
        # ----- converting by player -----
        for p in self.playergroup:
            ix, iy = self.pos_to_grid(p.pos)
            affected = []
            for y in range(self.maxy+1):
                for x in range(self.maxx+1):
                    cellvector = pygame.math.Vector2(self.gridsize//2 + x*self.gridsize, -self.gridsize//2-y*self.gridsize)
                    distance = p.pos - cellvector
                    if distance.length() < self.influence_radius:
                        affected.append((x,y))
            #print("affected:", affected)
            for (x,y) in affected:
                cvalue = self.cells[y][x][0]
                if p.side == 1:
                    if cvalue == 255:
                        continue
                    sign = 1
                    r=255
                    rd=10
                    b=0
                    bd=0
                elif p.side == 2:
                    if cvalue == 0:
                        continue
                    sign = -1
                    r=0
                    rd=0
                    b=255
                    bd=10
                else:
                    sign = 0
                self.cells[y][x][0] += sign * seconds * self.convert_rate
                # color sanity check
                self.cells[y][x][0] = min(255, self.cells[y][x][0])
                self.cells[y][x][0] = max(0, self.cells[y][x][0])
                if random.random() < 0.1:
                    Explosion(posvector=pygame.math.Vector2(self.gridsize//2 + x * self.gridsize,
                          -self.gridsize//2-y*self.gridsize), shape="ring", minsparks=1, maxsparks=1, 
                          minspeed=10, maxspeed = 55, red=r, red_delta=rd, green=128, green_delta=32, blue=b, blue_delta=bd)
                    
                    
                    
               
          
    
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
            if self.player1.hitpoints <= 0 or self.castle1.hitpoints <= 0:
                print("Victory for  player 2")
                running = False
            if self.player2.hitpoints <= 0 or self.castle2.hitpoints <= 0:
                print("Victory for player 1")
                running = False
                
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
                    
                    
                    # ------======== MOVEMENT ==========--------
                    # ----- player 1------
                    dx1, dy1 = 0, 0
                    if event.key == pygame.K_a:
                        dx1 = -self.gridsize
                        #self.player1.pos.x -= self.gridsize # left
                    if event.key == pygame.K_d:
                        dx1 = self.gridsize
                        #self.player1.pos.x += self.gridsize # right
                    if event.key == pygame.K_w:
                        dy1 = self.gridsize
                        #self.player1.pos.y += self.gridsize # up
                    if event.key == pygame.K_s:
                        dy1 = -self.gridsize
                        #self.player1.pos.y -= self.gridsize # down
                    # ----- player 2------
                    dx2, dy2 = 0, 0
                    if event.key == pygame.K_LEFT:
                        dx2 = -self.gridsize
                        #self.player1.pos.x -= self.gridsize # left
                    if event.key == pygame.K_RIGHT:
                        dx2 = self.gridsize
                        #self.player1.pos.x += self.gridsize # right
                    if event.key == pygame.K_UP:
                        dy2 = self.gridsize
                        #self.player1.pos.y += self.gridsize # up
                    if event.key == pygame.K_DOWN:
                        dy2 = -self.gridsize
                        #self.player1.pos.y -= self.gridsize # down

                    # =======movement (both) ===========
                    # --- check for tower ---
                    for player, dx, dy in [(self.player1, dx1, dy1), (self.player2, dx2, dy2)]:
                        for t in self.movementblockgroup:   # tower and player
                            if t.side == player.side:
                                continue  # it's a friendly tower
                            if t.pos.x == player.pos.x + dx and t.pos.y == player.pos.y +dy:
                                Flytext(pos=pygame.math.Vector2(player.pos.x, player.pos.y),
                                            text="path blocked by enemy {}".format(t.__class__.__name__),
                                            move=pygame.math.Vector2(0,15), max_age=2)
                                break
                            if player.pos.x + dx < 0 or player.pos.x + dx > self.gridsize//2+self.gridsize * self.maxx  or player.pos.y + dy > 0 or player.pos.y + dy < -self.gridsize//2-self.gridsize * self.maxy:
                                    Flytext(pos=pygame.math.Vector2(player.pos.x, player.pos.y),
                                            text="end of game world reached",
                                            move=pygame.math.Vector2(0,15), max_age=2)
                                    break
                        else:
                            # no enemy tower was in the way
                            player.pos.x += dx
                            player.pos.y += dy
                    
                    # --- player build tower -----
                    for player, key in [(self.player1, pygame.K_LCTRL), (self.player2, pygame.K_RCTRL)]:
                        if event.key == key:
                            # ---- check if tryint to build on water ----
                            x,y = self.pos_to_grid(player.pos)
                            print("x, y:", x,y, self.cells[y][x][2])
                            if self.cells[y][x][2] == "water":
                                Flytext(pos=pygame.math.Vector2(player.pos.x, player.pos.y),
                                            text="Building on Water not possible!",
                                            color=(255,255,0), fontsize=22, max_age=2,
                                            move=pygame.math.Vector2(0, 15))
                                break 
                            # ---- check if there is already a tower ----
                            for t in self.towergroup:
                                if t.pos==player.pos:
                                    Flytext(pos=pygame.math.Vector2(player.pos.x, player.pos.y),
                                            text="Building not possible, There is already a building!",
                                            color=(255,255,0), fontsize=22, max_age=2,
                                            move=pygame.math.Vector2(0, 15))
                                    break
                            else:  
                                # no tower was in the way 
                                Tower(side=player.side, pos=pygame.math.Vector2(
                                      player.pos.x, player.pos.y))

            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            
            
                
           
            
            # ------ mouse handler ------
            left,middle,right = pygame.mouse.get_pressed()
            oldleft, oldmiddle, oldright = left, middle, right

           
            # ------ joystick handler -------
            for number, j in enumerate(self.joysticks):
                pass
                #if number == 0:
                #    player = self.cannon1
                #else:
                #    continue
                #x = j.get_axis(2)
                #y = j.get_axis(1)
                #if y > 0.2:
                #    player.forward(-1)
                #if y < -0.8:
                #    player.forward(15)
                #elif y < -0.5:
                #    player.forward(10)
                #elif y < -0.2:
                #    player.forward(5)
                #if x > 0.2:
                #    player.rotate(7)
                #if x < -0.2:
                #    player.rotate(-7)
                
                buttons = j.get_numbuttons()
                for b in range(buttons):
                    pushed = j.get_button( b )
                    #if b == 0 and pushed:
                    #    player.fire()
                    #if b == 1 and pushed:
                    #    t = random.choice((self.cannon3, self.cannon2))
                    #    player.launch(t)
                        #if b == 5 and pushed:
                            #player.strafe_right()                
            
            # ========== COLLISION DETECTION =====================
            # ----- collision between bullet and target2---
            for bu in self.bulletgroup:
                crashgroup=pygame.sprite.spritecollide(bu,
                           self.targetgroup2, False, 
                           pygame.sprite.collide_mask)
                for target2 in crashgroup:
                      if target2.side == bu.side:
                          continue
                      #elastic_collision(o, p)
                      target2.hitpoints -= bu.damage
                      bu.kill()
                      
            #---- collision between rocket and target? ----          
            for rocket in self.rocketgroup:
                crashgroup=pygame.sprite.spritecollide(
                               rocket, self.targetgroup, False, 
                               pygame.sprite.collide_mask) # collide_rect collide_circle
                           
                           
                for target in crashgroup:
                    if target.side == rocket.side:
                        continue # friendly fire
                    elif rocket.side == 2:
                            r = 0
                            rd = 0
                            b = 225
                            bd = 25
                    elif rocket.side == 1:
                            r = 225
                            rd = 25
                            b = 0
                            bd = 0
                    Explosion(posvector=rocket.pos, minsparks=5, maxsparks=15, minangle = rocket.angle+180+60, maxangle=rocket.angle+180-60,
                              red=r, red_delta=rd, blue=b, blue_delta=bd, green=0, green_delta=0,
                              maxlifetime = 2.5, minspeed=15.5, maxspeed=55.5)
                    #select_sound = random.choice((1, 2, 3, 4))
                    #if select_sound == 1:
                    #    Viewer.sounds["explosion_rocket1"].play()
                    #if select_sound == 2:
                    #    Viewer.sounds["explosion_rocket2"].play()
                    #if select_sound == 3:
                    #    Viewer.sounds["explosion_rocket3"].play()
                    #if select_sound == 4:
                    #    Viewer.sounds["explosion_rocket4"].play()
                    target.hitpoints -= rocket.damage
                    rocket.kill()
                    
                    
                        
             
              
           
            # ---- castle launch soldier ----
            # --- castle1 ---
            for c in self.castlegroup:
                armysize = len([s for s in self.armygroup if s.side == c.side])
                if armysize >= c.max_army:
                    continue
                if random.random() < 0.01:
                    if c.side == 1: 
                        t = self.castle2
                        m = pygame.math.Vector2(random.randint(10,50), -random.randint(10,50))
                    elif c.side == 2:
                        t = self.castle1
                        m = pygame.math.Vector2(-random.randint(10,50), random.randint(10,50))
                        
                    Soldier(side=c.side, target=t, 
                        pos=pygame.math.Vector2(c.pos.x, c.pos.y),move=m,
                        max_age = 120, bounce_on_edge = True)
                        
            # --- soldier shoots (rocket)  ----
            for s in self.armygroup:
                if random.random() < 0.01:
                    targets = [t for t in self.targetgroup if t.side != s.side]
                    targets2 = []
                    for ta in targets:
                        diff = s.pos - ta.pos
                        if diff.length() < s.weaponrange:
                            targets2.append(ta)
                    if len(targets2) == 0:
                        continue
                    victim = random.choice(targets2)
                    Rocket(boss=s, side=s.side, pos=pygame.math.Vector2(s.pos.x, s.pos.y),
                           target=victim, color=s.color)
              
            
            # ---- tower launch bullet ----
            for t in self.towergroup:
                if random.random() < 1.00 :   # 100% chance, 30x pro sec
                    targets = [o for o in self.targetgroup if o.side != t.side]
                    targets2 = []
                    for ta in targets:
                        diff = t.pos - ta.pos
                        if diff.length() < t.weaponrange:
                            targets2.append(ta)
                    if len(targets2) == 0:
                        continue
                    victim = random.choice(targets2)
                    #print("tower", t.number, t.side, "victim: ", victim.number, victim.side, victim.__class__.__name__)
                    #Rocket(boss= t, side=t.side, pos=pygame.math.Vector2(t.pos.x, t.pos.y),
                    #       target=victim, color=t.color)
                    rv = pygame.math.Vector2(50,0)
                    diff = victim.pos - t.pos
                    a = diff.angle_to(pygame.math.Vector2(1,0)) 
                    #print("winkel",a)
                    rv.rotate_ip(a)
                    rv.y *= -1
                    
                    
                    #a = rv.angle_to(pygame.math.Vector2(0,1))-90
                    Bullet(pos=pygame.math.Vector2(t.pos.x, t.pos.y),
                           move = rv, side = t.side, angle=-a, max_distance = t.weaponrange)
                           
              
           
            
            # =========== delete everything on screen ==============
            self.screen.blit(self.background, (0, 0))
            

            #---- draw vertical border ------
            ##pygame.draw.line(self.screen, (255, 255, random.randint(200,255)), (Viewer.border_x, 0), (Viewer.border_x, Viewer.height), 5)
            # ----- draw horizontal border 
            ##pygame.draw.line(self.screen, (255, 255, random.randint(200,255)), (0, -Viewer.border_y), (Viewer.width, -Viewer.border_y),5)         
            
            self.paint_cells()
            self.screen.blit(self.terrain_layer, (0,0))
            self.draw_grid()
            
            # ---- draw weapon ranges ----
            if pressed_keys[pygame.K_r]:
                # show weapon ranges of soldiers and towers
                for a in self.armygroup:
                    c = random.randint(200,255)
                    print("circle", a.pos)
                    pygame.draw.circle(self.screen, (c,c,c), (int(a.pos.x), -int(a.pos.y)), a.weaponrange, 1) 
                 
                for t in self.towergroup:
                    c = random.randint(200,255)
                    pygame.draw.circle(self.screen, (c,c,c), (int(t.pos.x), -int(t.pos.y)), t.weaponrange, 1) 
            
            
            #--- trails for rockets ----
            for r in self.rocketgroup:
                if len(r.trail) > 1:
                    for rank, (x,y) in enumerate(r.trail):
                        if rank > 0:
                            pygame.draw.line(self.screen, (150,150,150), 
                                        (x,y), (old[0], old[1]), (rank // 10))
                        old = (x,y)
            
            ##self.paint_world()
                       
            # write text below sprites (fps, sparks)
            write(self.screen, "FPS: {:8.3}".format(
                self.clock.get_fps() ), x=Viewer.width-200, y=10, color=(200,200,200))
            
            # ---------- cell counter ---------
            redcells = 0
            bluecells = 0
            #for y, line in enumerate(self.cells):
            #for (color, age) in line:
            for y in range(0, self.maxy+1):
                for x in range(0, self.maxx+1):
                    color, age, terrain = self.cells[y][x]
                    if color == 0:
                        bluecells += 1
                    elif color == 255:
                        redcells += 1
                    # ----- cells generate gold -----   
                    age += seconds
                    if color == 255 and age > 10:
                        age = 0
                        self.player1.gold += self.player1.gold_per_grid
                        Flytext(pos = pygame.math.Vector2(self.gridsize//2 + x*self.gridsize, -self.gridsize//2-y*self.gridsize),
                                text="+{} $ for player1".format(self.player1.gold_per_grid), color=(255,255,0), 
                                move=pygame.math.Vector2(0, 15), max_age =1)
                    elif color == 0 and age > 10:
                        age = 0
                        self.player2.gold += self.player2.gold_per_grid
                        Flytext(pos = pygame.math.Vector2(self.gridsize//2 + x*self.gridsize, -self.gridsize//2-y*self.gridsize),
                                text="+{} $ for player2".format(self.player2.gold_per_grid), color=(255,255,0), 
                                move=pygame.math.Vector2(0, 15), max_age =1)
                    self.cells[y][x][1] = age
                    
            
                        
                        
            write(self.screen, "player1: {} cells earn {} $/10 sec. Fortune: {} $".format(redcells, 
                  self.player1.gold_per_grid, self.player1.gold), x=Viewer.width//2, y=10, color=(255, 255,0), fontsize = 20, center=True)
            write(self.screen, "player2: {} cells earn {} $/10 sec. Fortune: {} $".format(bluecells, 
                  self.player2.gold_per_grid, self.player2.gold), x=Viewer.width//2, y=35, color=(255, 255,0),fontsize = 20, center=True)
             
            
           
       
                   
            # ================ UPDATE all sprites =====================
            self.allgroup.update(seconds)
            self.update_cells(seconds)

            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)

            
           
                
            # -------- next frame -------------
            pygame.display.flip()
        #-----------------------------------------------------
        pygame.mouse.set_visible(True)    
        pygame.quit()

if __name__ == '__main__':
    Viewer(1430,800).run()
