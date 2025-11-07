#!/usr/bin/env python3
# Tic-Tac-Toe with Minimax and Alpha-Beta Pruning (rough prototype)
# Adheres to project proposal: decision tree search, alpha-beta pruning, node counts, timing.

#Prototype------------------------------------------------------------------------

from dataclasses import dataclass
from typing import List, Optional, Tuple
import time

# ──────────────────────────────────────────────────────────────────────────────
# Basic Board Utilities
# Board is a simple list of 9 cells: ['X','O',' '] with indices 0..8
# Rows: (0,1,2), (3,4,5), (6,7,8)
# Cols: (0,3,6), (1,4,7), (2,5,8)
# Diagonals: (0,4,8), (2,4,6)
# ──────────────────────────────────────────────────────────────────────────────
WIN_LINES = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6),
]

def print_board(b: List[str]) -> None:
    cells = [c if c != ' ' else str(i+1) for i, c in enumerate(b)]
    print(f"\n {cells[0]} | {cells[1]} | {cells[2]}")
    print("---+---+---")
    print(f" {cells[3]} | {cells[4]} | {cells[5]}")
    print("---+---+---")
    print(f" {cells[6]} | {cells[7]} | {cells[8]}\n")

def winner(b: List[str]) -> Optional[str]:
    """Return 'X' or 'O' if someone has won, else None."""
    for a, c, d in WIN_LINES:
        if b[a] != ' ' and b[a] == b[c] == b[d]:
            return b[a]
    return None

def is_full(b: List[str]) -> bool:
    return all(cell != ' ' for cell in b)

def game_over(b: List[str]) -> bool:
    return winner(b) is not None or is_full(b)

def legal_moves(b: List[str]) -> List[int]:
    return [i for i, c in enumerate(b) if c == ' ']

def apply_move(b: List[str], idx: int, mark: str) -> List[str]:
    nb = b.copy()
    nb[idx] = mark
    return nb

# ──────────────────────────────────────────────────────────────────────────────
# Evaluation
# We evaluate terminal states only for Tic-Tac-Toe optimal play (solved game).
# Score from AI's perspective (ai='X' or 'O'):
#   +10 - depth : AI win (prefer faster wins)
#   -10 + depth : AI loss (prefer slower losses)
#   0           : draw
# Depth tiebreaks help pick quicker wins & avoid shallow traps.
# ──────────────────────────────────────────────────────────────────────────────
def evaluate_terminal(b: List[str], ai: str, depth: int) -> Optional[int]:
    w = winner(b)
    if w is None and not is_full(b):
        return None  # non-terminal
    if w is None:
        return 0  # draw
    # Win/loss relative to AI
    if w == ai:
        return 10 - depth
    else:
        return -10 + depth

# ──────────────────────────────────────────────────────────────────────────────
# Minimax (plain) — for comparison & correctness checking
# Returns (score, move, nodes_expanded)
# ──────────────────────────────────────────────────────────────────────────────
def minimax_plain(b: List[str], depth: int, is_max: bool, ai: str, human: str) -> Tuple[int, Optional[int], int]:
    nodes = 1  # count current node
    term = evaluate_terminal(b, ai, depth)
    if term is not None:
        return term, None, nodes

    best_move = None
    if is_max:  # AI's turn
        best_val = -10_000
        for mv in legal_moves(b):
            child = apply_move(b, mv, ai)
            val, _, c_nodes = minimax_plain(child, depth+1, False, ai, human)
            nodes += c_nodes
            if val > best_val:
                best_val = val
                best_move = mv
        return best_val, best_move, nodes
    else:       # Human's turn
        best_val = 10_000
        for mv in legal_moves(b):
            child = apply_move(b, mv, human)
            val, _, c_nodes = minimax_plain(child, depth+1, True, ai, human)
            nodes += c_nodes
            if val < best_val:
                best_val = val
                best_move = mv
        return best_val, best_move, nodes

# ──────────────────────────────────────────────────────────────────────────────
# Minimax with Alpha-Beta Pruning — main algorithm per proposal
# Returns (score, move, nodes_expanded)
# ──────────────────────────────────────────────────────────────────────────────
def minimax_ab(b: List[str], depth: int, is_max: bool, ai: str, human: str,
               alpha: int, beta: int) -> Tuple[int, Optional[int], int]:
    nodes = 1  # count current node
    term = evaluate_terminal(b, ai, depth)
    if term is not None:
        return term, None, nodes

    best_move = None
    if is_max:  # AI's turn (maximize)
        best_val = -10_000
        for mv in legal_moves(b):
            child = apply_move(b, mv, ai)
            val, _, c_nodes = minimax_ab(child, depth+1, False, ai, human, alpha, beta)
            nodes += c_nodes
            if val > best_val:
                best_val = val
                best_move = mv
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break  # prune
        return best_val, best_move, nodes
    else:       # Human's turn (minimize)
        best_val = 10_000
        for mv in legal_moves(b):
            child = apply_move(b, mv, human)
            val, _, c_nodes = minimax_ab(child, depth+1, True, ai, human, alpha, beta)
            nodes += c_nodes
            if val < best_val:
                best_val = val
                best_move = mv
            beta = min(beta, best_val)
            if beta <= alpha:
                break  # prune
        return best_val, best_move, nodes

