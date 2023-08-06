##Vytvorenie mapy levela

1. Stiahneme si nastroj Tiled, ktory sluzi na vytvorenie levelov
2. Po spusteni stlacime "Subor" > "Nova mapa"
3. Nastavime mapu a to:
   1. Orientation: Orthogonal
   2. Tile layer format: Base64 uncompressed
   3. Tile render order: Right down
   4. Map size:
      1. Width: 32
      2. Height: 18
   5. Tile size:
      1. Width: 32px
      2. Height 32px
4. Nasledne ju ulozime s priponou ".tmx"

Kazda mapa musi obsahovat tieto vrstvy:
1. walls (tile layer) - kde su zaznacene steny levela
2. items (Object layer) - Itemy a ich rozmiestnenie v leveli
3. actors (Object layer) - Aktori a ich rozmiestnenie v leveli
4. background (tile layer) - Pozadie levela

Vrstvy vytvorime ak klikneme vpravo na panel kde je zobrazena jedina vrstva "Tile layer 1"
Ak pod tuto vrstvu klikneme pravim tlacidlom mame moznost vytvorenia novej vrstvy

Aby ste zakazdym nemuseli vytvarat znova to iste pripravili sme si pre vas predpripravenu mapu levela

Nasledne je potrebne pridat Tileset. Klikneme na new Tileset, nasledne mu nastavime nazov, zaskrtneme embeed in map.
Ako zdroj(source) vyberieme bud poskytnute tilesety alebo si viete tilesety vytvorit aj samy (Pridat link)