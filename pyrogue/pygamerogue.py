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

####
import pygame
import random
####

SIDE = 32     # constant


def write(msg="pygame is cool", fontcolor=(255,0,255), fontsize=42, font=None):
    print(msg)
    myfont = pygame.font.SysFont(font, fontsize)
    mytext = myfont.render(msg, True, fontcolor)
    mytext = mytext.convert_alpha()
    return mytext


def hilfe():
    """zeigt hilfstext, wartet auf ENTER Taste"""
    txt = []
    txt.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    txt.append("Befehle:")
    txt.append("[w] [a] [s] [d]......steuere den Spieler")
    txt.append("[<] [>]..............Level rauf / Level runter")
    txt.append("[i]..................zeige Rucksack (inventory)")
    txt.append("[quit] [exit] [Q]....Spiel verlassen")
    txt.append("[?] [help]...........diesen Hilfstext anzeigen")
    txt.append("[q]..................Heiltrank trinken (quaff potion")
    txt.append("[Enter]..............eine Runde warten")
    txt.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    txt.append("Legende:")
    txt.append("[#]..................Mauer")
    txt.append("[.]..................Boden")
    txt.append("[M]..................Monster")
    txt.append("[k]..................Schlüssel (key)")
    txt.append("[L]..................Gegenstand (loot)")
    txt.append("[D]..................Türe (door)")
    txt.append("[!]..................Schild")
    txt.append("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")


def kampfrunde(m1, m2):
    """ Kampf gegen Monster Object"""
    txt = []
    if m1.hitpoints > 0 and m2.hitpoints > 0:
        txt.append("{} ({} hp) schlägt nach {} ({} hp)".format(m1.name, m1.hitpoints, m2.name, m2.hitpoints))
        if "Schwert" in m1.rucksack:      # and rucksack["Waffe"] >0:
            damage = random.randint(1, 4)
            waffe = "Schwert"
        elif "Taschenmesser" in m1.rucksack:
            damage = random.randint(1, 3)
            waffe = "Taschenmesser"
        else:
            damage = random.randint(1, 2)
            waffe = "Faust"
        txt.append("{} attackiert {} mit {} für {} Schaden".format(
            m1.name, m2.name, waffe, damage))
        if "Rüstung" in m2.rucksack:
            damage -= 1
            txt.append("Rüstung von {} absorbiert einen Schadenspunkt".format(m2.name))
        if "Schild" in m2.rucksack:
            damage -= 1
            txt.append("Schild von {} aborbiert einen Schadenspunkt".format(m2.name))
        if damage > 0:
            m2.hitpoints -= damage
            txt.append("{} verliert {} hitpoints ({} hp übrig)".format(m2.name, damage, m2.hitpoints))
        else:
            txt.append("{} bleibt unverletzt".format(m2.name))
    return txt


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


class Monster(object):
    def __init__(self,x,y,hp, bild=""):
        self.x = x
        self.y = y
        if hp == 0:
            self.hitpoints = random.randint(10,20)
        else:
            self.hitpoints = hp
        if bild == "":
            self.bild = PygView.MONSTERBILD
        else:
            self.bild = bild
        self.name = "Monster"
        self.strength = random.randint(1,10)
        self.dexterity = random.randint(1,10)
        self.intelligence = random.randint(1,10)

        self.rucksack = {}
        for z in ["Taschenmesser", "Schwert", "Schild", "Rüstung"]:
            if random.random() < 0.1:  # 10% Chance
                self.rucksack[z] = 1

    def ai(self):
        """returns dx, dy: where the monster wants to go"""
        dirs = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        return random.choice(dirs)   #return dx, xy


class Boss(Monster):
    def __init__(self, x,y,hp, bild):
        Monster.__init__(self, x, y, hp, bild)

    def ai(self):
        """a Boss is intelligent enough to chase the player"""


class Player(Monster):
    def __init__(self, x, y, hp=0, bild = ""):
        Monster.__init__(self, x, y, hp, bild)
        self.name = "Player"
        self.rucksack = {}
        self.z = 0
        self.keys = []
        if hp == 0:
            self.hitpoints = random.randint(5,10)
        else:
            self.hitpoints = hp
        self.bild = PygView.PLAYERBILD

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
        self.bild = PygView.WALL


