
![the t-project](images/tproject.gif)

# The T-Project

A RPG game running on Casio graph65 (CFX-9960GT).

First released on 15th december 2001.

# Backlog

- [x] 1st dialog : clarify with "tiens, prends cet argent pour etc."
- [x] Fix typo "scull" in user menu
- [x] Dynamic step to display score
- [x] User menu : remove 'options', 'retour', 'quitter le jeu'
- [x] ~~Suggest to load a game if a save exists~~ → impossible
- [x] Fix dialogs typos
- [x] ~~Facilitate the arm wrestling against the troll~~ → not necessary (on graph65)
- [x] Enable F6 key (go to world) during city loading
- [x] Objects : do not display 'Epee' and 'Livre'
- [x] Objects : remove menu entry [jeter]
- [x] Shop : Enable [exit] key to exit shop
- [x] Objects : allow to take several objects in a row, except during fight : Not r, TNT9
- [ ] Check if we can use pict-2 to store last visited city. probably requires 4096 bytes saving elsewhere
- [x] ~~Check if 'vision' power exists~~ → it does
- [x] ~~Extract shop init from TNT15~~ → TNT16
- [x] ~~Extract hostel from TNT4~~ → TNT17
- [ ] Display 'hum?' only if progress < W ?
- [ ] Port to graph35+/graph100+
    - [ ] remove ':' separators
	- [ ] monochrome
		- [ ] modify menus using [    ] brackets to select entries
	- [ ] ¥ not rendered with `Text` command
	- [ ] factorize sleep loops into TNT18 + use a global sleep factor (using free Mat Z cell ?)
- [x] Simplify cat encoding : Re, Ra, E, r, or, a, an, milli, Cnt, etc.
- [ ] Notice in markdown/pdf
	- [ ] screenshots of attaks/powers
	- [ ] 'hum?' in points of interest
	- [x] sequence diagram for TNT2 (main loop)
	- [x] sequence diagram for TNT3 (city loop)
	- [ ] sequence diagram for TNT14 (fight loop)
