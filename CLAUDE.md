# CLAUDE.md — projet Pac-Man (42)

Binôme : Elhadj (graphisme, branche `graphic`) et Luc (logique, branche `logic`).

## Documents de référence (fournis avec ce fichier)

- `project_management/pacman.pdf` : le sujet officiel (v1.5).
- `project_management/trello.json` : l'export du Trello (tâches et sous-tâches).
- `text.txt` (dans le dépôt) : les décisions de jeu prises avec Luc.

## Le dépôt et la répartition

- Dépôt GitHub : `larchimb/pacman` (appartient à Luc).
- Branches : `main` (fusion via Pull Request), `graphic` (moi), `logic` (Luc).
- Workflow : chacun travaille sur sa branche → PR vers `main` → l'autre relit.
  Avant chaque session : `git fetch origin && git merge origin/main`.
- Répartition Trello (par couleur d'étiquette, aucune carte n'est assignée nominativement) :
  - 🟨 jaune = **moi** : bibliothèque graphique, fenêtre, sprites, écrans, menus,
    HUD, pause, game over / victoire, saisie du nom, highscores, packaging.
  - 🟦 bleu = **Luc** : config (parser JSON), labyrinthe (A-Maze-ing), placement,
    niveaux, joueur, IA des fantômes, cheat mode.
  - 🟩 vert = commun : cadrage, lint, tests, README, gestion de projet, Itch.io.
