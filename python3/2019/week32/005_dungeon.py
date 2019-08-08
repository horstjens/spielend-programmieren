import random
import time



gameoverscreen = """
##############################################################
#.......###......#......#.#....####..........................#
#......#...#....##.....#.#.#...#.............................#
#......#.......#..#....#.#.#...#.............................#
#......#.##...#####....#...#...##............................#
#......#..#...#...#....#...#...#.............................#
#.......##...#.....#...#...#...#####.........................#
#............................................................#
#.....###...#.....#.#####...##...............................#
#....#...#...#...#..#......#..#..............................#
#...#.....#..#...#..#......#.##..............................#
#...#-....#...#.#...###....###...............................#
#....#-..#....#.#...#......#..#..............................#
#.....###......#....#####..#...#.............................#
##############################################################"""

# . here can a random casino machine be placed
# : protected area. nothing is allowed to be placed here
# > stair down
# < stair up

level1 = """
##############################################################
#............................................................#
#...............>.......###############......................#
#.........M............:D:::::::::k:k:#......................#
#...M..M................###############......................#
#............k...............................................#
#............................................................#
#............................................................#
#............................................................#
#............................................................#
#............................................................#
#............................................................#
#............................................................#
#............................................................#
######################.......................................#
#....................##......................................#
#....................####....................................#
#........$.b........:DD:::...................................#
#....................####....................................#
#....................#.......................................#
##############################################################"""

level2 = """
##############################################################
#............................................................#
#............................................................#
#............................................................#
#.....<......................................................#
#............................................................#
##############################################################"""

def prepare():
    dungeon = []
    for raw in (level1, level2):
        
        level = []
        for line in raw.splitlines():
            level.append(list(line))


        ## --- randomize items in level ----

        for y, line in enumerate(level):
            for x, char in enumerate(line):
                if char == "." and random.random() < 0.05:
                    level[y][x] = random.choice(("b","$","$","$"))
        
        ### -----try to place one single casino -----
        for i in range(500):
            x = random.randint(1, len(level[1])-2)
            y = random.randint(1, len(level) - 2)
            if level[y][x] == ".":
                level[y][x] = "R"
                break
        
        # ---- add this level to the dungeon -----
        dungeon.append(level)
    #----- finish ---
    return dungeon     
        
def mathquiz():
    """returns delta hitpoints and delta hunger"""
    print("Das unerbittliche Mathemonster stellt Dir eine Aufgabe")
    print("Antworte schnell und richtig!")
    starttime = time.time()
    a = random.randint(2,12)
    b = random.randint(2,12)
    while True:
        print("wieviel ist {} x {}?".format(a,b))
        answer = input(">>>")
        try:
            answer = int(answer)
        except:
            print("das war keine Zahl")
            continue
        break
    if answer != a * b:
        print("Falsche Antwort...Du verlierst einen Hitpoint")
        input("Drücke ENTER")
        return -1, 0
    endtime = time.time()
    thinktime = endtime - starttime
    dhp, dhu = 0, 0
    if thinktime < 2:
        dhp, dhu = 3, -10
    elif thinktime < 2.5:
        dhp, dhu = 2, -9
    elif thinktime < 3:
        dhp, dhu = 1, -7
    elif thinktime < 4:
        dhp, dhu = 0, -6
    elif thinktime < 5:
        dhp, dhu = 0, -5
    else:
        dhp, dhu = 0, -1
    print("Bravo! {} Sekunden.".format(thinktime))
    print("Du gewinnst {} hp und {} Essen".format(dhp, dhu*-1))
    input("Drücke ENTER")
    return dhp, dhu
    

def fight(a, d):
    print("{} starts a fight with {}".format(a.__class__.__name__,
                                             d.__class__.__name__))
    strike(a, d)
    if d.hp > 0:
        print("counterstrike")
        strike(d, a)
    x = input("press ENTER to continue")
    
