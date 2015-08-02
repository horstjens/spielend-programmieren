# -*- coding: utf-8 -*-                # nur wichtig für python version2
from __future__ import print_function  # nur wichtig für python version2
from __future__ import division        # nur wichtig für python version2 
try:                                   # nur wichtig für python version2
    input = raw_input                  # nur wichtig für python version2
except NameError:                      # nur wichtig für python version2
    pass                               # nur wichtig für python version2

import random    # ab hier ist der code für python3 und python2 gleich


def wait(msg="drücke ENTER"):
    a = input(msg)
    return a


def loot():
    """erzeuge einen zufälligen Gegenstand"""
    zeugs = ["Müll", "Knochen", "Münze", "Taschenmesser", "Stoffreste",
             "Essbesteck", "Spielzeug", "Schwert", "Rüstung",
             "Edelstein", "Heiltrank", "Schild"]
    return random.choice(zeugs)   


def hilfe():
    """zeigt hilfstext, wartet auf ENTER Taste"""
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("Befehle:")
    print("[w] [a] [s] [d]......steuere den Spieler")
    print("[<] [>]..............Level rauf / Level runter")
    print("[i]..................zeige Rucksack (inventory)")
    print("[quit] [exit] [Q]....Spiel verlassen")        
    print("[?] [help]...........diesen Hilfstext anzeigen")
    print("[q]..................Heiltrank trinken (quaff potion)")
    print("[Enter]..............eine Runde warten")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("Legende:")
    print("[#]..................Mauer")
    print("[.]..................Boden")
    print("[M]..................Monster")
    print("[k]..................Schlüssel (key)")
    print("[L]..................Gegenstand (loot)")
    print("[D]..................Türe (door)")
    print("[!]..................Schild")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    wait()


def kampfrunde(m1, m2):
    txt = []         # """ Spieler kämpft gegen Monster Object"""
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
    #return txt
    for line in txt:
        print(line)
    wait()


class Monster(object):
    def __init__(self, x, y, hp=0):
        if hp == 0:
            self.hitpoints = random.randint(5, 10)
        else:
            self.hitpoints = hp
        self.x = x
        self.y = y
        self.name = "Monster"
        self.rucksack = {}
        for z in ["Taschenmesser", "Schwert", "Schild", "Rüstung"]:
            if random.random() < 0.1:  # 10% Chance
                self.rucksack[z] = 1
        
        
class Player(Monster):
    def __init__(self, x, y, hp=25):
        Monster.__init__(self, x, y, hp)
        # self.rucksack = {}   # lösche zufallsausrüstung von class Monster
        self.name = "Spieler"
        self.keys = 0
        self.z = 0             # 0 ist der erste Level, 1 ist der 2. Level usw.

    def zeige_rucksack(self):
        """Zeigt Anzahl und Art von Gegenständen im Rucksack"""
        print("Folgende Sachen befinden sich in deinem Rucksack:")
        if len(self.rucksack) == 0:
            print("dein Rucksack ist leer")
        else:
            print("Anzahl, Gegenstand")
            print("==================")
            for ding in self.rucksack:
                print(self.rucksack[ding], ding)
                
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
                            self.monsters.append(Monster(x, y))
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
        """bewegt Monster zufällig (oder gar nicht)"""
        for monster in self.monsters:
            x, y = monster.x, monster.y
            dirs = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
            dx, dy = random.choice(dirs)
            if self.is_monster(x + dx, y + dy):
                continue
            if x+dx == player.x and y+dy == player.y:
                kampfrunde(monster, player)
                kampfrunde(player, monster)
                continue     # Monster würde in player hineinlaufen
            wohin = self.lines[y+dy][x+dx]
            if wohin in "#TD":
                continue     # Monster würde in Falle oder Mauer oder Tür laufen
            monster.x += dx
            monster.y += dy 
    
    def paint(self, px, py):
        """druckt den Level und die Position des spielers (px,py)"""
        y = 0
        for line in self.lines:
            x = 0
            for char in line:
                if x == px and y == py:
                    print("@", end="")
                elif self.is_monster(x, y):
                    print("M", end="")
                elif char in "123456789":
                    print("!", end="")
                else:
                    print(char, end="")
                x += 1
            print()
            y += 1


