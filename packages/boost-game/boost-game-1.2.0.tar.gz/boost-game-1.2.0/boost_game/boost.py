"""
Boost game implementation, AI, and command line interface.
"""

from argparse import ArgumentParser
from enum import Enum
from math import inf
from math import floor
import random
from sys import stderr, stdout
from time import time
from heapq import heapify, heappop, heappush

from .rulesets import rulesets, DEFAULT_RULESET

TERMCOLOR = True
try:
    from termcolor import colored
except ImportError:
    TERMCOLOR = False

VERBOSE = None
COLOR = None

EMPTY_CELL_SHORT = "."
EMPTY_CELL_LONG = ". "

DRAGON_OWNER = 0
OWNER_COLORS = ["green", "red", "blue", "yellow", "magenta", "cyan", "white"]

# Static evaluation scores
PAWN_SCORE = 20
KNIGHT_SCORE = 30
TOWER_SCORE = 80
CONSTRUCTION_CIRCLE_SCORE = 10
DRAGON_CIRCLE_SCORE = 20
DRAGON_CLAIM_SCORE = 5
ACTIVE_PAWN_SCORE = 1
ACTIVE_KNIGHT_SCORE = 2
MOBILE_KNIGHT_SCORE = 1  # Multiplied by boost


def distance(row1, col1, row2, col2):
    # Manhattan distance
    return abs(row2 - row1) + abs(col2 - col1)


def cell_distance(cell1, cell2):
    return distance(cell1.row, cell1.col, cell2.row, cell2.col)


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        # Assumes a board of size 9
        if 0 <= self.row < 9 and 0 <= self.col < 9:
            return chr(self.col + ord("a")) + str(9 - self.row)
        return f"{self.col},{self.row}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.row == other.row and self.col == other.col
        return False

    def __hash__(self):
        return hash((self.row, self.col))

    @property
    def neighbors(self):
        return [
            Cell(self.row - 1, self.col),
            Cell(self.row + 1, self.col),
            Cell(self.row, self.col - 1),
            Cell(self.row, self.col + 1),
        ]


class PieceType:
    def __init__(self, name, symbol, score=0):
        self.name = name
        self.symbol = symbol
        self.score = score


class PieceTypes(Enum):
    DRAGON = PieceType("Dragon", "D")
    PAWN = PieceType("Pawn", "P", PAWN_SCORE)
    KNIGHT = PieceType("Knight", "K", KNIGHT_SCORE)
    TOWER = PieceType("Tower", "T", TOWER_SCORE)


class Piece:
    def __init__(self, owner, piece_type):
        # assert isinstance(owner, int)
        # assert owner >= 0
        # assert piece_type in PieceTypes
        # assert (owner == DRAGON_OWNER) == (piece_type is PieceTypes.DRAGON)
        self.owner = owner
        self.piece_type = piece_type

    def __str__(self):
        return str(self.piece_type.value.symbol) + str(self.owner)

    def __eq__(self, other):
        if isinstance(other, Piece):
            return (
                self.owner == other.owner
                and self.piece_type is other.piece_type
            )
        return False

    def __hash__(self):
        return hash((self.owner, self.piece_type))

    @property
    def name(self):
        return self.piece_type.value.name

    @property
    def symbol(self):
        return self.piece_type.value.symbol

    @property
    def color(self):
        return OWNER_COLORS[self.owner]

    @property
    def valid(self):
        return (
            self.owner >= 0
            and self.piece_type in PieceTypes
            and (self.owner == DRAGON_OWNER)
            == (self.piece_type is PieceTypes.DRAGON)
        )

    @staticmethod
    def parse(string):
        for piece_type in PieceTypes:
            if piece_type.value.symbol == string[0]:
                return Piece(int(string[1]), piece_type)
        return None


class Move:
    def __init__(self, start, end=None):
        self.start = start
        self.end = end if end is not None else start

    def __str__(self):
        return str(self.start) + str(self.end)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.start == other.start and self.end == other.end
        return False

    def __hash__(self):
        return hash((self.start, self.end))

    @property
    def distance(self):
        return cell_distance(self.start, self.end)


