import random
import time

player = "@"
hunger = 0
gold = 0
keys = 0
hp = 100

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

level1 = """
##############################################################
#............................................................#
#.......................###############......................#
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

px = 1
py = 2
level = []
for line in level1.splitlines():
    level.append(list(line))


## --- randomize items in level ----

for y, line in enumerate(level):
    for x, char in enumerate(line):
        if char == "." and random.random() < 0.05:
            level[y][x] = random.choice(("b","$","$","$"))

### ----- place one single casino -----
while True:
    x = random.randint(1, len(level[1])-2)
    y = random.randint(1, len(level) - 2)
    if level[y][x] == ".":
        level[y][x] = "R"
        break
        
        
        
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
        if answer == a * b:
            break
        else:
            print("Falsche Antwort...Du verlierst einen Hitpoint")
            return -1, 0
    endtime = time.time()
    print("Bravo! {}".format(endtime-starttime))
    if endtime < 1:
        return 3, -10
    elif endtime < 2:
        return 2, -9
    elif endtime < 3:
        return 1, -7
    elif endtime < 4:
        return 0, -6
    elif endtime < 5:
        return 0, -5
    else:
        return 0, -1
    
    
            
def gamble():
    print("----------------------------------------------")
    print("------- Willkommen im Dungeon-Casiono --------")
    print("----------------------------------------------")
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
            gewinn = [20, 10, 5, 4, 3, 2, 1, 0 , 0, 0]
            return gewinn[i]
        print("{} es wäre {} gewesen....".format("ha"*(i+2), secret))
    print("Game Over")        
    return 0


# ------- Grafik engine ------
while hp > 0:
    for y, line in enumerate(level):
        for x, char in enumerate(line):
            if x == px and y == py:
                print(player, end="")
            else:
                if char == ":":
                    print(".", end="")
                else:
                    print(char, end="")
        print()
    # ---- control ----
    command = input("hp: {} gold: {} hunger: {} keys: {} wasd>>>".format(
                    hp, gold, hunger, keys))
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
        hp -= 1
        dx, dy = 0, 0
    
    # ------ mathemonster check ----
    if target == "M":
        dx, dy = 0, 0
        dhp, dhunger = mathquiz()
        hp += dhp
        hunger += dhunger
    
    # ------ casino check ----
    if target == "R":
        dx, dy = 0, 0
        if gold == 0:
            print("Du bist zu arm um im Casino zu spielen.")
        else:
            a = input("Magst Du um 1 Goldstück im Casino spielen?")
            if a.lower() in ("ja", "j", "yes", "y", "ok"):
                gold -= 1
                gold += gamble()
            else:
                print("na gut, dann nicht")
        
    # ----- door check -----
    if target == "D":
        if keys == 0:
            print("Aua. die Türe ist hart")
            dx, dy = 0, 0
            hp -= 1
        else:
            print("Ich verwende einen Schlüssel um die Türe zu öffnen. Ahhahahahahahah. So schlau!")
            keys -= 1
            level[py+dy][px+dx] = "." # türe kaputt
            
            
        
    # ---- move ---
    px += dx
    py += dy
    # ----- hunger -----
    if random.random() < 0.4:   # 40% chance
        hunger += 1
    if hunger >= 100:
        hp -= 1
        print("Du verhungerst! Finde schnell Essen")
    # ---- auswertung -----
    tile = level[py][px]
    if tile == "k":
        print("hurra, ein Schlüssel, ich kann eine Türe öffnen")
        keys += 1
        level[py][px] = "."
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


# ----- end ----
print(gameoverscreen)










