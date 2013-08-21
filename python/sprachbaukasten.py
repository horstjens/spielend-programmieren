import random
verben=["isst","prügelt sich mit","schaut fern mit","haut", "lernt mit",
    "schreibt ab von", "liebt", "bestiehlt", "spielt mit", "ärgert", "küsst",
        "bekämpft","verzaubert"]
objekte=["Haus","Auto","Flugzeug","Schiff"] # muss sächlich sein
wiesehr=["gar nicht","ein wenig","etwas","ziemlich",
         "sehr", "viel", "zu viel"]
grundwort=["ohne","und denkt dabei an","trotz","wegen"]
wowort =["in","neben","unter","auf"]
zeitwort = ["Eines Tages", "Danach", "Zuerst", "Morgen", "Nächstes Jahr",
            "Aus heiterem Himmel"]
for x in range(5):
    zeit = random.choice(zeitwort)
    leute=["Horst","Michi","Claudia","Doris"]    
    subj = random.choice(leute)
    verb = random.choice(verben)
    leute.remove(subj)
    subj2 = random.choice(leute)
    leute.remove(subj2)
    subj3 = random.choice(leute)
    obj = random.choice(objekte)
    wie = random.choice(wiesehr)
    grund = random.choice(grundwort)
    wo = random.choice(wowort)
    print(zeit, verb, subj, subj2, wo, "einem", obj, grund, subj3)

