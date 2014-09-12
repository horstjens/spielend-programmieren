import easygui as e
import random
kekse=10
angst=20
raum=-1
tiucsibhp=30
t500="""Welcome to The Biscuit Quest!"""
t1="""You are in a cursed temple in a deep jungle.While nibbling your biscuit,you head to the evil castle of tiucsib,
who wants to end the biscuits very existence!You see a sleeping (evil) guard."""
t2="""A raveging hoard of evil warriors notices you,and are planning to make you their breakfast."""
t3="""You take the pass of NOTbiscuitness,and a hazard awiated you."""
t4="""You wander on until you see two doors."""
t5="""You see a dusty chest,a intact minecart and a pile of dust.The rails are a bit unstable,but they should work."""
t6="""You see a smartphone zombie and he looks scary"""
t7="""A turned off Cyborferris awaits you."""
t8="""You see a crack of light..."""
buttons=["Play","Tutorial"]
buttons1=["Menu","Punch","Spit","Let Rip","Throw a biscuit"]
buttons2=["Run","Fight","shoot 'em","Act crazy"]
buttons3=["Jump","Walk","Biscuit","Swim"]
buttons4=["Door1","Door2","Go on"]
buttons5=["Chest","Minecart","Walk"]
buttons6=["Sword","Punch","Biscuit","Run off"]
buttons7=["Kick","Go","*___*"]
buttons8=["Go outa here","Go back"]



while raum==-1:
    a0=e.buttonbox(t500,"Welcome!",buttons,"temple.gif")
    if a0=="Play":
        raum=1
        t0="Welcome!"
    elif a0=="Tutorial":
        t0="Up here  |  are your biscuits(life energy), it also tells you in wich room you are.\nBelow the image that will appear in every level, are your options.\nSelect an option with left mouse click."
    e.msgbox(t0)  

