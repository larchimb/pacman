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

Contrat proposé entre nous (à valider avec Luc) — objet `Game` côté logique :
```python
game.maze            # la grille (murs de chaque case)
game.player          # .x, .y, .direction
game.ghosts          # liste : .x, .y, .color, .state ("normal"/"edible"/"eaten")
game.pacgums         # cases avec une pacgum
game.super_pacgums
game.score, game.lives, game.level, game.time_left
game.is_over, game.is_won
game.set_direction("left")   # graphisme → logique
game.update(dt)              # graphisme → logique : avancer de dt secondes
```
En attendant le vrai `Game`, je travaille avec un faux `Game` (stub).

Mes fichiers prévus :
```
src/graphical/
├── __init__.py
├── renderer.py         Renderer : seul fichier qui importe pygame (FAIT)
├── app.py              App : boucle + écran courant + méthodes de transition (FAIT)
├── screens/
│   ├── __init__.py
│   ├── screen.py       Screen : classe mère (handle_event, update, draw) (FAIT)
│   ├── menu.py         MenuScreen (FAIT, version test : Entrée / Échap)
│   ├── game.py         GameScreen (plateau + HUD) (FAIT, version test : direction)
│   ├── pause.py        PauseScreen (FAIT, version test : reprendre / M = menu)
│   ├── end.py          EndScreen (game over / victoire + saisie du nom)
│   ├── highscores.py   HighscoresScreen
│   └── instructions.py InstructionsScreen
├── board_view.py       BoardView : murs, pacgums, Pac-Man, fantômes
└── hud.py              draw_hud() : score, vies, niveau, temps, cheat actif
src/highscores.py       HighscoreTable : charger / ajouter / top 10 / sauvegarder (JSON)
assets/                 sprites PNG
pacman.spec             PyInstaller (à la racine)
```

## Mon `renderer.py` (déjà écrit)

- Couleurs au format MLX `0xRRGGBB` (entiers), converties par `to_rgb()`.
- `InputEvent(kind, key)` : kind = `"quit"`, `"key_down"`, `"key_up"` ;
  key = `"up"`, `"down"`, `"left"`, `"right"`, `"escape"`, `"space"`,
  `"return"`, `"backspace"`, lettres `a-z`, chiffres `0-9`, ou `""` si non gérée.
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
  `show_menu()`, `start_game()`, `pause(game)`.
- Imports absolus depuis la racine : `from src.graphical.screens.menu import ...`
  (chemin du fichier, `/` → `.`, sans `.py`).
- Test : `spike_app.py` à la racine (`App(640, 480, "Pac-Man").run()`).

## Machine à états des écrans (carte 3, en cours)

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
- Transitions faites (3.2a) : Menu —Entrée→ Jeu —Échap→ Pause —Échap/Entrée→ Jeu ;
  Pause —M→ Menu ; Menu —Échap→ quitter ; croix → quitter partout.
- Reste (3.2b) : `EndScreen` (Fin + saisie du nom), `HighscoresScreen`,
  `InstructionsScreen` et leurs transitions (Jeu → Fin → Menu, Menu ↔ Highscores,
  Menu ↔ Instructions), touches de test temporaires en attendant le vrai `Game`.

## Notions vues (pour la soutenance)

- `sys.path` et imports absolus / relatifs ; import circulaire et `TYPE_CHECKING`.
- Cadence fixe (frame de 20 ms → ~50 FPS, le jeu « rame » mais continue), `dt`.
- Double buffering (`present`), coût de `new_filled_image` (créer une seule fois).
- KEY_DOWN = intention ; KEY_UP pour suivre les touches maintenues.
- Bits des murs (N=1, E=2, S=4, W=8) et `cell & bit`.
- Héritage, `super()`, polymorphisme, ordre de résolution (`__mro__`) ;
  « hérite de » (MenuScreen → Screen) ≠ « utilise » (App → écran).

## Plan, étape par étape (lié aux cartes Trello jaunes)

