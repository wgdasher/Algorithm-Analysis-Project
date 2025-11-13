# Authors: Elizabeth Rodriguez, Ian Campbell, Chandler Armstrong, Garrett Dasher
# Minimax Tic-Tac-Toe with Alpha-Beta Pruning
# Objective: Compare the performance of a Tic-Tac-Toe game between a Minimax implementation and
# a Minimax with Alpha Beta Pruning for reduction in redundant recursion calls.

# Imports:
# dataclass used to simplify constructors
# List, Optional, Tuple used as type hints
# time used to measure how long things take to run
from dataclasses import dataclass
from typing import List, Optional, Tuple
import time

# tuples created to represent winning lines in game
# locations stored in values 0 - 8
# stored in List (dynamic array)
# Rows: (0,1,2), (3,4,5), (6,7,8)
# Cols: (0,3,6), (1,4,7), (2,5,8)
# Diagonals: (0,4,8), (2,4,6)
# Example board:
#   0 | 1 | 2
#   3 | 4 | 5
#   6 | 7 | 8
WIN_LINES = [
    (0,1,2), (3,4,5), (6,7,8), # Three horizontal rows
    (0,3,6), (1,4,7), (2,5,8), # Three vertical columns 
    (0,4,8), (2,4,6),           # Two Diagonal lines
]
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////
#                       Helper Functions
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////

# ----------------------------------------------------------------
# print_board function
# Outputs the state of the board in a structured format
# Parameters: List of 9 strings. Either 'X', 'O', or ' '
# Return: None: void function
def print_board(b: List[str]) -> None:
    # enumerate creates pair (i, c): i = index 1-8, c = cell value ('X','O', or ' ')
    # conditional expression:
    #   -if board cell = 'X' or 'O', do nothing
    #   -if board cell = ' ', output index(i + 1) to show position of cell for input
    cells = [c if c != ' ' else str(i+1) for i, c in enumerate(b)]

    # Prints the grid with separators in the form of f strings for easy concatenation
    print(f"\n {cells[0]} | {cells[1]} | {cells[2]}")
    print("---+---+---")
    print(f" {cells[3]} | {cells[4]} | {cells[5]}")
    print("---+---+---")
    print(f" {cells[6]} | {cells[7]} | {cells[8]}\n")

# ----------------------------------------------------------------
# winner function:
# declares if either the AI or the User has won
# Parameters: List of 9 strings representing board state:
#   -'X' - cell occupied by User
#   -'O' - cell occupied by AI
#   -' ' - empty cell, unoccupied
# returns: String -- either 'X' - Player won, 'O' - AI won, None if no winner
# Time Complexity: O(1)
# Space Complexity: O(1)
def winner(b: List[str]) -> Optional[str]:
    # Check that the first cell in this line is not empty
    # and that all three cells contain the same symbol
    # Checks each winning line
    for a, c, d in WIN_LINES:
        # Verify first cell is not empty AND all three cells match
        if b[a] != ' ' and b[a] == b[c] == b[d]: 
            # returns the symbol 'X' or 'O' of the winning player
            return b[a]
    # If the loop finishes with no matches, no winner is selected: return None
    return None

# ----------------------------------------------------------------
# is_full function:
# Checks if board is full or not full
# Parameters: List of strings representing the cells
# returns: boolean -- True if empty, False if not
# Time Complexity: O(n)
# Space Complexity: O(1)
def is_full(b):
    for cell in b:
        if cell == ' ':
            return False
    return True

# ----------------------------------------------------------------
# game_over function:
# Determines if the game has ended
# Parameters: List of 9 strings representing the board state
# Returns: boolean
# Time Complexity: O(n)
# Space Complexity: O(1)
def game_over(b: List[str]) -> bool:
    # calls winner function. if not none, a winner is determined
    if winner(b) is not None:
        return True # Someone has won
    if is_full(b):
        return True # Board is full but it's a draw
    return False # Game is still in progress

