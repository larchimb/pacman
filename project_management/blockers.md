# Blocking points and conflicts

## Technical blocking points

**1. The display needed the logic (Oct 16 → Nov 4).**
The board, the HUD and the highscores need a real `Game` object, but the logic was not
ready before the end of October.
*Solution*: interface contract (22 Oct), then a fake `Game` with the same attribute
names (23 Oct), so the board could be drawn before the connection. The real `Game` was
plugged in on 3–4 Nov without changing the drawing code.

**2. The MLX rule.**
Many usual pygame functions are forbidden (`draw`, `transform`, transparency, TTF fonts).
*Solution*: everything is built pixel by pixel in images created once (walls, gums,
big titles). Black is the "empty" color: only the colored pixels of a sprite are drawn.
One sprite per direction instead of rotating images.

**3. Smooth movement vs grid logic.**
The logic moves by whole cells, so a smooth display was always one step behind. Gums
were eaten and collisions happened one cell too early, and Pac-Man and a ghost could
cross without touching.
*Solution*: the display slides between `prev_pos` and `pos`, and the rules use the
**displayed** cell (`Entity.cell`).

**4. Window size.**
The school screens are 4K without scaling, so everything looked small. A Mac Retina
counts in points, so a big window does not fit. Images cannot be scaled.
*Solution*: one fixed window size chosen for the school machines (2048 × 1450), cells
of 52 px, and every position computed from the window size.

**5. Packaging paths (9 Nov).**
The executable could not find its images, because the paths were relative to the
current folder.
*Solution*: `src/paths.py` (`sys._MEIPASS` when packaged, saves next to the executable).

## Team and Git conflicts

**6. Files deleted by a merge (15 Oct).**
A merge conflict was solved by keeping the wrong side.
*Solution*: files restored. Lesson: read the result of a merge before pushing.

**7. Diverged branch between two computers (2 Nov).**
Commits made at school and on a personal computer without syncing. The push was
refused, then there was an add/add conflict on the same new file.
*Solution*: merge, keep one version. Rule since then: `git pull` when arriving,
`git push` when leaving.

**8. Who owns the pause? (21 Oct → 3 Nov)**
The logic had a `paused` flag and the display had a pause screen.
*Solution*: the pause is a screen (`PauseScreen`). While it is shown,
`game.update(dt)` is not called, so the timer and the ghosts stop. `paused` was
removed from `Game`.

**9. Changes in the other person's files.**
The board file `board_view.py` was merged into `GameScreen` directly on `main`, and the
HUD disappeared on the way. A logic file was also changed by the display side
(`Entity.cell`).
*Solution*: the HUD was added again. Rule: warn the other before changing his files.

**10. Action names.**
The strings sent by the display (`"up"`, `"invincible"`…) had to match exactly the
strings expected by the logic. A typo would be ignored without any error.
*Solution*: names checked together and listed in the contract.

**11. Delay.**
The submission was planned for 7 Nov. Packaging, final lint, README and this folder
were finished on 9 Nov (see [planning.md](planning.md)).
