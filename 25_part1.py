from __future__ import annotations
from dataclasses import dataclass
from collections import namedtuple

BoardMove = namedtuple('BoardMove', ['from_sq', 'to_sq'])


@dataclass
class Board:
    board: list[list[str]]

    @classmethod
    def from_matrix(cls, board: list[list[str]]):
        return cls(board)

    def __post_init__(self):
        self.h = len(self.board)
        self.w = len(self.board[0])

    def next_step(self):
        board_changed = False

        east_movers = []
        for r in range(self.h):
            for c in range(self.w):
                next_col = (c + 1) % self.w
                if self.board[r][c] == '>' and self.board[r][next_col] == '.':
                    move = BoardMove(from_sq=(r, c), to_sq=(r, next_col))
                    east_movers.append(move)

        if len(east_movers):
            board_changed = True
        for move in east_movers:
            self.board[move.from_sq[0]][move.from_sq[1]] = '.'
            self.board[move.to_sq[0]][move.to_sq[1]] = '>'

        south_movers = []
        for r in range(self.h):
            for c in range(self.w):
                next_row = (r + 1) % self.h
                if self.board[r][c] == 'v' and self.board[next_row][c] == '.':
                    move = BoardMove(from_sq=(r, c), to_sq=(next_row, c))
                    south_movers.append(move)

        if len(south_movers):
            board_changed = True
        for move in south_movers:
            self.board[move.from_sq[0]][move.from_sq[1]] = '.'
            self.board[move.to_sq[0]][move.to_sq[1]] = 'v'

        return board_changed


input_file = 'input1'
with open(input_file) as f:
    board_matrix = f.readlines()
    board_matrix = list(map(lambda l: l.strip(), board_matrix))
    board_matrix = list(map(list, board_matrix))
    board = Board.from_matrix(board_matrix)

for move_no in range(1, 10**6):
    if not board.next_step():
        print(move_no)
        break