# ----------------------------------------------------------------
# legal_moves function:
# Returns valid move positions that the User or AI can choose
# Parameters: List of 9 strings representing the board state
# Returns: List[int] -- List of indices corresponding to legal moves
# Time Complexity: O(n)
# Space Complexity: O(k): stores up to n indices of empty cells
def legal_moves(b: List[str]) -> List[int]:
    moves = [] # list created to store valid moves
    # loops through cells of list b
    # enumerate(b) returns pairs of (i,c) i = index of cell, c = value of cell
    for i, c in enumerate(b):
        if c == ' ': # if cell empty, append to list.
            moves.append(i)
    return moves #returns moves List

# ----------------------------------------------------------------
# apply_move function
# Creates and returns new version of board with new move applied
# Parameters:
#   - b (list[str]): current board state
#   - index: position of the move to be updated
#   - mark: Players mark of either 'X' or 'O'
# Returns: List[str] (new board): new board list
# Time Complexity: O(n)
# Space Complexity: O(n): creates a list of equal size to input board
def apply_move(b: List[str], index: int, mark: str) -> List[str]:
    new_board = [] # Create List for new board
    for cell in b: # Copies each cell from the original board
        new_board.append(cell)

    new_board[index] = mark # Applies the players new move to board
    return new_board #returns board

# ----------------------------------------------------------------
# choose_first function
# Prompts the user to decide who moves first in the console game
# Returns: str -- "human" if player chooses to move first, "ai" if the player chooses to move second
# Time Complexity: O(1)
# Space Complexity: 0(1)
def choose_first() -> str:
    while True:
        # Prompt user for first turn preference
        ans = input("Do you want to go first? (y/n): ").strip().lower()
        # Return "human" if user wants to go first
        if ans in ("y", "yes"):
            return "human"
            # Return "ai" if user wants AI to go first
        if ans in ("n", "no"):
            return "ai"
        print("Please enter 'y' or 'n'.")
        # Loop continues if invalid input

# ----------------------------------------------------------------
# read_human_move function
# Reads and validates the players move from the console input
# Parameters: board(List[str]) - Current board state
# returns: int -- index of the valid cell chosen by the player
# Time Complexity: O(1)
# Space Complexity: O(1)
def read_human_move(board: List[str]) -> int:
    while True:
        try:
            s = input("Your move (1-9): ").strip()
            index = int(s) - 1
            if index not in range(9):
                print("Enter a number between 1 and 9.")
                continue
            if board[index] != ' ':
                print("That square is taken. Choose another.")
                continue
            return index
        except ValueError:
            print("Please enter a valid integer (1-9).")

# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////
#                       Minimax functions
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////

# ----------------------------------------------------------------
# evaluate_terminal function
# Evaluates the terminal state of the game from the AI's perspective.
# Used by the Minimax algorithm to assign values to leaf nodes in the game tree
#Parameters:
#   -b(List[str]) - current state of the board
#   -ai: Symbol for the AI player ('X' or 'O')
#   -depth: Current recursion depth in Minimax. Used to prioritize faster wins and delay losses
# Returns: Optional[int]
#   - +10 - depth = AI win (reward faster win)
#   - -10 + depth = AI loss (prefer slower loss)
#   - 0 = draw
#   - None = game is still in progress
# Time complexity: O(1)
# Space Complexity: 0(1)
def evaluate_terminal(b: List[str], ai: str, depth: int) -> Optional[int]:
    w = winner(b) #call winner function. check if game has a winner
    # If there's no winner and the board isn't full - game in progress, return None
    if w is None and not is_full(b):
        return None
    # If there's no winner but the board is full, game ends with a draw
    if w is None:
        return 0  # draw
    # There is a winner at this point
    # If the winner is the AI, return a positive score
    if w == ai:
        return 10 - depth
    else: # Otherwise, Player has won. Return negative score
        return -10 + depth

