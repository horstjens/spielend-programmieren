#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       polarbear.py
#       
#       Copyright 2011 Xixi Edelsbrunner <xedelsbrunner@gmail.com>
#       
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
#       Pictures taken from Wikimedia Commons http://commons.wikimedia.org/wiki/Main_Page
#		Sound taken from Wikimedia Commons and Scratch


#def main():
	
#	return 0

#if __name__ == '__main__':
#	main()

import easygui
import random
import subprocess
temp=0
time=0
maxtime = 45
maxtemp = 25
cage = True
zoo = False
penguins = False
pvisited = False
icecream = False
ivisited = False
pzookeeper = False
gun = False
child = False
zoo2 = False
escape = False
fountain = False
garage = False
gameover=False
warning1=False
def clock ():
	global gameover
	global warning1
	msg = "time: %i temp: %i you feel fine" % (time,temp)
	if time > maxtime:
		gameover=True
		easygui.msgbox("You ran out of time. You fell asleep.","Game Over",image="sleep.jpg")
	elif time > 35 and not warning1:
		easygui.msgbox("You're running out of time.")
		warning1=True
		msg = "time: %i temp: %i you feel restless" % (time,temp)
	elif temp > maxtemp:
		gameover=True
		easygui.msgbox("Your tempurature has reached %i You had a heat stroke and fainted." % temp,"Game Over",image="sleep.jpg")
	return msg
