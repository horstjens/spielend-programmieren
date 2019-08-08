import random

while True:
    a = random.randint(1,10)
    print("hahaha, du erratest nie meine Zahl (1-10)")
    x = input(">>>")
    if x == "ende":
        break
    try:
        x = int(x)
    except:
        print("das war nicht einmal eine Zahl")
        continue
    # ---- Auswertung ---
    if x == a:
        print("Wahnsinn! Du hast die Zahl erraten!")
        break
    print("Tja, schade.... es wäre {} gewesen".format(a))
print("Game Over")
    
