import time
import random

def fight(a, d):
    battleround = 0
    while a.hitpoints > 0 and d.hitpoints > 0:
        battleround += 1
        print("----======= round {} =======-----".format(battleround))
        strike(a, d)
        if d.hitpoints > 0:
            strike(d, a)
        print("Do you want to continue to fight (y) or flee (n) ?")
        if not yesno():
            return

def strike(a, d):
    print("{} ({} hp) strikes vs. {} ({} hp)".format(
            a.__class__.__name__, a.hitpoints, 
            d.__class__.__name__, d.hitpoints))
    print("attack: {} + 2d6 vs. defense: {} + 2d6".format(a.attack, d.defense))
    w1 = random.randint(1,6)
    w2 = random.randint(1,6)
    w3 = random.randint(1,6)
    w4 = random.randint(1,6)
    print("attack: {}+{}+{} = {} vs. defense: {}+{}+{}= {}".format(a.attack, w1, w2,
          a.attack+w1+w2, d.defense, w3, w4, d.defense + w3+ w4))
    if a.attack + w1 + w2 < d.defense + w3 + w4:
        print("{} fails to penetrate the {} of {}. No damage!".format(
              a.__class__.__name__, d.armor, d.__class__.__name__))
        return
    w5 = random.randint(1,6)
    print("{} hit {} with his {} and inflicts {} damage ({}+d6)".format(
          a.__class__.__name__, d.__class__.__name__, a.weapon,
          w5+a.damage, a.damage))
    d.hitpoints -= (w5+a.damage)
    

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
        self.body = random.choice(("creature", "bird", "lizard", 
                                   "spider", "mammal", "insect",
                                   "snake", "slime-blob", "snail",
                                   "worm"))
        
        self.adj = random.choice(("horrible", "weird", "strange", "ugly", 
                                  "very ugly", "smelly", "slimy", "wild"))
        self.size = random.choice(("Tiny", "Small", "Medium", "Medium", "Large",
                                   "Gigantic", "Titanic"))
        self.movement = random.choice(("creeping", "crawling", "running", 
                                       "sneaking", "hobbling", "jumping",
                                       "flapping", "walking"))
        
        
    def describe(self):
        self.text = "{} {} {} {} with {} {}.".format(   #  {} legs, {} arms and {} heads".format(
                     self.size, self.adj, self.movement,
                     self.body, self.color, self.armor)
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
        self.attack = 4
        self.defense = 4
        self.damage = 4
        self.weapon = "Sword"
        self.armor = "leather armor"
        #self.color = "red"
        self.legs = 2
        self.arms = 2
        self.heads = 1
        self.size = "normal"
        self.body = "human"
        self.movement = "walking"
        self.gold = 0
        self.crazy = 0
        self.princess = 0
        self.fame = 0
        
    def status(self):
        print("Hitpoints: {} Crazyness: {}% Gold: {} Princesses: {} Fame: {}".format(
               self.hitpoints, self.crazy, self.gold, 
               self.princess, self.fame))
        
        

# ------- player stats ------- 
hero = Player()
print("Welcome, young hero. You look fantastic today:")
hero.describe()

while hero.hitpoints > 0 and hero.crazy < 100:
    hero.status()
    rooms = []
    for i in range(random.randint(2,6)):
        rooms.append(random.choice(("monster","monster", "nothing","princess",
                                    "shop", "stair")))
    print("You see several doors. Please choose the number of the door:")
    for nr, what in enumerate(rooms):
        print(nr+1, "......", "room with", what)
    answer = door(len(rooms))
    print("You open the door to ", rooms[answer-1])
    # ----- event -----
    effect = rooms[answer-1]
    if effect == "princess":
        hero.princess += 1
        hero.fame += 10
        print("You rescue (another) princess. Hurraaa!")
    if effect == "monster":
        print("You see a monster!")
        mo = Monster()
        mo.describe()
        fight(hero, mo)
        if mo.hitpoints > 0:
            # ---- monster alive ---
            if hero.hitpoints <= 0:
                # --- player dead ---
                print("You are killed")
                break
            # ----- player flees ? --------
            print("You flee like a coward")
            damage = random.randint(1,10)
            print("While you flee, the monster strikes you!")
            print("You loose {} hp".format(damage))
            hero.hitpoints -= damage
            hero.fame -= mo.hitpoints
            hero.gold = int(hero.gold / 2)
            print("You loose fame and gold")
        else:
            # ------ victory ------                 
            hero.fame += 1
            print("*** ---- **** ---- **** ---- **** ---- ****")
            print("You become more famous after this victory!")
            print("*** ---- **** ---- **** ---- **** ---- ****")
            # ----- loot ? ------
            if random.random() < 0.8:     # 0.35 = 35% chance
                loot = random.randint(1, 10)
                print("You find {} gold at the dead monster.".format(loot))
                hero.gold += loot
            else:
                print("You find no gold at the dead monster....")

    if effect == "stair":
        print("You can end the game now. Do you want to exit the dungeon?")
        if yesno():
            break
    if effect == "shop":
        if hero.gold < 10:
            print("You find a healer, but you have not enough gold")
        else:
            print("Do you want to spend 10 gold for healing? Works almost always!")
            if yesno():
                hero.gold -= 10
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
                hero.hitpoints += heal
                if hero.hitpoints > 100:
                    print("you already reached your maximum healt of 100")
                    hero.hitpoints = 100
                
                input("press ENTER to continue")

print("Game Over")                
if hero.fame >= 100:
    print("Victory")
                
        

