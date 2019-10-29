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
#.....................W...........................#
#.................................#####...........#
#...#.............................#...D...........#
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
        self.char = "M"
        self.hitpoints = 100
        self.overwrite_parameters()
        
    def overwrite_parameters(self):
        pass

class Door(Monster):
    
    def overwrite_parameters(self):
        self.hitpoints = 15
        self.char = "D"
    
        
class Hero(Monster):
    
    def overwrite_parameters(self):
        self.hitpoints = 500
        self.char = "@"
        
class Wolf(Monster):
    
    def overwrite_parameters(self):
        self.hitpoints = 200
        self.char = "W"
    
    
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
        status = "hitpoints: {} x:{} y:{} z:{}".format(player.hitpoints,
                  player.x, player.y, player.z)
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
        else:
            player.x += dx
            player.y += dy
        
game()
        
                    
                
                        
    
    
    
    
    
    
    