def game(levels , playerx=1, playery=1, playerhp=50):
    p = Player(playerx, playery, playerhp)              # Spieler startet mit 50 hitpoints auf Position x:1,y:1
    status = ""
    while p.hitpoints > 0:            # so lange der player mehr als null hitpoints hat
        level = levels[p.z]
        level.paint(p.x, p.y)
        print(status)                 
        dx, dy = 0, 0
        status = ""                   # ----------- ask ----------------------  
        a = input("was jetzt? hp: {} keys: {} >".format(p.hitpoints, p.keys))
        if a == "exit" or a == "quit" or a == "Q":  # ----- quit ------
            break    
        elif a == "i":                # --------- inventory --------
            p.zeige_rucksack()
            wait()
            continue
        elif a == "?" or a == "help":  # ---- help -------
            hilfe()
            continue
        if a == "a":                   # ------------- Bewegung ---------
            dx -= 1
        elif a == "d":
            dx += 1
        elif a == "w":
            dy -= 1
        elif a == "s":
            dy += 1
        elif a == "<":                 # ------ level up
            if level.lines[p.y][p.x] != "<":
                status = "Du musst erst eine Stiege nach oben finden [<]"
            elif p.z == 0:
                print("Du verlässt den Dungeon und kehrst zurück an die Oberfläche")
                break
            p.z -= 1
        elif a == ">":                  # ------ level down
            if level.lines[p.y][p.x] != ">":
                status = "Du musst erst eine Stiege nach unten finden [>]"
            p.z += 1
        elif a == "q":                  # --------- Heiltrank ------------
            if "Heiltrank" in p.rucksack and p.rucksack["Heiltrank"] > 0:
                p.rucksack["Heiltrank"] -= 1
                effekt = random.randint(2, 5)
                p.hitpoints += effekt
                status = "Du trinkst einen Heiltrank und erhälst {} hitpoints".format(effekt)
            else:
                status = "in Deinem Rucksack befindet sich kein Heiltrank. Sammle Loot!"
        wohin = level.lines[p.y+dy][p.x+dx] # ----- testen ob spieler gegen Wand, Monster oder Tür läuft ----
        monster = level.is_monster(p.x+dx, p.y+dy)
        if monster:
            kampfrunde(p, monster)
            kampfrunde(monster, p)
        elif wohin == "#":         # in die Wand gelaufen?
            status = "aua, nicht in die Wand laufen!"
            p.hitpoints -= 1
        elif wohin == "D":
            if p.keys > 0:
                p.keys -= 1
                status = "Türe aufgesperrt (1 Schlüssel verbraucht)"
                level.ersetze(p.x+dx, p.y+dy, ".") 
            else:
                status = "Aua! Du knallst gegen eine versperrte Türe"
                p.hitpoints -= 1
        else:
            p.x += dx
            p.y += dy   # ----------------- spieler ist an einer neuen position --------
        wo = level.lines[p.y][p.x]                # wo bin ich jetzt
        if wo in "123456789":
                status = "hier steht: " + level.schilder[wo]
        elif wo == "T":                           # in die Falle gelaufen?
            schaden = random.randint(1, 4)
            status = "aua, in die Falle gelaufen. {} Schaden!".format(schaden)
            p.hitpoints -= schaden
            if random.random() < 0.5:             # 50% Chance # Falle verschwunden?
                level.ersetze(p.x, p.y, ".")
                status += " Falle kaputt!"
        elif wo == "k":                           # schlüssel gefunden? 
            status = "Schlüssel gefunden!"
            p.keys += 1
            level.ersetze(p.x, p.y, ".")
        elif wo == "L":                           # Loot gefunden ?
            p.nimm(loot())
            level.ersetze(p.x, p.y, ".")
        elif wo == "<":
            status = "Stiege rauf: [<] drücken und [Enter] zum raufgehen"
        elif wo == ">":
            status = "Stiege runter: [>] drücken und [Enter] zum runtergehen"
        level.update()                             # tote monster löschen
        level.move_monster(p)                      # lebende monster bewegen
    print("Game Over. Hitpoints: {}".format(p.hitpoints))
    if p.hitpoints < 1:
        print("Du bist tot")
    p.zeige_rucksack()

if __name__ == "__main__":
    # Spieler startet in level1.txt auf position x1,y1 mit 50 hitpoints
    game([Level("level1demo.txt"), Level("level2demo.txt")], 1, 1, 50)
