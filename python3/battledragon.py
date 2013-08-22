#!/usr/bin/env python
"""battledragon

a simple text game to learn the basics of pyhton (game) programming. 
For mor information, see https://github.com/horstjens/spielend-programmieren
Uses python3
gpl licensed, see http://www.gnu.org/licenses/gpl.html
"""

import random

# http://stackoverflow.com/questions/1523427/python-what-is-the-common-header-format

__author__ = "Horst JENS" 
__copyright__ = "Copyright 2013, Horst JENS"
__credits__ = ["Horst JENS"]
__license__ = "GPL"  # see http://www.gnu.org/licenses/gpl.html'
__version__ = "0.1"
__maintainer__ = "Horst JENS"
__email__ = "horstjens@gmail.com"
__status__ = "Development" # "Prototype", "Development", or "Production"


    
class Monster(object):
    """generic monster in game"""
    #class variables
    number = 0 
    dm = {} # damage modifier matrix. zero means no damage, 1 means full damage
    dm["breath"] = {"shield":0,  "evading":0.5, "hiding":1, "drink potion":2}
    dm["bite"]   = {"shield":1,  "evading":0, "hiding":0.5, "drink potion":2}
    dm["talon"]  = {"shield":0.5,"evading":1, "hiding":0, "drink potion":2}
    dm["stun"]   = {"evading":0.1, "block": 0.3 }
    dm["sword"]  = {"evading":0.6, "block": 0.9 }

    
    #methods
    
    def __init__(self, name="unknown monster", **kwargs):
        """parent Monster class"""
        self.name = name
        self.hitpoints = random.randint(3,18)
        #self.attack = random.randint(2, 12)
        #self.defense = random.randint(2,12)
        self.mindamage = random.randint(1,6)
        self.maxdamage = random.randint(1,6) + 6 + self.mindamage
        self.criticalhit = random.random() * 0.2 # 20% or less
        self.criticalfail = random.random() * 0.05 # 5% or less
        self.attacks = []
        self.defenses = []
        self.stunned = 0 # how many rounds stunned
        self.ai = False # ai controlled
        # overwrite attributes with keyword-arguments
        for key in kwargs:
            self.__setattr__(key, kwargs[key])
        
    def __repr__(self):
        """the output when this instance object is printed"""
        return "{} hp:{:.1f} stunned: {}".format(self.name, self.hitpoints,
            self.stunned)
            
class Dragon(Monster):
    def __init__(self, name="Dagobert", **kwargs):
        Monster.__init__(self, name, **kwargs) # call __init__ of parent
        self.hitpoints = 100 + random.randint(-10,10)
        self.defenses=["block", "evading"]
        self.attacks=["breath","talon", "bite"]
        self.ai = True # dragon is computer controlled
        self.mindamage = random.randint(6,12)
        for key in kwargs:
            self.__setattr__(key, kwargs[key])
        
class Knight(Monster):
    def __init__(self, name="Alf", **kwargs):
        Monster.__init__(self, name, **kwargs)
        self.hitpoints = 30 + random.randint(-5,5)
        self.potions = random.randint(3,7)
        self.attacks = ["sword","stun"]
        self.defenses=["shield", "evading", "hiding", "drink potion"]
        self.criticalstun = 0.4 # 40 %
        self.ai = False # kight is player controlled
        for key in kwargs:
            self.__setattr__(key, kwargs[key])
            
    def drink_potion(self):
        text = ["potion:"] # list of text, must return more than one line
        if self.stunned > 0:
            text.append("{} is stunned and can not drink potions".format(self.name))
            return text
        if self.potions <= 0:
            text.append("Sadly, {} has no more potions left to drink".format(self.name))
            return text
        gain = random.randint(10,20)
        text.append("{} drinks a healt potion".format(self.name))
        text.append("and gains {} hitpoints".format(gain))
        self.hitpoints += gain
        self.potions -= 1
        return text    
    
    def stun(self, victim):
        """effect of stun attack for attacker and victim"""
        text=["stun attack:"] # must return more than one line of text !
        if self.stunned > 0:
            text.append("{} can not stun because he is stunned himself".format(attacker.name))
        if victim.stunned >0:
            text.append("{} was already stunned and is now even more stunned".format(victim.name))
            victim.stunned += random.randint(2,6)
        success = random.random()
        if success < self.criticalstun:
            text.append("{} successfully stunned his victim ({:.2f} < {:.2f}) !".format(
                self.name, success, self.criticalstun))
            victim.stunned += random.randint(2,3)
        else:
            text.append("stun action failed ({:.2f} >= {:.2f})".format(success, self.criticalstun))
        return text
                
    def __repr__(self):
        """overwrite __repr__ because only kinght has potions"""
        return "{} hp:{:.1f} stunned: {} potions: {}".format(self.name, self.hitpoints,
            self.stunned, self.potions)
        