# ──────────────────────────────────────────────────────────────────────────────
# AI Move Decision Wrapper
#   - Uses Alpha-Beta as default (fast)
#   - Optionally computes plain minimax too for comparison
# ──────────────────────────────────────────────────────────────────────────────
@dataclass
class Metrics:
    ab_nodes: int
    ab_time_ms: float
    mm_nodes: Optional[int] = None
    mm_time_ms: Optional[float] = None

def best_ai_move(board: List[str], ai: str, human: str, compare_plain_minimax: bool = True) -> Tuple[int, Metrics]:
    # Alpha-Beta (primary)
    t0 = time.perf_counter()
    score, move, nodes = minimax_ab(board, depth=0, is_max=True, ai=ai, human=human, alpha=-10_000, beta=10_000)
    t1 = time.perf_counter()
    ab_ms = (t1 - t0) * 1000.0

    mm_nodes = None
    mm_ms = None
    if compare_plain_minimax:
        t2 = time.perf_counter()
        score2, move2, nodes2 = minimax_plain(board, depth=0, is_max=True, ai=ai, human=human)
        t3 = time.perf_counter()
        mm_ms = (t3 - t2) * 1000.0
        mm_nodes = nodes2
        # Sanity: both algorithms should recommend equivalent outcomes
        # (moves can differ due to symmetry/tiebreaks but scores should match)
        # We won't enforce equality here—just report.

    if move is None:
        # Should not happen unless terminal/non-legal call
        # Fallback to any legal move
        lm = legal_moves(board)
        move = lm[0] if lm else -1

    metrics = Metrics(ab_nodes=nodes, ab_time_ms=ab_ms, mm_nodes=mm_nodes, mm_time_ms=mm_ms)
    return move, metrics

# ──────────────────────────────────────────────────────────────────────────────
# Interactive Console Game
# ──────────────────────────────────────────────────────────────────────────────
def choose_first() -> str:
    while True:
        ans = input("Do you want to go first? (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return "human"
        if ans in ("n", "no"):
            return "ai"
        print("Please enter 'y' or 'n'.")

def read_human_move(board: List[str]) -> int:
    while True:
        try:
            s = input("Your move (1-9): ").strip()
            idx = int(s) - 1
            if idx not in range(9):
                print("Enter a number between 1 and 9.")
                continue
            if board[idx] != ' ':
                print("That square is taken. Choose another.")
                continue
            return idx
        except ValueError:
            print("Please enter a valid integer (1-9).")

def play():
    print("\n=== Tic-Tac-Toe (Minimax + Alpha-Beta) ===")
    print("You are 'O' by default. AI is 'X'.\n")

    board = [' '] * 9
    ai, human = 'X', 'O'
    turn = choose_first()

    print_board(board)

    while not game_over(board):
        if turn == "human":
            mv = read_human_move(board)
            board = apply_move(board, mv, human)
            print_board(board)
            turn = "ai"
        else:
            print("AI is thinking...")
            move, m = best_ai_move(board, ai=ai, human=human, compare_plain_minimax=True)
            board = apply_move(board, move, ai)
            print_board(board)

            # Report metrics for evaluation (Proposal: compare nodes before/after pruning)
            print(f"AI chose square {move+1}")
            print(f"Alpha–Beta: {m.ab_nodes} nodes, {m.ab_time_ms:.3f} ms")
            if m.mm_nodes is not None:
                print(f"Plain Minimax: {m.mm_nodes} nodes, {m.mm_time_ms:.3f} ms")
                if m.mm_nodes > 0:
                    savings = 100.0 * (1.0 - (m.ab_nodes / m.mm_nodes))
                    print(f"Pruning saved ≈ {savings:.1f}% nodes")
            print()
            turn = "human"

        if game_over(board):
            break

    w = winner(board)
    if w is None:
        print("Result: Draw.")
    elif w == ai:
        print("Result: AI (X) wins.")
    else:
        print("Result: You (O) win!")

if __name__ == "__main__":
    play()
