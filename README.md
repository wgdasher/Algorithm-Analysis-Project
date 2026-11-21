# Algorithm Analysis Project — Minimax Tic-Tac-Toe with Alpha-Beta Pruning

**Authors:** Elizabeth Rodriguez, Ian Campbell, Chandler Armstrong, Garrett Dasher

A console Tic-Tac-Toe game in Python where you play against an unbeatable AI.
The project compares two game-tree search algorithms:

- **Plain Minimax**: explores every possible game state.
- **Minimax with Alpha-Beta Pruning**: skips branches that cannot change
  the final decision.

On every AI turn, both algorithms run on the same board. The game reports
how many nodes each one explored, how long each took, and the percentage
reduction from pruning.

## File Structure

```
Algorithm-Analysis-Project/
├── main.py      # Game logic, both Minimax variants, metrics, and console driver
├── .idea/       # PyCharm project settings
└── README.md
```

`main.py` is organized into three sections:

| Section | Functions | Purpose |
|---|---|---|
| Helper functions | `print_board`, `winner`, `is_full`, `game_over`, `legal_moves`, `apply_move`, `choose_first`, `read_human_move` | Board representation, win/draw detection, move generation, user input |
| Minimax functions | `evaluate_terminal`, `minimax_plain`, `minimax_ab`, `Metrics`, `best_ai_move` | Search algorithms and performance measurement |
| Driver | `play` | Console game loop |

## How It Works

- **Board:** a list of 9 cells indexed 0–8 (shown to the player as 1–9).
  Each cell holds `'X'`, `'O'`, or `' '`.
- **Scoring** (from the AI's perspective): `10 - depth` for an AI win,
  `-10 + depth` for a loss, and `0` for a draw. Using depth makes the AI
  prefer faster wins and slower losses.
- **Alpha-Beta:** `alpha` is the maximizer's guaranteed lower bound and
  `beta` is the minimizer's guaranteed upper bound. The search stops
  checking a node's remaining moves once `beta <= alpha`. Pruning never
  changes the result; it only skips branches that don't matter.
- **Metrics:** each search is timed with `time.perf_counter()` and counts
  every node it visits. The results are stored in a `Metrics` dataclass.

### Complexity

| Algorithm | Time | Space |
|---|---|---|
| Plain Minimax | O(b^d) | O(d) |
| Alpha-Beta | O(b^d) worst case, about O(b^(d/2)) with good move ordering | O(d) |

*b* = branching factor, *d* = search depth.

## Running

Requires **Python 3.7+**. It uses only the standard library.

```bash
python3 main.py
```

You play `O` and the AI plays `X`. Choose whether to go first, then enter a
square number (1–9) on each turn.

### Sample AI Turn Output

```
AI chose square 5
Alpha–Beta: <n> nodes, <t> ms
Plain Minimax: <n> nodes, <t> ms
Alpha-Beta Performance Improvement ≈ <p>%
```
