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
├── app.py              App : boucle principale à cadence fixe + écran courant
├── screens/
│   ├── screen.py       Screen : classe mère (handle_event, update, draw)
│   ├── menu.py         MenuScreen
│   ├── game.py         GameScreen (plateau + HUD)
│   ├── pause.py        PauseScreen
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

## Plan, étape par étape (lié aux cartes Trello jaunes)

| # | Carte Trello | Contenu | État |
|---|---|---|---|
| 1 | Choisir et tester la bibliothèque | `Renderer` + `spike_renderer.py` (images, texte, clavier) | renderer écrit, test en cours |
| 2 | Fenêtre graphique minimale | `App.run()` : boucle à cadence fixe (60 FPS via `time`), flèches + WASD, Échap / croix sans traceback | à faire |
| 2b | Premier build de test | PyInstaller sur le mini-programme, tôt | à faire |
| 3 | Machine à états des écrans | `Screen` + `App.change_screen()`, écrans vides | à faire |
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

## Décisions de jeu (text.txt, prises avec Luc)

- Fin du timer = Game Over. 90 s par niveau. 10 niveaux.
- Taille de fenêtre fixe ; labyrinthes de 10x10 (niveau 1) à 20x20 (niveau 10).
- Fantômes et super-pacgums dans les 4 coins. Respawn des fantômes après 5 s.
- Fantômes : rouge = traque, rose = piège, bleu = aléatoire, orange = timide.
- Cheat mode : `c` pour activer, puis `1` invincibilité, `2` gel des fantômes,
  `3` vies en plus, `4` vitesse +, `5` niveau suivant.

## Commandes utiles

```bash
source .venv/bin/activate          # activer le venv
pip install pygame flake8 mypy     # (une fois)
python spike_renderer.py           # test du renderer
flake8 src && mypy src --strict    # vérifier avant chaque commit
deactivate
```
Plus tard (quand la PR de Luc est dans main) : `make install`, `make run`, `make lint` (uv).
Ne jamais committer : `.venv/`, `__pycache__/`, `.mypy_cache/`, `spike_*.py`.