def strike(a, d):
    attack_value = a.attack()
    defense_value = d.defense()
    #print("{} strikes with {} points against {} defense points of {}".format(
    #      a.__class__.__name__, attack_value, 
    #      defense_value, d.__class__.__name__))
    if defense_value >= attack_value:
        print("{} is unable to hurt {}".format(a.__class__.__name__, 
                                               d.__class__.__name__))
        return
    damage = attack_value - defense_value
    print("{} suffers {} damage and has {} hp left".format(d.__class__.__name__,
                                                           damage, d.hp- damage))
    d.hp -= damage
    if d.hp <= 0:
         print("{} flees, victory for {}".format(d.__class__.__name__, 
                                                 a.__class__.__name__))
                                            
    
    
    
            
def gamble():
    print("----------------------------------------------")
    print("------- Willkommen im Dungeon-Casino ---------")
    print("----------------------------------------------")
    gewinn = [20, 10, 5, 4, 3, 2, 1, 0 , 0, 0]
    for i in range(10):
        secret = random.randint(1,20)
        print("Errate meine Zahl (1-20). Noch {} Versuche".format(10-i))
        x = input(">>>")
        try:
            x = int(x)
        except:
            print("Das war keine Zahl!")
            continue
        if x == secret:
            print("Bravo, richtig!")
            cash = gewinn[i]
            break
        print("{} es wäre {} gewesen....".format("ha"*(i+2), secret))
    else:
        cash = 0
    print(" Vielen Dank für Ihren Besuch. Ihr Gewinn: {}".format(cash))      
    input("Bitte drücken Sie [ENTER]")  
    return cash



class Monster():
    
    number = 0
    zoo = {}
    
    def __init__(self, x, y, z):
        self.number = Monster.number
        Monster.number += 1
        Monster.zoo[self.number] = self
        self.x = x
        self.y = y
        self.z = z
        self.hp = 100
        self.char = "U"
    
    def attack(self):
        w1 = random.randint(1,6)
        w2 = random.randint(1,6)
        print("{} attack (2d6): {}+{}={}".format(
              self.__class__.__name__,w1,w2,w1+w2))
        return w1+w2
        
    def defense(self):
        w1 = random.randint(1,6)
        w2 = random.randint(1,6)
        
        print("{} defense (2d6): {}+{}={}".format(
              self.__class__.__name__,w1,w2,w1+w2))
        return w1+w2
        
        
    def ai(self):
        return 0, 0

class Dragon(Monster):
    
    def __init__(self, x, y, z):
        Monster.__init__(self, x, y, z)
        self.hp = 150
        self.char = "Ö"
    
    def ai(self):
        dx = random.choice((-1,-1,0,0,0,0,1,1))
        dy = random.choice((-1,-1,0,0,0,0,1,1))
        return dx, dy

class Player(Monster):
    
    def __init__(self, x, y, z):
        Monster.__init__(self, x, y, z)
        self.hp = 200
        self.char = "@"
        self.gold = 0
        self.hunger = 0
        self.keys = 0
        #self.stones = 0
    
    
    
    def status(self):
        text = "hp: {} hunger: {} keys: {} gold: {}".format(
                self.hp, self.hunger, self.keys, self.gold)
        return text
    

