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

monster drawing

maybe the grass line of the scene drawn at the start of a battle

## TNT6
draw attacks and spells in battle

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

Apply item : resotre heal, strength, magic, etc.

some animation drawings
- groseye (C = 7)
- summonings (prisms C = 11,12,13)

## TNT10
Display user menu

## TNT11
Shop menu + 1 dialogue in a shop

## TNT12
Draw battle screen

call TNT5 near the end

monster name override after TNT5

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