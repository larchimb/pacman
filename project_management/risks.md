# Risk analysis

Likelihood and impact: **L** = low, **M** = medium, **H** = high.

| # | Risk | Likelihood | Impact | Mitigation | What happened |
|---|---|---|---|---|---|
| 1 | Using a graphics function that has no MLX equivalent (forbidden by the subject) | M | H | pygame is imported in **one file only** (`renderer.py`), a facade whose methods match MLX functions; a table of allowed and forbidden functions | No forbidden call. Sprites, gums and titles are drawn pixel by pixel; black is used as the "empty" color because MLX has no transparency |
| 2 | Logic and display not compatible when connected | H | H | Interface contract decided on 22 Oct; a fake `Game` with the same attribute names to develop the display alone | Connection done on 3–4 Nov with few changes, but later than planned (see planning.md) |
| 3 | Window too big or too small depending on the screen (4K school screens, Mac Retina) | H | M | Fixed window size, cell size computed so the biggest level fits, positions computed from the window size | Window set to 2048 × 1450 for the school machines; too high for a MacBook Air |
| 4 | Invalid config during the defense causes a crash | H | H | Default value for each key, range checks, clear `[VALUE ERROR]` messages, `try/except` at the entry point | Invalid values are replaced by the defaults with a message |
| 5 | Corrupted or missing highscore file | M | M | Validation of each entry, fallback files (default, then `.back_up.json`), file created on first save | Several bugs found and fixed (see bug log) |
| 6 | Maze generator fails or returns a wrong size | L | H | Size check, retry with another seed, clear error message | Not observed |
| 7 | Packaged game cannot find its files | M | H | Paths computed from `sys._MEIPASS` when packaged (`src/paths.py`) | Happened on 9 Nov, fixed the same day |
| 8 | Python version: code that only works on recent Python (≥ 3.12) | M | H | Check with `python3.10 -m py_compile` | One f-string only valid on 3.12+ found and fixed on 6 Nov |
| 9 | Git conflicts or lost work between the two branches and two computers | M | M | `git pull` before working, `git push` after; warn before editing a shared file | Files deleted by a merge (15 Oct), a diverged branch (2 Nov); both recovered |
| 10 | Not enough time before the deadline | H | H | Phases with due dates; core features first, polish last | Display, packaging and documentation finished after the planned date |
| 11 | One team member cannot explain the other's code at the defense | M | H | Interface contract, README and this folder; explain each part to each other before the defense | In progress: this documentation is part of the preparation |
