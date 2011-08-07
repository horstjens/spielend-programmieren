# -*- coding: utf-8 -*-
"""
Mampfi. A game by Teresa. 

download & more information: 

http://www.spielend-programmieren.at/wiki/doku.php?id=de:games:mampfi

Teresa's copyright:
Für drei Tafeln Milka Schokolade ist es gestattet dieses spiel
zu spielen, kopieren etc.  Geizige Naschkatzen werden gnadenlos verfolgt 
grafiken:
http://en.wikipedia.org/wiki/File:Pommes-1.jpg
http://en.wikipedia.org/wiki/File:Hamburger_sandwich.jpg
http://de.wikipedia.org/w/index.php?title=Datei:Bloemkool.jpg&filetimestamp=20050425131830
http://de.wikipedia.org/w/index.php?title=Datei:Kropsla_herfst_.jpg&filetimestamp=20070324200758
http://de.wikipedia.org/w/index.php?title=Datei:Malus-Idared_on_tree.jpg&filetimestamp=20051023150814
http://de.wikipedia.org/w/index.php?title=Datei:Erdbeere_2008-2-27.JPG&filetimestamp=20080227154749
sound vom modarchive.org
""" 

def mampfi(datadir = "data"):

    import pygame
    import random
    import os
    #damit der sound funktioniert
    pygame.mixer.pre_init(44100,-16,2,2048)
    pygame.init() # pygame startet
    schuss=pygame.mixer.Sound(os.path.join(datadir, "boom.wav"))#ladet sound spielet sie aber nicht
    #schoot.ogg und loop.ogg müssen sich im selben verzeichniss befinden wie teresa1.py
    pygame.mixer.music.load(os.path.join(datadir,"loop.ogg"))#ladet musik spielet sie aber nicht
    pygame.mixer.music.play(-1)#spielt musik endlos    

    BIRDSPEEDMAX = 100
    BIRDSPEEDMIN = 10
    FRICTION =.999
    HITPOINTS = 100.0
    FORCE_OF_GRAVITY = 9.81 # in pixel per second² .See http://en.wikipedia.org/wiki/Gravitational_acceleration



    def write(msg="pygame is cool"):
        myfont = pygame.font.SysFont("None", 150)
        mytext = myfont.render(msg, True, newcolour())
        mytext = mytext.convert_alpha()
        return mytext
    def newcolour():
        # any colour but black or white 
        return (random.randint(10,250), random.randint(10,250), random.randint(10,250))
     

    if pygame.ver >= 1.8:    
        breite=0
        hoehe=0
        screen=pygame.display.set_mode((breite,hoehe))#erzeugt spielfenser
        breite = screen.get_rect().width
        hoehe= screen.get_rect().height
        hoehe = int(hoehe* 0.9) # only use 90% of height to allow taskbar to be visible
        screen=pygame.display.set_mode((breite,hoehe))#erzeugt spielfenser mit weniger hoehe
    else:
        screen=pygame.display.set_mode((800,600))#erzeugt spielfenser mit weniger hoehe
    hintergrund=pygame.Surface(screen.get_size())#erzegt einen hintergrund
    hintergrund2=pygame.image.load(os.path.join(datadir,"coolekidsobst.jpg"))
    gameoverscreen = [ pygame.image.load(os.path.join(datadir,"losemarki.jpg")).convert(),
                       pygame.image.load(os.path.join(datadir,"loseraffi.jpg")).convert(),
                       pygame.image.load(os.path.join(datadir,"losemira.jpg")).convert(),
                       pygame.image.load(os.path.join(datadir,"loseterri.jpg")).convert(),
                       pygame.image.load(os.path.join(datadir,"youwin.jpg")).convert(),
                       pygame.image.load(os.path.join(datadir,"youdied.jpg")).convert()]
        
    #textsurface = write("Coole Kids")
    offsetx = screen.get_width() / 2 - hintergrund2.get_width() / 2
    offsety = screen.get_height() / 2 - hintergrund2.get_height() / 2
    hintergrund.fill((200,200,200)) # grau?
    #hintergrund.blit(textsurface, (50,50))
    hintergrund.blit(hintergrund2,(offsetx, offsety))#hintergrund zeichnen
    #hintergrund.fill((50,50,255))#farbe rot grün blau
    hintergrund=hintergrund.convert()#macht das spiel schneller
    raffi=pygame.image.load(os.path.join(datadir,"raphael.png")).convert_alpha()
    terri=pygame.image.load(os.path.join(datadir,"tersalacht3.png")).convert_alpha()
    mira=pygame.image.load(os.path.join(datadir,"miralacht1.png")).convert_alpha()
    marki=pygame.image.load(os.path.join(datadir,"marki.png")).convert_alpha()

    screen.blit(hintergrund,(0,0))

    #----------------------------
    class Zauberer(pygame.sprite.Sprite):
        """kinder fangen zauberer"""
        wizards={}
        def __init__(self):
             pygame.sprite.Sprite.__init__(self, self.groups )
             self.pos = [300.0,200.0]
             self.image=pygame.image.load(os.path.join(datadir,"icon-hostgame.png")).convert_alpha()
             self.dx=0
             self.dy=0
             self.rect=self.image.get_rect()
             self.radius = self.rect.height / 2
             self.area=screen.get_rect()
             self.hitpointsfull = HITPOINTS  / 2# maximal hitpoints
             self.hitpoints = HITPOINTS / 2 # actual hitpoints
             self.number = 0
             Zauberer.wizards[0] = self # store myself into the Kind directory
             Livebar(self, "wizard") #create a Livebar for this Kind. 
            
                  
        def kill(self):
            """because i want to do some special effects (sound, directory etc.)
            before killing the Kind sprite i have to write my own kill(self)
            function and finally call pygame.sprite.Sprite.kill(self) 
            to do the 'real' killing"""
            schuss.play()
            #print Kind.Kinds, "..."
            for _ in range(1000):
                Fragment(self.pos)
            #Kind.birds[self.number] = None # kill Kind in sprite Directory
            pygame.sprite.Sprite.kill(self) # kill the actual Kind 
            
        def update(self,seconds):
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_UP]:
                 self.dy -= 10
            if pressed_keys[pygame.K_DOWN]:
                 self.dy += 10
            if pressed_keys[pygame.K_RIGHT]:
                self.dx += 10
            if pressed_keys[pygame.K_LEFT]:
                self.dx -= 10
            if pressed_keys[pygame.K_SPACE]:
                self.dx = 0
                self.dy = 0
            # reibung----------
            self.dx *= 0.99
            self.dy *= 0.99
            self.pos[0] += self.dx *seconds
            self.pos[1] += self.dy *seconds
            #gemüse legen--------------------
            if pressed_keys[pygame.K_a]:
                 Junkfood(self.pos,2) #salat
            elif pressed_keys[pygame.K_s]:
                 Junkfood(self.pos,3) #kohl
            elif pressed_keys[pygame.K_d]:
                 Junkfood(self.pos,4) #apfel
            elif pressed_keys[pygame.K_f]:
                 Junkfood(self.pos,5) #erdbeere
            #------peppppppeln-----------#
            if self.pos[0] + self.rect.width/2 > self.area.right:
                self.pos[0] = self.area.right - self.rect.width/2
                self.dx *=-1
                #screen.fill((0,0,0))
            if self.pos[0] - self.rect.width/2 < self.area.left:
                self.pos[0] = self.area.left + self.rect.width/2
                self.dx *=-1
                #screen.fill((0,0,0))
            if self.pos[1] + self.rect.height/2 > self.area.bottom:
                self.pos[1] = self.area.bottom - self.rect.height/2
                self.dy *=-1
                #screen.fill((0,0,0))
            if self.pos[1] - self.rect.height/2 < self.area.top:
                self.pos[1] = self.area.top + self.rect.height/2
                self.dy*=-1
                #screen.fill((0,0,0))
            # blitte zaubaraaa
            self.rect.centerx = round(self.pos[0],0)
            self.rect.centery = round(self.pos[1],0)
            if self.hitpoints<0:
                self.kill()
        

    class Kind(pygame.sprite.Sprite):
            """a nice little sprite that bounce off walls and other sprites
            kids shoot unhealty food at player. if kid eats healthy food,
            hitpoints increase. if kid bounce off wall, hitpoints decrease.
            if hitpoints of kid are full, it moves toward gameover position.
            kids start with half-full hitpoints.
            """
            image=[]  # list of all images
            # not necessary:
            birds = {} # a directory of all Birds, each Bird has its own number
            number = 0  
            def __init__(self, startpos=(50,50), area=screen.get_rect()):
                pygame.sprite.Sprite.__init__(self, self.groups )
                self.pos = [0.0,0.0]
                self.startpos = startpos 
                self.pos[0] = startpos[0]*1.0 # float
                self.pos[1] = startpos[1]*1.0 # float
                self.number = Kind.number # get my personal Birdnumber
                Kind.number+= 1           # increase the number for next Kind
                Kind.birds[self.number] = self # store myself into the Kind directory
                #print "my number %i Kind number %i " % (self.number, Kind.number)
                self.image = Kind.image[self.number]
                self.hitpointsfull = HITPOINTS # maximal hitpoints
                self.hitpoints = 50.0 # actual hitpoints
                self.rect = self.image.get_rect()
                self.radius=self.rect.width/2
                self.radius = max(self.rect.width, self.rect.height) / 2.0
                self.area = area # where the sprite is allowed to move
                self.newspeed()
                #self.cleanstatus()
                #self.catched = False
                #self.crashing = False
                #--- not necessary:

                Livebar(self) #create a Livebar for this Kind. 
                
            def newspeed(self):
                # new Kindspeed, but not 0
                if self.hitpoints < self.hitpointsfull:
                    speedrandom = random.choice([-1,1]) # flip a coin
                    self.dx = random.random() * BIRDSPEEDMAX * speedrandom + speedrandom * BIRDSPEEDMIN
                    self.dy = random.random() * BIRDSPEEDMAX * speedrandom + speedrandom * BIRDSPEEDMIN
                else:
                    #return to startpos
                    self.dx = self.startpos[0] -  self.rect.centerx 
                    self.dy = self.startpos[1] -  self.rect.centery
                
            def kill(self):
                """because i want to do some special effects (sound, directory etc.)
                before killing the Kind sprite i have to write my own kill(self)
                function and finally call pygame.sprite.Sprite.kill(self) 
                to do the 'real' killing"""
                schuss.play()
                for _ in range(75):
                    Fragment(self.pos, (1,1,1), False)
                Kind.birds[self.number] = None # kill Kind in sprite Directory
                pygame.sprite.Sprite.kill(self) # kill the actual Kind 

            
            def update(self, seconds):
                if self.hitpoints >= self.hitpointsfull:
                    self.newspeed()
                # new position
                self.pos[0] += self.dx * seconds
                self.pos[1] += self.dy * seconds
                # -- check if Kind out of screen
                #self.crashing=False
                if not self.area.contains(self.rect):
                    #print "aua"
                    self.hitpoints -=1
                    # --- compare self.rect and area.rect
                    if self.pos[0] + self.rect.width/2 > self.area.right:
                        self.pos[0] = self.area.right - self.rect.width/2
                    if self.pos[0] - self.rect.width/2 < self.area.left:
                        self.pos[0] = self.area.left + self.rect.width/2
                    if self.pos[1] + self.rect.height/2 > self.area.bottom:
                        self.pos[1] = self.area.bottom - self.rect.height/2
                    if self.pos[1] - self.rect.height/2 < self.area.top:
                        self.pos[1] = self.area.top + self.rect.height/2
                    self.newspeed() # calculate a new direction
                #--------- schussssssssssss
                if random.randint(1,100)>98:
                    if self.hitpoints < self.hitpointsfull:
                        Junkfood(self.pos,random.randint(0,1)) # burger or pommes frites
                    else:
                        Junkfood(self.pos,0) # no burgers because no movement
                #--- calculate new position on screen -----
                self.rect.centerx = round(self.pos[0],0)
                self.rect.centery = round(self.pos[1],0)
                #--- loose hitpoins
                ##--- check if still alive
                #if self.hitpoints <= 0:
                #    self.kill()
                
    class Fragment(pygame.sprite.Sprite):
            """a fragment of an exploding Kind"""
            #gravity = True # fragments fall down ?
            def __init__(self, pos,farbe=0, grav = True):
                pygame.sprite.Sprite.__init__(self, self.groups)
                if farbe==0:
                    self.farbe=(random.randint(1,250),random.randint(1,250),random.randint(1,250))
                else:
                    self.farbe=farbe
                self.area=screen.get_rect()
                self.pos = [0.0,0.0]
                self.pos[0] = pos[0]
                self.pos[1] = pos[1]
                self.image = pygame.Surface((10,10))
                self.image.set_colorkey((0,0,0)) # black transparent
                self.gravity = grav
                pygame.draw.circle(self.image, self.farbe, (5,5), 
                                                random.randint(2,5))
                self.image = self.image.convert_alpha()
                self.rect = self.image.get_rect()
                self.lifetime = 1 + random.random()*5 # max 6 seconds
                if not self.gravity:
                    self.lifetime = 0.2 + random.random() * 0.8
                self.time = 0.0
                self.fragmentmaxspeed = BIRDSPEEDMAX * 2 # try out other factors !
                self.dx = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
                self.dy = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
                
            def update(self, seconds):
                self.time += seconds
                if self.time > self.lifetime:
                    self.kill() 
                self.pos[0] += self.dx * seconds
                self.pos[1] += self.dy * seconds
                  #------peppeln-----------#
                if self.pos[0] + self.rect.width/2 > self.area.right:
                    self.pos[0] = self.area.right - self.rect.width
                    self.dx *=-1
                    #screen.fill((0,0,0))
                if self.pos[0] - self.rect.width/2 < self.area.left:
                    self.pos[0] = self.area.left + self.rect.width/2
                    self.dx *=-1
                    #screen.fill((0,0,0))
                if self.pos[1] + self.rect.height/2 > self.area.bottom:
                    self.pos[1] = self.area.bottom - self.rect.height/2
                    self.dy *= -random.random() # rebouncce from floor
                    #screen.fill((0,0,0))
                if self.pos[1] - self.rect.height/2 < self.area.top:
                    self.pos[1] = self.area.top + self.rect.height/2
                    self.dy*=-1
                    #screen.fill((0,0,0))
                #if Fragment.gravity:
                if self.gravity:
                    self.dy += FORCE_OF_GRAVITY # gravity suck fragments down
                self.rect.centerx = round(self.pos[0],0)
                self.rect.centery = round(self.pos[1],0)
                
    class Livebar(pygame.sprite.Sprite):
            """shows a bar with the hitpoints of a Kind sprite"""
            def __init__(self, boss, bosstype="kind"):
                pygame.sprite.Sprite.__init__(self,self.groups)
                self.boss = boss
                self.image = pygame.Surface((self.boss.rect.width,7))
                self.image.set_colorkey((1,1,1)) # black transparent
                pygame.draw.rect(self.image, (0,0,0), (0,0,self.boss.rect.width,7),1)
                self.rect = self.image.get_rect()
                self.oldpercent = 0
                #if self.bosstype == "kind":
                self.bossnumber = self.boss.number # the unique number (name) of my boss
                self.bosstype = bosstype
            def update(self, time):
                self.percent = self.boss.hitpoints / self.boss.hitpointsfull * 1.0
                if self.percent != self.oldpercent:
                    pygame.draw.rect(self.image, (1,1,1), (1,1,self.boss.rect.width-2,5)) # fill black
                    pygame.draw.rect(self.image, (0,255,0), (1,1,
                        int(self.boss.rect.width * self.percent),5),0) # fill green
                self.oldpercent = self.percent
                self.rect.centerx = self.boss.rect.centerx
                self.rect.centery = self.boss.rect.centery - self.boss.rect.height /2 - 10
                #check if boss is still alive
                if self.bosstype == "wizard":
                    if not Zauberer.wizards[self.bossnumber]:
                        self.kill()
                else:
                    if not Kind.birds[self.bossnumber]:
                        self.kill() # kill the hitbar
               
    class Junkfood(pygame.sprite.Sprite):
            """a fragment of junkfood"""
            gravity = False # fragments fall down ?
            image=[]
            image.append(pygame.image.load(os.path.join(datadir,"pommes.png")).convert_alpha())#0
            image.append(pygame.image.load(os.path.join(datadir,"burger.png")).convert_alpha())#1
            image.append(pygame.image.load(os.path.join(datadir,"salat1.png")).convert_alpha())#2
            image.append(pygame.image.load(os.path.join(datadir,"kohl.png")).convert_alpha())#3
            image.append(pygame.image.load(os.path.join(datadir,"apfel.png")).convert_alpha())#4
            image.append(pygame.image.load(os.path.join(datadir,"erdbeere.png")).convert_alpha())#5
            def __init__(self, pos, bild=0):
                pygame.sprite.Sprite.__init__(self, self.groups)
                self.pos = [0.0,0.0]
                self.area=screen.get_rect()
                self.pos[0] = pos[0]
                self.pos[1] = pos[1]
                self.bild=bild
                self.image=Junkfood.image[bild]
                self.rect = self.image.get_rect()
                self.radius=self.rect.width/2
                self.rect.centerx = round(self.pos[0],0)
                self.rect.centery = round(self.pos[1],0)
                #self.lifetime = 10 + random.randint(0,40) # max 50 seconds
                self.lifetime = 30
                self.time = 0.0
                self.fragmentmaxspeed = BIRDSPEEDMAX * 2 # try out other factors !
                if self.bild==0:
                    #pommes
                    self.dx = Zauberer.wizards[0].rect.centerx -  self.rect.centerx 
                    self.dy = Zauberer.wizards[0].rect.centery -  self.rect.centery
                    # do not fly too fast
                    if (abs(self.dx) > self.fragmentmaxspeed or 
                        abs(self.dy) > self.fragmentmaxspeed):
                            faktor = self.fragmentmaxspeed * 1.0 / max(abs(self.dx),abs(self.dy))
                            self.dx *= faktor
                            self.dy *= faktor
                else:
                    #burger
                    self.dx=0
                    self.dy=0 #nicht bewegen
                    
            def update(self, seconds):
                self.time += seconds
                if self.time > self.lifetime:
                    self.kill(True) #black
                self.pos[0] += self.dx * seconds
                self.pos[1] += self.dy * seconds
                if not self.area.contains(self.rect):
                    #print "aua"
                    self.kill(True,10,15) # little explosion
                #if Fragment.gravity:
                #    self.dy += FORCE_OF_GRAVITY # gravity suck fragments down
                self.rect.centerx = round(self.pos[0],0)
                self.rect.centery = round(self.pos[1],0)
            def kill(self, black=False, min=15, max=25):
                #pygame.draw.circle(screen,(0,0,0),self.rect.center,50,0)
                if black:
                    for _ in range(7):
                        Fragment(self.pos, (5,5,5), False) # no gravity !
                else:
                    for _ in range(random.randint(min,max)):
                        if self.bild==1:
                            Fragment(self.pos,(255,0,0)) #burger rot
                        elif self.bild==0:
                            Fragment(self.pos,(150,128,60)) #burger gelb
                        elif self.bild==2:
                            Fragment(self.pos,(0,255,0))   #salat grün
                        elif self.bild==3:                 
                            Fragment(self.pos,(255,255,255)) #kohl 
                        elif self.bild==4:
                            Fragment(self.pos,(151,35,72)) #apfel
                        elif self.bild==5:
                            Fragment(self.pos,(139,0,0)) #erdbeere
                        
                pygame.sprite.Sprite.kill(self) # kill the actual Kind 



    #---------------before spielschleife---------------
    kindgroup = pygame.sprite.Group()   
    bargroup = pygame.sprite.Group()
    stuffgroup = pygame.sprite.Group()
    junkgroup = pygame.sprite.Group()
    fragmentgroup = pygame.sprite.Group()
    zauberergroup = pygame.sprite.Group()
    # LayeredUpdates instead of group to draw in correct order
    allgroup = pygame.sprite.LayeredUpdates() # important
    Zauberer.groups=allgroup, zauberergroup
    #assign default groups to each sprite class
    # (only allgroup is useful at the moment)
    Livebar.groups =  bargroup, allgroup 
    Junkfood.groups = junkgroup,allgroup
    Kind.groups =  kindgroup, allgroup
    Fragment.groups = fragmentgroup, allgroup

    #assign default layer for each sprite (lower numer is background)

    Fragment.layer = 4

    Kind._layer = 2
    Livebar._layer = 1
    Zauberer._layer =7
    #-------------new.----
    mittex = screen.get_width()/2
    mittey = screen.get_height()/2
    Kind.image.append( marki )
    Kind.image.append( raffi )
    Kind.image.append( mira )
    Kind.image.append( terri )
    # ------ fill the world with sprites -----
    Kind((mittex-100,mittey-100)) # marki
    Kind((mittex-30,mittey-70)) #raffi
    Kind((mittex+50,mittey-60)) #mira
    Kind((mittex+100,mittey-70)) #terri
    zauberer=Zauberer()
    # -------------------


    FPS=30#frames per seconds 
    uhr=pygame.time.Clock()
    spielschleife=True
    result = "game canceled"

    gameover = False
    overtime = 7000 # 7 seconds to watch effects and game over message
    while spielschleife:
        milisekunden=uhr.tick(FPS)#das das spiel nicht zu schnell wird
        seconds=milisekunden/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spielschleife = False
            elif event.type == pygame.KEYDOWN:
                # tasten drücken und loslassen
                if event.key == pygame.K_ESCAPE:
                    spielschleife = False
        # taste gedrückt halten
            #-----------------------------------
       
        if gameover:
            overtime -= milisekunden
        #print overtime
        if overtime < 0:
            spielschleife = False        
        #pygame.display.set_caption("fps: %.2f x: %i y: %i dx: %i dy: %i" % (uhr.get_fps() , x, y, dx, dy)) 
        pygame.display.set_caption("press ESC to exit. Fps: %.2f" % uhr.get_fps())
        
        crashgroup = pygame.sprite.spritecollide(zauberer, junkgroup, False, pygame.sprite.collide_circle)
        for junkie in crashgroup:
            if junkie.bild<2:
                #pommes oder burger
                schuss.play()
                zauberer.hitpoints-=1
                junkie.kill()
                       
        for kind in kindgroup:
            crashgroup = pygame.sprite.spritecollide(kind, junkgroup, False, pygame.sprite.collide_circle)
            for junkie in crashgroup:
                if junkie.bild -2== kind.number:
                    #mampf.play()
                    kind.hitpoints+=1 #sofiele hitpoinsts bekommt er
                    junkie.kill()
        
        #----------------- winning or loosing the game -------------------------
        if not gameover:
            winning = True
            for kind in kindgroup:
                if kind.hitpoints < 1:
                    result = "Game Over. You lose. One kid lost all hitpoints. Take better care next time."
                    hintergrund.blit(gameoverscreen[kind.number],(offsetx, offsety)) # you loose, kind kaputt
                    kind.kill()
                    gameover = True
                    winning = False
                    break
                elif kind.hitpoints < kind.hitpointsfull:
                    winning = False # not won yet
            if winning:
                gameover = True
                result = "Game Over. You win. Congratulation !"
                hintergrund.blit(gameoverscreen[4],(offsetx, offsety))# you win
                for kid in kindgroup:
                    kid.kill()
            # loose because lost all hitponts ?
            if zauberer.hitpoints < 1:
                result = "Game Over. You lose. You lost all your hitpoints. Be more careful next time"
                gameover = True
                hintergrund.fill((0,0,0))
                hintergrund.blit(gameoverscreen[5],(offsetx, offsety))# you loose
                zauberer.kill()
        
        if gameover:
            # do that in every case of gameover
            screen.blit(hintergrund,(0,0))
            for food in junkgroup:
                food.kill()
        
        # ------ not game over ----------
        # ------------- stuff to do every frame ----------------------------
        #screen.blit(hintergrund,(0,0))#auskommentieren=cooler effect
        #screen.blit(hintergrund,(offsetx, offsety))#hintergrund zeichnen
        allgroup.clear(screen, hintergrund)
        allgroup.update(seconds)
        allgroup.draw(screen)           
        pygame.display.flip() # nächster frame
    #-------- end of spielschleife -----
    return result
        
if __name__ == "__main__":
    print "game start"
    print mampfi() # play game and return result
    
