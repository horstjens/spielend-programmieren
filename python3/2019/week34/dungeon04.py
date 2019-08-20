import time

def yesno(text="press yes or no and ENTER"):
    while True:
        answer = input(text)
        answer = answer.lower()
        if answer == "yes" or answer == "y":
            return True
        if answer == "no" or answer == "n":
            return False
        print("wrong answer. Try again")
        
    

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