while kekse >0:
          
    while raum==1 and kekse>0:
        a1=e.buttonbox(t1,"room:{},biscuits:{},scaredness:{}".format(raum,kekse,angst),buttons1,"temple.gif")
        if a1=="Punch":
            t0="You punch the guard.He wakes up and kills you."
            kekse=0
        elif a1=="Spit":
            t0="The Guard continues to sleep."
        elif a1=="Let Rip":
            t0="The guard dies due to an really eggy fart."
            raum=2    
        elif a1=="Throw a biscuit":
            t0="The ultimate power of biscuit unleashes and kills the guard."
            kekse-=1
            raum=2
        e.msgbox(t0)
    while raum==2 and kekse>0:
        a2=e.buttonbox(t2,"room:{},biscuits{},scaredness:{}".format(raum,kekse,angst),buttons2,"warriors.gif")
        if a2=="Run":
            t0="You trip over a stone and the warriors kill you."
            kekse=0
        elif a2=="Fight":
            t0="You fight of the hoard,but take damage."
            raum=3
            kekse-=3
            angst-=1    
        elif a2=="shoot 'em":
            t0="You shoot down the warriors,and your bow snaps."
            raum=3
            angst-=1
        elif a2=="Act crazy":    
            t0="You escape,but got sniped."
            raum=3
            kekse-=5
        e.msgbox(t0)
    while raum==3 and kekse>0:
         a3=e.buttonbox(t3,"Room:{},Biscuits:{},Scaredness:{}".format(raum,kekse,angst),buttons3,"acid.gif")
         if a3=="Jump":
             t0="You narrowly got over the acid"
             raum=4
             kekse-=2
         elif a3=="Walk":
             t0="Are you totally bonkers?Just walking into acid as if it were nothin'?Anyway you died."
             kekse=0
         elif a3=="Biscuit":
             t0="You throw a biscuit of awesomeness,\nwich then swells up to a raft.\nYou epically travel over the acid."          
             kekse-=1
             raum=4
         elif a3=="Swim":
             t0="So the only thing you came up with was to swim through the acid.\nThat's what you did."
             kekse-=5
             raum=4
         e.msgbox(t0)        
    while raum==4 and kekse>0:
        a4=e.buttonbox(t4,"Room:{},Biscuits:{},Scaredness:{}".format(raum,kekse,angst),buttons4,"doors.gif")
        if a4=="Door1":
            t0="You land in an ole' mineshaft,with lots of dust and debris."
            raum=5
        elif a4=="Door2":
            t0="You stumble into an old cave,full of bones and creepy crawlees."
            kekse-=1
            raum=8       #------------------------------------------room 8=cave-------------------!!!!!!!!!!!!!!
        elif a4=="Go on":
            t0="You go on,and soon got lost.Were you here before?!"
            raum=2
        e.msgbox(t0)
    while raum==5 and kekse>0:
        a5=e.buttonbox(t5,"Room:{},Biscuits:{},Scaredness{}".format(raum,kekse,angst),buttons5,"mineshaft.gif")
        if a5=="Chest":
            t0="You open the chest and find a biscuit!"
            kekse+=1
            buttons5.remove("Chest")
        elif a5=="Minecart":
            t0="You experience an awesome minecart ride!"
            raum=7
        elif a5=="Walk":
            t0="You walk further on."
            raum=6
        e.msgbox(t0)
    while raum==6 and kekse>0:
        a6=e.buttonbox(t6,"Room:{},Biscuits:{},Scaredness{}".format(raum,kekse,angst),buttons6,"smartphonezombie.gif")
        if a6=="Sword":
            t0="You slay the evil Smartphone zombie!"
            raum=7
        elif a6=="Punch":
            t0="You punch the Smartphone zombie to death.(Even though he already is dead.)"
            raum=7
            kekse-=1
        elif a6=="Run off":
            t0="You are so shy and run off"
            raum=7
            angst-=5
        elif a6=="Biscuit":
            t0="The awsome power of biscuit unleashes, and lets the guard vanish.\n***You got a smartphone***"
            raum=7
            kekse-=1
        e.msgbox(t0)
    while raum==7 and kekse>0:  
        a7=e.buttonbox(t7,"Room:{},Biscuits:{},Scaredness{}".format(raum,kekse,
                        angst),buttons7,"cyborferris.gif")
        if a7=="Kick":
            t0="You kicked the Cyborferris in the private parts"
        elif a7=="Go":
            t0="You go on, and reach the end of the mineshaft."
            raum=8
        elif a7=="*___*":
            kekse+=3
            t0="Zd65676g78fdsfu8feh87e9zwfsg8erzjoig9rz9ehgghg88fjw90aj5jaeru_____________________!"
            raum=5    
        e.msgbox(t0)
        #Warning,stuff is mixed up down 'ere    
    while raum==8 and kekse>0:
        a9=e.buttonbox("You landed in a dim dank cave","Room:{},Biscuits:{},Scaredness:{}".format(raum,
                    kekse,angst),["Chest","Wander","Biscuit"],"monsterchest.gif")
        if a9=="Chest":
            kekse-=5
            t0="The chest tries to eat you up."
        elif a9=="Wander":
            raum=9
            t0="You wander on"
        elif a9=="Biscuit":
            kekse-=1
            raum=10
            t0="You travel with a biscuit through the cave."
        e.msgbox(t0)                             
    while raum==9 and kekse>0:
        a8=e.buttonbox(t8,"Room:{},Biscuits:{},Scaredness:{}".format(raum,
                        kekse,angst),buttons8,"crack.gif")
        if a8=="Go outa here":
            t0="You get outa here"
            raum=10
        elif a8=="Go back":
            t0="You go back"
            raum=7   
        e.msgbox(t0)
    #_______________________________________________________________________
    while raum==10 and kekse>0:
        a10=e.buttonbox("You see the castle of tiucsib in the horizon","Room:{},Biscuits:{},Scaredness:{}".format(raum,
                        kekse,angst),["Take a nice walk to the castle of tiucsib","Fly a Flyingbiscuitswine","Point your butt at the castle of tiucsib"],"lookout.gif")
        if a10=="Take a nice walk to the castle of tiucsib":
            raum=11
            t0="The Flyingbiscuitswines are sad..."
        elif a10=="Fly a Flyingbiscuitswine":
            raum=13
            t0="The Flyingbiscuitswines are happy to help you"
        else:
            t0="You point your butt at the castle of tiucsib"                        
    while raum==11 and kekse>0:
        a11=e.buttonbox("On the path to the castle you see Officer.Leutennant.Supervegetablesoupman,\nhe is throughing vitamins at you!Nnnnnnnoooooooooo!","Room:{},Biscuits:{}".format(raum,
        kekse,angst),["Biscuit","Battle","Flee"],"carrot.gif")
        if a11=="Biscuit":
            raum=12
            kekse-=2
            t0="The high-calorie biscuit power destroys the healthines of the vitamins"
        elif a11=="Battle":
            kekse-=3
            raum=12
            t0="An epic battle unleshes and you trounce the Veggiesoupman.You lost 3 Biscuits"        
        elif a11=="Flee":
            remove("Flee")
            raum=10
            t0="You Flee"
        e.msgbox(t0)
    while raum==12 and kekse>0:
        a12=e.buttonbox("You are on the drawbridge of the castle.It seems like you're not  welcome...","Room:{},Biscuit:{}".format(raum,
        kekse),["Call for help","Take 'em on!","Poop in your pants","Biscuit"],"bridge.gif")
        if a12=="Call for help":
            raum=13
            t0="The Flyingbuscuitswines hear your call,and take on the hoard."
        elif a12=="Take 'em on!":
            raum=13
            kekse-=4
            t0="You take on the hoard,but lose 4 Biscuits."
        elif a12=="Poop in your pants":
            t0="You poop in your pants.The smell is abnonxious."
        e.msgbox(t0)
    while raum==13 and kekse>0:
        a13=e.buttonbox("Well...Duh.","Room:{},Biscuits".format(raum,
        kekse),["1","2","3","4","5","6"],"doors1.gif")
        if a13=="1":
            raum=3
            t0="You go back in time."
        elif a13=="6":
            raum=8
            t0="An endless passage leads you underground."
        elif a13=="2":
            raum=14
            t0="You enter the feasting table of tiucsib."
        elif a13=="3":
            raum=15
            t0="You climb up the tower of tiucsib"
        elif a13=="4":
            kekse-=5
            t0="A gigantic lizard is hidden behind the cobble door, and scratches you."
        elif a13=="5":
            kekse-=9
            t0="zTDztdZDdDFzuSxEXFCDCCz8VZtdtdDTdD"
        e.msgbox(t0)    
    while raum==14 and kekse>0:
        actions=["Feast","Go back"]
        a14=e.buttonbox("The feasting room...delicous..","Room:{},Buscuits:{}".format(raum,
        kekse),actions,"table.gif")
        if a14=="Feast":
            kekse+=3
            actions.remove("Feast")                                                                                                                                                    
            t0="You are stuffed."
        else:
            raum=13
            t0="You go back"
        e.msgbox(t0)
    while raum==15 and kekse>0:
        a15=e.buttonbox("The final battle is at hand.","Room:{},Buscuits:{}".format(raum,
        kekse),["Go"],"b4boss.gif")
        if a15=="Go":
            kekse+=1
            raum=16
    while raum==16 and kekse>0:
        a16=e.buttonbox("***The Final Battle***","Buscuits:{},tiucsib's HP:{}".format(kekse,
        tiucsibhp),["Sword","Biscuitray(5)","Shield","Buscuitpunch(1)","Biscuitlightning(2)"],"tiucsib.gif")
        defense = 0.0
        if a16=="Sword":
            defense=0.5
            zufall=random.random() # 0.0 und 1.0
            # 55% chance tiuxib zu treffen
            if zufall < 0.55:
                tiucsibhp-=3
                e.msgbox=("You struck!")
            else:
                e.msgbox("Tiucsib parried you.")
      
        elif a16=="Biscuitray(5)":
            tiucsibhp-=13
            kekse+=random.randint(1,8)
            kekse-=5
            e.msgbox("You rayed Tiucsib and drowned some HP out of him and got it yourself!")
            defense = 0.2
        elif a16=="Shield":
            defense = 0.9        
        elif a16=="Buiscuitpunch(1)":
            tiucsibhp-=5
            kekse-=1
            e.msgbox("You Bicuit-punched Tiucsib!")
            defense = 0.1
        elif a16=="Biscuitlightning(2)":       
            tiucsibhp-=4
            #Tiucsib kann sich nicht bewegen
            kekse-=2  
            continue 
        # boss tot ? 
        if tiucsibhp<1:
                raum=17# boss am a****
                break           
        # boss shlägt z'ruck
        zufall = random.random()
        if zufall > defense:
            kekse-=random.randint(1,4)
            e.msgbox("Tiucsib struck you!")
        else:
            e.msgbox("You blocked Tiucsib's attack.")
            #continue
    while raum==17 and kekse>0:
        a17=e.buttonbox("You won!The biscuits are saved!Well done.","Buscuits:{}".format(kekse),["Awesome!"],"victory.gif")
        if a17=="awesome!":
            break    
# zu wenig kekse
if kekse < 1:
     e.msgbox("You died.The biscuits are no more...",image="blood.gif")
e.msgbox("game over")
