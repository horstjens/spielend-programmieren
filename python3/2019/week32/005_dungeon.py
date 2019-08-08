import random

player = "@"
hunger = 0
gold = 0

level1 = """
##############################################################
#............................................................#
#............................................................#
#............................................................#
#............................................................#
#............................................................#
##############################################################"""

px = 0
py = 2
level = []
for line in level1.splitlines():
    level.append(list(line))


## --- randomize items in level ----

for y, line in enumerate(level):
    for x, char in enumerate(line):
        if char == "." and random.random() < 0.2:
            level[y][x] = random.choice(("b","$","T","$","$"))
            

while True:
    for y, line in enumerate(level):
        for x, char in enumerate(line):
            if x == px and y == py:
                print(player, end="")
            else:
                print(char, end="")
        print()
    # ---- control ----
    command = input("wasd? gold: {} hunger: {} >>>".format(
                    gold, hunger))
    # ---- parsing command ----
    if command in ["end", "exit", "quit", "bye"]:
        break
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
    # ------ wall check -----
    target = level[py+dy][px+dx]
    if target == "#":
        print("ouch! a wall")
        dx, dy = 0, 0
    # ---- move ---
    px += dx
    py += dy
    # ----- hunger -----
    if random.random() < 0.4:   # 40% chance
        hunger += 1
    # ---- auswertung -----
    tile = level[py][px]
    if tile == "b":
        print("mmmm, lecker, eine Banane")
        hunger -= 1        ############
        level[py][px] = "."  
    if tile == "$":
        print("hurra, Geld")
        gold += 1
        level[py][px] = "."  
    if tile == "t":
        level[py][px] = "x"  
        print("Schon wieder ein widerlicher Tisch. Du verwandelst ihn in Brennholz")











