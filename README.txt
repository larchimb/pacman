==================================================================
                            PAC-MAN
==================================================================

Eat every pacgum, avoid the ghosts, clear all the levels before
the timer runs out.


------------------------------------------------------------------
 1. LAUNCH THE GAME (Linux)
------------------------------------------------------------------

Unzip the archive, then in a terminal, inside the "pac-man" folder:

    chmod +x pac-man        (only the first time)
    ./pac-man

You can also give another configuration file:

    ./pac-man my_config.json

Without an argument, the game uses the "config.json" file next to
the executable. If it is missing, a copy shipped inside the game is
used instead.

Keep the "_internal" folder next to the executable: the game needs
it to run.


------------------------------------------------------------------
 2. CONTROLS
------------------------------------------------------------------

  In game
    Arrows or W A S D     Move Pac-Man
    Space                 Pause / resume

  In menus
    Up / Down or W / S    Select an option
    Enter                 Confirm
    Escape                Back to the main menu (highscores and
                          instructions screens)

  Pause menu
    Resume                Back to the game (or press Space)
    Main menu             Leave the game (the score is lost)

  End screen
    Type your name        1 to 10 letters, digits or spaces
    Enter                 Save your score
    Escape                Skip, back to the main menu


------------------------------------------------------------------
 3. RULES
------------------------------------------------------------------

  - Eat every pacgum to clear the level.
  - The 4 super-pacgums in the corners make the ghosts edible
    for a while: eat them for bonus points.
  - Touching a ghost costs one life. No life left: game over.
  - Each level has a timer. When it reaches 0: game over.
    Every new level gives 10 more seconds than the previous one.
  - Clear every level to win the game.


------------------------------------------------------------------
 4. CHEAT MODE
------------------------------------------------------------------

  C       Enable / disable cheat mode, then:
  1       Invincible (on / off)
  2       Freeze the ghosts (on / off)
  3       One extra life
  4       Speed up Pac-Man (on / off)
  5       Go to the next level


------------------------------------------------------------------
 5. CONFIGURATION (config.json)
------------------------------------------------------------------

Open "config.json" (next to the executable) with any text editor.
It is a JSON object. Lines can contain comments starting with "#".

  Key                   Allowed values         Default
  -------------------   --------------------   -----------------
  lives                 3 to 99                3
  level_max_time        60 to 800 (seconds)    90
  pacgum                20 to 10000            10000 (*)
  points_per_pacgum     10 to 10000            10
  points_per_supergum   10 to 10000            50
  points_per_ghost      10 to 10000            200
  seed                  10 to 10000            41
  levels                [[width, height], ...] 10 levels, from
                        width 14 to 37         [14, 10]
                        height 10 to 25        to [23, 19]
  highscore_filename    a file name or path    ".highscores.json"

  (*) If there are more pacgums than free cells, every free cell
      gets one.

  - "seed" only sets the maze of the first level, so it is always
    the same. The other levels are random.
  - "levels": the game always has 10 levels. A missing level uses
    its default size, extra levels are ignored. A level with only
    a width keeps it and uses the default height.

If a value is missing or invalid, the game does not stop: it uses
the default value and writes a message in the terminal. If the
whole file is missing or is not valid JSON, every default value is
used.

Example:

    {
        "lives": 5,
        "level_max_time": 120,
        "pacgum": 100,
        "seed": 42,
        "levels": [[14, 10], [16, 12], [18, 14]],
        "highscore_filename": "my_scores.json"
    }


------------------------------------------------------------------
 6. HIGHSCORES
------------------------------------------------------------------

The 10 best scores are saved in ".highscores.json", next to the
executable (or in the file given by "highscore_filename"; a
relative path is taken from the game folder).

  - If the file does not exist yet, it is created on the first save.
  - If it is damaged, the game never overwrites it: it tries the
    default file, then saves in ".back_up.json" instead. Fix or
    delete the damaged file to use it again.
  - If no file can be written, the score is not saved, the game
    goes back to the main menu and the reason is written in the
    terminal.

Files starting with "." are hidden: use "ls -a" to see them.
