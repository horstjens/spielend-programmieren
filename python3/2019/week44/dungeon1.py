""" a roguelike game using pure python3"""

import random

# raw level 

legend = {
        ".":"empty space",
        "#":"a solid wall",
        "D":"a door",
        "W":"a dangerous wolf",
        "@":"the player",
        "k":"a key to open a door",
            }
        


d1 = """
###################################################
#......D.W............W...........................#
#.................................#####...........#
#...#..k..........................#...D...........#
###################################################
"""

d2 = """
###################################################
#.................................................#
#.................................#####...........#
#...#.#...........................#...D...........#
###################################################
"""

d3 = """
###################################################
#.................................................#
#.................................#####...........#
#.....#.#.#.......................#...D...........#
###################################################
"""


# create levels
def create():        
    dungeon = []
    for z, d in enumerate((d1, d2, d3)):
        level = []
        for y, line in enumerate(d.splitlines()):
            row = []
            for x, char in enumerate(list(line)):
                if char == "W":
                    row.append(".")
                    Wolf(x,y,z)
                elif char == "D":
                    row.append(".")
                    Door(x,y,z)
                else:
                    row.append(char)
            level.append(row)
        dungeon.append(level)
    return dungeon
        
        
def roll_dice(number, sides, bonus=0):
    total = 0
    print("rolling {}D{}+{}....".format(number, sides, bonus))
    for d in range(number):
        roll = random.randint(1, sides)
        total += roll
        print("die #{} rolls a {}".format(d+1, roll))
    print("-------")
    print("sum:", total, "+", bonus, "=", total+bonus)
    return total + bonus

def strike(a, d):
    # a = attacker, d=defender
    aname = a.__class__.__name__
    dname = d.__class__.__name__
    # 3d6 + dex > 2d6 + dex
    print(aname, "tries to attack", dname,
          "(3d6+{} > 2d6+{})".format(a.dexterity, d.dexterity))
    aroll = roll_dice(3,6, a.dexterity)
    droll = roll_dice(2,6, d.dexterity)
    if aroll > droll:
        print("attack sucessfull, 10 damage")
        d.hitpoints -= 10
    else:
        print("attack failed")

            

class Monster():
    
    number = 0
    zoo = {}
    
    def __init__(self, x,y,z):
        self.number = Monster.number
        Monster.number += 1
        Monster.zoo[self.number] = self
        self.x = x
        self.y = y
        self.z = z
        self.keys = 0
        self.strength = 5
        self.dexterity = 5
        self.char = "M"
        self.hitpoints = 100
        self.overwrite_parameters()
    
    def collision(self, other):
        print("Boing! {} is attacking {}".format(other.__class__.__name__,
                                                 self.__class__.__name__))
        
    def overwrite_parameters(self):
        pass

class Door(Monster):
    
    def collision(self, other):
        #print("Boing! {} is attacking {}".format(other.__class__.__name__,
        #                                         self.__class__.__name__))
        print("A massive wooden door is blocking your path")
        if other.keys > 0:
            print("You open the door with one of your keys")
            self.hitpoints = 0   # destroy door
            other.keys -= 1      # use up one key
            print("You have now {} key(s) left".format(other.keys))
        else:
            print("Sadly, you have no key to open this door")
            command = input("Do you want to try to (s)mash the door, (p)ick the lock or (c)ancel ?")
            if command == "s":
                print("You try to smash the door open (2D6 < {})".format(other.strength))
                roll = roll_dice(2,6)
                if roll < other.strength:
                    print("The door is destroyed!")
                    self.hitpoints = 0
                else:
                    print("too weak, not sucessfull")
                    other.hitpoints -= 1
                    print("You hurt yourself")
            elif command == "p":
                print("You try to pick the lock (2D6 < {})".format(other.dexterity))
                roll = roll_dice(2,6)
                if roll < other.dexterity:
                    print("You pick the lock!")
                    self.hitpoints = 0
                else:
                    print("too butterfingered, not sucessfull")
                    other.hitpoints -= 1
                    print("You hurt yourself")


    def overwrite_parameters(self):
        self.hitpoints = 15
        self.char = "D"
    
        
class Hero(Monster):
    
    def overwrite_parameters(self):
        self.hitpoints = 500
        self.char = "@"
        self.dexterity = 5
        self.strength = 8
        
class Wolf(Monster):
    
    def overwrite_parameters(self):
        self.hitpoints = 200
        self.char = "W"
        self.dexterity = 7
        self.strength = 4
    
    
def game():
    player = Hero(1,2,0)
    dungeon = create()
    
    # ------
    while player.hitpoints > 0:
        for y, line in enumerate(dungeon[player.z]):
            for x, char in enumerate(line):
                # Monster ? 
                for m in Monster.zoo.values():
                    if m.hitpoints <= 0:
                        continue
                    if m.z == player.z and m.y==y and m.x == x:
                        print(m.char, end="")
                        break
                else:
                    print(char, end="")
            print() # end of line
        # --- status ---
        status = "hitpoints: {} keys: {}".format(player.hitpoints,
                  player.keys) # player.x, player.y, player.z)
        command = input(status + " >>>")
        dx, dy = 0, 0
        if command == "quit":
            break
        if command == "up" and player.z > 0:
            player.z -= 1
        if command == "down" and player.z < len(dungeon) - 1:
            player.z += 1
        if command == "w":
            dy = -1
        if command == "s":
            dy = 1
        if command == "a":
            dx = -1
        if command == "d":
            dx = 1
        # ---- collision test with wall ----
        target = dungeon[player.z][player.y + dy][player.x + dx] 
        if target == "#":
            print("Oouch!")
            player.hitpoints -= 1
            dx, dy = 0, 0
        #elif target:
        #--- collision detection with Monsters----
        for m in Monster.zoo.values():
            if m.number == player.number:
                continue 
            if m.hitpoints <= 0:
                continue 
            if m.z == player.z and m.y == player.y +dy and m.x == player.x +dx:
                dx = 0
                dy = 0
                m.collision(player)
            
        player.x += dx
        player.y += dy
        # ---- pick up items ----
        target = dungeon[player.z][player.y][player.x]
        if target == "k":
            player.keys += 1
            print("you found a key! You have now {} keys".format(player.keys))
            dungeon[player.z][player.y][player.x] = "." # remove the key
        
game()
        
                    
                
                        
    
    
    
    
    
    
    