# ----------------------------------------------------------------
# minimax_plain function
# Recursive Minimax search without alpha-beta pruning
# Used as a correctness baseline and for comparing node counts against the pruned version (minimax_ab)
# Parameters:
#   -b(List[str]): Current board state
#   -depth: Current recursion depth of the game tree
#   -is_max: Ture if its the AI's turn, else false
#   -ai: AI players symbol ('X' or 'O')
#   -human: Human players symbol ('X' or 'O')
# Returns: Tuple[int, Optional[int],int]:
#   -score: Minimax evaluation at this node (AI perspective)
#   -move: Chosen move index at this node (None for terminals)
#   -nodes: Number of nodes explored in this subtree
# Time Complexity: 0(b^d) b = branching factor, d = remaining depth
# Space Complexity: O(d) due to recursion stack plus O91) locals per frame
def minimax_plain(b: List[str], depth: int, is_max: bool, ai: str, human: str) -> Tuple[int, Optional[int], int]:
    nodes = 1  # count this node as explored

    # Evaluate terminal states (win/loss/draw). If terminal, return None
    term = evaluate_terminal(b, ai, depth)
    if term is not None:
        # Terminal node: no move to return; nodes = 1 for this leaf
        return term, None, nodes

    best_move = None # track the best move found at this node

    if is_max:
        # AI's turn (Maximizer)
        best_val = -10_000 # Initialize to very low so any legal score will be higher
        for mv in legal_moves(b): #Try every legal move the AI can play
            child = apply_move(b, mv, ai) #Simulate AI playing at index mv
            # Recurse to opponent's turn (minimizer). We don't need child's chosen move here
            val, _, c_nodes = minimax_plain(child, depth+1, False, ai, human)
            nodes += c_nodes # Accumulate total nodes explored

            #keep the best score we could achieve and hte move that attains it
            if val > best_val:
                best_val = val
                best_move = mv
        # Return the best score we could achieve and the move that attains it
        return best_val, best_move, nodes
    else:       # Human's turn (Minimizer)
        best_val = 10_000 # Initialize to very high so any legal score will be lower
        for mv in legal_moves(b): # Try every legal move the human can play
            child = apply_move(b, mv, human) # Simulate human playing at index mv
            # Recurse to AI's turn (maximizer)
            val, _, c_nodes = minimax_plain(child, depth+1, True, ai, human)
            nodes += c_nodes # Accumulate total nodes explored

            # Keep the lowest-valued child (worst for the AI, Best for the human)
            if val < best_val:
                best_val = val
                best_move = mv
        #return the worst-case score (from AI's perspective) and the move that causes it
        return best_val, best_move, nodes