easygui.msgbox("You are a polar bear, and it's getting hot in the summertime. You should break out of your cage and cool down. Make sure you don't overheat though. You can only take %i degrees, and you've only got %i minutes to get out!" % (maxtemp,maxtime) ,image="polarbear.jpg")
while not gameover:	
	while cage and not gameover:	
		action1=easygui.buttonbox("You're in your cage. What do you do?",clock(),("Steal a key","Scare children","Break a wall"),image="face.jpg")
		if action1=="Steal a key":
			easygui.msgbox("The zookeeper is too smart for you. You failed to steal the key.",image="key.png")
			time+=5
		elif action1=="Scare children":
			subprocess.Popen(("play","BabyCry.wav"))
			easygui.msgbox("The child cries, and a zookeeper comes to see what's happening. He takes the kid to a different exhibit.",image="cry.jpg")
			time+=2
		elif action1=="Break a wall":
			easygui.msgbox("You broke out of the cage, and you're adrenaline is running. You'd better run away quickly.",image="wall.JPG")
			time+=2
			temp+=6
			cage=False
			zoo=True
		clock()
	while zoo and not gameover:
		if (not ivisited) and (not pvisited):
			action2=easygui.buttonbox("You're out of the cage now, and you want to cool down. What's you're plan?",clock(),("Go to the penguins","Look for ice cream"),image="face2.jpg")
		elif pvisited and not ivisited:
			action2=easygui.buttonbox("You're out of the cage now, and you want to cool down. What's you're plan?",clock(),("Look for ice cream","Continue"),image="face2.jpg")
		elif ivisited and not pvisited:
			action2=easygui.buttonbox("You're out of the cage now, and you want to cool down. What's you're plan?",clock(),("Go to the penguins","Continue"),image="face2.jpg")
		elif ivisited and pvisited:
			action2="Continue"
		if action2=="Go to the penguins":
			subprocess.Popen(("play","Goose.wav"))
			easygui.msgbox("You went to the penguins. It's cooler there.",image="penguins.jpg")
			time+=8
			temp-=4
			zoo=False
			penguins=True
		elif action2=="Look for ice cream":
			easygui.msgbox("You found some ice cream, but people are holding it.",image="icecream.jpg")
			time+=8
			zoo=False
			icecream=True
		elif action2=="Continue":
			time+=2
			zoo=False
			zoo2=True
		clock()
	while penguins and not gameover:
		pvisited=True
		action3=easygui.buttonbox("You arrive at the penguin exhibit. What do you do?",clock(),("Rest on the ice","Eat a penguin"))
		if action3=="Rest on the ice":
			easygui.msgbox("You took a nice nap, but you wasted a lot of time, and the penguin exhibit is getting hot too. You leave the penguins.")
			penguins=False
			zoo=True
			time+=20
			temp-=15
		elif action3=="Eat a penguin":
			easygui.msgbox("The penguins are making noise. A zookeeper comes to see what's going on, and takes you back to your cage.")
			penguins=False
			pzookeeper=True
			time+=5
			temp+=2
		clock()
	while icecream and not gameover:
		ivisited=True
		action4=easygui.buttonbox("There is a woman and a child with ice cream. What do you want to do?",clock(),("Attack the woman","Attack the child","Keep looking"))
		if action4=="Attack the woman":
			easygui.msgbox("You go for the ice cream, but she pulls something out of her purse. It's a gun! You're heart is pumping and temperature rising.")
			icecream=False
			gun=True
			time+=2
			temp+=10
		elif action4=="Attack the child":
			easygui.msgbox("You get the ice cream from the defenseless child. Yum, it's vanilla, you're favorite.",image="Child.jpg")
			time+=2
			temp-=8
			child=True
			icecream=False
		elif action4=="Keep looking":
			easygui.msgbox("You decide to skip the ice cream. You need to watch the pounds anyway.")
			zoo=True
			icecream=False
			time+=2
		clock()
	while pzookeeper and not gameover:
		pvisited=True
		action5=easygui.buttonbox("The zookeeper is coming to get you. What do you do?",clock(),("Attack him","Run away"))
		if action5=="Attack him":
			easygui.msgbox("You manage to take off a leg or two, but more zookeepers come, and take you back to your cage.")
			subprocess.Popen(("play","Scream-male2.mp3"))
			time+=10
			temp+=4
			pzookeeper=False
			cage=True
		elif action5=="Run away":
			easygui.msgbox("You managed to escape, but you're using up energy to run away.")
			time+=5
			temp+=10
			pzookeeper=False
			zoo=True
		clock()
	while gun and not gameover:
		ivisited=True
		action6=easygui.buttonbox("She's pointing a gun at you. What do you do?",clock(),("Run away","Attack anyway"))
		if action6=="Run away":
			easygui.msgbox("You ran away safely.")
			time+=2
			temp+=6
			zoo=True
			gun=False
		elif action6=="Attack anyway":
			easygui.msgbox("She shot you! Bummer")
			gameover=True
			gun=False
		clock()
	while child and not gameover:
		ivisited=True
		easygui.msgbox("You decide to eat the child too, and continue on your journey.")
		time+=2
		temp+=4
		child=False
		zoo=True
		clock()
	while zoo2 and not gameover:
		action7=easygui.buttonbox("The zookeepers are hot on your trail. What do you want to do?",clock(),("Visit Grizzly","Escape Zoo"))
		if action7=="Visit Grizzly":
			subprocess.Popen(("play","bear.wav"))
			easygui.msgbox("You go to ask advice of your friend, the grizzly bear. His exhibit is a bit warm for you, but he gives you a drink of water and some cold salmon. He tells you yo try and escape, and also to 'stick it to the man', whatever that means.",image="grizzly.jpg")
			time+=4
			temp-=2
			zoo2=False
			escape=True
		elif action7=="Escape Zoo":
			zoo2=False
			escape=True
			time+=6
			temp+=2
		clock()
	while escape and not gameover:
		action8=easygui.buttonbox("You successfully escape the zoo. There are a lot of people out here, but you see a water fountain across the street.",clock(),("Go to fountain","Look for a place to hide"))
		if action8=="Go to fountain":
			easygui.msgbox("You cooled off in the fountain a bit. How refreshing! For some reason, a lot of people are looking at you.",image="fountain.jpg")
			time+=4
			temp-=15
			fountain=True
			escape=False
		elif action8=="Look for a place to hide":
			easygui.msgbox("You walk along the sidewalk for a while, pushing people aside and into traffic. You find see a little house with an empty garage. It looks cool in there, so you go inside, and take a nap.")
			garage=True
			escape=False
		clock()
	while fountain and not gameover:
		action9=easygui.buttonbox("The people look kind of scared.",clock(),("Look for a place to hide","Attack civilians"))
		if action9=="Look for a place to hide":
			easygui.msgbox("You walk along the sidewalk for a while, pushing people aside and into traffic. You find see a little house with an empty garage. It looks cool in there, so you go inside, and take a nap.")
			time+=8
			temp+=2
			garage=True
			fountain=False
		elif action9=="Attack civilians":
			subprocess.Popen(("play","hit.wav"))
			easygui.msgbox("You eat plenty of people, and soon become drowsy and full. You sit down to rest, and feel the sun growing hotter above you. You fall asleep in the middle of the road, and are hit by a truck.",image="semi.JPG")
			gameover=True
			fountain=False
		clock()
	while garage and not gameover:
		easygui.msgbox("When you wake up, you see an old couple. They make you some steak and ice packs, and say you can stay in their garage. You win!",image="oldcouple.jpg")
		gameover=True
		garage=False
		clock()
easygui.msgbox("Thanks for playing!",image="float.jpg")
