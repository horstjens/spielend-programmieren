#!/usr/bin/env python
# -*- coding: utf-8 -*-                # nur wichtig für python version2
from __future__ import print_function  # nur wichtig für python version2
from __future__ import division        # nur wichtig für python version2
try:                                   # nur wichtig für python version2
    input = raw_input                  # nur wichtig für python version2
except NameError:                      # nur wichtig für python version2
    pass                               # nur wichtig für python version2



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

SIDE = 32     # constant



def write(msg="pygame is cool", fontcolor=(255,0,255), fontsize=42, font=None):
    myfont = pygame.font.SysFont(font, fontsize)
    mytext = myfont.render(msg, True, fontcolor)
    mytext = mytext.convert_alpha()
    return mytext


def wait(msg="drücke ENTER"):
    #a = input(msg)
    #return a
    pass


def loot():
    """erzeuge einen zufälligen Gegenstand"""
    zeugs = ["Müll", "Knochen", "Münze", "Taschenmesser", "Stoffreste",
             "Essbesteck", "Spielzeug", "Schwert", "Rüstung",
             "Edelstein", "Heiltrank", "Schild"]
    return random.choice(zeugs)



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
    wait()


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
        pass


class Player(Monster):
    def __init__(self, x, y, hp=0, bild = ""):
        Monster.__init__(self, x, y, hp, bild)
        self.name = "Player"
        self.z = 0
        self.keys = 0
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
                lines.append(self.rucksack[ding], ding)
        return lines

    def nimm(self, zeug):
        """Erhöht Anzahl von Gegenständen im Rucksack"""
        if zeug in self.rucksack:
            self.rucksack[zeug] += 1
        else:
            self.rucksack[zeug] = 1
        



