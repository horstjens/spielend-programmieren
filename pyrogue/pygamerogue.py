#!/usr/bin/env python
# -*- coding: utf-8 -*-                # nur wichtig für python version2
from __future__ import print_function  # nur wichtig für python version2
from __future__ import division        # nur wichtig für python version2
try:                                   # nur wichtig für python version2
    input = raw_input                  # nur wichtig für python version2
except NameError:                      # nur wichtig für python version2
    pass                               # nur wichtig für python version2

"""
name: pygamerogue
URL: https://github.com/horstjens/spielend-programmieren/tree/master/pyrogue
Author:  Horst JENS
Email: horstjens@gmail.com
Licence: gpl, see http://www.gnu.org/licenses/gpl.html
descr: a rogue game using python + pygame. graphics from dungeon crawl stone soup
"""

#
import pygame, random, os, sys


def write(msg="pygame is cool", fontcolor=(255,0,255), fontsize=42, font=None):
    """erzeugt eine Pygame Surface zum blitten mit Text"""
    myfont = pygame.font.SysFont(font, fontsize)
    mytext = myfont.render(msg, True, fontcolor)
    mytext = mytext.convert_alpha()
    return mytext


def display_textlines(lines, screen, color=(0,0,255)):
    """zeigt (scrollbare) Text linien, wartet auf ENTER Taste"""

    offset = 0
    pygame.display.set_caption("Press ENTER")
    while True:
        screen.fill((0,0,0))
        y = 0
        for textline in lines:
            line = write(textline, color, 24 )
            screen.blit(line,(20, offset + 14 * y ))
            y += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type != pygame.KEYDOWN:
                continue
            elif event.key == pygame.K_DOWN:
                offset -= 14
            elif event.key == pygame.K_UP:
                offset += 14
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                return
        pygame.display.flip()



def kampfrunde(m1, m2):
    """Eine Kampfrunde (Schlag). Beste Waffe bzw. beste Rüstung hat Priorität"""
    txt = []
    if m1.hitpoints > 0 and m2.hitpoints > 0:
        PygView.macesound.play()
        txt.append("Kampf: {} ({}, {} hp) haut {} ({}, {} hp)".format(m1.name, type(m1).__name__, m1.hitpoints,
                                                                      m2.name, type(m2).__name__, m2.hitpoints))
        schaden = m1.level
        if "Schwert" in m1.rucksack:      # and rucksack["Waffe"] >0:
            damage = random.randint(schaden, schaden+3)
            waffe = "Schwert"
        elif "Taschenmesser" in m1.rucksack:
            damage = random.randint(schaden+1, schaden+2)
            waffe = "Taschenmesser"
        else:
            damage = random.randint(schaden, schaden+1)
            waffe = "Faust"
        txt.append("Kampf: {} attackiert {} mit {} für {} Schaden".format(
            m1.name, m2.name, waffe, damage))
        blocked_damage = 0
        if "Rüstung" in m2.rucksack:
            damage -= schaden+1
            blocked_damage += 1
            txt.append("Kampf: Rüstung von {} absorbiert einen Schadenspunkt".format(m2.name))
        if "Schild" in m2.rucksack:
            damage -= (schaden-1)+1
            blocked_damage += 1
            txt.append("Kampf: Schild von {} aborbiert einen Schadenspunkt".format(m2.name))
        Flytext(m2.x, m2.y, "dmg: {}".format(damage))
        if blocked_damage > 0:
            Flytext(m2.x, m2.y+1, "blocked: {}".format(blocked_damage), (0,255,0))
        if damage > 0:
            m2.hitpoints -= damage
            txt.append("Kampf: {} verliert {} hitpoints ({} hp übrig)".format(m2.name, damage, m2.hitpoints))
            if m2.hitpoints < 1:
                exp = random.randint(7, 10)
                m1.xp += exp
                m1.kills += 1
                victim = type(m2).__name__    # der Name der Class vom Opfer
                if victim in m1.killdict:
                    m1.killdict[victim] += 1
                else:
                    m1.killdict[victim] = 1
                txt.append("Kampf: {} hat keine Hitpoints mehr, {} bekommt {} Xp".format(m2.name, m1.name, exp))
                line = m1.check_levelup()
                if line:
                    txt.append(line)
        else:
            txt.append("Kampf: {} bleibt unverletzt".format(m2.name))
    return txt


