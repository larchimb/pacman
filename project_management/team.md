# Team organization

## Who did what

The Trello cards were shared by color label (no card was assigned by name).

| Area | elbarry (graphics, yellow) | larchimb (logic, blue) |
|---|---|---|
| Library | `Renderer`: pygame restricted to MLX equivalents | — |
| Window and loop | `App`: fixed 60 FPS loop, events, screen transitions | — |
| Screens | menu, instructions, pause, game over / victory, name input, highscores | first highscore screen, layout fixes |
| Board | walls, gums, sprites, smooth movement, HUD | cheat mode display, merge of the board into `GameScreen` |
| Assets | sprites and background image | — |
| Config | — | `Parser`, `MazeLoader` (checks, defaults) |
| Maze and levels | — | generator loader, `Level`, placement, progression |
| Gameplay | visible cell (`Entity.cell`) for contacts | `Game`, `PacMan`, ghosts and BFS AI, rules, timer, cheat mode |
| Highscores | display, top 10, player highlight | storage, validation, robust loading |
| Packaging | — | `pac-man.spec`, `make build`, `src/paths.py` |
| Shared | architecture, lint, README, this folder | architecture, Makefile, Itch.io |

## How we made decisions

- **Reading the subject together** (9 Oct): we listed the open points and decided
  them together. Examples: the end of the timer is a game over, 10 levels, ghosts and
  super-pacgums in the 4 corners, ghost respawn after 5 seconds, cheat keys `C` then
  `1`–`5`. We wrote them down so that the logic and the display followed the same
  rules.
- **Interface contract** (22 Oct): the display only calls
  `game.handle_action(action)` and `game.update(dt)`, and only reads the other
  attributes. Once this contract was agreed, each of us could work on his side
  without waiting for the other.
- **Owner decides, but warns the other**: each of us decides inside his own folder
  (`src/graphical/` or `src/logical/`). Shared files (`pac-man.py`, `Makefile`,
  `pyproject.toml`, `config.json`, `README.md`) are changed only after telling the
  other.

## Git workflow

- Until 4 Nov: one branch each (`graphic`, `logic`), then a pull request to `main`
  (13 pull requests).
- From 4 Nov, once the game was connected: everyone works directly on `main`, with
  `git pull` before working and `git push` after, to go faster near the deadline.
- Rule: no merge if `make lint` fails.

## How issues were handled

See [blockers.md](blockers.md) for the main problems, and
[acceptance_tests.md](acceptance_tests.md) for the bug log.

## Communication and code review

- **Face to face at school**: we talked each time we were both at school. That is
  where we took the decisions, split the next tasks and solved the problems between
  the logic and the display.
- **Trello** kept the plan and the progress visible to both of us between two
  meetings.
- **Code review**: until 4 Nov, each pull request to `main` was read by the other
  before the merge. After that, we checked each other's changes after each
  `git pull`, and talked about them at the next meeting.
