import random

player = "@"

level1 = """
##############################################################
..............................................................
.................................bbbbbbb......................
.............a..........................b.$.........b.........
.....................e....................b.b.......b.........
.....................................c.......b.b.b.b..........
##############################################################"""

px = 0
py = 2
level = []
for line in level1.splitlines():
    level.append(list(line))

while True:
    for y, line in enumerate(level):
        for x, char in enumerate(line):
            if x == px and y == py:
                print(player, end="")
            else:
                print(char, end="")
        print()
    # ---- control ----
    command = input("wasd?>>>")
    if command == "w":
        py -= 1
    if command == "s":
        py += 1
    if command == "a":
        px -= 1
    if command == "d":
        px += 1




