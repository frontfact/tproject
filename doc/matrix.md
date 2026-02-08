## Mat Z

|  | 1 | 2 | 3 | 4 | 5 | 6 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | Life | Life max | Spell 1 | Attak 1 | Object 1<br>(soin) | Object 11<br>(ANGEL) |
| 2 | Strength | Strength max | Spell 2 | Attak 2 | Object 2<br>(soin+) | Object 12<br>(MAGMA) |
| 3 | Magic | Magic max | Spell 3 | Attak 3 | Object 3<br>(adrena) | Object 13<br>(PHOENIX) |
| 4 | Att | Att max | Spell 4 | Attak 4 | Object 4<br>(chlore) | Object 14<br>(fusil) |
| 5 | Def | Def max | Spell 5 | Attak 5 | Object 5<br>(protec) | Object 15<br>(balles) |
| 6 | Monster life | Monster att | Monster def | Monster inertia<br>(adjusted) | Object 6<br>(power+) | Object 16<br>(LUNE) |
| 7 | Monster<br>Attak 1 | Monster<br>Attak 2 | Monster<br>Attak 3 | Monster<br>Life max | Object 7<br>(groseye) | Object 17<br>(rhum) |
| 8 | Monster<br>Spell 1 | Monster<br>Spell 2 | Monster<br>Spell 3 | regular monster ➜ 0<br>persona monster ➜ 1 | Object 8<br>(tarte) | In city (1)<br>or world (0) |
| 9 | X coordinate<br>in world map | Y coordinate<br>in world map | Last Getkey<br>code in city | Last Getkey<br>code in world | Winhill<br>fights | Old man<br>cooking |
| 10 | Groseye found<br>in Helenia  | Treasure found<br>in WorldMap | Countdown<br>in WorldMap | $$$ | calculator<br>speed factor | Monster inertia<br>(raw) |
| 11 | Current city ID | Z Level | Attak (1)<br>or<br>Spell (2) | Attak/Spell ID | City is cached<br>in Pict 1 | Z Experience |
| 12 | Countdown<br>in city | Plymout<br>quest | Victories<br>count | X coordinate<br>in city | Y coordinate<br>in city | Progress<br>in game |

## Z12

| id | Monster |  | Attak | Defense | Life | Inertia | A1 | A2 | A3 | S1 | S2 | S3 |
|:-:|:-|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|1 | lapranak | 1 | 2+N/2 | 2+N/2 | 18+10N+8NRan# | 10 |  |  |  |  |  |  |
|2 | srilane | 2 | 2+N/3 | 2+3N/4 | 20+11N+8NRan# | 12 |  |  |  |  |  |  |
|3 | mandivor | 3 | N+1 | 1+2N/3 | 16+12N+6NRan# | 9 |  |  |  |  |  |  |
|4 | arakn' | 4 | 2+4N/5 | 2+4N/5 | 20+14N+7NRan# | 12 |  |  |  |  |  |  |
|5 | orinaphe | 5 | N+2 | N+2 | 25+20N+8NRan# | 14 |  |  |  |  |  |  |
|6 | goa geant | 6 | N+1 | 1+3N/4 | 20+16N+8NRan# | 8 |  |  |  |  |  |  |
|7 | spectre | 7 | N+2 | 2+2N/3 | 40+15N+13NRan# | 8 |  |  |  |  |  |  |
|8 | Enzo | 6 | 9 | 9 | 99 | 11 |  |  |  |  |  |  |
|11 | Minautor | 5 | 4 | 4 | 120 | 11 |  |  |  |  |  |  |
|23 | mandivor | 3 | 7 | 6 | 400 | 7 |  |  |  |  |  |  |
|29 | srilanes | 2 | 10 | 9 | 150~200 | 7 |  |  |  |  |  |  |
|99 | lapranak | 1 | 15 | 12 | 800 | 7 |  |  |  |  |  |  |

## Z06

| Attak/Spell| Name | ID | P | Q | note |
|:-:|:-:|:-:|:-:|:-:|:-:|
| A | coup | 1 | 6 | 6 | |
| A | garde | 2 | 9 | 1 | |
| A | feinte | 3 | 4 | -1 | |
| A | tranch | 4 | 6 | 10 | |
| A | double | 5 | 6 | 15 | |
| A | charge | 6 | 6 | 24 | 6+6Ran# self-damages |
| A | furie | 7 | 6 | 26 | |
| A | Xmeta | 8 | 6 | 30 | |
| S | acier | 1 | 9 | 1 | |
| S | force | 2 | 8 | 1 | |
| S | onde | 3 | 6 | 7 | |
| S | eclair | 4 | 6 | 10 | |
| S | vision | 5 | 0 | 0 | |
| S | boost | 6 | 4 | 1 | +1 att/def |
| S | vague | 7 | 6 | 16 | |
| S | morsur | 8 | 6 | 14 | |
| S | griffe | 9 | 6 | 14 | |
| S | soleil | 10 | 6 | 24 | 9+6Ran# self-damages |
| S | vital | 11 | 7 | 40+9Ran# | |
| S | onde+ | 12 | 6 | 20 | |
| S | foudre | 13 | 6 | 29 | |
| S | vampyr | 14 | 6 | 22 | + 16+10Ran# life |
| S | flamme | 15 | 6 | 34 | |
| S | orage | 16 | 6 | 41 | |
| S | enfers | 17 | 6 | 50 | 20+9Ran# self-damages |

P = 6 :

```txt
        Q   2Q  Mat Z[6,2]
2Ran# + _ + __(___________)
        3    3  Mat Z[5,1]
```

## Z14

| Attak/Spell| Name | ID | P | Q | note |
|:-:|:-:|:-:|:-:|:-:|:-:|
| A | coup | 1 | 1 | 6 | |
| A | garde | 2 | 4 | 1 | |
| A | feinte | 3 | 9 | -1 | |
| A | tranch | 4 | 1 | 10 | |
| A | double | 5 | 1 | 15 | |
| A | charge | 6 | 1 | 24 | 6+6Ran# self-damages |
| A | furie | 7 | 1 | 26 | |
| A | Xmeta | 8 | 1 | 32 | |
| S | acier | 1 | 4 | 1 | |
| S | force | 2 | 3 | 1 | |
| S | onde | 3 | 1 | 7 | |
| S | eclair | 4 | 1 | 10 | |
| S | vision | 5 | 0 | 0 | |
| S | boost | 6 | 4 | 1 | +1 att/def |
| S | vague | 7 | 1 | 16 | |
| S | morsur | 8 | 1 | 14 | |
| S | griffe | 9 | 1 | 14 | |
| S | soleil | 10 | 1 | 24 | 9+6Ran# self-damages |
| S | vital | 11 | 2 | 60+20Ran# | |
| S | onde+| 12 | 1 | 20 | |
| S | foudre | 13 | 1 | 28 | |
| S | vampyr | 14 | 1 | 22 | + 20+10Ran# life |
| S | flamme | 15 | 1 | 34 | |
| S | orage | 16 | 1 | 40 | |
| S | enfers | 17 | 1 | 50 | 20+9Ran# self-damages |

P = 1 :

```txt
        Q   2Q  Mat Z[4,1]
2Ran# + _ + __(___________)
        3    3  Mat Z[6,3]
```