class Path:
    def __init__(self, path, heuristic=0):
        self.path = path
        self.heuristic = heuristic

    @property
    def start(self):
        return self.path[0] if self.path else None

    @property
    def end(self):
        return self.path[-1] if self.path else None

    @property
    def total_heuristic(self):
        return len(self.path) + self.heuristic

    def __lt__(self, other):
        return self.total_heuristic < other.total_heuristic

    def __gt__(self, other):
        return self.total_heuristic > other.total_heuristic

    def __eq__(self, other):
        return self.total_heuristic == other.total_heuristic

    def __len__(self):
        return len(self.path) - 1

    def __contains__(self, item):
        return item in self.path

    def __str__(self):
        return str(self.path)


class Board:
    def __init__(self, ruleset, board=None):
        self.ruleset = ruleset
        self.board = Board.empty(ruleset.width, ruleset.height)
        if board:
            # Deep copy
            self.owners = 0
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    if board[row][col] is not None:
                        self.board[row][col] = board[row][col]
                        self.owners = max(self.owners, board[row][col].owner)
            # Account for the dragon owner
            self.owners += 1
        else:
            self.load(ruleset.board_string)
            self.place_dragons(ruleset.dragons)
        self.forfeited = set()
        self.piece_counts_cache = None

    @property
    def width(self):
        return len(self.board[0])

    @property
    def height(self):
        return len(self.board)

    @staticmethod
    def empty(width, height):
        return [[None for col in range(width)] for row in range(height)]

    def copy(self):
        new_board = Board(self.ruleset, self.board)
        new_board.forfeited = self.forfeited
        return new_board

    def __str__(self):
        string = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col]:
                    string += str(self.board[row][col])
                else:
                    string += EMPTY_CELL_LONG
                string += " "
            string += "\n"
        # Slice off trailing newline
        return string[:-1]

    def __hash__(self):
        return hash(str(self))

    @property
    def cell_width(self):
        return 2 if COLOR or self.owners <= 3 else 3

    @property
    def pretty(self):
        file_labels = "  "
        for col in range(len(self.board[0])):
            file_labels += f"{chr(col + 65)}" + (self.cell_width - 1) * " "
        string = file_labels + "\n"
        horizontal_border = "─" * (self.cell_width * len(self.board[0]) - 1)
        string += f" ┌{horizontal_border}┐\n"
        for row in range(len(self.board)):
            row_string = f"{len(self.board) - row}"
            string += row_string + "│"
            for col in range(len(self.board[row])):
                piece = self.board[row][col]
                if piece:
                    if COLOR:
                        string += colored(piece.symbol.upper(), piece.color)
                    else:
                        string += self.format_piece(piece)
                else:
                    if self.cell_width == 2:
                        string += EMPTY_CELL_SHORT
                    else:
                        string += EMPTY_CELL_LONG
                if col < len(self.board[row]) - 1:
                    string += " "
                else:
                    string += "│"
            string += row_string + "\n"
        string += f" └{horizontal_border}┘\n"
        string += file_labels
        return string

    @property
    def cells(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                yield Cell(row, col)

    def __iter__(self):
        yield from self.cells

    @property
    def tower_cells(self):
        for row in range(1, len(self.board) - 1):
            for col in range(1, len(self.board[row]) - 1):
                yield Cell(row, col)

    @property
    def piece_counts(self):
        if self.piece_counts_cache is not None:
            return self.piece_counts_cache

        piece_counts = {}
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                piece = self.get_piece(Cell(row, col))
                if piece is not None:
                    if piece in piece_counts:
                        piece_counts[piece] += 1
                    else:
                        piece_counts[piece] = 1
        self.piece_counts_cache = piece_counts
        return piece_counts

    def get_owned_pieces(self, owners):
        if not isinstance(owners, list):
            owners = [owners]
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                piece = self.get_piece(Cell(row, col))
                if piece is not None and piece.owner in owners:
                    yield piece

    def parse_cell(self, string):
        row_string = string[0]
        col_string = string[1]
        row = self.height - int(col_string)
        col = ord(row_string.upper()) - 65
        return Cell(row, col)

    def format_cell(self, cell):
        return f"{chr(cell.col + 65)}{str(self.height - cell.row)}"

    def parse_move(self, string):
        start = self.parse_cell(string[0:2])
        end = start
        if len(string) == 4:
            end = self.parse_cell(string[2:4])
        return Move(start, end)

    def format_move(self, move):
        return self.format_cell(move.start) + self.format_cell(move.end)

    def format_piece(self, piece):
        if self.owners > 3:
            return str(piece)
        symbol = piece.piece_type.value.symbol
        return symbol.lower() if piece.owner == 1 else symbol.upper()

    def load(self, string):
        row, col = 0, 0
        self.owners = 0
        for line in string.splitlines():
            if row < len(self.board):
                for (piece_type_string, owner_string) in zip(
                    line[0::], line[1::]
                ):
                    if col < len(self.board[row]):
                        piece_string = piece_type_string + owner_string
                        piece = Piece.parse(piece_string)
                        self.board[row][col] = piece
                        if piece:
                            if piece.owner > self.owners:
                                self.owners = piece.owner
                        if piece or piece_string == EMPTY_CELL_LONG:
                            col += 1

            # Ignore blank lines
            if col > 0:
                row += 1
                col = 0

        # Account for the dragon owner
        self.owners += 1

    def place_dragons(self, dragons):
        assert dragons >= 0
        if dragons == 0:
            return

        middle_row = floor(self.height / 2)
        middle_col = floor(self.width / 2)
        available_cells = []
        for row in range(self.height):
            for col in range(middle_col - 1):
                if not self.board[row][col]:
                    available_cells.append(Cell(row, col))

        # To place an odd number of dragons, we have to place one in the
        # middle, since it's the only non-mirrored cell
        remaining_dragons = dragons
        dragon = Piece(DRAGON_OWNER, PieceTypes.DRAGON)
        if dragons % 2 != 0:
            if self.board[middle_row][middle_col]:
                raise ValueError(
                    "Cannot place an odd number of dragons on this board "
                    "(center must be unoccupied)"
                )
            self.board[middle_row][middle_col] = dragon
            remaining_dragons -= 1

        while remaining_dragons > 0:
            cell = random.choice(available_cells)
            available_cells.remove(cell)

            mirror_row = self.height - cell.row - 1
            mirror_col = self.width - cell.col - 1
            mirror_cell = Cell(mirror_row, mirror_col)
            if not self.get_piece(mirror_cell):
                self.set_piece(cell, dragon)
                self.set_piece(mirror_cell, dragon)
                remaining_dragons -= 2

    def in_bounds(self, cell):
        return 0 <= cell.row < self.height and 0 <= cell.col < self.width

    def on_border(self, cell):
        return cell.row in (0, self.height - 1) and cell.col in (
            0,
            self.width - 1,
        )

    def inside_border(self, cell):
        return 0 < cell.row < self.height - 1 and 0 < cell.col < self.width - 1

    def get_piece(self, cell):
        return self.board[cell.row][cell.col] if self.in_bounds(cell) else None

    def set_piece(self, cell, piece):
        if self.in_bounds(cell):
            self.board[cell.row][cell.col] = piece

    def get_boost(self, cell):
        boost = 1
        for neighbor in cell.neighbors:
            if self.get_piece(neighbor):
                boost += 1
        return boost

    def find_path(self, source, destination, target_distance=None):
        # A* with Manhattan distance heuristic (cell_distance)
        worklist = [Path([source], cell_distance(source, destination))]
        heapify(worklist)

        while len(worklist) > 0:
            path = heappop(worklist)

            if path.end == destination and (
                target_distance is None or len(path) == target_distance
            ):
                return path

            if len(path) == target_distance:
                continue

            for neighbor in path.end.neighbors:
                if not self.in_bounds(neighbor) or neighbor in path:
                    continue

                piece = self.get_piece(neighbor)
                if piece is not None:
                    continue

                heappush(
                    worklist,
                    Path(
                        path.path + [neighbor],
                        len(path) + 1 + cell_distance(neighbor, destination),
                    ),
                )
        return None

    def path_exists(self, move):
        return (
            self.find_path(move.start, move.end, self.get_boost(move.start))
            is not None
        )

    def can_move_dragon(self, cell, owner):
        assert owner != DRAGON_OWNER
        assert self.get_piece(cell).piece_type is PieceTypes.DRAGON
        for neighbor in cell.neighbors:
            neighbor_piece = self.get_piece(neighbor)
            if neighbor_piece and neighbor_piece.owner == owner:
                return True
        return False

    def can_build_tower(self, cell, owner):
        if self.get_piece(cell):
            return False

        for neighbor in cell.neighbors:
            neighbor_piece = self.get_piece(neighbor)
            if not neighbor_piece or neighbor_piece.owner != owner:
                return False

        owner_towers = self.piece_counts.get(Piece(owner, PieceTypes.TOWER), 0)
        return owner_towers < self.ruleset.max_towers

    def can_promote_knight(self, cell, owner):
        piece = self.get_piece(cell)
        if (
            not piece
            or piece.owner != owner
            or piece.piece_type != PieceTypes.PAWN
        ):
            return False

        piece_counts = self.piece_counts
        knight = Piece(owner, PieceTypes.KNIGHT)
        tower = Piece(owner, PieceTypes.TOWER)
        if (
            knight in piece_counts
            and tower in piece_counts
            and piece_counts[knight]
            >= piece_counts[tower] * self.ruleset.knights_per_tower
        ):
            return False

        for neighbor in cell.neighbors:
            neighbor_piece = self.get_piece(neighbor)
            if (
                neighbor_piece
                and neighbor_piece.owner == owner
                and neighbor_piece.piece_type is PieceTypes.TOWER
            ):
                return True

        return False

    def get_move_error(self, move, owner, skip_pathfinding=False):
        if move.start == move.end:
            if self.can_build_tower(move.start, owner):
                return ""
            if self.can_promote_knight(move.start, owner):
                return ""
            return (
                "You cannot build a tower here nor promote a pawn to a "
                "knight here."
            )

        piece = self.get_piece(move.start)
        destination = self.get_piece(move.end)
        boost = self.get_boost(move.start)
        if not piece:
            return (
                f"There is no piece at {self.format_cell(move.start)} "
                "to move."
            )
        if piece.piece_type is PieceTypes.DRAGON and not self.can_move_dragon(
            move.start, owner
        ):
            return (
                f"To move the {piece.name} at "
                f"{self.format_cell(move.start)}, "
                "you must have an adjacent piece."
            )
        if piece.owner not in (owner, DRAGON_OWNER):
            return (
                f"You are not the owner of the {piece.name} at "
                f"{self.format_cell(move.start)}."
            )
        if piece.piece_type is PieceTypes.TOWER:
            return "Towers cannot move."
        if not skip_pathfinding and not self.path_exists(move):
            return f"You must move this piece exactly {boost} cell(s)."
        if not self.in_bounds(move.end):
            return f"{self.format_cell(move.end)} is out of bounds."
        if destination and piece.piece_type != PieceTypes.KNIGHT:
            return f"A {piece.name} cannot capture pieces directly."
        if destination and destination.owner == owner:
            return "You cannot capture your own piece."
        if destination and destination.piece_type is PieceTypes.DRAGON:
            return "Dragons cannot be captured."
        return ""

    def is_valid(self, move, owner, skip_pathfinding=False):
        return not self.get_move_error(move, owner, skip_pathfinding)

    def capture(self, cell, owner):
        # Processes captures made by the piece moved to the given cell by the
        # given owner
        piece = self.get_piece(cell)
        assert piece
        assert (
            piece.piece_type is PieceTypes.PAWN
            or piece.piece_type is PieceTypes.DRAGON
        )
        captures = 0
        for neighbor in cell.neighbors:
            neighbor_piece = self.get_piece(neighbor)
            if (
                neighbor_piece
                and neighbor_piece.owner != owner
                and neighbor_piece.owner != DRAGON_OWNER
            ):
                flank = Cell(
                    neighbor.row + (neighbor.row - cell.row),
                    neighbor.col + (neighbor.col - cell.col),
                )
                flanking_piece = self.get_piece(flank)
                if flanking_piece and flanking_piece.owner in (
                    owner,
                    DRAGON_OWNER,
                ):
                    self.set_piece(neighbor, None)
                    captures += 1
        return captures

    @property
    def defeated(self):
        defeated = set()
        piece_counts = self.piece_counts
        for owner in range(self.owners):
            if owner != DRAGON_OWNER:
                owner_total = 0
                for piece_type in PieceTypes:
                    count = piece_counts.get(Piece(owner, piece_type))
                    if count:
                        owner_total += count
                owner_towers = piece_counts.get(Piece(owner, PieceTypes.TOWER))
                tower_victory_possible = (
                    self.ruleset.tower_victory
                    and owner_towers
                    and owner_total > owner_towers
                )
                if (
                    owner_total < self.ruleset.min_pieces
                    and not tower_victory_possible
                ):
                    defeated.add(owner)
        return defeated | self.forfeited

    @property
    def capture_winner(self):
        defeated = self.defeated
        # 2 corresponds to the dragon owner + one remaining player
        if self.owners - len(defeated) == 2:
            for candidate in range(self.owners):
                if candidate != DRAGON_OWNER and candidate not in defeated:
                    return candidate
        return None

    def is_dragon_tower(self, cell):
        tower = self.get_piece(cell)
        if not tower or tower.piece_type is not PieceTypes.TOWER:
            return False

        for neighbor in cell.neighbors:
            dragon = self.get_piece(neighbor)
            if dragon is None or dragon.piece_type != PieceTypes.DRAGON:
                return False

        return True

    def move(self, move, owner, apply=True):
        if not apply:
            new_board = self.copy()
            new_board.move(move, owner, apply=True)
            return new_board

        # Clear cached piece counts since the board may change
        self.piece_counts_cache = None

        if move.start == move.end:
            piece = self.get_piece(move.start)
            if not piece:
                # Build tower
                self.board[move.start.row][move.start.col] = Piece(
                    owner, PieceTypes.TOWER
                )
            else:
                # Promote knight
                self.board[move.start.row][move.start.col] = Piece(
                    owner, PieceTypes.KNIGHT
                )
        else:
            # Move piece
            piece = self.board[move.start.row][move.start.col]
            target = self.board[move.end.row][move.end.col]
            self.set_piece(move.start, None)
            self.set_piece(move.end, piece)

            captures = 0
            # Check for direct knight capture
            if piece.piece_type is PieceTypes.KNIGHT and target:
                captures = 1
            # Check for pawn or dragon capture
            elif (
                piece.piece_type is PieceTypes.PAWN
                or piece.piece_type is PieceTypes.DRAGON
            ):
                captures = self.capture(move.end, owner)

            # Check for capture victory if any pieces were captured
            if captures > 0:
                winner = self.capture_winner
                if winner:
                    return winner

            # Check for tower victory if a dragon was moved
            # Must be checked after captures in case a player captured a tower
            # by moving a fourth dragon next to it
            if (
                self.ruleset.tower_victory
                and piece.piece_type is PieceTypes.DRAGON
            ):
                for neighbor in move.end.neighbors:
                    if self.is_dragon_tower(neighbor):
                        return self.get_piece(neighbor).owner
        return None

    def get_piece_moves(self, cell, owner=None):
        # Ensure that a piece is present and movable
        piece = self.get_piece(cell)
        if piece is None or piece.piece_type is PieceTypes.TOWER:
            return set()

        # Ensure that the owner can actually move this piece
        if owner is None:
            owner = piece.owner
        elif owner != piece.owner and not (
            piece.owner == DRAGON_OWNER and self.can_move_dragon(cell, owner)
        ):
            return set()

        # Breadth-first search to find all possible moves
        boost = self.get_boost(cell)
        moves = set()
        worklist = [Path([cell])]
        heapify(worklist)

        while len(worklist) > 0:
            path = heappop(worklist)

            if len(path) > boost:
                return moves

            if len(path) == boost:
                move = Move(path.start, path.end)
                if self.is_valid(move, owner, skip_pathfinding=True):
                    moves.add(move)
                continue

            for neighbor in path.end.neighbors:
                if not self.in_bounds(neighbor) or neighbor in path:
                    continue

                piece = self.get_piece(neighbor)
                if piece is not None:
                    continue

                heappush(worklist, Path(path.path + [neighbor]))
        return moves

    def get_owner_moves(self, owner):
        # Use sets to prevent duplicates, but also for a pseudo-random ordering
        construction_moves = set()
        promotion_moves = set()
        normal_moves = set()
        for cell in self.cells:
            normal_moves |= self.get_piece_moves(cell, owner)
            if self.can_build_tower(cell, owner):
                construction_moves.add(Move(cell))
            elif self.can_promote_knight(cell, owner):
                promotion_moves.add(Move(cell))

        # Consider moves that create towers and knights first, as they are
        # likely to yield higher scores (best-first search)
        return (
            list(construction_moves)
            + list(promotion_moves)
            + list(normal_moves)
        )

    def mobility_score(self, cell):
        piece = self.get_piece(cell)
        if not piece:
            return 0

        if piece.piece_type is PieceTypes.PAWN and self.inside_border(cell):
            return ACTIVE_PAWN_SCORE

        if piece.piece_type is not PieceTypes.KNIGHT:
            return 0

        boost = self.get_boost(cell)
        score = 0
        if 1 < boost < 5:
            score += MOBILE_KNIGHT_SCORE * boost
        if self.inside_border(cell):
            score += ACTIVE_KNIGHT_SCORE
        return score

    def count_dragon_circle(self, cell):
        piece = self.get_piece(cell)
        if piece.piece_type is not PieceTypes.TOWER:
            return 0

        dragon_circle = 0
        for neighbor in cell.neighbors:
            neighbor_piece = self.get_piece(neighbor)
            if (
                neighbor_piece
                and neighbor_piece.piece_type == PieceTypes.DRAGON
            ):
                dragon_circle += 1
        return dragon_circle

    def count_construction_circle(self, cell, owner):
        if not self.inside_border(cell):
            return 0

        piece = self.get_piece(cell)
        if piece:
            return 0

        # Don't award any points if there is just one piece in the "circle"
        construction_circle = -1
        for neighbor in cell.neighbors:
            neighbor_piece = self.get_piece(neighbor)
            if neighbor_piece:
                if neighbor_piece.owner == owner:
                    construction_circle += 1
                else:
                    construction_circle -= 1
        return max(construction_circle, 0)

    def count_dragon_claims(self, cell, owner):
        piece = self.get_piece(cell)
        if piece.piece_type is not PieceTypes.DRAGON:
            return 0

        dragon_claims = 0
        for neighbor in cell.neighbors:
            neighbor_piece = self.get_piece(neighbor)
            claimants = set()
            if (
                neighbor_piece
                and neighbor_piece.piece_type != PieceTypes.DRAGON
            ):
                claimants.add(neighbor_piece.owner)
            for claimant in claimants:
                if claimant == owner:
                    dragon_claims += 1
                else:
                    dragon_claims -= 1
        return dragon_claims

    def evaluate(self, owner):
        score = 0
        tower_count = 0
        max_dragon_circle = 0
        max_construction_circle = 0
        dragon_claims = 0
        owner_pieces = [0] * self.owners
        for cell in self.cells:
            piece = self.get_piece(cell)
            if piece:
                # Owned piece valuation
                if piece.owner == owner:
                    score += piece.piece_type.value.score
                    score += self.mobility_score(cell)
                    max_dragon_circle = max(
                        self.count_dragon_circle(cell), max_dragon_circle
                    )
                    if max_dragon_circle == 4:
                        return inf

                # Dragon claim scoring
                elif piece.piece_type is PieceTypes.DRAGON:
                    dragon_claims += self.count_dragon_claims(cell, owner)

                # Opponent piece valuation
                else:
                    score -= piece.piece_type.value.score

                owner_pieces[piece.owner] += 1
            else:
                # Construction circle scoring
                max_construction_circle = max(
                    self.count_construction_circle(cell, owner),
                    max_construction_circle,
                )

        # Check for capture victory (in a multiplayer game)
        if self.owners > 2:
            is_winner = True
            for other in range(1, self.owners):
                if (
                    other != owner
                    and owner_pieces[other] >= self.ruleset.min_pieces
                ):
                    is_winner = False
                    break
            if is_winner:
                return inf

        # No capture victory, return normal evaluation
        score += max_dragon_circle * DRAGON_CIRCLE_SCORE
        if tower_count < self.ruleset.max_towers:
            score += max_construction_circle * CONSTRUCTION_CIRCLE_SCORE
        if tower_count > 0:
            score += dragon_claims * DRAGON_CLAIM_SCORE
        return score


class Game:
    def __init__(self, ruleset, depth=4, cache=True):
        self.ruleset = ruleset
        self.board = Board(ruleset)
        self.players = ruleset.players
        self.depth = depth
        self.turn = 1
        self.history = [str(self.board)]
        if cache:
            self.maxi_cache = {}
            self.mini_cache = {}
        else:
            self.maxi_cache = None
            self.mini_cache = None
        self.recursions = 0
        self.cache_hits = 0

    def get_next_turn(self, turn=None):
        if turn is None:
            turn = self.turn
        return turn + 1 if turn < self.players else 1

    def next_turn(self):
        defeated = self.board.defeated
        if len(defeated) == self.players:
            raise ValueError("Every player in the game is defeated")

        self.turn = self.get_next_turn()
        while self.turn in defeated:
            self.turn = self.get_next_turn()

    def get_prev_turn(self, turn=None):
        if turn is None:
            turn = self.turn
        return self.turn - 1 if self.turn > 1 else self.players

    def prev_turn(self):
        defeated = self.board.defeated
        if len(defeated) == self.players:
            raise ValueError("Every player in the game is defeated")

        self.turn = self.get_prev_turn()
        while self.turn in defeated:
            self.turn = self.get_prev_turn()

    def get_move_error(self, move):
        return self.board.get_move_error(move, self.turn)

    def move(self, move):
        winner = self.board.move(move, self.turn)
        self.next_turn()
        self.history.append(str(self.board))
        return winner

    def undo(self):
        if len(self.history) > 1:
            self.prev_turn()
            self.history.pop()
            self.board.load(self.history[-1])
            return ""
        return "There are no previous moves to undo."

    def forfeit(self):
        self.board.forfeited.add(self.turn)
        self.next_turn()
        return self.board.capture_winner

    def get_best_move(self):
        # Choose a completely random move at AI depth 0
        if self.depth == 0:
            return random.choice(self.board.get_owner_moves(self.turn))

        start_time = time()
        self.recursions = 0
        self.cache_hits = 0

        # Minimax with alpha-beta pruning
        move, _ = self.maxi(
            board=self.board,
            owner=self.turn,
            turn=self.turn,
            alpha=-inf,
            beta=inf,
            depth=self.depth,
        )

        if VERBOSE:
            end_time = time()
            print("Time Elapsed:", end_time - start_time)

        return move

    def maxi(self, board, owner, turn, alpha, beta, depth):
        entry = self.recursions == 0
        self.recursions += 1

        if depth == 0:
            return None, board.evaluate(owner)

        if self.maxi_cache is not None:
            cached = self.maxi_cache.get(hash((board, owner, turn)))
            if cached:
                if entry and VERBOSE:
                    print("Returning cached value")
                self.cache_hits += 1
                return cached

        best_move = None
        best_next_move = None
        best_immediate = -inf
        move_number = 1
        all_moves = board.get_owner_moves(turn)
        for move in all_moves:
            if entry and VERBOSE:
                print(
                    "Considering move",
                    f"{move_number:2d}/{len(all_moves):2d}:  {move} ",
                    end="",
                )
                prev_best = best_move
                stdout.flush()
                move_number += 1

            # If a move exists, the player must make a move
            if best_move is None:
                best_move = move

            new_board = board.move(move, turn, apply=False)
            immediate_score = new_board.evaluate(owner)

            if entry:
                # Exit early if we can win with this move right now
                if immediate_score == inf:
                    return move, immediate_score

            next_turn = self.get_next_turn(turn)
            if self.players == 2:
                # Use minimax in a 2-player game
                next_move, score = self.mini(
                    new_board, owner, next_turn, alpha, beta, depth - 1
                )
            else:
                # Use max^n in a non-2-player game
                next_move, score = self.maxi(
                    new_board, owner, next_turn, alpha, beta, depth - 1
                )

            if not entry and score >= beta:
                # Fail-soft beta cutoff
                return move, score

            if score > alpha or (
                score == alpha and immediate_score > best_immediate
            ):
                best_move = move
                best_next_move = next_move
                alpha = score
                best_immediate = immediate_score

            if entry and VERBOSE:
                print(f"(score: {score}, immediate: {immediate_score})")
                if self.cache_hits > 0:
                    print(
                        self.cache_hits,
                        "cache hit" + ("s" if self.cache_hits != 1 else ""),
                    )
                    self.cache_hits = 0
                new = " (NEW):" if prev_best != best_move else ":      "
                print(
                    f"Current best move{new} {best_move}",
                    f"(alpha: {alpha}, immediate: {best_immediate})",
                )

        if entry and VERBOSE:
            print("Chosen Move:", best_move)
            if self.players == 2:
                print("Next Move:", best_next_move)
            print("Current Score:", best_immediate)
            print("Potential Score:", alpha)
            print("Recursions:", self.recursions)

        if self.maxi_cache is not None:
            self.maxi_cache[hash((board, owner, turn))] = best_move, alpha
        return best_move, alpha

    def mini(self, board, owner, turn, alpha, beta, depth):
        self.recursions += 1

        if depth == 0:
            return None, -board.evaluate(owner)

        if self.mini_cache is not None:
            cached = self.mini_cache.get(hash((board, owner, turn)))
            if cached:
                self.cache_hits += 1
                return cached

        best_move = None
        best_next_move = None
        best_immediate = inf
        for move in board.get_owner_moves(turn):
            # If a move exists, the player must make a move
            if best_move is None:
                best_move = move

            new_board = board.move(move, turn, apply=False)
            immediate_score = -new_board.evaluate(owner)

            next_turn = self.get_next_turn(turn)
            next_move, score = self.maxi(
                new_board, owner, next_turn, alpha, beta, depth - 1
            )

            if score <= alpha:
                # Fail-soft alpha cutoff
                return next_move, score

            if score < beta or (
                score == beta and immediate_score < best_immediate
            ):
                best_move = move
                best_next_move = next_move
                beta = score
                best_immediate = immediate_score

        if self.mini_cache is not None:
            self.mini_cache[hash((board, owner, turn))] = best_next_move, beta
        return best_next_move, beta


def main():
    parser = ArgumentParser(
        description="A Python implementation of the Boost "
        "board game; CLI mode"
    )
    parser.add_argument(
        "-r",
        "--ruleset",
        default=DEFAULT_RULESET,
        choices=rulesets.keys(),
        help="which ruleset to use",
    )
    parser.add_argument(
        "-c",
        "--color",
        dest="color",
        action="store_true",
        help="force colored output",
    )
    parser.add_argument(
        "-C",
        "--no-color",
        dest="color",
        action="store_false",
        help="disable colored output",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="display logging information for debugging",
    )
    parser.add_argument(
        "-a",
        "--auto",
        action="store_true",
        help="enable auto mode automatically",
    )
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=4,
        help="AI minimax depth: "
        "higher values equate to a stronger AI; "
        "standard values range from 2-4; "
        "use 0 for completely random AI moves",
    )
    parser.add_argument(
        "-G" "--no-cache",
        action="store_false",
        help="disable caching the best AI move for previously "
        "considered board states",
    )
    parser.set_defaults(color=TERMCOLOR)
    parser.set_defaults(cache=True)
    args = parser.parse_args()

    global VERBOSE
    VERBOSE = args.verbose

    if args.color and not TERMCOLOR:
        print("Color is not supported on this system", file=stderr)
        print("Install termcolor via pip for color support", file=stderr)
        return 1

    global COLOR
    COLOR = args.color

    if args.depth < 0:
        print(f"AI minimax depth must be non-negative (was {args.depth})")
        return 1

    game = Game(rulesets[args.ruleset], args.depth, args.cache)
    message = ""
    winner = None
    auto = args.auto
    moved = False
    print(game.board.pretty)
    print()
    while True:
        if moved:
            print()
            print(game.board.pretty)
            print()
            moved = False

        if winner:
            print(f"Player {winner} won the game!")
            input("Press enter to exit.")
            return 0

        if message:
            print(message)
            print()
            message = ""

        if auto:
            print(f"Running AI for Player {game.turn}...")
            best_move = game.get_best_move()
            if best_move is not None:
                message = f"Player {game.turn} (AI) chose {best_move}."
                winner = game.move(best_move)
                moved = True
            else:
                game.next_turn()

        else:
            # Don't print a traceback on user-generated exit signals
            try:
                move_input = input(f"Player {game.turn}'s Move: ")
            except KeyboardInterrupt:
                print()
                return 1
            except EOFError:
                print()
                return 0

            if move_input == "":
                continue

            if move_input == "help":
                message = (
                    "a1b2: move a piece from A1 to B2 (for example)\n"
                    "d2: build a tower or promote a pawn at D2 (for example)\n"
                    "undo: undo the last move\n"
                    "ai: let an AI move for the current player\n"
                    "auto: run the AI automatically for every move\n"
                    "forfeit: forfeit the current game without exiting\n"
                    "exit: exit the current game"
                )
            elif move_input == "undo":
                message = game.undo()
            elif move_input == "ai":
                print(f"Running AI for Player {game.turn}...")
                best_move = game.get_best_move()
                if best_move is not None:
                    winner = game.move(best_move)
                    moved = True
                else:
                    game.next_turn()
            elif move_input == "auto":
                auto = True
            elif move_input == "forfeit":
                winner = game.forfeit()
            elif move_input == "exit":
                return 0
            else:
                try:
                    move = game.board.parse_move(move_input)
                except (ValueError, IndexError):
                    message = (
                        "Moves should be given in algebraic notation.\n"
                        'e.g. "a1b2" to move from A1 to B2.'
                    )
                else:
                    message = game.get_move_error(move)
                    if not message:
                        winner = game.move(move)
                        moved = True
