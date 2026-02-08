## TPROJECT
Start screen
- new game
- continue

## Z0
Sleep function

Reads seconds in `$X` 

## Z01
Draw world map

## Z02
Game main routine

Always start in last city

Then, world exploration loop with

- Check city collision → Z03
- Check number of moves before battle → Z14
- Heliport travel
- Random traveling merchant → Z16 + Z11
- User menu

## Z03
City main routine

Starts by calling Z13 (load +draw city, a 10x16 matrix)

`H, G` → coordinates in the city matrix

- `F6` : exit to worldmap
- Collision with boundaries, wall, or decorative element
- User menu (Z10)
- Inn (Z17)
- Shop (Z11)
- Scenario (static, Z04)
- Scenario (dynamic, Z15)

## Z04
Game scenario/dialogues (static)
- dispatch to Z31~Z38
- `D` ≡ `Int(W)=Z`
- save output `Z` to `Mat Z`

## Z05
Z drawing routines
- X position in `$R`
- sequence in `List Ans`
    - `0`: Z
    - `1`: sword up
    - `2`: sword horizontal high
    - `3`: sword horizontal down
    - `4`: Xmeta
    - `5`: clear <1>
    - `6`: clear <2>
    - `7`: clear <3>
    - `8`: clear Z & sword

## Z06
Monsters fight round, att or spells

@see notice for IDs

## Z07
Increment item counter in the inventory

## Z08
Display attack, power, or item name
- `argv[1]`: category
    - `1`: attack
    - `2`: power
    - `3`: item
- `argv[2]`: item
- `argv[3]`: Y coordinate
- `argv[4]`: X coordinate

## Z09
Item menu

Apply item : restore heal, strength, magic, etc.

Some animations
- groseye (7)
- pie (8)
- prisms (11,12,13)

## Z10
User menu : stats, objects

## Z11
Shop menu + 1 dialogue in a shop

## Z12
Load battle data, draw battle screen

Init monster stats

## Z13
Load & draw city

## Z14
Battle main routine

## Z15
Game dialogues (dynamic)

## Z16
Init shop prices

## Z17
Inn menu

## Z18
Draw life gauge

## Z19
Game Over routine

## Z20
Monsters drawing routines

- `argv[1]`: Monster ID
- `argv[2]`: What to draw :
    - `0`: monster's ranged attack
    - `2`: clear monster
    -`!0`: draw monster
    - `7`: furie

## Z21
Draw explosion

Used for PLYMOUT destruction and for pie explosion

## Z22
Load monsters coordinates lists & drawstat configs

## Z23
Bit getter, result in `Ans`
- `argv[1]`: bit
- `argv[2]`: Mat Z cell row 
- `argv[3]`: Mat Z cell col

## Z24
Bit setter
- `argv[1]`: bit
- `argv[2]`: Mat Z cell row 
- `argv[3]`: Mat Z cell col

## Z25
Tomberry drawing routine

## Z31~Z38
Cities dialogues
- `31`: Botma
- `32`: Tara
- `33`: Atlantis
- `34`: Elos
- `35`: Helenia
- `36`: Winhill
- `37`: Plymout
- `38`: Sanctua