def load_sound(file):
    if not pygame.mixer:
        return NoSound()
    file = os.path.join("sounds", file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print('Warning, unable to load,', file)
    return NoSound()


def load_music(file):
    if not pygame.mixer:
        return NoSound()
    file = os.path.join("music", file)
    try:
        music = pygame.mixer.music.load(file)
        return music
    except pygame.error:
        print('Warning, unable to load,',file)
    return NoSound()


def ask(question, x, y, screen):   # from pygame newsgroup
    """ask(screen, question) -> answer"""
    pygame.font.init()
    text = ""
    line = write(question)
    screen.blit(line, (x, y))
    pygame.display.flip()
    while True:
        pygame.time.wait(50) # wartet 50 millisekunden?
        #event = pygame.event.poll()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type != pygame.KEYDOWN:
                continue
            elif event.key == pygame.K_BACKSPACE:
                text = text[0:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if text == "":
                    continue
                return text
            elif event.key == pygame.K_ESCAPE:
                return "Dorftrottel"
            elif event.key <= 127:
                text += chr(event.key)
        line = write(question + ": " + text)
        screen.fill((0,0,0))
        screen.blit(line, (x, y))
        pygame.display.flip()


class NoSound(object):
    """wird von der Funktion load_sound benötigt, falls die Soundausgabe nicht funktioniert"""
    def play(self):
        pass


class Spritesheet(object):
    """ from pygame.org
    #import spritesheet
    #...
    #ss = spritesheet.spriteshee('somespritesheet.png')
    ## Sprite is 16x16 pixels at location 0,0 in the file...
    #image = ss.image_at((0, 0, 16, 16))
    #images = []
    ## Load two images into an array, their transparent bit is (255, 255, 255)
    #images = ss.images_at((0, 0, 16, 16),(17, 0, 16,16), colorkey=(255, 255, 255))
    #...
    """
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(os.path.join("images", filename)).convert()
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


class Monster(object):
    def __init__(self, x, y, xp=0, level=1, hp=0, bild=""):
        self.x = x
        self.y = y
        self.xp = xp
        self.kills = 0
        self.killdict = {}
        self.level = level   # normalerweise startet mit level 1
        self.rank = ""
        if hp == 0:
            self.hitpoints = random.randint(10,20)
        else:
            self.hitpoints = hp
        if bild == "":
            self.bild = PygView.MONSTERBILD
        else:
            self.bild = bild
        self.name = random.choice(("Frank", "Kunibert", "Eisenfresser", "Galomir"))
        self.strength = random.randint(1,10)
        self.dexterity = random.randint(1,10)
        self.intelligence = random.randint(1,10)
        # Startausrüstung (gilt für Monster und Spieler)
        self.rucksack = {}
        for z in ["Taschenmesser", "Schwert", "Schild", "Rüstung"]:
            if random.random() < 0.1:  # 10% Chance
                self.rucksack[z] = 1

    def check_levelup(self, rank="nobody"):
        return ""

    def ai(self, player):
        """returns dx, dy: where the monster wants to go"""
        dirs = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        return random.choice(dirs)   #return dx, xy


class Boss(Monster):
    def __init__(self, x, y, xp=0, level=1, hp=0, bild=""):
        Monster.__init__(self, x, y, xp, level, hp, bild)

    def ai(self, player):
        """a Boss is intelligent enough to chase the player"""
        #dirs = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        dx, dy = 0, 0
        if self.x > player.x:
            dx = -1
        elif self.x < player.x:
            dx = 1
        if self.y > player.y:
            dy = -1
        elif self.y < player.y:
            dy = 1
        return dx, dy

class Goblin(Monster):
    def __init__(self, x, y, xp=0, level=1, hp=0, bild=""):
        """ein Beispiel für ein schwaches Monster"""
        Monster.__init__(self, x, y, xp, level, hp, bild)
        # ------- ab hier selber coden ----
        # self.bild = random.choice((PygView.GOBLIN1, PygView.GOBLIN2, PygView.GOBLIN3))
        # self.strength = random.randint(1,6)   # andere Stärke als Standard MONSTER
        # -- etwas in den Rucksack geben
        # self.rucksack["Goblin-Amulett"] = 1

class Wolf(Monster):
    def __init__(self, x, y, xp=0, level=1, hp=0, bild=""):
        """ein Beispiel für ein schwaches Monster"""
        Monster.__init__(self, x, y, xp, level, hp, bild)
        # ------- ab hier selber coden ----
        # self.bild = random.choice((PygView.WOLF1, PygView.WOLF2, PygView.WOLF3))
        # self.strength = random.randint(3,4)   # andere Stärke als Standard MONSTER
        # self.dexterity = random.randint(5,8)  # andere Geschicklichkeit als Standard Monster

class EliteWarrior(Boss):
    def __init__(self, x, y, xp=0, level=1, hp=0, bild=""):
        """ein Beispiel für einen starken Boss"""
        Monster.__init__(self, x, y, xp, level, hp, bild)
        # ------- ab hier selber coden ----
        # self.bild = random.choice((PygView.WARRIOR1, PygView.WARRIOR2, PygView.WARRIOR3))
        # self.strength = random.randint(12,24)   # andere Stärke als Standard MONSTER
        # self.rucksack["Schwert"] = 1
        # self.rucksack["Schild"] = 1

class Golem(Boss):
    def __init__(self, x, y, xp=0, level=1, hp=0, bild=""):
        """ein Beispiel für einen starken Boss"""
        Monster.__init__(self, x, y, xp, level, hp, bild)
        # ------- ab hier selber coden ----
        # self.bild = random.choice((PygView.GOLEM1, PygView.GOLEM2, PygView.GOLEM3))
        # self.strength = random.randint(20,30)   # andere Stärke als Standard MONSTER



class Player(Monster):
    def __init__(self, x, y, xp=0, level=1, hp=0, bild=""):
        Monster.__init__(self, x, y, xp, level, hp, bild)
        self.name = "Player"
        self.rank = "Zivilist"
        self.rucksack = {}
        self.z = 0
        self.keys = []
        if hp == 0:
            self.hitpoints = random.randint(5,10)
        else:
            self.hitpoints = hp
        if bild == "":
           self.bild = PygView.PLAYERBILD
        else:
            self.bild = bild

    def levelup(self, rank="Nobody"):
        self.level += 1
        self.hitpoints += self.level* 2 + random.randint(1,6)
        self.rank = rank

    def check_levelup(self):
        if self.xp >= 100 and self.level == 1:
            self.levelup("Page")  # level wird 2
        elif self.xp >= 200 and self.level == 2:
            self.levelup("Knappe")
        elif self.xp >= 400 and self.level == 3:
            self.levelup("Ritter")
        else:
            return "" ## hier weiterprogrammieren
        return "{} erreicht Level {}: {}".format(self.name, self.level, self.rank)

    def ai(self):
        return (0,0)

    def zeige_rucksack(self):
        """Zeigt Anzahl und Art von Gegenständen im Rucksack"""
        lines = ["Folgende Sachen befinden sich in deinem Rucksack:"]
        if len(self.rucksack) == 0:
            lines.append("dein Rucksack ist leer")
        else:
            lines.append("Anzahl, Gegenstand")
            lines.append("==================")
            for ding in self.rucksack:
                lines.append(str(self.rucksack[ding]) + ".........." + str(ding))
        return lines

    def nimm(self, zeug):
        """Erhöht Anzahl von Gegenständen im Rucksack"""
        if zeug in self.rucksack:
            self.rucksack[zeug] += 1
        else:
            self.rucksack[zeug] = 1
        
class Block(object):
    def __init__(self):
        self.visible = True
        self.bloody = False

class Floor(Block):
    def __init__(self):
        Block.__init__(self)
        self.bild = random.choice((PygView.FLOOR, PygView.FLOOR1))

class Wall(Block):
    def __init__(self):
        Block.__init__(self)
        self.bild = random.choice((PygView.WALL, PygView.WALL1, PygView.WALL2))


class Stair(Block):
    def __init__(self, direction):
        Block.__init__(self)
        if direction == "down":
            self.down = True
            self.bild = PygView.STAIRDOWN
        else:
            self.down = False
            self.bild = PygView.STAIRUP
        self.target = (0,0,0) # x,y,z


class Item(object):
    def __init__(self, x, y):
        """a moveable thing laying in the dungeon"""
        self.x = x
        self.y = y
        self.visible = True
        self.hitpoints = 1
        self.bild = PygView.LOOT  # wird überschrieben
        self.carried = False # in someone's inventory?


class Sign(Item):
    def __init__(self, x, y, char):
        Item.__init__(self, x, y)
        self.bild = PygView.SIGN
        self.char = char    # number from level source code
        self.text = ""      # the long text of the sign


class Trap(Item):
    def __init__(self, x, y):
        Item.__init__(self, x, y)
        self.level = random.randint(1, 5)
        self.hitpoints = self.level * 2
        self.bild = PygView.TRAP



class Key(Item):
    def __init__(self, x, y, color="dull"):
        Item.__init__(self, x, y)
        self.color = color
        self.bild = PygView.KEY


class Door(Item):
    def __init__(self, x, y, color="dull"):
        Item.__init__(self, x, y)
        self.locked = True
        self.closed = True
        self.bild = PygView.DOOR
        self.color = color


class Loot(Item):
    def __init__(self, x, y):
        Item.__init__(self, x, y)
        self.text = random.choice(["Müll", "Knochen", "Münze", "Taschenmesser", "Stoffreste",
             "Essbesteck", "Spielzeug", "Schwert", "Rüstung",
             "Edelstein", "Heiltrank", "Schild"])

class Level(object):
    def __init__(self, dateiname):
        """liest den dateinamen ein und erzeugt ein Level-Object"""
        #self.lines = []
        self.layout = {}         # lines of non-movable stuff
        self.schilder = {}       # schildnummer: schildtext
        self.monsters = []
        self.signs = []
        self.traps = []
        self.doors = []
        self.loot = []
        self.keys = []
        self.width = 0
        self.depth = 0
        self.sichtweite = 10
        with open(dateiname) as f:
            y = 0
            for line in f:
                if line.strip() == "":
                    continue
                if line[0] in "123456789":
                    self.schilder[line[0]] = line[1:-1]
                    continue
                x = 0
                for char in line[:-1]:
                    #print("xy:",x,y)
                    if char == "M":
                        self.monsters.append(random.choice([Goblin(x, y), Wolf(x,y)]))
                        self.layout[(x,y)] = Floor()
                    elif char == "B":
                        self.monsters.append(random.choice([EliteWarrior(x, y), Golem(x,y)]))
                        self.layout[(x,y)] = Floor()
                    elif char == "T":
                        self.traps.append(Trap(x,y))
                        self.layout[(x,y)] = Floor()
                    elif char == "D":
                        self.doors.append(Door(x,y))
                        self.layout[(x,y)] = Floor()
                    elif char == "L":
                        self.loot.append(Loot(x,y))
                        self.layout[(x,y)] = Floor()
                    elif char == "k":
                        self.keys.append(Key(x,y))
                        self.layout[(x,y)] = Floor()
                    elif char == "<":
                        self.layout[(x,y)] = Stair("up")
                    elif char == ">":
                        self.layout[(x,y)] = Stair("down")
                    elif char == ".":
                        self.layout[(x,y)] = Floor()
                    elif char in "123456789":
                        self.signs.append(Sign(x,y,char))
                        self.layout[(x,y)] = Floor()
                    elif char == "#":
                        self.layout[(x,y)] = Wall()
                    x += 1
                y += 1
                self.width = max(self.width, x)
                self.depth = max(self.depth, y)
        #schild texte ersetzten, geht erst nachdem level komplett gelesen wurde
        for sign in self.signs:
            sign.text = self.schilder[sign.char]


    def update(self):
        """löscht alle Monster und Fallen etc. die keine hitpoints mehr haben"""
        self.monsters = [m for m in self.monsters if m.hitpoints > 0]
        self.traps = [t for t in self.traps if t.hitpoints > 0]
        self.keys = [k for k in self.keys if not k.carried]
        self.loot = [i for i in self.loot if not i.carried]
        self.doors = [d for d in self.doors if d.closed]

    def is_monster(self, x, y):
        """testet ob sich an einer stelle ein monster befindet"""
        for monster in self.monsters:
            if monster.hitpoints > 0 and monster.x == x and monster.y == y:
                return monster
        return False




class Flytext(pygame.sprite.Sprite):
    def __init__(self, x, y, text="hallo", rgb=(255,0,0), blockxy = True,
                  dx=0, dy=-50, duration=2, acceleartion_factor = 0.96 ):
        """a text flying upward and for a short time and disappearing"""
        self._layer = 7 # bestimmt die Sichtbarkeit von Sprites (vor / hinter anderen Sprites)
        pygame.sprite.Sprite.__init__(self, self.groups) # WICHTIG !!
        self.text = text
        self.r, self.g, self.b = rgb[0], rgb[1], rgb[2]
        self.dx = dx
        self.dy = dy
        if blockxy:
            self.x, self.y = PygView.scrollx + x * 32, PygView.scrolly + y * 32
        else:
            self.x, self.y = x, y
        self.duration = duration  # wie lange das Sprite fliegt in Sekunden
        self.acc = acceleartion_factor  # kleiner 1: Sprite wird langsamer. Größer 1: Sprite wird schneller
        self.image = write(self.text, (self.r, self.g, self.b), 22) # font 22
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.time = 0

    def update(self, seconds):
        self.y += self.dy * seconds
        self.x += self.dx * seconds
        self.dy *= self.acc  # langsamer werden
        self.dx *= self.acc
        self.rect.center = (self.x, self.y)
        self.time += seconds
        if self.time > self.duration:
            self.kill()      # lösche Sprite




class PygView(object):
    scrollx = 0  # class variables, can be read from everywhere
    scrolly = 0

    def __init__(self, levelnames, width=640, height=400, x=1,y=1, xp=0, level=1, hp=50, fullscreen=False):
        if fullscreen:
            winstyle = pygame.FULLSCREEN
        else:
            winstyle = 0
        pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
        pygame.init()
        # ----------- Bildschirm einrichten --------
        self.width = width
        self.height = height
        #self.screenrect = pygame.Rect(0, 0, self.width, self.height)
        #bestdepth = pygame.display.mode_ok(self.screenrect.size, winstyle, 32)
        #self.screen = pygame.display.set_mode(self.screenrect.size, winstyle, bestdepth)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.fps = 30  # frames per second
        pygame.display.set_caption("Press ESC to quit")

        # ------- Resourcen als Class Variable laden, (nach pygame.init), damit sie global verfügbar sind
        # ----- bilder liegen im Verzeichnis "images" ---------
        PygView.WALLS = Spritesheet("wall.png")     # 32 x 39
        PygView.FLOORS = Spritesheet("floor.png")   # 32 x 29
        PygView.FIGUREN = Spritesheet("player-keanu.png") # 32 x 57
        PygView.GUI = Spritesheet("gui.png")        # 32 x 17
        PygView.FEAT = Spritesheet("feat-keanu.png")      # 32 x 16
        PygView.MAIN = Spritesheet("main-keanu.png")      # 32 x 29
        # ------ einzelnes Bild mit image_at holen: (x linke obere Ecke,y linke obere Ecke, Breite, Tiefe)
        PygView.WALL = PygView.WALLS.image_at((0, 0, 34, 32))  # x oben links, y oben links, höhe, teife
        PygView.WALL1 = PygView.WALLS.image_at((34, 0, 32, 32))
        PygView.WALL2 = PygView.WALLS.image_at((68, 0, 32, 32))
#        PygView.SIGN  = PygView.GUI.image_at((32*6,0,32,32))
        PygView.FLOOR  = PygView.FLOORS.image_at((160, 32*2, 32, 32))
        PygView.FLOOR1 = PygView.FLOORS.image_at((192, 160, 32, 32))
        PygView.TRAP  = PygView.FEAT.image_at((30, 128, 32, 32), (0, 0, 0))
        PygView.PLAYERBILD = PygView.FIGUREN.image_at((111, 1215, 32, 32), (0, 0, 0))
        PygView.STAIRDOWN = PygView.FEAT.image_at((32*4, 32*5, 32, 32))
        PygView.STAIRUP  = PygView.FEAT.image_at((32*5, 32*5, 32, 32))
        PygView.MONSTERBILD  =  PygView.FIGUREN.image_at((0, 0, 32, 32), (0, 0, 0))
        PygView.DOOR  = PygView.FEAT.image_at((32*2, 32, 32, 32))
        PygView.LOOT  = PygView.MAIN.image_at((155, 672, 32, 32), (0, 0, 0))
        PygView.KEY = PygView.FIGUREN.image_at((54, 1682, 32, 32), (0, 0, 0))
        PygView.SIGN = PygView.GUI.image_at((197, 0, 32, 32), (0, 0, 0))


        # --------- Spieler einrichten --------------
        self.player = Player(x, y, xp, level, hp)
        # Spieler nach seinem Namen fragen
        self.player.name = ask("Dein Name [Enter]? >>", int(self.width/3), int(self.height/2), self.screen )
        self.player.name = self.player.name[0].upper() + self.player.name[1:].lower()
        self.levels = []
        for filename in levelnames:
            self.levels.append(Level(filename))
        self.status = [""]
        self.level = self.levels[0]
        self.seconds = 0
        self.turns = 0
        self.level = self.levels[self.player.z]
        self.background = pygame.Surface((self.level.width*32, self.level.depth*32))
        #self.black = pygame.Surface((self.level.width*32, self.level.depth*32))
        # ------------ Sprite Groups -----------
        self.flytextgroup = pygame.sprite.Group()
        self.allgroup = pygame.sprite.LayeredUpdates() # sprite group with layers
        # --------- Zuweisung der Sprite groups zu den einzelnen Sprite Class
        Flytext.groups = self.flytextgroup, self.allgroup
        # ---------- sound and music ----------
        # sounds liegen im Verzeichnis "sounds", Musik liegt im Verzeichnis "music"
        PygView.bowsound = load_sound("bow.ogg")
        PygView.macesound = load_sound("mace.wav")
        load_music("the_king_is_dead.ogg") # lädt ein music loop in den Mixer
        #pygame.mixer.music.play()  # hintergrundmusik starten
        #pygame.mixer.music.stop()
        #pygame.mixer.music.pause()
        #pygame.mixer.music.unpause()
        #PygView.macesound.play()   # soundeffekt starten

        # -------- Hilftext ------
        self.hilftextlines = []
        self.hilftextlines.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.hilftextlines.append("Befehle:")
        self.hilftextlines.append("[w] [a] [s] [d]......steuere den Spieler")
        self.hilftextlines.append("[<] [>]..............Level rauf / Level runter")
        self.hilftextlines.append("[i]..................zeige Rucksack (inventory)")
        self.hilftextlines.append("[quit] [exit] [Q]....Spiel verlassen")
        self.hilftextlines.append("[?] [help]...........diesen Hilfstext anzeigen")
        self.hilftextlines.append("[q]..................Heiltrank trinken (quaff potion")
        self.hilftextlines.append("[Enter]..............eine Runde warten")
        self.hilftextlines.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.hilftextlines.append("Legende:")
        self.hilftextlines.append("[#]..................Mauer")
        self.hilftextlines.append("[.]..................Boden")
        self.hilftextlines.append("[M]..................Monster")
        self.hilftextlines.append("[k]..................Schlüssel (key)")
        self.hilftextlines.append("[L]..................Gegenstand (loot)")
        self.hilftextlines.append("[D]..................Türe (door)")
        self.hilftextlines.append("[!]..................Schild")
        self.hilftextlines.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")


    def paint(self):
        """malt den Level, und das GUI"""
        for y in range(self.level.depth):
            for x in range(self.level.width):
                self.background.blit(self.level.layout[(x,y)].bild, (x * 32, y * 32))
                for sign in [s for s in self.level.signs if s.x == x and s.y ==y]:
                    self.background.blit(sign.bild, (x * 32, y * 32))
                for trap in [t for t in self.level.traps if t.x == x and t.y == y and t.hitpoints >0
                             and t.visible]:
                    self.background.blit(trap.bild, (x * 32, y * 32))
                for door in [d for d in self.level.doors if d.x == x and d.y == y and d.closed]:
                    self.background.blit(door.bild, (x * 32, y * 32))
                for loot in [l for l in self.level.loot if l.x == x and l.y == y and not l.carried]:
                    self.background.blit(loot.bild, (x * 32, y * 32))
                for key in [k for k in self.level.keys if k.x == x and k.y == y and not k.carried]:
                    self.background.blit(key.bild, (x * 32, y * 32))
        # Scrolling: der spieler wird immer in der Mitte vom Screen geblittet
        PygView.scrollx = self.width / 2 - self.player.x * 32
        PygView.scrolly = self.height / 2 - self.player.y * 32
        self.screen.fill((0, 0, 0))  # bildschirm löschen mit schwarzer Farbe
        self.screen.blit(self.background, (PygView.scrollx, PygView.scrolly))
        # ----- GUI für textbereich
        gui_height = 100
        # ---- paint monsters ---
        for monster in self.level.monsters:
            self.screen.blit(monster.bild, (PygView.scrollx + monster.x * 32, PygView.scrolly + monster.y * 32))
        # ---- paint player -----
        self.screen.blit(self.player.bild, (PygView.scrollx + self.player.x * 32, PygView.scrolly + self.player.y * 32))
        # ---- textbereich schwarz übermalen ---
        pygame.draw.rect(self.screen, (0, 0, 0), (0, self.height - gui_height, self.width, gui_height))
        # Textbereich ist 250 px hoch
        # ---- player status ----
        line = write("{}: hp:{} keys:{}".format(self.player.name,
                     self.player.hitpoints, len(self.player.keys)), (0, 255, 0), 24) # fontsize = 24
        self.screen.blit(line, (self.width / 2, self.height - gui_height))
        line = write("turn:{} x:{} y:{} Ebene:{}".format(self.turns, self.player.x, self.player.y,
                      self.player.z),   (0, 255, 0), 24)
        self.screen.blit(line, (self.width / 2, self.height - gui_height + 16))
        line = write("Exp: {} Level:{}".format(self.player.xp, self.player.level), (0, 255, 0), 24)
        self.screen.blit(line, (self.width / 2, self.height - gui_height + 16*2))

        # ---- paint status messages ----- start 200 pixel from screen bottom
        for number in range(-7, 0, 1):
            if self.status[number][:6] == "Kampf:":
                r, g, b = 255, 0, 255
            else:
                r, g, b = 0, 0, 255
            line = write("{}".format(self.status[number]), (r, g, b+30*number), 24)  # Farbe wird heller
            self.screen.blit(line, (0, self.height + number * 14))


    def run(self):
        """The mainloop---------------------------------------------------"""
        self.clock = pygame.time.Clock() 
        running = True
        self.status = ["The game begins!", "You enter the dungeon...", "Hint: Avoid traps",
                       "Hint: Battle monsters", "Hint: Plunder!", "press ? for help", "good luck!"]

        while running and self.player.hitpoints > 0:
            self.seconds = self.clock.tick(self.fps)/1000.0  # seconds since last frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    # -------- Taste wurde gedrückt und wieder losgelassen ---------
                    wo = self.level.layout[(self.player.x, self.player.y)]
                    self.status.append("Turn {}".format(self.turns))
                    self.turns += 1
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    self.player.dx = 0
                    self.player.dy = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.dy -= 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player.dy += 1
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.dx -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.dx += 1
                    elif event.key == pygame.K_QUESTION or event.key == pygame.K_h:
                        display_textlines(self.hilftextlines, self.screen)
                        continue
                    elif event.key == pygame.K_PERIOD or event.key == pygame.K_RETURN:
                        pass      # player steht eine runde lang herum

                    #elif event.key == pygame.K_t:
                    #    Flytext(self.player.x, self.player.y, "player test")
                    elif event.key == pygame.K_LESS or event.key == pygame.K_GREATER:     # "<":                 # ------ level up
                        if type(wo).__name__ == "Stair":
                            if not wo.down:
                                if self.player.z == 0:
                                    print("Du verlässt den Dungeon und kehrst zurück an die Oberfläche")
                                    running = False
                                    break
                                else:
                                    self.player.z -= 1
                                    self.level = self.levels[self.player.z]
                            else:
                                self.player.z += 1
                                self.level = self.levels[self.player.z]
                        else:
                            self.status.append("{}: Du musst erst eine Stiege nach oben/unten finden [<],[>]".format(self.turns))
                            break
                    elif event.key == pygame.K_q:                  # q --------- Heiltrank ------------
                            if "Heiltrank" in self.player.rucksack and self.player.rucksack["Heiltrank"] > 0:
                                self.player.rucksack["Heiltrank"] -= 1
                                effekt = random.randint(2, 5)
                                self.player.hitpoints += effekt
                                self.status.append("{}: Du trinkst einen Heiltrank und erhälst {} hitpoints".format(
                                                   self.turns, effekt))
                            else:
                                self.status.append("{}: In Deinem Rucksack befindet sich kein Heiltrank. Sammle Loot!".format(
                                                   self.turns))

                    # --------------- new location ----------
                    # wohin: Block (Floor, Wall, Stair)
                    wohin = self.level.layout[(self.player.x+self.player.dx,self.player.y+self.player.dy)]
                    monster = self.level.is_monster(self.player.x+self.player.dx, self.player.y+self.player.dy)
                    #self.refresh_background = False
                    if monster:
                        self.status.extend(kampfrunde(self.player, monster))
                        self.status.extend(kampfrunde(monster, self.player))
                        self.player.dx, self.player.dy = 0,0
                    # ----- testen ob Spieler gegen Wand läuft
                    elif type(wohin).__name__ == "Wall":         # in die Wand gelaufen?
                        self.status.append("{}: Aua, nicht in die Wand laufen!".format(self.turns))
                        self.player.hitpoints -= 1
                        Flytext(self.player.x, self.player.y, "Dmg: 1")
                        self.player.dx, self.player.dy = 0,0
                    # ----- testen ob Spieler gegen Tür läuft
                    for door in [d for d in self.level.doors if d.x == self.player.x+self.player.dx and
                                 d.y == self.player.y + self.player.dy and d.closed]:
                        if len(self.player.keys) > 0:
                            mykey = self.player.keys.pop()
                            door.closed = False  # aufgesperrt !
                            self.status.append("{}: Türe aufgesperrt (1 Schlüssel verbraucht)".format(self.turns))
                        else:
                            self.player.dx, self.player.dy = 0,0
                            self.status.append("{}: Aua! Du knallst gegen eine versperrte Türe".format(self.turns))
                            self.player.hitpoints -= 1
                    # ----------------- Spieler ist an einer neuen position --------
                    self.player.x += self.player.dx
                    self.player.y += self.player.dy
                    wo = self.level.layout[(self.player.x, self.player.y)]               # wo bin ich jetzt
                    #if type(wo).__name__ == "Sign":
                    for sign in self.level.signs:
                        if sign.x == self.player.x and sign.y == self.player.y:
                            self.status.append("{}: hier steht: {}".format(self.turns, sign.text))
                    if type(wo).__name__ == "Stair":
                        if wo.down:
                            self.status.append("{}: Stiege runter: [>] drücken zum runtergehen".format(self.turns))
                        else:
                            self.status.append("{}: Stiege rauf: [<] drücken zum raufgehen".format(self.turns))
                    # --------- liegt eine Falle auf dem Boden herum ?
                    for trap in self.level.traps:
                        if trap.x == self.player.x and trap.y == self.player.y:
                            schaden = random.randint(1, 4)
                            self.status.append("{}: Aua, in die Falle gelaufen. {} Schaden!".format(self.turns, schaden))
                            self.player.hitpoints -= schaden
                            if random.random() < 0.5:             # 50% Chance # Falle verschwunden?
                                self.status.append("{}: Falle kaputt!".format(self.turns))
                                trap.hitpoints = 0
                    # --------- liegt ein Schlüssel auf dem Boden herum ?
                    for key in self.level.keys:
                        if key.x == self.player.x and key.y == self.player.y:
                            key.carried = True
                            self.player.keys.append(key)
                            self.status.append("{} Schlüssel gefunden".format(self.turns))
                    # --------- liegt Loot auf dem Boden herum ?
                    for i in self.level.loot:
                        if i.x == self.player.x and i.y == self.player.y and not i.carried:
                            i.carried = True
                            if i.text in self.player.rucksack:
                                self.player.rucksack[i.text] += 1
                            else:
                                self.player.rucksack[i.text] = 1
                            self.status.append("{} Loot gefunden! ({})".format(self.turns, i.text))
                            Flytext(self.player.x, self.player.y, i.text + " gefunden!", (0,200,0))
                    # ------------------- level update (Fallen, Türen etc. löschen ------
                    self.level.update()                                             # tote monster löschen
                    # -------------- Monster bewegen ------------------
                    #self.level.move_monster(self.player, self)                      # lebende monster bewegen
                    #    def move_monster(self, player, game):
                    #"""bewegt Monster (NICHT den Player) zufällig (oder gar nicht)"""
                    for monster in self.level.monsters:
                        x, y = monster.x, monster.y
                        dx, dy = monster.ai(self.player)
                        if self.level.is_monster(x + dx, y + dy):
                            continue  # Monster wollte in anderes Monster laufen, wartet stattdessen
                        if x+dx == self.player.x and y+dy == self.player.y:
                            self.status.extend(kampfrunde(monster, self.player))
                            self.status.extend(kampfrunde(self.player, monster))
                            continue     # Monster würde in player hineinlaufen, kämpft stattdessen
                        wohin = self.level.layout[(x+dx, y+dy)]
                        if type(wohin).__name__ == "Wall":
                            continue     # Monster würde in Mauer laufen, wartet stattdessen
                        if len([t for t in self.level.traps if t.x == x + dx and t.y == y + dy]) > 0:
                            continue     # Monster würde in Falle laufen, wartet stattdessen
                        if len([d for d in self.level.doors if d.x == x + dx and d.y == y + dy]) > 0:
                            continue # Monster würde in Türe laufen, wartet stattdessen
                        monster.x += dx
                        monster.y += dy


            #pressedkeys = pygame.key.get_pressed() 
            # ------------ Bildschirm neu malen, Sprites bewegen --------------
            pygame.display.set_caption("  press Esc to quit. Fps: %.2f (%i x %i)"%(
                                self.clock.get_fps(), self.width, self.height))
            self.paint()
            #self.allgroup.clear(self.screen, self.background)
            self.allgroup.update(self.seconds)
            self.allgroup.draw(self.screen)
            #  ------- draw the sprites ------
            pygame.display.flip()
        # ------------ game over -----------------
        pygame.mixer.music.stop()
        print("**** Game Over *******")
        print("Hitpoints: {}\nTurns: {}\nXP: {}\nLevel: {}\nRank: {}\nKills: {}".format(self.player.hitpoints,
              self.turns, self.player.xp, self.player.level, self.player.rank, self.player.kills))
        if self.player.hitpoints < 1:
           print("=========Du bist tot==========")
        lines = self.player.zeige_rucksack()
        print("Dein Rucksack:")
        for line in lines:
            print(line)
        print("======= Deine Kills =======")
        for v in self.player.killdict:
            print(v, ":", self.player.killdict[v])
        pygame.quit()    # beendet pygame
        #sys.exit()      # beendet python


if __name__ == '__main__':
    levels = ["level1demo.txt",
              "level2demo.txt"]
    # 800 x 400 pixel, Player startet at x=1, y=1, Erfahrung: 0 xp, level: 1 HP: 50
    PygView(levels, 1600, 1000, 1, 1, 0, 1, 50).run()
