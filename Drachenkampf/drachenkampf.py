#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       drachenkampf.py
#       
#       Copyright 2011 Jeffrey Cheung 
#       see http://www.spielend-programmieren.at for more information

#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       



#def main():
#   
#   return 0
#
#if __name__ == '__main__':
#   main()

import easygui
import random
import subprocess
hitpoints_spieler = 50
hitpoints_drache = 100
angst_spieler = 0
angst_drache = 0
angst_max = 100
global gameover
gameover = False

class Typ_im_Spiel(object):
    def __init__(self, spielername):
       self.hitpoints = 50
       self.angst = 0
       self.name = spielername
       self.zaubertrank = 0

    def check(self):
        status = "%s hat noch %i hitpoints und %i zaubertränke" % (self.name, self.hitpoints,self.zaubertrank)
        if self.hitpoints < 1:
            easygui.msgbox("%s ist tot" % self.name)
            gameover = True
        if self.angst > angst_max:
            easygui.msgbox("%s hat die Hosen voll vor Angst und flieht. So ein Feigling !" % self.name)
            gameover = True
        return status

ritter  = Typ_im_Spiel("Ritter")
ritter.zaubertrank = 5
drache = Typ_im_Spiel("Drache")
drache.hitpoints = 100



def angriff(angreifer, verteidiger):
    wa = random.randint(1,6) + random.randint(1,6) + random.randint(1,6)
    wv = random.randint(1,6) + random.randint(1,6)
    if wa == wv:
        easygui.msgbox("Der Angriff von %s war nicht erfolgreich, da der Gegner %s genau gleich stark war" % (angreifer.name, verteidiger.name), "%i:%i" % (wa,wv),image='wesnoth-icon.png')
    elif wa > wv:
        easygui.msgbox("Der Angriff von %s gegen %s war erfolgreich"  % (angreifer.name, verteidiger.name), "%i:%i" % (wa,wv),image='baneblade2.png')
        # schaden
        wa = random.randint(1,6) + random.randint(1,6)
        wv = random.randint(1,6)
        if wa == wv:
            easygui.msgbox("Kein Schaden, da die Rüstung genau so gut ist wie der Schaden" , "%i:%i" % (wa,wv),image='wesnoth-icon.png')
        elif wa > wv:
            easygui.msgbox("Schaden: %i" % (wa-wv) , "%i:%i" % (wa,wv),image='ritter schaden.png')
            verteidiger.hitpoints -= (wa-wv)
        elif wa < wv:
            easygui.msgbox("Kein Schaden." , "%i:%i" % (wa,wv),image='schade.png')
    elif wa < wv:
        easygui.msgbox("Der Angriff von %s gegen %s ist misslungen"  % (angreifer.name, verteidiger.name), "%i:%i" % (wa,wv),image='schade.png')
    


while not gameover:

    action1 = easygui.buttonbox("was willst du tun",ritter.check(),("angreifen","ducken","zaubertrank","fliehen",'superattacke'),image="fencer-attack-8.png")
    if action1 == "angreifen":
        subprocess.Popen(("play","Laser_Shoot.wav"))
        easygui.msgbox("du greifst den Drachen an.",image='picki.png')
        angriff(ritter, drache)
    elif action1 == "ducken":
        easygui.msgbox('du duckst dich und erholst dich ein bisschen.',image='ducken.png')
        w=random.randint(0,3) 
        easygui.msgbox('du erholst dich und gewinnst %i lebenspunkte zurück' %w)
        ritter.hitpoints+=w 
    elif action1 == 'zaubertrank':
        if ritter.zaubertrank > 0:
            subprocess.Popen(("play","Powerup.wav"))
            easygui.msgbox('du wurdest geheilt',image='hp.png')
            ritter.hitpoints += 20
            ritter.zaubertrank -= 1
        else:
            easygui.msgbox('du hast keine tränke mehr') 
    elif action1 == 'fliehen':
        easygui.msgbox('du bist geflohen, du feigling',image='lauf.png')
        gameover = True
    elif action1 == 'superattacke':
        subprocess.Popen(("play","Jump.wav"))
        easygui.msgbox('du greifst mit zwei schwertern gleichzeitig an',image='schwerti.png')
        for x in range(random.randint(1,3)):
            easygui.msgbox("Superattacke Nummer %i" %x)
            angriff(ritter, drache)
    
    # Drache
    was_tut_drache = random.randint(1,5)
    easygui.msgbox(drache.check())
    if was_tut_drache == 1:
        easygui.msgbox('du wurdest angegriffen',image='drache.png')
        angriff(drache,ritter)
    elif was_tut_drache == 2:
        easygui.msgbox('der drache hat sich verteidigt',image='glider.png')
    elif was_tut_drache == 3:
        easygui.msgbox('der drache versteckt sich und du kannst ihn nicht angreifen',image='verstecken.png')
    elif was_tut_drache == 4:
        easygui.msgbox('der drache bekommt angst',image='angst.png')
        drache.angst += random.randint(1,10)
    elif was_tut_drache == 5:
        easygui.msgbox('der drache speit Feuer',image='feuer.png')
        feuerschaden = random.choice((0,0,0,0,1,1,1,5,5,10,20))
        ritter.hitpoints -= feuerschaden
        easygui.msgbox("Du erleidest %i Feuerschaden" % feuerschaden,image='brennen.png')
        
        
easygui.msgbox("Auf Wiedersehen, bis zum nächsten Mal",image='assassin.png') 
