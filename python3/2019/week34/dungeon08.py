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
        
class Monster():
    
    number = 0
    zoo = {}
    
    def __init__(self):
        self.number = Monster.number
        Monster.number += 1
        Monster.zoo[self.number] = self
        
        self.hitpoints = random.randint(10, 30)
        self.attack = random.randint(1,6)
        self.defense = random.randint(1,6)
        self.damage = random.randint(1,6)
        self.weapon = random.choice(("claw", "bite", "punch", "kick", "horn"))
        self.armor = random.choice(("fur", "scales", "mane", "shell", "hide"))
        self.color = random.choice(("brown", "black", "pink", "red", "white", "grey", "green", "blue"))
        self.legs = random.choice((2,2,2,4,4,4,4,4,8,8,0,0,100))
        self.arms = random.choice((2,2,2,2,2,4,4,8,3,0,0,0,0,0))
        self.heads = random.choice((1,1,1,1,1,1,2))
        self.adj = random.choice(("horrible", "weird", "strange", "ugly", 
                                  "very ugly", "smelly", "slimy", "wild"))
        self.size = random.choice(("Tiny", "Small", "Medium", "Medium", "Large",
                                   "Gigantic", "Titanic"))
        self.movement = random.choice(("creeping", "crawling", "running", 
                                       "sneaking", "hobbling", "jumping",
                                       "flapping", "walking"))
        
        
    def describe(self):
        self.text = "{} {} {} creature with {} {}.".format(   #  {} legs, {} arms and {} heads".format(
                     self.size, self.adj, self.movement,
                     self.color, self.armor)
                     #self.legs, self.arms,
                     #self.heads)
        if self.heads != 1:
            self.text += " {} heads ".format(self.heads)
        if self.legs != 0:
            self.text += " {} legs ".format(self.legs)
        if self.arms != 0:
            self.text += " {} arms ".format(self.arms)
        print(self.text)             
        
class Player(Monster):
    
    def __init__(self):
        Monster.__init__(self)
        self.hitpoints = 50
        self.attack = 7
        self.defense = 7
        self.damage = 7
        self.weapon = "Sword"
        self.armor = "leather armor"
        #self.color = "red"
        self.legs = 2
        self.arms = 2
        self.heads = 1
        self.size = "human-sized"
        self.movement = "walking"
        
        
        
        
                
        
        
                    
        

# ------- player stats ------- 
hitpoints = 100
gold = 0
crazy = 0
princess = 0
fame = 0

while hitpoints > 0 and crazy < 100:
    print("Hitpoints: {} Crazyness: {}% Gold: {} Princesses: {} Fame: {}".format(
          hitpoints, crazy, gold, princess, fame))
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
            
        fame += 10
        print("You rescue (another) princess. Hurraaa!")
    if effect == "monster":
        Monster().describe()
        damage = random.randint(1, 15)
        print("You fight the monster, but you loose {} hp!".format(damage))
        # hitpoints = hitpoints - damage
        hitpoints -= damage 
        fame += 1
        # ----- loot ? ------
        if random.random() < 0.35:     # 0.35 = 35% chance
            loot = random.randint(1, 10)
            print("You find {} gold in the dead monster.".format(loot))
            gold += loot

    if effect == "stair":
        print("You can end the game now. Do you want to exit the dungeon?")
        if yesno():
            break
    if effect == "shop":
        if gold < 10:
            print("You find a healer, but you have not enough gold")
        else:
            print("Do you want to spend 10 gold for healing? Works almost always!")
            if yesno():
                gold -= 10
                healing = ["good", "good", "good", "good", "good", "good",
                           "good", "good", "good", "very good", "not at all",
                           "not at all", "not at all", "bad", "bad",
                           "very bad"]
                outcome = random.choice(healing)
                print("The healing process works {}".format(outcome))
                if outcome == "not at all":
                    heal = 0
                elif outcome == "bad":
                    heal = random.randint(-6, -1)
                elif outcome == "very bad":
                    heal = random.randint(-18, -12)
                elif outcome == "good":
                    heal = random.randint(1,6)
                elif outcome == "very good":
                    heal = random.randint(7, 18)
                print("your hitpoints change by {}".format(heal))
                if hitpoints > 100:
                    print("you already reached your maximum healt of 100")
                    hitpoints = 100
                hitpoints += heal
                input("press ENTER to continue")

print("Game Over")                
if fame >= 100:
    print("Victory")
                
        