class Sign(Block):
    def __init__(self, char):
        Block.__init__(self)
        self.bild = PygView.SIGN
        self.char = char # number from level source code
        self.text = "" # the long text of the sign


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
        self.bild = None
        self.carried = False # in someone's inventory?


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
        self.open = False
        self.bild = PygView.DOOR
        self.color = color


class Loot(Item):
    def __init__(self, x, y):
        Item.__init__(self, x, y)
        zeugs = ["Müll", "Knochen", "Münze", "Taschenmesser", "Stoffreste",
             "Essbesteck", "Spielzeug", "Schwert", "Rüstung",
             "Edelstein", "Heiltrank", "Schild"]
        self.text = random.choice(zeugs)
        self.bild = PygView.LOOT


class Level(object):
    def __init__(self, dateiname):
        """liest den dateinamen ein und erzeugt ein Level-Object"""
        #self.lines = []
        self.layout = {} # lines of non-movable stuff
        self.schilder = {}       # schildnummer: schildtext
        self.monsters = []
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
                    print("xy:",x,y)
                    if char == "M":
                        self.monsters.append(Monster(x, y, 0))
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
                        self.layout[(x,y)] = Sign(char)
                    elif char == "#":
                        self.layout[(x,y)] = Wall()
                    x += 1
                y += 1
                self.width = max(self.width, x)
                self.depth = max(self.depth, y)
        # schild texte ersetzten
        y,x = 0,0
        for y in range(self.depth):
            for x in range(self.width):
                block = self.layout[(x,y)]
                if type(block).__name__ == "Sign":
                    block.text = self.schilder[block.char]

    def update(self):
        """löscht alle Monster und Fallen die keine hitpoints mehr haben"""
        self.monsters = [m for m in self.monsters if m.hitpoints > 0]
        self.traps = [t for t in self.traps if t.hitpoints > 0]
        self.keys = [k for k in self.keys if not k.carried]
        self.loot = [i for i in self.loot if not i.carried]
        self.doors = [d for d in self.doors if not d.open]

    def is_monster(self, x, y):
        """testet ob sich an einer stelle ein monster befindet"""
        for monster in self.monsters:
            if monster.hitpoints > 0 and monster.x == x and monster.y == y:
                return monster
        return False

    def move_monster(self, player):
        """bewegt Monster (NICHT den Player) zufällig (oder gar nicht)"""
        for monster in self.monsters:
            #if monster.name == "Player":
            #    continue
            x, y = monster.x, monster.y
            dx, dy = monster.ai()
            if self.is_monster(x + dx, y + dy):
                continue
            if x+dx == player.x and y+dy == player.y:
                kampfrunde(monster, player)
                kampfrunde(player, monster)
                continue     # Monster würde in player hineinlaufen
            wohin = self.layout[(x+dx, y+dy)]
            if type(wohin).__name__ == "Wall":
                continue     # Monster würde in Mauer laufen
            for trap in self.traps:
                if trap.x == x+dx and trap.y == y+dy:
                    continue # Monster würde in Falle laufen
            for door in self.doors:
                if door.x == x+dx and door.y == y+dy:
                    continue # Monster würde in Türe laufen
            monster.x += dx
            monster.y += dy