class Level(object):
    def __init__(self, dateiname):
        """liest den dateinamen ein und erzeugt ein Level-Object"""
        self.lines = []
        self.schilder = {}       # schildnummer: schildtext
        self.monsters = []
        self.sichtweite = 10
        with open(dateiname) as f:
            y = 0
            for line in f:
                goodline = ""
                if line[0] in "123456789":
                    self.schilder[line[0]] = line[1:-1]
                    continue
                elif line.strip() == "":
                    continue
                else:
                    x = 0
                    for char in line[:-1]:
                        if char == "M":
                            self.monsters.append(Monster(x, y, 0))
                            goodline += "."
                        else:
                            goodline += char
                        x += 1
                self.lines.append(goodline)
                y += 1

    def update(self):
        """löscht alle Monster die keine hitpoints mehr haben"""
        self.monsters = [m for m in self.monsters if m.hitpoints > 0]

    def ersetze(self, x, y, new="."):
        """ersetzt ein Zeichen in einem Level durch das new Zeichen"""
        self.lines[y] = self.lines[y][:x]+new+self.lines[y][x+1:]

    def is_monster(self, x, y):
        """testet ob sich an einer stelle ein monster befindet"""
        for monster in self.monsters:
            if monster.hitpoints > 0 and monster.x == x and monster.y == y:
                return monster
        return False

    def move_monster(self, player):
        """bewegt Monster (NICHT den Player) zufällig (oder gar nicht)"""
        for monster in self.monsters:
            if monster.name == "Player":
                continue
            x, y = monster.x, monster.y
            #dirs = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
            #dx, dy = random.choice(dirs)
            dx, dy = monster.ai()
            if self.is_monster(x + dx, y + dy):
                continue
            if x+dx == player.x and y+dy == player.y:
                kampfrunde(monster, player)
                kampfrunde(player, monster)
                wait()
                continue     # Monster würde in player hineinlaufen
            wohin = self.lines[y+dy][x+dx]
            if wohin in "#T":
                continue     # Monster würde in Falle oder Mauer laufen
            monster.x += dx
            monster.y += dy

    def paint(self, player):
        """druckt den Level ohne Monster mit Zeichen"""
        output = [""]
        y = 0
        for line in self.lines:
            x = 0
            for char in line:
                #if x == player.x and y == player.y:
                #    output[y]+="@"
                #elif self.is_monster(x, y):
                #    output[y]+="M"
                if char in "123456789":
                    output[y] +="!"
                else:
                    output[y] +=char
                x += 1
            y += 1
            output.append("")
        return output # lines


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
        PygView.TRAP  = PygView.FEAT.image_at((SIDE*1, SIDE*4, SIDE, SIDE))
        PygView.PLAYERBILD = PygView.FIGUREN.image_at((0, 30, SIDE, SIDE), (0, 0, 0))
        PygView.STAIRDOWN = PygView.FEAT.image_at((SIDE*4, SIDE*5, SIDE, SIDE))
        PygView.STAIRUP  = PygView.FEAT.image_at((SIDE*5, SIDE*5, SIDE, SIDE))
        PygView.MONSTERBILD  =  PygView.FIGUREN.image_at((0, 0, SIDE, SIDE), (0, 0, 0))
        PygView.DOOR  = PygView.FEAT.image_at((SIDE*2,SIDE,SIDE,SIDE))
        PygView.LOOT  = PygView.MAIN.image_at((SIDE*17,SIDE*21,SIDE,SIDE))


        self.player = Player(x,y,hp)
        self.levels = []
        for filename in levelnames:
            self.levels.append(Level(filename))
        self.status = [""]


    def paint(self):
        y = 0
        for line in self.level.paint(self.player):
            x = 0
            for char in line:
                if char == "#":
                    self.screen.blit(self.WALL, (x,y))
                elif char == ".":
                    self.screen.blit(self.FLOOR, (x,y))
                elif char in "123456789":
                    self.screen.blit(self.SIGN, (x,y))
                elif char == "<":
                    self.screen.blit(self.STAIRUP, (x,y))
                elif char == ">":
                    self.screen.blit(self.STAIRDOWN, (x,y))
                elif char == "T":
                    self.screen.blit(self.TRAP, (x,y))
                elif char == "L":
                    self.screen.blit(self.LOOT, (x,y))
                elif char == "D":
                    self.screen.blit(self.DOOR, (x,y))
                x += SIDE
            y += SIDE
        line = write(self.status[-1])
        ##### paint player and monsters over background
        for monster in self.level.monsters:
            self.screen.blit(monster.bild, (monster.x * SIDE, monster.y * SIDE))
        ### paint player
        self.screen.blit(self.player.bild, (self.player.x * SIDE, self.player.y * SIDE))
        self.screen.blit(line, (0,y+50))


    def run(self):
        """The mainloop---------------------------------------------------"""
        self.clock = pygame.time.Clock() 
        running = True
        self.status = ["game start"]
        while running and self.player.hitpoints > 0:
            self.status = self.status[:50] # only keep the last 50 lines
            self.level = self.levels[self.player.z]
            self.seconds = self.clock.tick(self.fps)/1000.0  # seconds since last frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
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
                            self.status = "Du musst erst eine Stiege nach oben finden [<]"
                        elif self.player.z == 0:
                            print("Du verlässt den Dungeon und kehrst zurück an die Oberfläche")
                            running = False
                        self.player.z -= 1
                    elif event.key == pygame.K_GREATER: #  ">":                  # ------ level down
                            if self.level.lines[self.player.y][self.player.x] != ">":
                                self.status = "Du musst erst eine Stiege nach unten finden [>]"
                            self.player.z += 1
                    elif event.key == pygame.K_q:                  # q --------- Heiltrank ------------
                            if "Heiltrank" in self.player.rucksack and self.player.rucksack["Heiltrank"] > 0:
                                self.player.rucksack["Heiltrank"] -= 1
                                effekt = random.randint(2, 5)
                                self.player.hitpoints += effekt
                                self.status = "Du trinkst einen Heiltrank und erhälst {} hitpoints".format(effekt)
                            else:
                                self.status = "in Deinem Rucksack befindet sich kein Heiltrank. Sammle Loot!"

                    #elif a == "i":                # --------- inventory --------
                    #    p.zeige_rucksack()
                    #    wait()
                    #elif a == "?" or a == "help":  # ---- help -------
                    # hilfe()

                    # --------------- new location ----------
                    wohin = self.level.lines[self.player.y+self.player.dy][self.player.x+self.player.dx]
                    monster = self.level.is_monster(self.player.x+self.player.dx, self.player.y+self.player.dy)
                    if monster:
                        kampfrunde(self.player, monster)
                        kampfrunde(monster, self.player)
                        wait()
                    # ----- testen ob spieler gegen Wand, Monster oder Tür läuft ----
                    elif wohin == "#":         # in die Wand gelaufen?
                        self.status = "aua, nicht in die Wand laufen!"
                        self.player.hitpoints -= 1
                    elif wohin == "D":
                        if self.player.keys > 0:
                            self.player.keys -= 1
                            self.status = "Türe aufgesperrt (1 Schlüssel verbraucht)"
                            self.level.ersetze(self.player.x+self.player.dx, self.player.y+self.player.dy, ".")
                        else:
                            self.status = "Aua! Du knallst gegen eine versperrte Türe"
                            self.player.hitpoints -= 1
                    else:
                        self.player.x += self.player.dx
                        self.player.y += self.player.dy
                    # ----------------- spieler ist an einer neuen position --------
                    wo = self.level.lines[self.player.y][self.player.x]                # wo bin ich jetzt
                    if wo in "123456789":
                        self.status = "hier steht: " + self.level.schilder[wo]
                    elif wo == "T":                           # in die Falle gelaufen?
                        schaden = random.randint(1, 4)
                        self.status = "aua, in die Falle gelaufen. {} Schaden!".format(schaden)
                        self.player.hitpoints -= schaden
                        if random.random() < 0.5:             # 50% Chance # Falle verschwunden?
                            self.level.ersetze(self.player.x, self.player.y, ".")
                            self.status += " Falle kaputt!"
                    elif wo == "k":                           # schlüssel gefunden?
                        self.status = "Schlüssel gefunden!"
                        self.player.keys += 1
                        self.level.ersetze(self.player.x, self.player.y, ".")
                    elif wo == "L":                           # Loot gefunden ?
                        self.player.nimm(loot())
                        self.level.ersetze(self.player.x, self.player.y, ".")
                    elif wo == "<":
                        self.status = "Stiege rauf: [<] drücken zum raufgehen"
                    elif wo == ">":
                        self.status = "Stiege runter: [>] drücken zum runtergehen"
                    # ------------------- level update
                    self.level.update()                             # tote monster löschen
                    self.level.move_monster(self.player)                      # lebende monster bewegen

            #pressedkeys = pygame.key.get_pressed() 

            pygame.display.set_caption("player hp: %i press Esc to quit. Fps: %.2f (%i x %i)"%(self.player.hitpoints, self.clock.get_fps(), self.width, self.height))
            self.paint()
            pygame.display.flip()          
        # ------------ game over -----------------
        pygame.quit()
        print("Game Over. Hitpoints: {}".format(self.player.hitpoints))
        if self.player.hitpoints < 1:
           print("Du bist tot")
        self.player.zeige_rucksack()

####



if __name__ == '__main__':
    levels = ["level1.txt","level2.txt"]
    PygView(levels, 1920, 1000, 1, 1, 50).run() # player at 1,1 with 50 hp
