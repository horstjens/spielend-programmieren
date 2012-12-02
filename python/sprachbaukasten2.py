import random
# verb + präp
verben=[("beisst",""),("prügelt sich", "mit"),("schaut", "fern mit"),("haut",""),
        ("lernt", "mit"), ("schreibt", "ab von"), ("liebt",""),
        ("bestiehlt",""),("spielt","mit"), ("ärgert",""), ("küsst","")]
nomen=["Haus","Auto","Flugzeug","Schiff","Bagger","BMW"]
                                       # muss sächlich oder männlihc sein
mengenangabe=["gar nicht","ein wenig","etwas","ziemlich",
         "sehr", "viel", "zu viel","heftigst","leidentschaftlich","halbherzig"]
grundwort=["ohne","und denkt dabei an","trotz","wegen","aufgrund von",
           "sich schämend wegen", "aus Rache für"]
ortsangabe =["in","neben","unter","auf"]#präp und fall 3?
zeitangabe = ["Eines Tages", "Danach", "Zuerst", "Morgen", "Nächstes Jahr",
            "Aus heiterem Himmel"]
for x in range(5):
    zeit = random.choice(zeitangabe)
    leute=["Horst","Michi","Claudia","Doris","Manfred","Bettina","Joe"]    
    subj = random.choice(leute)
    verb = random.choice(verben)
    leute.remove(subj)
    subj2 = random.choice(leute)
    leute.remove(subj2)
    subj3 = random.choice(leute)
    obj = random.choice(nomen)
    wie = random.choice(mengenangabe)
    grund = random.choice(grundwort)
    wo = random.choice(ortsangabe)
    print(zeit, verb[0], subj, wie, verb[1], subj2, wo, "einem", obj, grund, subj3)

