import time
import random

def create_room(maxx = 75, maxy = 20, boss=False, shop=False, stair=False):
    lines = []
    line = "#"*maxx
    line = list(line)
    lines.append(line)
    for y in range(maxy-2):
        line = "#"+"."*(maxx-2)+"#"
        line = list(line)
        lines.append(line)
    line = "#"*maxx
    line = list(line)
    lines.append(line)
    # ------ stair, boss, shop -----
    if stair:
        for i in range(500):
            x = random.randint(3, maxx-1)
            y = random.randint(2, maxy -1)
            if lines[y][x] == ".":
                lines[y][x] = "<"
                break
        else:
            print("Error: cannot place stair")
    # ------ shop -----
    if shop:
        for i in range(500):
            x = random.randint(3, maxx-1)
            y = random.randint(2, maxy -1)
            if lines[y][x] == ".":
                lines[y][x] = "S"
                break
        else:
            print("Error: cannot place shop")
    # ----random rocks ------    
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if lines[y][x] == "." and random.random() < 0.15:
                lines[y][x] = "#"
    
    return lines
 
def paint(room):
    for y, line in enumerate(room):
        for x, char in enumerate(line):
            for mo in Monster.zoo.values():
                if mo.hitpoints > 0 and mo.x==x and mo.y==y:
                    print(mo.char, end="")
                    break
            else:
                print(char, end="")
        print()
    
    
    

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
        self.x = 5
        self.y = 5
        self.char = "M"
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

class Princess(Monster):
    
    def __init__(self):
        Monster.__init__(self)
        self.hitpoints = 10
        self.x = 1
        self.y = 4
        self.char = "P"
        self.attack = 1
        self.defense = 2
        self.damage = 1
        self.weapon = "handbag"
        self.armor = "dress"
        self.legs = 2
        self.arms = 2
        self.heads = 1
        self.size = "normal"
        self.body = "human"
        self.movement = "walking"
        self.gold = 0
        self.crazy = random.randint(5, 15)
        self.eyecolor = random.choice(("green", "blue", "brown",
                                       "red", "violet"))
        self.haircolor = random.choice(("blond", "brown", "black",
                                        "white", "red"))
        self.figure = random.choice(("slim", "thick", "big", "tall",
                                     "sporty", "average"))
        self.decorations = []
        self.hairstyle = random.choice(("long", "short", "very long",
                                        "incredible long", "curly",))
        self.intelligence = random.choice((-3,-2,-2,-1,-1,-1,0,0,0,0,0,
                                            1,1,1,2,2,3,3))
        self.firstname = random.choice(("Yvonne", "Beatrix", "Caroline",
                                        "Esmeralda", "Rapunzel", "Cinderella",
                                        "Ekatharina", "Annabelle"))
        self.name = "{} #{}".format(self.firstname, self.number)
        self.mood = 5
    
    def status(self):
        print("{} mood: {} hp: {}".format(self.name, self.mood,
                                          self.hitpoints))
        
    def describe(self):
        print("{} has {} eyes, a {} figure and {} {} hair.".format(self.name,
               self.eyecolor, self.figure, self.hairstyle, self.haircolor))
    
    def groupdynamic(self):
        others = []
        for p in Monster.zoo[0].army :
            if p.number != self.number:
                others.append(p)
        # in others are now all princesses except this princess
        victim = random.choice(others)
        for x in range(10):
            ally = random.choice(others)
            if ally.number != victim.number:
                break
        else:
            ally = None
        if self.mood < 0:
            text, effect1, effect2 = random.choice((
               ("makes fun of {}".format(victim.name), -5, 1),
               ("slaps {} with her handbag...".format(victim.name), -10, -1),
               ("steal some item of {}".format(victim.name), -8, 3)
               ))
        else:
            text, effect1, effect2 = random.choice((
               ("tells a funny story about {}".format(victim.name), 3, 1),
               ("make a compliment about the look of {}".format(victim.name), 5, 0),
               ("makes a little gift for {}".format(victim.name), 5, 1)
               ))
        victim.mood += effect1
        text = text + "changing her mood by {}".format(effect1)
        if ally is not None and effect2 != 0:
            ally.mood += effect2
            text += "\n and also effecting the mood of her friend {} by {}".format(ally.name, effect2)
        print(text)
            
            
        
            
        
        
    
    def moodswing(self):
        if random.random() < self.crazy / 100:
            delta = random.randint(-self.crazy, self.crazy)
            print("{} changes her mood by {}".format(self.name, delta))
            self.mood += delta
        
    def act(self):
        if self.mood < -20:
            text, effect=random.choice((
                  ("slaps you angry", 5),
                  ("sings loud and false", 3),
                  ("start crying sensless", 2),
                  ("wants to stay here", 1),
                  ("does nothing, in a disturbing way", 1)
                  ))
        elif self.mood < -10:
            text, effect = random.choice((
                  ("sings loud and false", 2),
                  ("start crying sensless", 1),
                  ("wants to stay here", 0),
                  ("does nothing, in a disturbing way", 0),
                  ("refuse to speak with you", 1),
                  ("is sulking", 2)
                  ))
        elif self.mood < 0:
            text, effect = random.choice((
                  ("is bored", 0),
                  ("is bored in an annoying way", 1),
                  ("wants to stay here", 0),
                  ("starts to act strange", 1),
                  ("is not interested in you...at all", 1),
                  ("is sulking a bit", 1)
                  ))
        elif self.mood < 10:
            text, effect = random.choice((
                  ("sings loud and beautyful", -1),
                  ("is flirting with you", -1),
                  ("tells you a joke", -1),
                  ("does nothing, in a harmless way", 0),
                  ("wants to generally speak with you", -1),
                  ("is dancing around akward", -1)
                  ))
        else:
            text, effect = random.choice((
                  ("sings loud and very beautiful", -3),
                  ("tells you a good joke", -2),
                  ("is excited about this adventure", -2),
                  ("creates a tasty meal for you", -1),
                  ("dances around, beautiful", -3),
                  ("is chatting about flowers", -2)
                  ))
        return text, effect
        
        
                
            

        