- Mes dossiers : `src/graphical/`, `assets/`. Luc : `src/logical/`.
- Fichiers communs (prévenir l'autre avant de modifier) : `pac-man.py`,
  `pyproject.toml`, `Makefile`, `.gitignore`, `README.md`, `config.json`.

## Contraintes du sujet à toujours respecter

- Python ≥ 3.10, **flake8**, **mypy** (type hints partout), docstrings PEP 257.
- **Docstrings sur une seule ligne** (`"""Do X."""`), sans sections Args / Returns /
  Raises : la docstring dit *ce que fait* la fonction. Le *pourquoi* va dans des
  commentaires `#` à l'endroit concerné (ex. : pourquoi pas `pygame.init()`).
  Une docstring en tête de chaque fichier, y compris les `__init__.py`.
- `make lint` = `flake8 .` + `mypy . --warn-return-any --warn-unused-ignores
  --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`
  (viser aussi `mypy --strict`).
- **Jamais de traceback** : erreurs gérées avec try/except et messages clairs,
  context managers pour les fichiers.
- Lancement : `python3 pac-man.py config.json` (exactement un argument).
- Le générateur de labyrinthe (`mazegenerator-2.1.0-py3-none-any.whl`) doit être
  utilisé tel quel, avec PERFECT=False.
- Le jeu doit être packagé (PyInstaller) et publié sur Itch.io (build privé / non listé).

## Règle MLX (très important)

Le sujet impose une bibliothèque « similaire à MLX » : **chaque fonction graphique
utilisée doit avoir un équivalent dans MLX**, sinon elle est interdite.
On utilise **pygame restreint**, et **pygame n'est importé que dans
`src/graphical/renderer.py`** (classe `Renderer`, une façade). Le reste du jeu
passe par `Renderer` et n'appelle jamais pygame directement.

Autorisé (avec son équivalent MLX) :

| pygame | MLX |
|---|---|
| `pygame.display.init()` + `pygame.font.init()` | `mlx_init` |
| `pygame.display.set_mode()` + `set_caption()` | `mlx_new_window` |
| `pygame.display.Info()` | `mlx_get_screen_size` |
| `pygame.Surface((w, h))` | `mlx_new_image` |
| `pygame.image.load()` | `mlx_png_file_to_image` / `mlx_xpm_file_to_image` |
| `Surface.set_at()` sur une image | écriture dans le buffer `mlx_get_data_addr` |
| `Surface.set_at()` sur la fenêtre | `mlx_pixel_put` |
| `window.blit(image, (x, y))` (sur la fenêtre uniquement) | `mlx_put_image_to_window` |
| `window.fill(noir)` | `mlx_clear_window` |
| `pygame.font.Font(None, taille fixe)` + `render` | `mlx_string_put` |
| `pygame.display.flip()` | `mlx_do_sync` |
| `pygame.event.get()` (QUIT, KEYDOWN, KEYUP) | `mlx_hook` / `mlx_loop_hook` |
| `pygame.key.set_repeat()` | `mlx_do_key_autorepeaton/off` |
| `pygame.mouse.get_pos / set_pos / set_visible` | `mlx_mouse_get_pos / move / hide / show` |
| `pygame.quit()` | `mlx_destroy_window` + `mlx_release` |

Interdit (pas d'équivalent MLX) :
- `pygame.init()` (démarre le son) → utiliser `display.init()` + `font.init()`.
- `pygame.draw.*` → images pixel par pixel ou sprites PNG.
- `pygame.transform.*` (scale, rotate, flip) → un sprite par direction.
- `pygame.mixer` (pas de son), polices TTF / `SysFont`.
- `pygame.key.get_pressed()`, `pygame.key.name()` → suivre les touches soi-même
  via KEYDOWN / KEYUP.
- `blit` d'une image sur une autre image, `set_alpha`, `set_colorkey`,
  `subsurface`, `Rect.colliderect`.
- `pygame.time.Clock` / `get_ticks` → utiliser le module standard `time`
  (`time.monotonic()`, `time.sleep()`).

## Architecture

Principe : **la logique (Luc) et le graphisme (moi) sont séparés.**
La logique ne fait jamais `import pygame` ; le graphisme ne décide jamais des
règles, il lit l'état du jeu et le dessine.

### Contrat avec Luc (discuté le 22 oct., remplace l'ancien contrat proposé)

**Deux points d'entrée seulement** dans `src/logical/game.py` (`Game`) :
```python
game.handle_action(action: str)   # graphisme → logique : une action du joueur
game.update(dt: float)            # graphisme → logique : avancer de dt secondes
```
Tout le reste = **lecture d'attributs** dans mes `draw` (je ne modifie jamais `Game`) :
`game.score`, `game.lives`, `game.current_level` (+ 1 pour l'affichage),
`game.timer`, `game.result` (`"victory"` / `"defeat"` / `None`), `game.level`
(objet `Level` : grille, `pacman.pos` / `pacman.direction`, `ghosts`, `pacgums`,
`supergums`).

Chaînes d'action (à copier **exactement**, une faute = action ignorée sans erreur) :

| Touche | Action | Source |
|---|---|---|
| Espace | `"pause"` | `game.py` (inverse `game.paused`) |
| `c` | `"cheat"` | text.txt |
| `1` / `2` / `3` / `4` / `5` | `"invinsible"` / `"freeze"` / `"life"` / `"speed"` / `"level"` | Luc, 22 oct. |
| flèches / WASD | **à confirmer** (`"N"`/`"E"`/`"S"`/`"W"` comme `Entity.DIRECTIONS` ?) | — |

À confirmer avec Luc :
1. Les chaînes des directions (mon `DIRECTION_KEYS` envoie `"up"`/`"down"`… → changer les valeurs).
2. L'orthographe `"invinsible"` (anglais : `invincible`) : choisir et copier à l'identique.
3. Pause : je propose de **ne pas** envoyer `"pause"` (mon `PauseScreen` n'appelle
   plus `update`, ça suffit). Si on l'envoie, il faut le renvoyer en reprenant,
   sinon `game.paused` reste `True`.
4. Accès public à la grille (propriété `maze` dans `Level`, au lieu de lire `_maze`).

Forces : interface étroite, sens unique (actions + temps → logique ; état → dessin).
Faiblesses : chaînes non vérifiées par mypy ; dépendance aux noms d'attributs de Luc.

En attendant que le vrai `Game` marche, je travaille avec un faux `Game` (stub) qui
imite ces attributs (le vrai plante pour l'instant : `pacgum` = `None`, voir bugs).

Mes fichiers prévus :
```
src/graphical/
├── __init__.py
├── renderer.py         Renderer : seul fichier qui importe pygame (FAIT)
├── app.py              App : boucle + écran courant + méthodes de transition (FAIT)
├── screens/
│   ├── __init__.py
│   ├── screen.py       Screen : classe mère (handle_event, update, draw) (FAIT)
│   ├── menu.py         MenuScreen (FAIT : menu à curseur, 4 options, carte 4)
│   ├── game.py         GameScreen (plateau + HUD) (FAIT, version test : direction, G / V)
│   ├── pause.py        PauseScreen (FAIT : curseur Resume / Main menu, partie figée derrière)
│   ├── end.py          EndScreen (FAIT : game over / victoire + félicitations + saisie du nom)
│   ├── highscores.py   HighscoresScreen (FAIT, version test : texte fixe)
│   └── instructions.py InstructionsScreen (FAIT : contrôles, règles, triche, carte 4)
├── fake_game.py        FakeGame : faux Game (mêmes attributs que Luc), temporaire (FAIT, pas committé)
├── board_view.py       BoardView : murs, pacgums, Pac-Man, fantômes
└── hud.py              draw_hud() : score, vies, niveau, temps, cheat actif
src/highscores.py       HighscoreTable : charger / ajouter / top 10 / sauvegarder (JSON)
assets/                 sprites PNG 32 × 32 (FAIT : 11 sprites arcade, 23 oct.)
pacman.spec             PyInstaller (à la racine)
```

## Mon `renderer.py` (déjà écrit)

- Couleurs au format MLX `0xRRGGBB` (entiers), converties par `to_rgb()`.
- `InputEvent(kind, key)` : kind = `"quit"`, `"key_down"`, `"key_up"` ;
  key = `"up"`, `"down"`, `"left"`, `"right"`, `"escape"`, `"space"`,
  `"return"`, `"backspace"`, `"shift"` (Maj gauche et droite, ajouté le 23 oct.),
  lettres `a-z` (toujours en minuscules, comme MLX), chiffres `0-9`, ou `""`.
- `RendererError` pour les erreurs (fenêtre, image introuvable).
- Méthodes : `get_screen_size()` (static), `new_image`, `new_filled_image`,
  `image_pixel_put`, `load_image` (avec cache), `clear`, `pixel_put`,
  `put_image`, `string_put`, `present`, `poll_events`, `close`.
- À prévoir (étape 5) : un alias `Image = pygame.Surface` exporté par le
  renderer, pour typer les images ailleurs sans importer pygame.

## Mon `app.py` (carte 2 le 19 oct., machine à états le 21 oct.)

- Constantes `FPS = 60`, `FRAME_TIME = 1 / FPS`.
- `App(width, height, title)` crée le `Renderer` ; `self._running` (drapeau d'arrêt),
  `self._screen: Screen = MenuScreen(self)` (écran de départ, créé dans `__init__`).
- `run()` : `start = time.monotonic()`, `dt = start - last` → `_handle_events()` →
  `self._screen.update(dt)` → `_draw()` → `time.sleep(FRAME_TIME - elapsed)` ;
  `try / finally` pour toujours appeler `renderer.close()`.
  `dt` = temps réel depuis la frame précédente (≈ 0,0167 s) ; `elapsed` = travail
  de la frame seule (sert au sleep).
- `_handle_events()` : QUIT (croix) → `quit()` (règle globale) ; tout le reste →
  `self._screen.handle_event(event)` (Échap change de sens selon l'écran).
- `_draw()` : `clear()` → `self._screen.draw(renderer)` → `present()`.
- Méthodes publiques appelées par les écrans : `change_screen(screen)`, `quit()`,
  `show_menu()`, `show_highscores()`, `show_instructions()`, `start_game()`,
  `pause(game)`, `end_game(won, score)`, `save_score(name, score)` (pour l'instant
  revient juste au menu ; `HighscoreTable` sauvegardera ici).
- Imports absolus depuis la racine : `from src.graphical.screens.menu import ...`
  (chemin du fichier, `/` → `.`, sans `.py`).
- Test : `spike_app.py` à la racine (`App(1440, 960, "Pac-Man").run()`).

## Machine à états des écrans (carte 3, faite le 21 oct.)

Carte Trello « Machine à états des écrans » :
- Définir les états : Menu, Jeu, Pause, Fin, Saisie du nom, Highscores, Instructions
  → fait ; **« Saisie du nom » est intégrée à `EndScreen`** (décision du 21 oct. :
  l'écran de fin connaît déjà le score, pas besoin d'un écran de plus). La saisie
  elle-même se code à la carte 7.
- Transitions : Menu → Jeu → Fin → Saisie du nom → Menu → fait (Fin + saisie = `EndScreen`).
- Router le clavier vers l'écran actif → fait : `App._handle_events()` traite `QUIT`
  (règle globale), puis donne tout le reste à `self._screen.handle_event(event)`.
  La pause n'est **pas** une règle globale : `App` ne sait pas quel écran est
  affiché, seul `GameScreen` sait qu'une partie est en cours.


- `Screen` (classe mère) : `self._app`, méthodes vides `handle_event`, `update`,
  `draw(renderer)`. Les enfants ne redéfinissent que ce dont ils ont besoin
  (sinon Python remonte à `Screen` : voir `MenuScreen.__mro__`).
- Import du type `App` dans les écrans : `if TYPE_CHECKING:` + `"App"` entre
  guillemets → évite l'import circulaire app ↔ screen.
- **Les écrans ne s'importent jamais entre eux** : c'est `App` qui crée les écrans
  (une méthode par transition) → pas de boucle menu → game → pause → menu, et
  toutes les transitions sont lisibles au même endroit.
- Enfant avec son propre `__init__` → appeler `super().__init__(app)`.
- `PauseScreen(app, game)` garde **le même objet** `GameScreen` → reprendre =
  `change_screen(self._game)` (partie conservée) ; `start_game()` = nouvel objet.
- `DIRECTION_KEYS` (flèches + WASD) est maintenant dans `screens/game.py`.
- `EndScreen(app, won, score)` reçoit ses données par le constructeur (comme
  `PauseScreen(app, game)`) ; le texte Victory / Game over est choisi dans `draw`.
- Transitions (toutes faites ; menu à curseur depuis la carte 4) :
  ```
  Menu ──Start Game──► Jeu ──Espace──► Pause ──Resume / Espace──► Jeu
   │                    │                └──Main menu──► Menu
   │                    └──G / V (test)──► Fin ──Entrée (nom) / Échap──► Menu
   ├──Highscores──► Highscores ──Échap──► Menu
   ├──Instructions──► Instructions ──Échap──► Menu
   └──Exit / Échap──► quitter        (croix → quitter partout)
  ```
- **Pause / reprise = Espace** (décision du 21 oct., le sujet n'impose aucune touche).
  Échap ne fait rien en jeu.
- Touches de test temporaires : G / V dans le jeu (remplacées plus tard par
  `game.is_over` / `is_won`). Les touches H / I du menu ont disparu (carte 4).
- Piège vu : `key in "space"` teste une **sous-chaîne** (`"s"`, `"a"`, `""` → True) ;
  `key in ("escape", "return")` teste l'appartenance à un **tuple**. Pour une
  seule touche : `==`.

## Menu principal (carte 4, faite le 21 oct.)

Carte Trello « Menu principal » (Phase 5, échéance 20 oct.) : Start Game, View
Highscores (top 10), Instructions (contrôles, règles, touches de triche), Exit.

- Partie 1 (fait, 21 oct., commit `f884484`) : `MenuScreen` à curseur.
  - `self._options: list[tuple[str, Callable[[], None]]]` = paires (texte, méthode
    de `App`) **sans parenthèses** : on range la fonction, on ne l'appelle pas.
    Entrée → `_, action = self._options[self._selected]` puis `action()`.
  - `self._selected` (index) ; ↑/W : `(selected - 1) % count`, ↓/S :
    `(selected + 1) % count`, avec `count = len(self._options)` (pas de `% 4` en dur).
  - `draw` : `enumerate(self._options)`, `y = OPTIONS_Y + index * LINE_HEIGHT`,
    sélection en jaune avec `"> "`, aide grise sous la dernière option.
  - Échap quitte toujours depuis le menu (carte 2 : fermeture croix + Échap).
  - Le « top 10 » n'est pas dans cette carte : il vient avec les cartes highscores.
- Partie 2 (fait, 21 oct.) : texte complet d'`InstructionsScreen` (contrôles, règles,
  touches de triche ; la carte « Cheat mode » de Luc le demande aussi).
  - Données séparées du code : constante de module `INSTRUCTIONS:
    tuple[tuple[int, str], ...]` = lignes `(couleur, texte)` ; `""` = ligne vide.
    Tuple car il ne change jamais (≠ `self._options` du menu, qui a besoin de `app`).
  - `draw` : `enumerate`, `if text:` (chaîne vide = fausse) ; la ligne vide garde
    son index pour décaler les suivantes.
  - Pas de nombres venant de la config (points, vies, temps) écrits en dur : la
    config peut être modifiée en soutenance.
  - ⚠️ Pavé numérique (text.txt) : le renderer ne traduit que `K_0`…`K_9` ; les
    touches `K_KP1`… donnent `""`. À ajouter dans `_SPECIAL_KEYS` si on garde le
    pavé (voir avec Luc, carte Cheat mode).

## Menu pause (carte, faite le 22 oct.)

Carte Trello « Menu pause » : Reprendre la partie ; Retour au menu principal
(abandon de la partie). Le sujet (pacman.pdf, « Pause Menu ») impose ces **deux**
choix : sans « retour au menu », on ne pourrait quitter une partie qu'en perdant.

- Fait (22 oct., testé à l'écran) : **menu à curseur** (choix d'Elhadj), même
  mécanique que le menu principal : options `("Resume", self._resume)` et
  `("Main menu", app.show_menu)`, ↑ / ↓ (W / S), Entrée ; **Espace = reprendre
  directement** (raccourci). Menu centré (`PAUSE_X = 620`, `PAUSE_Y = 380`).
  - `_resume()` : méthode privée de `PauseScreen` (elle a besoin de `self._game`),
    rangée sans `()` comme une méthode d'`App` (bound method).
  - **Partie figée derrière** : `draw` appelle d'abord `self._game.draw(renderer)`,
    puis le menu. Règle des calques : le dernier dessiné est au-dessus. Figée car
    seul `PauseScreen.update()` (vide) est appelé, pas `GameScreen.update()`.
  - Avec le vrai plateau (carte 5), le texte de pause tombera sur les murs → prévoir
    un rectangle noir derrière (image remplie + `put_image`, autorisé ; la
    transparence est interdite).
- Ancienne version (raccourcis Espace / M) : respectait aussi le sujet.
- Hors carte : timer et fantômes arrêtés en pause = carte verte « Règles de partie »
  (déjà vrai : `GameScreen.update()` n'est plus appelé pendant la pause).

## Écrans Game Over / Victoire et saisie du nom (carte, faite le 23 oct., commit `8fdd1c1`)

| Sous-tâche Trello | État (23 oct.) |
|---|---|
| Écran Game Over avec score final | ✅ (score = 0 tant qu'il n'y a pas de `Game`) |
| Écran Victoire avec score final et message de félicitations | ✅ « Congratulations, you cleared every level! » |
| Saisie du nom : max 10 caractères, alphanumérique + espaces, effacement | ✅ |
| Validation → sauvegarde du score → retour au menu | ✅ validation + retour ; **sauvegarde** = cartes highscores |

- Saisie dans `EndScreen`, **en victoire et en game over** (sujet : « win or lose »).
- **Facultative** : le sujet dit « *Allow* players to enter their name » (l. 382) et
  « the player *can* enter their name » (l. 521) → **Échap = menu sans sauvegarder**.
- `self._name` (chaîne) : lettre / chiffre ajouté si `len(key) == 1 and
  key.isalnum()` (le `len == 1` rejette `"up"`, `"escape"`… qui sont aussi
  alphanumériques), `"space"` → `" "`, `"backspace"` → `self._name[:-1]` (pas
  d'erreur si vide), max `MAX_NAME_LENGTH = 10`, curseur `_` caché quand c'est plein.
- **Majuscules** : `self._shift` suivi via KEY_DOWN / KEY_UP de `"shift"` (comme MLX,
  pas de `get_pressed`) ; le test de `"shift"` est placé **avant** le filtre
  `if kind != KEY_DOWN: return`, sinon le relâchement serait jeté et Maj resterait
  « enfoncée ». `key.upper() if self._shift else key` (ternaire).
- Entrée : `name = self._name.strip()` ; si non vide → `app.save_score(name, score)`.
- Mise en page : ligne n → `END_Y + n * LINE_HEIGHT` ; ligne 1 réservée aux
  félicitations (vide en game over) pour que score et nom restent au même endroit.
- ⚠️ Clavier AZERTY : les chiffres du haut donnent `&`, `é`… → `""` (à tester sur le Mac).
- Le nom et le score ne s'affichent pas encore dans Highscores : normal, c'est
  `HighscoreTable` (cartes « Stockage persistant » et « Robustesse et top 10 »).

## Sprites et rendu du plateau (carte 5, en cours depuis le 23 oct.)

Carte Trello « Sprites et rendu du plateau » (Phase 5, échéance 16 oct.) : Dessin des
murs et des couloirs ; Pacgums et super-pacgums ; Sprite du joueur orienté selon la
direction ; Sprites des fantômes : normal / comestible / mangé.

Plan en 4 étapes :
- **Étape 0 (faite, 23 oct.)** : `src/graphical/fake_game.py` (pas committé : il le
  sera avec `board_view.py`, qui en dépendra).
  - `FakeEntity` (`@dataclass`, non frozen) : `pos: tuple[int, int]` (en **cases**),
    `direction: str | None` (`"N"`/`"E"`/`"S"`/`"W"` comme Luc).
  - `FakeLevel(width, height, seed)` : `maze` = grille du **vrai** `MazeGenerator`
    (public, ce qu'on demande à Luc), `pacman` au centre `((w-1)//2, (h-1)//2)`
    tourné `"E"`, `ghosts` aux 4 coins **dans l'ordre de Luc** (index = couleur :
    0 rouge, 1 rose, 2 bleu, 3 orange), `supergums` = les 4 coins (`set`),
    `pacgums` = 50 cases libres tirées par `random.sample` (hors `CLOSED_CELL = 15`,
    coins et case de Pac-Man).
  - `FakeGame` : `level` = `FakeLevel(23, 19, seed=42)` (le plus grand niveau),
    `score`, `lives`, `current_level`, `timer`, `result` ; `handle_action` ne fait que
    tourner Pac-Man (pour tester les sprites) ; `update(dt)` avance `timer`.
  - Duck typing : mêmes noms d'attributs que Luc → à l'intégration, remplacer
    `FakeGame()` par `Game(config)` sans toucher au dessin.
  - Test : `spike_fake_game.py` (ignoré par git) affiche le plateau en texte
    (`P`, `G`, `#` pour le « 42 », `.` pour les pacgums).
- **Sprites (faits, 23 oct.)** : `assets/` = `pacman_right/left/up/down/closed.png`,
  `ghost_red/pink/blue/orange.png`, `ghost_edible.png`, `ghost_eaten.png` (32 × 32,
  style arcade, **fond noir** → pas de transparence, interdite en MLX). Générés par
  programme avec l'aide de l'IA (script non gardé dans le dépôt car il utilise pygame
  hors du renderer) → **à déclarer dans « Resources » du README**. `assets/preview.png`
  = aperçu agrandi, **ne pas committer** (à supprimer).
- **Étape 1** : `board_view.py`, murs et couloirs (bits N/E/S/W → barres d'image,
  cases 15 pleines), plateau centré sous le HUD de 80 px, affiché dans `GameScreen`.
- **Étape 2** : pacgums (petit point) et super-pacgums (gros point), générés dans le code.
- **Étape 3** : Pac-Man orienté (un sprite par direction) et fantômes (couleur par
  index ; état comestible / mangé à ajouter au contrat avec Luc).

## Taille de la fenêtre et du texte (décidé le 21 oct.)

- PC de l'école : écran **3840 × 2160 (4K) sans mise à l'échelle** → pygame compte
  en pixels physiques, tout paraît petit. Mac (Retina) : pygame compte en **points**
  (MacBook Air 15" ≈ 1710 × 1112). `pygame.transform.scale` étant interdit, une
  taille fixe doit rentrer sur le plus petit écran (le Mac).
- **Fenêtre fixe 1440 × 960** (testée dans `spike_app.py`).
- **`FONT_SIZE = 32`** dans `renderer.py` (une ligne fait 24 px de haut) ; menu :
  `OPTIONS_Y = 140`, `LINE_HEIGHT = 50` ; instructions : `LINE_HEIGHT = 34`.
- Proposition à envoyer à Luc : HUD de 80 px en haut → plateau 1440 × 880 ;
  cases de 32 px → **labyrinthe de 45 × 27 cases maximum** (cases max = plateau
  ÷ taille de case, division entière). Son plus grand niveau (23 × 19) rentre.
- La taille de case (32 px) fixe la taille des sprites (carte 5) : un sprite = une taille.

## Git : fichiers suivis et PR (23 oct.)

- Commit `5255472` : `spike_app.py`, `spike_renderer.py`, `pacman.json` ne sont plus
  suivis (`git rm --cached`, toujours sur le disque) ; `.gitignore` = `pacman.pdf`,
  `pacman.json`, `spike_*.py`, `.venv/`, `__pycache__/`, `.mypy_cache/`.
  `.gitignore` n'existe pas sur `main` : la PR l'apportera (prévenir Luc).
- **`CLAUDE.md` reste suivi volontairement** (synchro école ↔ Mac). Manip à chaque PR :
  avant → `git rm --cached CLAUDE.md` + commit + push ; après la fusion →
  `git add CLAUDE.md` + commit + push. Ne pas faire `git pull` sur le Mac entre les
  deux (le fichier y serait supprimé). Vérifier « Files changed » avant chaque PR.
- **`text.txt` est aussi sur `main`** : ne pas le supprimer sur `graphic` (la PR le
  supprimerait chez Luc). Mes modifications locales non committées de `text.txt`
  contiennent des notes perso (procédure git) → ne pas les committer telles quelles.
- Merge `origin/main` → `graphic` fait le 23 oct. (`1aed9dc`, aucun conflit), poussé.
  PR `graphic` → `main` **pas encore ouverte** (pas de `gh` ici : passer par le site).
- ⚠️ `src/logical/game.py` modifié en local (ligne vide de fin supprimée, sans doute
  par l'éditeur) : fichier de Luc → `git restore src/logical/game.py` ou le prévenir.

## Notions vues (pour la soutenance)

- `sys.path` et imports absolus / relatifs ; import circulaire et `TYPE_CHECKING`.
- Cadence fixe (frame de 20 ms → ~50 FPS, le jeu « rame » mais continue), `dt`.
- Double buffering (`present`), coût de `new_filled_image` (créer une seule fois).
- KEY_DOWN = intention ; KEY_UP pour suivre les touches maintenues.
- Bits des murs (N=1, E=2, S=4, W=8) et `cell & bit`.
- Héritage, `super()`, polymorphisme, ordre de résolution (`__mro__`) ;
  « hérite de » (MenuScreen → Screen) ≠ « utilise » (App → écran).
- Polymorphisme dans `App._draw()` : `self._screen.draw()` sans savoir quel écran.
- Créer un objet = repartir de zéro (`start_game()` → direction `"none"`) ;
  réutiliser la référence = conserver l'état (reprise de la pause). Un objet plus
  référencé est détruit automatiquement (garbage collector, pas de `free`).
- Couleurs `0xRRGGBB` : 3 octets rouge / vert / bleu (0 à 255) ; `FFFF00` jaune,
  `FFFFFF` blanc, 3 valeurs égales = gris (`888888`), `000000` noir.
- Coordonnées : origine en haut à gauche, x vers la droite, **y vers le bas**.
- Modulo `%` = reste de la division ; `(i + 1) % n` boucle comme une horloge.
  Python : `-1 % 4 == 3` (C : `-1`). `%` est prioritaire sur `+` → parenthèses.
- Une fonction est une valeur : `f` = la fonction (comme un pointeur en C),
  `f()` = l'appel. Avec `app.quit()` dans la liste du menu : appels immédiats,
  la liste contiendrait `None` → `None()` = TypeError ; **mypy l'attrape**
  grâce au type `Callable[[], None]`.
- Séparer les données (tuple de lignes) du code (boucle `draw`) ; constante de
  module + tuple pour ce qui ne change jamais ; `tuple[X, ...]` = longueur libre.
- Pixels physiques (Linux 4K) vs points (Mac Retina) ; pourquoi une taille fixe
  doit viser le plus petit écran quand on ne peut pas redimensionner l'image.
- Ordre de dessin = calques : le dernier dessiné est au-dessus ; dessiner sans
  appeler `update` = afficher figé (partie derrière la pause).
- `LINE_HEIGHT` = pas entre le **haut** de deux lignes (texte 24 px + vide) ;
  `string_put(x, y)` place le coin haut-gauche ; < 24 → les lignes se chevauchent.
- Suivre une touche maintenue (Maj) avec KEY_DOWN / KEY_UP ; `str.isalnum()`,
  slicing `s[:-1]`, `strip()`, ternaire `a if cond else b`, `x = (a == b)` range un booléen.
- Git : disque / index / dépôt ; `git rm --cached` = arrêter de suivre sans
  supprimer du disque ; `.gitignore` n'agit que sur les fichiers **non suivis** ;
  `fetch` (télécharge dans `origin/main`) ≠ `merge` (intègre) ; fusion à trois
  (ancêtre commun) : seules **mes modifications** sont appliquées, une suppression
  en est une ; fast-forward ; `git stash` / `stash pop` ; une PR prend toute la branche.
- `.whl` = archive ZIP d'un paquet (code + `dist-info`) ; `pip install` la décompresse
  dans les site-packages (le `.whl` reste tel quel) ; `py3-none-any` = Python pur,
  compatible partout ; Python trouve le paquet via `sys.path`.
- Duck typing / programmer contre une interface (faux `Game` interchangeable) ;
  `@dataclass` (génère `__init__` et `__repr__`) ; `str | None` + valeur par défaut ;
  `Any` d'un paquet non typé → annoter la variable qui le reçoit ; `set` (test
  `in` instantané, pas de doublon) ; compréhensions de liste (2 `for` + `if`) ;
  `random.sample` (sans remise) ; `//` division entière ; seed = hasard reproductible ;
  **`maze[y][x]`** (liste de lignes : boucle sur `y` puis `x`) ; magic number → constante.
- Python est sensible à la casse (`Mazegenerator` ≠ `MazeGenerator`).

## Plan, étape par étape (lié aux cartes Trello jaunes)

| # | Carte Trello | Contenu | État |
|---|---|---|---|
| 1 | Choisir et tester la bibliothèque | `Renderer` + `spike_renderer.py` (images, texte, clavier) | fait (packageable : vérifié à l'étape 2b) |
| 2 | Fenêtre graphique minimale | `App.run()` : boucle à cadence fixe (60 FPS via `time`), flèches + WASD, Échap / croix sans traceback | **fait** (19 oct.) |
| 2b | Premier build de test | PyInstaller sur le mini-programme, tôt | à faire |
| 3 | Machine à états des écrans | `Screen` + `App.change_screen()`, écrans vides | **fait** (21 oct.) : 7 états (saisie du nom dans `EndScreen`), routage |
| 4 | Menu principal | Start, Highscores, Instructions, Exit | **fait** (21 oct.) : menu à curseur + écran Instructions complet |
| 5 | Sprites et rendu du plateau | `assets/` + `BoardView` avec le faux `Game` | **en cours** : faux `Game` + sprites faits (23 oct.), reste étapes 1 à 3 |
| 6 | HUD + Menu pause | `draw_hud()`, `PauseScreen` (reprendre / retour au menu) | pause **faite** (22 oct., curseur + partie figée) ; HUD à faire |
| 7 | Game Over / Victoire + saisie du nom | max 10 caractères, alphanumérique + espaces, effacement | **fait** (23 oct.) ; sauvegarde → carte 8 |
| 8 | Highscores | JSON robuste (absent / corrompu), top 10 trié, affichés dans le menu | à faire |
| 9 | Packaging final | `pacman.spec`, assets inclus, Itch.io | à faire |
| — | Intégration | remplacer le stub par le vrai `Game` de Luc | à faire |

Dates Trello (2026) : rendu final le 7 nov. Sprites 16 oct, machine à états 17 oct,
menu 20 oct, HUD 21 oct, pause 22 oct, fin + saisie 24 oct, premier build 24 oct,
highscores 27-28 oct, packaging 31 oct.

Prochaine étape : **carte 5, étape 1** (`BoardView` : murs et couloirs dans
`GameScreen`), puis étapes 2 et 3, puis **« HUD en jeu »** (même stub), puis 2b
(premier build). Ouvrir la PR `graphic` → `main` quand je le décide (manip CLAUDE.md).
Envoyer à Luc la taille de fenêtre / le nombre de cases max.
À chaque nouvelle carte : annoncer son nom et ses sous-tâches (`pacman.json`) avant de coder.

## Code de Luc fusionné dans `graphic` (23 oct., `main` = `3818e62`)

Nouveautés depuis le 21 oct. (le détail plus bas reste valable sauf ceci) :
- `game.py` : `self.score += ...` corrigé ; `result: Literal["victory", "defeat"] | None`
  (→ remplace mes `is_over` / `is_won`) ; `timer` ; `update(self, time: float)`
  prend maintenant le temps écoulé (= mon `dt`) mais est encore vide ;
  `game_end()` : `lives == 0` → `"defeat"`, sinon `"victory"`.
- `level.py` : grille `self._maze` (privée → il me faudra un accès public), largeur
  14 à 23 et hauteur 10 à 19 (limites dans `MazeLoader`) → rentre dans 45 × 27.
- `config.json` : `levels` = liste de `[largeur, hauteur]`, `highscore_filename` =
  `.highscores.json`, `level_max_time` = 80.
- `.flake8` : `extend-exclude = .venv` → `flake8 .` ne vérifie pas les bibliothèques
  installées par `uv` dans `.venv` (sinon des milliers d'erreurs qui ne sont pas à nous).
- `.highscores.json` : fichier de highscores par défaut (le `.` le cache dans `ls`),
  format `{"Elhadj": 3000, "Luc": 200}` (données de test). Chargé par `MazeLoader`.
- `pyproject.toml` : **`pygame` ajouté** aux dépendances ; `mazegenerator` via le `.whl`.
- Pour lancer `pac-man.py` à l'école (sans venv) : `pip install --user
  mazegenerator-2.1.0-py3-none-any.whl` (sinon ModuleNotFoundError).

Bugs vus le 23 oct. (à signaler à Luc, pas à corriger moi-même) :
- `mazeloader.get_values()` : `self.datas[...] = self.get_lives(...)` (idem
  `get_max_time`, `get_pacgum`) alors que ces méthodes ne renvoient rien →
  `lives`, `level_max_time`, `pacgum` valent **`None`** (mypy le signale : 3 erreurs
  `func-returns-value`, donc `make lint` échoue).
- `get_pacgum` : condition inversée (message d'erreur quand la valeur est valide).
- `game.eat()` : `points_per_supergum` ≠ clé `points_per_superpacgum` → KeyError.
- `check_highscores` ne vérifie pas « alphanumérique + espaces » ; format dict = un
  seul score par nom (deux parties « Luc » s'écrasent).
- `pac-man.py` : les imports sont hors du `try` → si `mazegenerator` manque,
  **traceback** (interdit par le sujet).

## Ce que Luc avait mis sur `main` (vu le 21 oct., commit `33591a9`)

Fichiers (`src/logical/`) :
- `parser.py` : `Parser.check_file(path)` lit le JSON, enlève les `#`, lève `ParsingError`.
- `mazeloader.py` : `MazeLoader(data)` → `config.datas` (dict) avec valeurs par
  défaut et vérifications. Charge aussi les highscores : `datas["highscore"]`
  devient le dict `{nom: score}` (on perd le chemin du fichier).
- `level.py` : `Level(config, MazeGenerator)` = un niveau.
  - `_maze` (privé) : `list[list[int]]`, `maze[y][x]`, **bit à 1 = mur** :
    N=1, E=2, S=4, W=8 ; `15` = case fermée (logo « 42 »).
  - `pacman` : objet `PacMan`, départ au centre `((w-1)//2, (h-1)//2)`.
  - `pacgums` / `supergums` : `set` de `(x, y)` ; super-pacgums dans les 4 coins.
  - `ghosts` : `[Hunter (0,0), Tricky (w-1,0), Randomly (w-1,h-1), Scary (0,h-1)]`
    (= rouge traque, rose piège, bleu aléatoire, orange timide).
  - `eat(pos)` → `"pacgum"` / `"supergum"` / `None` ; `is_cleared()`.
- `entities.py` : `Entity` (mère) avec `pos` (tuple de cases entières), `direction`,
  `next_direction` (`"N"`/`"E"`/`"S"`/`"W"`), `can_move(maze, d)`,
  `possible_directions(maze)`, `move(maze)` (avance d'**une case**).
  Sous-classes `PacMan`, `Hunter`, `Tricky`, `Randomly`, `Scary` : IA vide (`...`).
- `game.py` : `Game(config)` — `levels` (10 niveaux : seed config pour le 1,
  `random` ensuite), `current_level` (int), `level` (propriété → objet `Level`),
  `score`, `lives`, `paused`, `eat()`, `next_level()`, `game_end()` (vide),
  `handle_action(action)` (gère `"pause"`), `update()` (vide, **sans `dt`**).
- `pac-man.py` : config → `MazeLoader` → `Game(config)` ; `try/except` actif.
  Ne lance encore rien de graphique.
- `config.json` : dict ; `levels` de `[14, 10]` à `[23, 19]` (le « 42 » exige
  ≥ 14×10) ; `level_max_time` = 80 (90 par défaut et dans text.txt).
- `pyproject.toml` : dépendance `pydantic` (plus utilisée dans le code).

Fusion simulée (`git merge-tree`) le 21 oct. : aucun conflit. Je merge quand je le décide.

Points à discuter avec Luc :
1. **Contrat** : décidé le 22 oct. (voir « Contrat avec Luc » dans Architecture) ;
   restent les 4 points à confirmer.
2. **Déplacement case par case** : `move()` saute d'une case ; décider la vitesse
   (combien de frames par case) et si l'affichage est fluide (interpolation) ou non.
3. **Pause** : `game.paused` existe chez lui, `PauseScreen` est chez moi → qui décide.
4. **Highscores** : cartes jaunes (moi) mais chargés par `MazeLoader` → il me passe
   le chemin, je gère `HighscoreTable` ; format liste plutôt que `{nom: score}`.
5. **Bugs repérés** : voir « Bugs vus le 23 oct. » (le `=+` est corrigé).
6. Temps par niveau 80 ou 90 s ; taille de case / fenêtre : proposer 1440 × 960,
   HUD 80 px, cases 32 px → 45 × 27 cases max (voir « Taille de la fenêtre »).
7. Touches de triche au pavé numérique ou chiffres du haut du clavier.

## Décisions de jeu (text.txt, prises avec Luc)

- Fin du timer = Game Over. 90 s par niveau. 10 niveaux.
- Taille de fenêtre fixe ; labyrinthes de 10x10 (niveau 1) à 20x20 (niveau 10).
  ⚠️ Changé par Luc dans `config.json` : de 14×10 à 23×19 (à valider ensemble).
- Fantômes et super-pacgums dans les 4 coins. Respawn des fantômes après 5 s.
- Fantômes : rouge = traque, rose = piège, bleu = aléatoire, orange = timide.
- Pause / reprise : touche Espace (décision d'Elhadj, 21 oct.).
- Saisie du nom en fin de partie : facultative (Échap), majuscules avec Maj (23 oct.).
- Cheat mode : `c` pour activer, puis `1` invincibilité, `2` gel des fantômes,
  `3` vies en plus, `4` vitesse +, `5` niveau suivant.

## Commandes utiles

Sur les PC de l'école : **pas de venv**, pygame / flake8 / mypy sont installés
avec `pip install --user` (dans `~/.local/lib/python3.13/site-packages/`). Le
dossier `.venv` qui apparaît dans le projet est vide et inutile. Pour plus tard :
ajouter `pygame` aux dépendances de `pyproject.toml` (fichier commun, avec Luc).

Générateur de labyrinthe à l'école : `python3 -m pip install --user
mazegenerator-2.1.0-py3-none-any.whl` (le `pip` seul est celui de Python 3.10,
alors que `python3` = 3.13 de pyenv ; déjà installé sur ce PC le 23 oct.).
Lint de ma partie : `flake8 src && mypy src/graphical --strict --ignore-missing-imports`
(`mypy src` inclut `src/logical/` de Luc, qui a encore des erreurs ; le générateur
n'est pas typé → `--ignore-missing-imports`, comme `make lint`).

```bash
source .venv/bin/activate          # activer le venv (chez moi, pas à l'école)
pip install pygame flake8 mypy     # (une fois)
python spike_renderer.py           # test du renderer
python spike_app.py                # test de la boucle App et des écrans
flake8 src && mypy src --strict    # vérifier avant chaque commit
                                   # (src/__init__.py doit exister, sinon mypy
                                   #  voit renderer.py "sous deux noms")
deactivate
```
Plus tard (quand la PR de Luc est dans main) : `make install`, `make run`, `make lint` (uv).
Ne jamais committer : `.venv/`, `__pycache__/`, `.mypy_cache/`, `spike_*.py`.
