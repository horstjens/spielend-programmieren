import time
import random

def door(limit=3):
    while True:
        print("press a number between 1 and", limit)
        answer = input(">>>")
        try:
            answer = int(answer)
        except:
            print("this was not a number. Try again")
            continue
        if answer < 1 or answer > limit:
            print("between 1 and", limit,"Try again")
            continue
        return answer 

def yesno(text="press yes or no and ENTER"):
    while True:
        answer = input(text)
        answer = answer.lower()
        if answer == "yes" or answer == "y":
            return True
        if answer == "no" or answer == "n":
            return False
        print("wrong answer. Try again")
        


# ------- player stats ------- 
hitpoints = 100
gold = 0
crazy = 0
princess = 0


while True:
    print("Hitpoints: {} Crazyness: {}% Gold: {} Princesses: {}".format(
          hitpoints, crazy, gold, princess))
    rooms = []
    for i in range(random.randint(2,6)):
        rooms.append(random.choice(("monster","monster", "nothing","princess",
                                    "shop", "stair")))
    print("You see several doors. Please choose the number of the door:")
    for nr, what in enumerate(rooms):
        print(nr+1, "......", "room with", what)
    answer = door(len(rooms))
    print("You open the door. You see:", rooms[answer-1])
    # ----- event -----
    effect = rooms[answer-1]
    if effect == "princess":
        princess +=1
        print("You rescue (another) princess. Hurraaa!")
    if effect == "monster":
        damage = random.randint(1, 15)
        print("You fight the monster, but you loose {} hp!".format(damage))
    if effect == "stairs":
        print("You can end the game now. Do you want to exit the dungeon?")
        if yesno():
            break
    if effect == "shop":
        if gold<= 10:
            print("You find a shop, but you have not enough gold")
        else:
            print("Do you want to spend 10 gold for healing?")
            if yesno():
                heal = random.randint(5,15)
                print("You gain {} hitpoints".format(heal))
            
        


    

start = time.time()
print('Hello and welcome to the dungeon game')  
print("You are in a dungeon")
input("press ENTER")
print("You see a terrible strong monster. Do you want to fight?")
if yesno():
    print("Ouch! The monster kills you. Game Over")
else:
    print("Very clever....")
    input("press ENTER")

    print("You see a sack of gold. Do you want to take it?")
    if yesno():
        print("You are rich")
    else:
        print("You stay poor")
        
    input("press ENTER")
    print("You see a princess. Do you want to rescue her?")
    if yesno():
        print("The princess kisses you")
    else:
        print("You remain unkissed")
    
    input("press ENTER")
    print("You have won. Game over")
end = time.time()
print("Your time:", end - start)