# ----------------------------------------------------------------
# minimax_ab function
# Recursive Minimax search with Alpha-Beta pruning
# This is the main decision algorithm. it returns:
#   - The best score from the Ai's perspective
#   - The associated move
#   - The number of nodes explored
# Alpha-beta eliminates branches that cannot affect the final choice, reducing the search dramatically
# Logic:
#   -If the position is terminal (win/loss/draw), return its score
#   -Otherwise, iterate legal moves and recurse:
#       -Maximizing (AI): keep the child with the highest score; update alpha.
#       -Minimizing (human): keep the child with the lowest score; update beta.
#   -Prune (cut off the loop) when beta <= alpha - remaining children. cannot improve the outcome for the player to move
# Notes:
#   -Alpha is a lower bound on the maximizer's achievable score.
#   -Beta is an upper bound on the minimizer's achievable score.
#   -As we search siblings, alpha is non-decreasing; beta is non-increasing
#   -Pruning never changes correctness; it only skips irrelevant branches
#
# Parameters:
#   -b(List[str]): Current board state
#   -depth: Current recursion depth in the game tree
#   -is_max: True if its AI's turn (maximize), else False (minimize)
#   -ai: AI player's symbol ('X' or 'O')
#   -human: Human player's symbol ('X' or 'O')
#   -alpha: best score the maximizer (AI) is guaranteed so far
#   -beta: best score the minimizer (Human) is guaranteed so far
#
# Returns: (Tuple[int, Optional[int], int])
#   - score: Minimax evaluation for this node (AI perspective)
#   - move: The move index chosen at this node (None for terminal)
#   -nodes: Total nodes explored in this subtree (for metrics)
#
# Time Complexity: Worst case = O(b^d) Often O(b^(d/2))
# Space Complexity: O(d): Recursion stack + 0(1) locals per frame
def minimax_ab(b: List[str], depth: int, is_max: bool, ai: str, human: str,
               alpha: int, beta: int) -> Tuple[int, Optional[int], int]:
    nodes = 1  # Count this node as explored
    term = evaluate_terminal(b, ai, depth)
    if term is not None:
        return term, None, nodes # leaf node: no move to report

    best_move = None # track the best move found from this node
    if is_max:  # AI's turn (maximize)
        best_val = -10_000 #start below any realistic score
        for mv in legal_moves(b): # consider every legal AI move
            child = apply_move(b, mv, ai) # Hypothetically apply the move
            # Recurse to the minimizing layer; pass current alpha/beta bounds
            val, _, c_nodes = minimax_ab(child, depth+1, False, ai, human, alpha, beta)
            nodes += c_nodes # Accumulate explored nodes

            # Keep the highest-valued child (best outcome for AI)
            if val > best_val:
                best_val = val
                best_move = mv

            # Update alpha: the maximizer's best so far lower bound
            alpha = max(alpha, best_val)

            # PRUNE: If the minimizer already has a better (<= beta) option elsewhere,
            # and our alpha exceeded beta, further siblings can't be chosen
            if beta <= alpha:
                break  # Cut off remaining moves (alpha-beta pruning)
        return best_val, best_move, nodes
    else:       # Human's turn (minimize)
        best_val = 10_000 #start above any realistic score
        for mv in legal_moves(b): # Consider every legal Human move
            child = apply_move(b, mv, human) # Hypothetically apply the move
            # Recurse to the maximizing layer; pass current alpha/beta bounds
            val, _, c_nodes = minimax_ab(child, depth+1, True, ai, human, alpha, beta)
            nodes += c_nodes # Accumulate explored nodes

            # Keep the lowest valued child (worst for AI, best for Human)
            if val < best_val:
                best_val = val
                best_move = mv
            # Update beta: the minimizer's best so far upper bound
            beta = min(beta, best_val)

            # PRUNE: If the maximizer already has a better (>= alpha) option elsewhere
            # and our beta fell below alpha, further siblings can't be chosen
            if beta <= alpha:
                break  # Cut off remaining moves (alpha-beta pruning)
        return best_val, best_move, nodes

# ----------------------------------------------------------------
# Dataclass Class
# Container for performance statistics gathered during AI move selection
# Primarily used to compare Alpha-Beta pruning against plain Minimax in terms of node expansions and wall-clock time.
# Fields:
#   -ab_nodes (int):
#       -Number of Game tree Nodes explored by the Alpha-Beta search for the current AI decision
#   -ab_time_ms (float):
#       -Elapsed time (in milliseconds) for the Alpha-Beta search for the current AI decision. Measured with time.perf_counter()
#   -mm_nodes (Optional[int]) [default: None]
#       -Number of nodes explored by the plain Minimax (un-pruned) search when run for comparison
#       None means the comparison was not executed.
#   -mm_time_ms (Optional[float]) [default: None]
#       -Elapsed time (in milliseconds) for the plain Minimax search.
#       None means the comparison was not executed.
@dataclass
class Metrics:
    ab_nodes: int #Alpha-Beta: node count
    ab_time_ms: float # Alpha-Beta: elapsed ms
    mm_nodes: Optional[int] = None # Plain Minimax: node count (optional)
    mm_time_ms: Optional[float] = None # Plain Minimax: elapsed ms (optional)

