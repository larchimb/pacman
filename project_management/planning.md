# Planning: planned vs actual

**Planned** = the due date of the Trello card. **Actual** = the date of the commits
that delivered the work (`git log --date=short`). We use the Git dates, not the dates
when the Trello boxes were ticked, because several boxes were ticked in bulk at the
end (6 and 9 Nov).

Owner: the login of the person in charge (both logins = shared card).

## Timeline

| Phase | Card | Owner | Planned | Actual | Gap |
|---|---|---|---|---|---|
| 0 | Read the subject, list ambiguities | elbarry, larchimb | 9 Oct | 9 Oct | on time |
| 0 | Understand the maze generator | elbarry, larchimb | 10 Oct | 9–10 Oct | on time |
| 0 | Choose and test the graphics library | elbarry | 10 Oct | 15 Oct | +5 days |
| 0 | Define the architecture | elbarry, larchimb | 12 Oct | 10–16 Oct | +4 days |
| 0 | Set up project management | elbarry, larchimb | 12 Oct | 9–15 Oct (board) / 9 Nov (folder) | folder late |
| 1 | Repository and tree | larchimb | 13 Oct | 10 Oct | early |
| 1 | Makefile | larchimb | 13 Oct | 13 Oct (`build` 6–9 Nov) | on time |
| 1 | flake8 / mypy setup | elbarry, larchimb | 14 Oct | 13–21 Oct | +7 days |
| 1 | Minimal window | elbarry | 14 Oct | 19 Oct | +5 days |
| 2 | JSON config parser with comments | larchimb | 15 Oct | 15–16 Oct | +1 day |
| 2 | Value checks and defaults | larchimb | 16 Oct | 16–18 Oct | +2 days |
| 2 | Global error handling (no traceback) | larchimb | 17 Oct | 18 Oct → 6 Nov | continuous |
| 2 | Test config files | larchimb | 17 Oct | 6–9 Nov (broken configs tested, see acceptance_tests.md) | +20 days |
| 3 | Loader for A-Maze-ing | larchimb | 19 Oct | 19 Oct (generator check 2 Nov) | on time |
| 3 | Placement of the elements | larchimb | 20 Oct | 19–20 Oct | on time |
| 3 | Level progression | larchimb | 21 Oct | 21–27 Oct | +6 days |
| 4 | Player movement and actions | larchimb | 23 Oct | 20–26 Oct (visible cell 4 Nov) | +3 days |
| 4 | Ghost AI | larchimb | 26 Oct | 27–30 Oct (BFS) | +4 days |
| 4 | Game rules (win, lose, timer, pause) | elbarry, larchimb | 27 Oct | 26 Oct → 3 Nov | +7 days |
| 4 | Cheat mode | larchimb | 28 Oct | 27 Oct (on screen 4 Nov) | on time |
| 5 | Sprites and board rendering | elbarry | 16 Oct | 23 Oct (sprites) → 4 Nov (board) | +19 days |
| 5 | Screen state machine | elbarry | 17 Oct | 21 Oct | +4 days |
| 5 | Main menu | elbarry | 20 Oct | 21 Oct | +1 day |
| 5 | In-game HUD | elbarry | 21 Oct | 4 Nov | +14 days |
| 5 | Pause menu | elbarry | 22 Oct | 22 Oct | on time |
| 5 | Game over / victory, name input | elbarry | 24 Oct | 23 Oct | early |
| 6 | Persistent highscore storage | elbarry, larchimb | 27 Oct | 2 Nov → 6 Nov | +10 days |
| 6 | Robustness and top 10 | elbarry, larchimb | 28 Oct | 4 → 9 Nov | +12 days |
| 7 | First test build | elbarry, larchimb | 24 Oct | 6 Nov | +13 days |
| 7 | Final packaging script and resources | elbarry, larchimb | 31 Oct | 6 → 9 Nov | +9 days |
| 7 | Publication on Itch.io | elbarry, larchimb | 3 Nov | 9 Nov | +6 days |
| 8 | Unit tests (pytest) | elbarry, larchimb | 31 Oct | replaced by the acceptance and crash tests (no pytest file in the repository) | — |
| 8 | Docstrings, type hints, final lint | elbarry, larchimb | 2 Nov | 9 Nov | +7 days |
| 8 | Acceptance test plan | elbarry, larchimb | 3 Nov | 9 Nov | +6 days |
| 8 | Crash tests | elbarry, larchimb | 4 Nov | 9 Nov | +5 days |
| 9 | README in English | elbarry, larchimb | 5 Nov | 9 Nov | +4 days |
| 9 | Project management folder | elbarry, larchimb | 6 Nov | 9 Nov | +3 days |
| 9 | Final submission and defense | elbarry, larchimb | 7 Nov | not done yet | — |

## Analysis of the gaps

- **Framing and base were on time.** The repository, the Makefile, the parser and the
  config checks were delivered within a few days of the plan.
- **The display waited for the logic.** The board, the HUD and the highscores were
  planned in mid-October, but they need the real `Game` object. The logic and the
  display were connected only on 3–4 Nov. Until then, elbarry worked with a fake
  `Game` (23 Oct) to draw the board, which limited the delay but could not remove it.
- **Packaging was started too late.** The plan had a first build on 24 Oct, early on
  purpose. It was made on 6 Nov. The path problem (assets not found in the
  executable) only appeared then and was fixed on 9 Nov.
- **Quality and documentation moved to the end.** Lint, README and this folder were
  finished after the planned submission date.

TODO (larchimb): add what you would plan differently next time.
