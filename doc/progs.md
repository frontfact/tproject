## TPROJECT
Start screen
- new game
- continue
Decrypt the save matrix, then call TNT2

## TNT1
Draw the world map

## TNT2
At game launch: retrieve city and position, then call TNT3. This where we see that we always start the game in a city. That could change if needed.

When exiting city : call TNT1 (draw world)

Then, world exploration loop with

- Check number of moves before battle → if = 0 → battle → TNT14
- Random traveling merchant → TNT15 + TNT11
- Check city collision → TNT3
- Heliport travel

## TNT3
City logic entry point

Starts by calling TNT13 (draw city) : a city is a 10x16 matrix.

I, J → starting coordinates in the city (viewwindow 127×63)

H, G → coordinates in the city matrix

City movement loop

## TNT4
Game dialogues

displays “hum?” if a tile has a script not matching current progress

## TNT5
drawing routines
sequence in List Ans
0: Z
1: epee levee 
2: epee horizontale haute
3: epee horizontale basse
4: Xmeta
5: efface epee 1
6: efface epee 2
7: efface epee 3
8: efface Z + epee

## TNT6
Monsters fight round, att or spells

## TNT7
increment an item counter in the inventory

special case for item 14 (rifle)

## TNT8
Display attack, power, and item lists

K, L → display coordinates

O → category

1. attacks
2. powers
3. items
not all powers from the manual are present (vision?)

## TNT9
Display item menu

Apply item : restore heal, strength, magic, etc.

some animation drawings
- groseye (C = 7)
- summonings (prisms C = 11,12,13)

## TNT10
Display user menu

## TNT11
Shop menu + 1 dialogue in a shop

## TNT12
Draw battle screen, Z & monster, StoPict 1
Init monster apts
Z=8     => Enzo     (@ Botma)
Z=11    => Minautor (Tara catacombs)
Z=23    => mandivor (Elos bounty)
Z=28.5  => Vegetal  (@ Helenia)
Z=29    => spectre  (@ Winhill)
Z=32    => Redox    (@ Plymout)
Z=33    => Enzo     (@ Plymout)
Z=43    => Redox    (@ Sanctua)
Z=44    => Enzo     (@ Sanctua)
Z=99    => lapranak (treasure)

## TNT13
draw city

dialogue when progress = 41

## TNT14
Battle loop

Program reads monster ID in W

## TNT15
Game dialogues (in cities ?)

Also draw final screen

## TNT16
Init merchant prices

## TNT17
Inn menu