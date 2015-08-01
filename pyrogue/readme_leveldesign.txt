generelle Regeln:


Jeder Level, auch der erste, braucht eine Treppe nach oben [<]
Jeder Level muss eine durchgehende Außenmauer [#] haben
Alle Textlinien eines Levels müssen gleich lang sein (Level muss rechteckig sein)
Level dürfen unterschiedlich groß sein, aber:
Eine Treppe in einen höheren oder tieferen Level darf nicht ins "Nichts" führen;
Die Position der Treppe (x,y) muss im oberen / unteren Level ein gültiges Feld sein;
Zum Beispiel ein Floor [.] , aber keine Wand [W]

Schilder: Pro Level darf es beliebig viele, aber maximal 9 verschiedene 
Hinweisschilder geben. Sie werden durch zahlen (1-9) im Level gesetzt.

Nach der letzten Level-Zeile werden die Hinweistexte für die Schilder geschrieben,
jeweils beginnend mit der entsprechenden Nummer. Beispiel für einen kleinen Level
mit 2 verschiedenen Schildern, Schild 1 kommt zwei mal vor:

#######
#.112.#
#.....#
#######
1 Vorsicht Falle 
2 Dieses Schild ist einzigartig

Erlaubte Zeichen in einem Level:

[.].....Boden / Floor()
[#].....Wand  / Wall()
[<].....Stiege hinauf in den höheren Level / zur Oberfläche
[>].....Stiege hinunter in den tieferen Level
[M].....Monster (Zufallsbewegung)
[B].....Boss (verfolgt den Spieler)
[S].....Statue (kämpft, aber bewegt sich nicht)
[k].....Schlüssel / key
[L].....Loot
[D].....Türe (Door, verschlossen)
1-9.....Schilder
[T].....Falle (trap)

  