# ----------------------------------------------------------------
# best_ai_move function
# Computer the AI's move using Alpha-Beta and optionally run plain Minimax for side by side performance comparison
# Returns the chosen move index and a metrics record with timing
# And node-expansion counts per teh projects evaluation plan
# Parameters:
#   - board (List[str]): Current board state
#   - ai: AI player symbols ('X' or 'O')
#   - human: Human player symbol ('X' or 'O').
#   - compare_plain_minimax: if True, also run un-pruned Minimax to collect baseline metrics
#
# Returns: (Tuple[int, Metrics]):
#   - move: Index of the selected AI move. If the position is terminal and no moves exist, return -1 as a sentinel
#   - metrics: Metrics dataclass with Alpha-Beta timing and nodes; possibly also plain Minimax timing and nodes
#
# Notes:
#   - Alpha-Beta is the decision algorithm. plain Minimax is for comparison
#   - The score outputs are not used directly here. Only the chosen move and metrics are returned to the caller for play + reporting
#   - If both searches disagree on the exact move, it can still be fine: scores should match, but different best moves (symmetry / tie-breaks) may occur and remain optimal.
#
# Time Complexity: worst case 0(b^d)
# Space Complexity: 0(d) due to recursion depth. O(1) extra locals here.
def best_ai_move(board: List[str], ai: str, human: str, compare_plain_minimax: bool = True) -> Tuple[int, Metrics]:
    # Alpha-Beta (primary)
    t0 = time.perf_counter() #start time
    # Run alpha-Beta from root: AI to move (is_max=True), wide initial bounds
    score, move, nodes = minimax_ab(board, depth=0, is_max=True, ai=ai, human=human, alpha=-10_000, beta=10_000)
    t1 = time.perf_counter() # Stop timer
    ab_ms = (t1 - t0) * 1000.0 # Convert seconds to milliseconds

    # Optional plain Minimax (baseline)
    mm_nodes = None
    mm_ms = None
    if compare_plain_minimax:
        t2 = time.perf_counter()
        # Un-pruned Minimax for metrics; same root conditions
        score2, move2, nodes2 = minimax_plain(board, depth=0, is_max=True, ai=ai, human=human)
        t3 = time.perf_counter()
        mm_ms = (t3 - t2) * 1000.0
        mm_nodes = nodes2

    # Fallback safety
    if move is None:
        # Should not happen unless teh position is terminal or inputs are invalid
        # Fall back to the first legal move if any. else return -1
        lm = legal_moves(board)
        move = lm[0] if lm else -1

    # Package metrics and return
    metrics = Metrics(ab_nodes=nodes, ab_time_ms=ab_ms, mm_nodes=mm_nodes, mm_time_ms=mm_ms)
    return move, metrics


# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////
#                       Driver Section
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////

# ----------------------------------------------------------------
# play function
# Runs the console game loop
# Returns: void
def play():
    # Title and role reminder
    print("\n=== Tic-Tac-Toe (Minimax + Alpha-Beta) ===")
    print("You are 'O' by default. AI is 'X'.\n")

    # Initialize empty 3x3 board and assign symbols
    board = [' '] * 9
    ai, human = 'X', 'O'

    # Ask user who should go first, return "human" or "ai"
    turn = choose_first()

    # Render the initial empty board with numbered hints
    print_board(board)

    # Main game loop: continue until a win or full board (draw)
    while not game_over(board):
        if turn == "human":  # Human's turn
            mv = read_human_move(board) # Get a legal index
            board = apply_move(board, mv, human) # Non-destructive apply
            print_board(board) # Re-render board
            turn = "ai" # Pass control to AI
        else: # AI's turn
            print("AI is thinking...")

            # Compute AI move using Alpha-Beta (and optionally plain Minimax for metrics)
            move, m = best_ai_move(board, ai=ai, human=human, compare_plain_minimax=True)

            #Apply AI move and re-render
            board = apply_move(board, move, ai)
            print_board(board)

            # Evaluation Metrics
            print(f"AI chose square {move+1}")  # adjusted to be human friendly (+1)
            print(f"Alpha–Beta: {m.ab_nodes} nodes, {m.ab_time_ms:.3f} ms")
            if m.mm_nodes is not None:
                print(f"Plain Minimax: {m.mm_nodes} nodes, {m.mm_time_ms:.3f} ms")
                if m.mm_nodes > 0:
                    savings = 100.0 * (1.0 - (m.ab_nodes / m.mm_nodes))
                    print(f"Alpha-Beta Space Improvement ≈ {savings:.1f}%")
            print()
            turn = "human" # passes control back to User

        # early exit check
        if game_over(board):
            break

    # Game is over
    w = winner(board)
    if w is None:
        print("Result: Draw.")
    elif w == ai:
        print("Result: AI (X) wins.")
    else:
        print("Result: You (O) win!")

# main function
# Return: Void
if __name__ == "__main__":
    play()