def integer_input( min_value=0, max_value=999, default=0, 
                   prompt="please type number and press ENTER"):
     """ask user for integer value beween min_value and max_value"""
     while True:
         raw = input(prompt)
         if not raw.isdigit():
             print("please enter a number")
             continue
         raw = int(raw)
         if min_value <= raw <= max_value:
            return raw
         print("please enter value between {} and {}".format(min_value,
            max_value))
            
def show_menu(menulist):
    """display menu, first point is always Cancel"""
    text = "0 ... Cancel\n"
    for item in menulist:
        text += "{} ... {}\n".format(menulist.index(item)+1, item)
    return text
        

def strike(attacker, defender):
    """attacker strikes against defender"""
    #print("----------------------------------")
    #print("{} attacks {}".format(attacker.name, defender.name))
    #print("----------------------------------")      
    if attacker.ai:
        attack = random.choice(attacker.attacks)
    else:
        print(show_menu(attacker.attacks))
        playeraction = integer_input(prompt="please select attack for {}".format(attacker.name),
            min_value = 0, max_value = len(attacker.attacks))
        if playeraction == 0:
            return None # user cancel
        attack = attacker.attacks[playeraction-1]
    if defender.ai:
        defense = random.choice(defender.defenses)
    else:
        print(show_menu(defender.defenses))
        playeraction = integer_input(prompt="please select defense for {}".format(defender.name),
            min_value = 0, max_value = len(defender.defenses))
        if playeraction == 0:
            return None # user cancel
        defense = defender.defenses[playeraction - 1]
    # damage calculation
    text = ["---------"] # list of text lines
    if attacker.stunned > 0:
        text.append("{} is still stunned and can not attack!".format(attacker.name))
        damage = 0
    else:
        text.append("{} attack with {}, {} defends by {}".format(attacker.name,
            attack, defender.name, defense))
        success = random.random()   # between 0.0 and 1.0
        raw_damage = random.randint(attacker.mindamage, attacker.maxdamage)
        # damage modifier matrix
        mod = Monster.dm[attack][defense]
        damage = raw_damage * mod
        text.append("raw damage: {} * modifier {:.1f} = damage: {:.2f}".format(
            raw_damage, mod, damage))
        if defender.stunned > 0:
            text.append("{} is still stunned and can not defend itself.".format(defender.name))
            text.append("Automatic double damage, ignoring defense !".format(defender.name))
            damage = raw_damage * 2 
        elif success < attacker.criticalfail:
            text.append("critical fail! ({:.2f} < {:.2f}) No damage".format(
                success, attacker.criticalfail))
            damage = 0
        elif mod >0:
            #new sucess chance for critical hit !
            success = random.random() 
            if success  < attacker.criticalhit:
                text.append("critical hit! ({:.2f} < {:.2f}) Triple damage !".format(
                    success, attacker.criticalhit))
                damage *= 3
    text.append("{} causes {:.2f} points of damage".format(attacker.name,
        damage))
    defender.hitpoints -= damage  
    text.append("{} has {:.1f} hitpoints left".format(defender.name, 
        defender.hitpoints))
    # -------------- special actions -------------
    # potion ?
    if defense == "drink potion":
        text.extend(defender.drink_potion()) # extend by more than one line
    # stun ?
    if attack == "stun":
        text.extend(attacker.stun(defender))
    if defender.hitpoints < 0:
        text.append("\nvictory for {}!".format(attacker.name))
    return text
    
    
def game(a,b, ):
    """player fight vs dragon"""
    attacker, defender = a, b
    combatround = 0
    while a.hitpoints > 0 and b.hitpoints > 0:
        combatround += 1 # increase combatround by 1
        if a.stunned > 0:
            a.stunned -= 1
        if b.stunned > 0:
            b.stunned -= 1
        print()
        print("=================================")
        print("combat round nr:", combatround)
        print("attacker:", attacker)
        print("defender:", defender)
        print("=================================")
        result = strike(attacker,defender)
        if result == None:
            break
        for line in result:
            print(line)
        if attacker == a and defender ==b:
            attacker, defender = b, a
        else:
            attacker, defender = a, b

    # game over    
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    if a.hitpoints > b.hitpoints:
        victor = a.name
    elif b.hitpoints > a.hitpoints :
        victor = b.name
    else:
        print("it is a draw")
        victor = None
    print("victor:", victor)
    
    
        
def main():
    human = Knight("Sir Arthur")
    # let the computer play the Knight by calling human=Knight("Robot", ai=True)
    dragon = Dragon("Puff the magic dragon")
    # play the dragon yourself by calling dragon=Dragon("me", ai=False)
    game(human, dragon)
    
if __name__ == "__main__":
    main()