class Player(Monster):
    
    def __init__(self):
        Monster.__init__(self)
        self.hitpoints = 50
        self.x = 2
        self.y = 2
        self.char = "@"
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
        #self.princess = 0
        self.army = []
        self.fame = 0
        
    def status(self):
        print("YOUR Hitpoints: {} Crazyness: {}% Gold: {}  Fame: {}".format(
               self.hitpoints, self.crazy, self.gold, 
               self.fame))
        
        
def game():
    # ------- player stats ------- 
    hero = Player()
    print("Welcome, young hero. You look fantastic today:")
    hero.describe()
    # ------- main loop --------
    while hero.hitpoints > 0 and hero.crazy < 100:
        print("You and your army:")
        for p in hero.army:
            p.moodswing()
            p.status()
        hero.status()
        input("press ENTER")
        if len(hero.army) > 0:
            print("your army starts acting:")
            for p in hero.army:
                if len(hero.army) > 2 and random.random() < p.crazy:
                    p.groupdynamic()
                text, delta = p.act()
                if   delta < 0:
                    text2 = "cooling you down (crazy {})".format(delta)
                elif delta > 0:
                    text2 = "driving you more crazy (+{})".format(delta)
                else:
                    text2 = "not affecting your crazyness"
                hero.crazy += delta
                print(p.name, text+",", text2)
            hero.status()
            input("press  ENTER")
                
                    
        
        
        rooms = []
        for i in range(random.randint(2,6)):
            rooms.append(random.choice(("monster","monster", "nothing","princess",
                                        "shop", "stair")))
        print("You see several doors. Please choose the number of the door:")
        for nr, what in enumerate(rooms):
            print(nr+1, "......", "room with", what)
        answer = door(len(rooms))
        print("You open the door to ", rooms[answer-1])
        # ------ graphic ------
        effect = rooms[answer-1]
        if effect == "stair":
            lines = create_room(stair=True)
        elif effect == "shop":
            lines = create_room(shop=True)
        else:
            lines = create_room()
        # ------- control --------
        while hero.x < 75:
            paint(lines)
            command = input("direction? wasd >>>")
            dx, dy = 0, 0
            if command == "w":
                dy = -1
            if command == "s":
                dy = 1
            if command == "a":
                dx = -1
            if command == "d":
                dx = 1
            # ------ rock test ----
            target = lines[hero.y+dy][hero.x+dx]
            if target == "#":
                # ---- rock ----
                
                print("Ouchhhhh! the rock is hard")
                hero.hitpoints -= 1
                if random.random() < 0.2:
                    print("The rock is destroyed!")
                    lines[hero.y+dy][hero.x+dx] = "."
                else:
                    print("The rock is damaged, but still there")
                dx, dy = 0, 0
                input("press ENTER")
            
            
            hero.x += dx
            hero.y += dy
        hero.x = 1
                
        
        # ----- event -----
       
        if effect == "princess":
            #hero.princess += 1
            hero.army.append(Princess())
            hero.fame += 10
            print("You rescue (another) princess. Hurraaa!")
            hero.army[-1].describe()
            input("press ENTER")
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
            if hero.fame >= 100:
                print("You can end the game now. Do you want to exit the dungeon?")
                if yesno():
                    break
            else:
                print("you need 100 fame or more to exit the dungeon")
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

                  
    if hero.fame >= 100:
        print("Victory")
    else:
        print("Game Over")  
                    
            
if __name__ == "__main__":
    game()









