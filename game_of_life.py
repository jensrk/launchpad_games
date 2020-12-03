import numpy as np

class GameOfLife():

    def __init__(self, size):
        self.size_x = size[0]
        self.size_y = size[1]
        self.board = np.zeros(size, dtype=np.bool)

    def toggle_cell(self, x, y):
        self.board[y,x] = 1 - self.board[y,x]

    def step(self):
        count_neighburs = np.zeros(self.board.shape, dtype=np.int8)
        # top
        count_neighburs[1:,:] += self.board[:-1,:]
        # right
        count_neighburs[:,:-1] += self.board[:,1:]
        # left
        count_neighburs[:,1:] += self.board[:,:-1]
        # bottom
        count_neighburs[:-1,:] += self.board[1:,:]
        # top-right
        count_neighburs[1:,:-1] += self.board[:-1,1:]
        # bottom-right
        count_neighburs[:-1,:-1] += self.board[1:,1:]
        # top-left
        count_neighburs[1:,1:] += self.board[:-1,:-1]
        # bottom-left
        count_neighburs[:-1,1:] += self.board[1:,:-1]

        new_board = np.zeros(self.board.shape, dtype=np.bool)
        # Any live cell with two or three live neighbours survives.
        new_board += self.board * (count_neighburs >= 2) * (count_neighburs <= 3) == 1
        # Any dead cell with three live neighbours becomes a live cell.
        new_board += (1 - self.board) * (count_neighburs == 3) == 1
        # All other live cells die in the next generation. Similarly, all other dead cells stay dead.
        self.board = new_board