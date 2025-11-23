
![the t-project](images/tproject.gif)

# The T-Project

An adventure game running on [Casio Graph 65](https://fr.wikipedia.org/wiki/Casio_CFX-9960GT) (CFX-9960GT).

First released on 15th december 2001, it has been recently dusted and ported to monochrome calculators (Casio Graph [35+](https://fr.wikipedia.org/wiki/Casio_Graph_35%2B) & [100+](https://fr.wikipedia.org/wiki/Casio_Graph_100%2B)).

[Instructions](./doc/notice.md) are available in french.

# Limitations

The game requires 64kB of memory to run (47kB of programs, 1 picture, 2-3 matrices and lists).

# Packages

- [TPROJECT.CAT](./packages/TPROJECT.CAT) for graph65 (3 colors)
- [TPROJECT35.CAT](./packages/TPROJECT35.CAT) for graph35+ (monochrome)
- [TPROJECT100.CAT](./packages/TPROJECT100.CAT) for graph100+ (monochrome)

# Contact

tntsoft@fastmail.com

# Backlog

- [x] Dynamic step to display score
- [x] ~~Suggest to load a game if a save exists~~ → impossible
- [x] Fix dialogs typos
- [x] Facilitate the arm wrestling against the troll
- [x] Enable F6 key (go to world) during city loading
- [x] Shop : Enable [exit] key to exit shop
- [x] Objects : allow to take several objects in a row, except during fight : Not r, TNT9
- [ ] Check if we can use pict-2 to store last visited city. probably requires 4096 bytes saving elsewhere
- [x] Port to graph35+/graph100+
    - [x] remove ':' separators
	- [x] monochrome
		- [x] modify menus using [    ] brackets to select entries
		- [x] life gauge in cities
		- [ ] make dialogs speaker explicit
	- [x] ¥ not rendered with `Text` command
	- [x] factorize sleep loops into Prog "T0" + use a global sleep factor
- [x] Simplify cat encoding : Re, Ra, E, r, or, a, an, milli, Cnt, etc.
- [ ] Add progress hint in user menu
- [ ] fix floating values in end-battle screen
- [x] Notice in markdown/pdf