def game():
    dungeon = prepare()        
    hero = Player(1, 2, 0)
    Dragon(5, 17, 0)         
    Dragon(8, 12 ,0)
            
    text = ""
    # ------- Grafik engine ------
    while hero.hp > 0:
        # ----- moving monsters ------
        for m in Monster.zoo.values():
            if m.number == hero.number :
                continue
            if m.z != hero.z:
                continue
            if m.hp <= 0:
                continue
            dx, dy = m.ai()
            # --- Monster check for Monster ---
            for m2 in Monster.zoo.values():
                if m2.z != hero.z or m2.hp <= 0:
                    continue 
                if m.y + dy == m2.y and m.x + dx == m2.x:
                    dx, dy = 0, 0
                    if m2.number == hero.number:
                        fight(m, hero)
            # --- wall check for Monster ---
            if dungeon[hero.z][m.y + dy][m.x + dx] in ("#","D"):
                dx, dy = 0, 0
            m.x += dx
            m.y += dy
                
        # ----- graphic engine ----
        for y, line in enumerate(dungeon[hero.z]):
            for x, char in enumerate(line):
                if x == hero.x and y == hero.y:
                    print(hero.char, end="")
                else:
                    for m in Monster.zoo.values():
                        if m.x == x and m.y == y and m.z == hero.z and m.hp >0:
                            print(m.char, end="")
                            break
                    else:
                        if char == ":":
                            print(".", end="")  
                        else:
                            print(char, end="")
            print()
        # ---- control ----
        print(text)
        command = input("{} >>>".format(hero.status()))
        text = ""
        # ---- parsing command ----
        if command in ["end", "ende", "exit", "quit", "bye"]:
            break
        
        # ----- up / down ---
        if command in ["up", "<", "climb up"]:
            if dungeon[hero.z][hero.y][hero.x] != "<":
                text = "Du musst erst eine Stiege nach oben finden (<)"
                continue
            hero.z -= 1
        if command in ["down", ">", "climb down"]:
            if dungeon[hero.z][hero.y][hero.x] != ">":
                text = "Du musst erst eine Stiege nach unten finden (>)"
                continue
            hero.z += 1
        
        # ----- moving ----
        dx, dy = 0, 0
        if command == "w":
            dy = -1
        if command == "s":
            dy = 1
        if command == "a":
            dx = -1
        if command == "d":
            dx = 1
            
        # ------ Monster check ----
        for m2 in Monster.zoo.values():
            if m2.z != hero.z or m2.number == hero.number or m2.hp <= 0:
                continue 
            if m2.x == hero.x+dx and m2.y == hero.y+dy:
                fight(hero, m2)
                dx, dy = 0, 0
                break
            
        
        # ------ wall check -----
        target = dungeon[hero.z][hero.y+dy][hero.x+dx]
        if target == "#":
            text += "ouch! a wall\n"
            hero.hp -= 1
            dx, dy = 0, 0
        
        # ------ mathemonster check ----
        if target == "M":
            dx, dy = 0, 0
            dhp, dhunger = mathquiz()
            hero.hp += dhp
            hero.hunger += dhunger
        
        # ------ casino check ----
        if target == "R":
            dx, dy = 0, 0
            if hero.gold == 0:
                text += "Du bist zu arm um im Casino zu spielen.\n"
            else:
                a = input("Magst Du um 1 Goldstück im Casino spielen?")
                if a.lower() in ("ja", "j", "yes", "y", "ok"):
                    hero.gold -= 1
                    hero.gold += gamble()
                else:
                    text += "na gut, dann nicht\n"
            
        # ----- door check -----
        if target == "D":
            if hero.keys == 0:
                text += "Aua. die Türe ist hart\n"
                dx, dy = 0, 0
                hero.hp -= 1
            else:
                text += "Ich verwende einen Schlüssel um die Türe zu öffnen. Ahhahahahahahah. So schlau!\n"
                hero.keys -= 1
                dungeon[hero.z][hero.y+dy][hero.x+dx] = "." # türe kaputt
                
                
            
        # ---- move ---
        hero.x += dx
        hero.y += dy
        # ----- stair message ----
        if dungeon[hero.z][hero.y][hero.x] == ">":
            text +="You found a stair down. press '>' or 'down' to use it\n"
        if dungeon[hero.z][hero.y][hero.x] == "<":
            text +="You found a stair up. press '<' or 'up' to use it\n"
        # ----- hunger -----
        if random.random() < 0.4:   # 40% chance
            hero.hunger += 1
        if hero.hunger >= 100:
            hero.hp -= 1
            text += "Du verhungerst! Finde schnell Essen\n"
        # ---- auswertung -----
        tile = dungeon[hero.z][hero.y][hero.x]
        if tile == "k":
            text += "hurra, ein Schlüssel, ich kann eine Türe öffnen\n"
            hero.keys += 1
            dungeon[hero.z][hero.y][hero.x] = "."
        if tile == "b":
            text += "mmmm, lecker, eine Banane\n"
            hero.hunger -= 1        ############
            dungeon[hero.z][hero.y][hero.x] = "." 
            #if hero.steine == 5:
            #    text += "Bravo, du hast 5 Bananen gegessen und wirst Bananenkönig\n"
            #    hero.keys += 1 # Bananenkönig bekommt einen schlüssel 
        if tile == "$":
            text += "hurra, Geld\n"
            hero.gold += 1
            dungeon[hero.z][hero.y][hero.x] = "."  
       

    # ----- end ----
    print(gameoverscreen)


if __name__ == "__main__":
    game()