class PygView(object):

    def __init__(self, levelnames, width=640, height=400, x=1,y=1, hp=50 ):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.fps = 30  # frames per second
        pygame.display.set_caption("Press ESC to quit")

        PygView.WALLS = Spritesheet("wall.png")     # 32 x 39
        PygView.FLOORS = Spritesheet("floor.png")   # 32 x 29
        PygView.FIGUREN = Spritesheet("player.png") # 32 x 57
        PygView.GUI = Spritesheet("gui.png")        # 32 x 17
        PygView.FEAT = Spritesheet("feat.png")      # 32 x 16
        PygView.MAIN = Spritesheet("main.png")      # 32 x 29
        PygView.WALL = PygView.WALLS.image_at((0, 0, SIDE, SIDE))
        PygView.SIGN  = PygView.GUI.image_at((SIDE*6,0,SIDE,SIDE))
        PygView.FLOOR  = PygView.FLOORS.image_at((160, SIDE*2 ,SIDE, SIDE))
        PygView.FLOOR1 = PygView.FLOORS.image_at((192, 162, SIDE, SIDE))
        PygView.TRAP  = PygView.FEAT.image_at((SIDE*1, SIDE*4, SIDE, SIDE))
        PygView.PLAYERBILD = PygView.FIGUREN.image_at((0, 30, SIDE, SIDE), (0, 0, 0))
        PygView.STAIRDOWN = PygView.FEAT.image_at((SIDE*4, SIDE*5, SIDE, SIDE))
        PygView.STAIRUP  = PygView.FEAT.image_at((SIDE*5, SIDE*5, SIDE, SIDE))
        PygView.MONSTERBILD  =  PygView.FIGUREN.image_at((0, 0, SIDE, SIDE), (0, 0, 0))
        PygView.DOOR  = PygView.FEAT.image_at((SIDE*2,SIDE,SIDE,SIDE))
        PygView.LOOT  = PygView.MAIN.image_at((SIDE*17,SIDE*21,SIDE,SIDE))
        PygView.KEY = PygView.FIGUREN.image_at((76, 1684,9,25))
        PygView.SIGN = PygView.GUI.image_at((6*SIDE, 0, SIDE, SIDE))


        self.player = Player(x,y,hp)
        self.levels = []
        for filename in levelnames:
            self.levels.append(Level(filename))
        self.status = [""]


        #self.refresh_background = True
        #self.refresh_removables = True

    def paint(self):
        x,y = 0, 0
        for y in range(self.level.depth):
            for x in range(self.level.width):
                self.background.blit(self.level.layout[(x,y)].bild, (x*SIDE, y*SIDE))

        scrollx = 0
        scrolly = 0
        self.screen.blit(self.background, (scrollx, scrolly))

        # ---- paint monsters ---
        for monster in self.level.monsters:
            self.screen.blit(monster.bild, (scrollx + monster.x * SIDE, scrolly + monster.y * SIDE))
        # ---- paint player -----
        self.screen.blit(self.player.bild, (scrollx + self.player.x * SIDE, scrolly + self.player.y * SIDE))
        # ---- textbereich schwarz übermalen ---
        pygame.draw.rect(self.screen, (0,0,0), (0, y * SIDE+50, self.width, self.height - y * SIDE + 50))
        # ---- player status ----
        line = write("Player: hp:{} keys:{} turn:{} x:{} y:{} level:{}".format(
                self.player.hitpoints, len(self.player.keys), self.turns, self.player.x,
                self.player.y, self.player.z), (0,255,0))

        self.screen.blit(line, (self.width - 800, y* SIDE+50))
        # ---- paint status messages -----
        for number in range(-5,0,1):
               line = write("{}".format(self.status[number]), (0,0,255+40*number))
               self.screen.blit(line, (0, SIDE* y +50 + 5*50 + number * 50))


    def run(self):
        """The mainloop---------------------------------------------------"""
        self.clock = pygame.time.Clock() 
        running = True
        self.status = ["The game begins!","You enter the dungeon...", "Hint: Avoid traps", "Hint: Battle monsters", "Hint: Plunder!"]
        self.turns = 0
        self.level = self.levels[self.player.z]
        self.background = pygame.Surface((self.level.width*SIDE, self.level.depth*SIDE))
        while running and self.player.hitpoints > 0:
            #self.status = self.status[:50] # only keep the last 50 lines
            self.seconds = self.clock.tick(self.fps)/1000.0  # seconds since last frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
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
                    elif event.key == pygame.K_PERIOD or event.key == pygame.K_RETURN:
                        pass # player steht eine runde lang herum
                    elif event.key == pygame.K_LESS:     # "<":                 # ------ level up
                        if self.level.lines[self.player.y][self.player.x] != "<":
                            self.status.append("{}: Du musst erst eine Stiege nach oben finden [<]".format(self.turns))
                            break
                        elif self.player.z == 0:
                            print("Du verlässt den Dungeon und kehrst zurück an die Oberfläche")
                            running = False
                            break
                        self.player.z -= 1
                        self.level = self.levels[self.player.z]
                        self.background = pygame.Surface((len(self.level.lines[0])*SIDE, len(self.level.lines)*SIDE))
                        #self.refresh_background = True
                    elif event.key == pygame.K_GREATER: #  ">":                  # ------ level down
                        if self.level.lines[self.player.y][self.player.x] != ">":
                            self.status.append("{}: Du musst erst eine Stiege nach unten finden [>]".format(self.turns))
                            break
                        self.player.z += 1
                        self.level = self.levels[self.player.z]
                        self.background = pygame.Surface((len(self.level.lines[0])*SIDE, len(self.level.lines)*SIDE))
                        #self.refresh_background = True
                    elif event.key == pygame.K_q:                  # q --------- Heiltrank ------------
                            if "Heiltrank" in self.player.rucksack and self.player.rucksack["Heiltrank"] > 0:
                                self.player.rucksack["Heiltrank"] -= 1
                                effekt = random.randint(2, 5)
                                self.player.hitpoints += effekt
                                self.status.append("{}: Du trinkst einen Heiltrank und erhälst {} hitpoints".format(
                                                   self.turns, effekt))
                            else:
                                self.status.append("{}: in Deinem Rucksack befindet sich kein Heiltrank. Sammle Loot!".format(
                                                   self.turns))

                    # --------------- new location ----------
                    wohin = self.level.layout[(self.player.x+self.player.dx,self.player.y+self.player.dy)]
                    monster = self.level.is_monster(self.player.x+self.player.dx, self.player.y+self.player.dy)
                    #self.refresh_background = False
                    if monster:
                        kampfrunde(self.player, monster)
                        kampfrunde(monster, self.player)
                    # ----- testen ob spieler gegen Wand, Monster oder Tür läuft ----
                    elif type(wohin).__name__ == "Wall":         # in die Wand gelaufen?
                        self.status.append("{}: aua, nicht in die Wand laufen!".format(self.turns))
                        self.player.hitpoints -= 1
                    elif wohin == "D":
                        if self.player.keys > 0:
                            self.player.keys -= 1
                            self.status.append("{}: Türe aufgesperrt (1 Schlüssel verbraucht)".format(self.turns))
                            self.level.ersetze(self.player.x+self.player.dx, self.player.y+self.player.dy, ".")
                            #self.refresh_background = True
                        else:
                            self.status.append("{}: Aua! Du knallst gegen eine versperrte Türe".format(self.turns))
                            self.player.hitpoints -= 1
                    else:
                        self.player.x += self.player.dx
                        self.player.y += self.player.dy
                    # ----------------- spieler ist an einer neuen position --------
                    wo = self.level.layout[(self.player.x, self.player.y)]               # wo bin ich jetzt
                    #self.refresh_removables = False
                    #if self.turns == 1:
                    #    self.refresh_removables = True
                    if type(wo).__name__ == "Sign":
                        self.status.append("{}: hier steht: {}".format(self.turns, wo.text))
                    elif type(wo).__name__ == "Stair":
                        if wo.down:
                            self.status.append("{}: Stiege runter: [>] drücken zum runtergehen".format(self.turns))
                        else:
                            self.status.append("{}: Stiege rauf: [<] drücken zum raufgehen".format(self.turns))
                    # --------- liegt etwas  auf dem Boden herum ?
                    for trap in self.level.traps:
                        if trap.x == self.player.x and trap.y == self.player.y:
                            schaden = random.randint(1, 4)
                            self.status.append("{}: Aua, in die Falle gelaufen. {} Schaden!".format(self.turns, schaden))
                            self.player.hitpoints -= schaden
                            if random.random() < 0.5:             # 50% Chance # Falle verschwunden?
                                self.status.append("{}: Falle kaputt!".format(self.turns))
                                trap.hitpoints = 0

                    for key in self.level.keys:
                        if key.x == self.player.x and key.y == self.player.y:
                            key.carried = True
                            self.player.keys.append(key)

                    for i in self.level.loot:
                        if i.x == self.player.x and i.y == self.player.y:
                            i.carried = True
                            name = type(i).__name__
                            if name in self.player.rucksack:
                                self.player.rucksack[name] += 1
                            else:
                                self.player.rucksack[name] = 1


                    # ------------------- level update
                    self.level.update()                             # tote monster löschen
                    self.level.move_monster(self.player)                      # lebende monster bewegen


            #pressedkeys = pygame.key.get_pressed() 

            pygame.display.set_caption("  press Esc to quit. Fps: %.2f (%i x %i)"%(
                                self.clock.get_fps(), self.width, self.height))
            self.paint()
            pygame.display.flip()          
        # ------------ game over -----------------
        pygame.quit()
        print("Game Over. Hitpoints: {}".format(self.player.hitpoints))
        if self.player.hitpoints < 1:
           print("Du bist tot")
        self.player.zeige_rucksack()


if __name__ == '__main__':
    levels = ["level1.txt", "level2.txt"]
    PygView(levels, 1920, 1000, 1, 1, 50).run() # player at 1,1 with 50 hp