| # | Carte Trello | Contenu | État |
|---|---|---|---|
| 1 | Choisir et tester la bibliothèque | `Renderer` + `spike_renderer.py` (images, texte, clavier) | fait (packageable : vérifié à l'étape 2b) |
| 2 | Fenêtre graphique minimale | `App.run()` : boucle à cadence fixe (60 FPS via `time`), flèches + WASD, Échap / croix sans traceback | **fait** (19 oct.) |
| 2b | Premier build de test | PyInstaller sur le mini-programme, tôt | à faire |
| 3 | Machine à états des écrans | `Screen` + `App.change_screen()`, écrans vides | **en cours** : 3.1 routage + 3.2a Menu/Jeu/Pause faits (21 oct.), reste 3.2b |
| 4 | Menu principal | Start, Highscores, Instructions, Exit | à faire |
| 5 | Sprites et rendu du plateau | `assets/` + `BoardView` avec le faux `Game` | à faire |
| 6 | HUD + Menu pause | `draw_hud()`, `PauseScreen` (en pause, seul « reprendre » marche) | à faire |
| 7 | Game Over / Victoire + saisie du nom | max 10 caractères, alphanumérique + espaces, effacement | à faire |
| 8 | Highscores | JSON robuste (absent / corrompu), top 10 trié, affichés dans le menu | à faire |
| 9 | Packaging final | `pacman.spec`, assets inclus, Itch.io | à faire |
| — | Intégration | remplacer le stub par le vrai `Game` de Luc | à faire |

Dates Trello (2026) : rendu final le 7 nov. Sprites 16 oct, machine à états 17 oct,
menu 20 oct, HUD 21 oct, pause 22 oct, fin + saisie 24 oct, premier build 24 oct,
highscores 27-28 oct, packaging 31 oct.

Prochaine étape : **3.2b** — `EndScreen`, `HighscoresScreen`, `InstructionsScreen`
et leurs transitions. Ensuite carte 4 (menu) ou 5 (sprites, en retard).

## Ce que Luc a mis sur `main` (vu le 21 oct., dernier commit `33591a9`, pas encore mergé dans `graphic`)

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
1. **Contrat** : grille publique (`maze`), directions `"N"/"E"/"S"/"W"` (mon `App`
   utilise `"up"/"down"/...` → choisir), `update(dt)` ou cadence fixe par case,
   `game.level` = objet `Level` chez lui (le HUD veut le numéro → `current_level + 1`),
   où passent les touches (`handle_action`) et le cheat mode, `is_over` / `is_won`.
2. **Déplacement case par case** : `move()` saute d'une case ; décider la vitesse
   (combien de frames par case) et si l'affichage est fluide (interpolation) ou non.
3. **Pause** : `game.paused` existe chez lui, `PauseScreen` est chez moi → qui décide.
4. **Highscores** : cartes jaunes (moi) mais chargés par `MazeLoader` → il me passe
   le chemin, je gère `HighscoreTable` ; format liste plutôt que `{nom: score}`.
5. **Bugs repérés** dans `game.eat()` : `self.score =+ ...` (affecte au lieu
   d'ajouter, seule erreur flake8 restante) et `f"points_per_{eaten}"` donne
   `points_per_supergum` alors que la clé est `points_per_superpacgum` → KeyError.
6. Temps par niveau 80 ou 90 s ; taille de case / fenêtre (plus grand niveau 23×19,
   32 px → plateau 736×608 + HUD).

## Décisions de jeu (text.txt, prises avec Luc)

- Fin du timer = Game Over. 90 s par niveau. 10 niveaux.
- Taille de fenêtre fixe ; labyrinthes de 10x10 (niveau 1) à 20x20 (niveau 10).
  ⚠️ Changé par Luc dans `config.json` : de 14×10 à 23×19 (à valider ensemble).
- Fantômes et super-pacgums dans les 4 coins. Respawn des fantômes après 5 s.
- Fantômes : rouge = traque, rose = piège, bleu = aléatoire, orange = timide.
- Cheat mode : `c` pour activer, puis `1` invincibilité, `2` gel des fantômes,
  `3` vies en plus, `4` vitesse +, `5` niveau suivant.

## Commandes utiles

```bash
source .venv/bin/activate          # activer le venv
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
