import random

adj = ["schön", "großartig", "wunderbar", "fantastisch", "gut" ]
adj2 = ["äußerst", "sehr", "etwas", "unglaublich", "einmalig"]


while True:
    a = random.choice(adj)
    b = random.choice(adj2)
    print("Ich wünsche einen {} {}en Morgen".format(b, a))
    x = input(">>>")
    if x == "ende":
        break
print("oh, Schade, ich hätte noch lange weitergemacht")

    
