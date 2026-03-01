# Fragmentum - Sliding Puzzle Game (NEA Project)

Fragmentum is a semi-fully-featured **Sliding Puzzle Game** developed using **Python** and **Pygame** as part of an A-Level Computer Science NEA (Non-Exam Assessment).
The project implements a playable n×n sliding tile puzzle with persistent statistics, save/load functionality, a leaderboard system, and a built-in puzzle solver visualiser, packed with tutorials & explanations for each of these sections.

---

## Overview

This game recreates the classic sliding puzzle (sometimes known as a picture puzzle or 8-puzzle or 15-puzzle), where the player rearranges shuffled numbered tiles into the correct order by sliding them into an empty space to re-order the numbers (or alternatively, re-form the original image).

The project focuses on:

* Algorithmic problem solving
* Game state management
* Persistent data storage
* User interface design
* Automated puzzle solving

---

## Features

### Gameplay

* Adjustable puzzle sizes (n×n boards)
* Random **solvable puzzle generation**
* Mouse and keyboard movement controls
* Move counter and live timer
* Pause and resume functionality
* Restart system after completion

### Solver System

* Integrated puzzle-solving algorithm
* Step-by-step solution viewer
* Navigation through solution states
* Visual replay of solving process

### Data Persistence

* Game history stored using SQLite databases
* Leaderboard tracking fastest solve times
* Automatic statistics tracking:
  * Fastest solve time
  * Average solve time
  * Average moves
  * Total solves
* Save current puzzle state and continue later

### User Interface

* Button-based UI built with Pygame
* Confirmation menus
* Themed colour configuration
* Stopwatch-style time formatting

---

## Project Structure (only main branches)

```
NEA/
│
├── main_menu.py        # Main menu
├── choose_screen.py    # Choose board size to solve
├── main_game.py        # Main game loop and gameplay logic
├── solver.py           # Puzzle solver screen
├── config.py           # Colour themes and configuration
├── stats.json          # Stored gameplay statistics
├── settings.json       # Stored theme options (feel free to add your own!)
├── ind.txt             # Important for settings, DO NOT MODIFY
├── CrimsonPro.ttf      # Main font used throughout the game
├── tutorial.py         # Main tutorial hub where explanations can be accessed
├── history.py          # Main history where saved games & stats are accessed
├── leaderboard.py      # Local leaderboard where fastest times are accessed
│
├── puzzle/
│   └── classes.py      # Core classes (Board, Button, Slider, Database)
|
├── all_tiles/
|   └── *tiles.png      # Images for the tiles for each theme (feel free to manually replace them with your own images!)   
│
├── tutorials/
|   └── *tutorials.py   # Where the tutorial images and screens are stored, DO NOT MODIFY
|
├── history.db          # Saved game history database
└── leaderboard.db      # Leaderboard records
```

---

## Requirements

* Python 3.10+
* Pygame

Install dependencies:

```bash
pip install pygame
```

---

## Running the Game

From the project root directory:

```bash
python main_menu.py
```

This launches the main menu interface. The main game can be run from there.

---

## Controls

### Movement

* **WASD** or **Arrow Keys** — Move tiles (by moving the blank tile in the given direction).
* **Mouse Click** — Select tiles to slide - simply click on the tile to swap it with the blank tile.

### Buttons

* **Pause / Resume** — Pause the timer and gameplay
* **Solve** — Opens the solver screen
* **Save** — Saves current progress
* **Quit** — Exit with confirmation

### Shortcuts

* Hold **Q** for 3 seconds to quit instantly
* Press **R** after solving to start a new puzzle of the same board size

---

## Saving & Statistics

The game automatically records:

* Puzzle size
* Solve time
* Number of moves
* Completion status
* Timestamp of play session

Statistics are stored in `stats.json`, while previous games and leaderboard data are stored in SQLite databases.

---

## Solver

The built-in solver computes a solution path for the current puzzle and allows the player to:

* Step forward and backward through moves
* Visually understand the solving process
* Analyse puzzle states

This component demonstrates algorithmic search and state reconstruction by using a priority-first search approach.

**Limited to boards up to 5*5**. Does not work for all board sizes.

---

## Educational Purpose

This project was created as part of an **OCR A-Level Computer Science NEA**, demonstrating:

* Object-oriented programming
* Event-driven game loops
* Data persistence with databases
* Algorithm implementation
* UI/UX design in Pygame
* Testing and robustness considerations

---

## Future Improvements (Ideas)

* Additional solving algorithms (A*, IDA*) that work for larger sizes
* Animation transitions between moves
* Sound effects and accessibility options
* Online leaderboard support

---

## License

This project is intended for educational use.
Modify and extend freely for learning purposes.

---
