import tkinter as tk
import random




class GameOfLife(tk.Canvas):
    def __init__(self, top, bg='black', height=200, width=200, size=2,
                 refresh_interval=400):
        super().__init__(top, bg=bg, height=height, width=width)
        self.height = height
        self.width = width
        self.size = size
        self.nrows = int(self.height / self.size)
        self.ncols = int(self.width / self.size)
        self.color = ['black', 'white' ]
        self.cells = [None]*(self.height * self.width)
        self.refresh_interval = refresh_interval
        self.pack()
        self.initCells()
        self.refresh()

    def rc2i(self, rowx, colx):
        return (rowx * self.ncols) + colx

    def i2rc(self, idx):
        return divmod(idx, self.ncols)

    def countNeighbors(self, idx):
        rowx, colx = self.i2rc(idx)
        num = 0
        ran = [-1, 0, 1]
        for drow in ran:
            for dcol in ran:
                if drow + dcol == 0: continue
                idx = self.rc2i(rowx + drow, colx + dcol)
                num += self.getCellState(idx)

        return num

    def getCellState(self, idx):
        return self.cells[idx][0]

    def setCellState(self, idx, state):
        self.cells[idx][0] = state
        self.itemconfig(self.cells[idx][1], fill=self.color[state])

    def initCell(self, rowx, colx, state):
        idx = self.rc2i(rowx, colx)
        cell = super().create_polygon(
            self.size * rowx,		self.size * colx,
            self.size * rowx,		self.size * (colx + 1),
            self.size * (rowx + 1), 	self.size * (colx + 1),
            self.size * (rowx + 1), 	self.size * colx,
            fill = self.color[state] )
        self.cells[idx] = [state, cell]

    def initCells(self, dflt_state=0):
        for rowx in range(self.nrows):
            for colx in range(self.ncols):
                self.initCell(rowx, colx, dflt_state)

    def updateCells(self):
        for rowx in range(1, self.nrows - 1):
            for colx in range(1, self.ncols - 1):
                idx = self.rc2i(rowx, colx)
                state = self.getCellState(idx)
                num = self.countNeighbors(idx)

                if (state == 1) and (num == 2 or num == 3):
                    self.setCellState(idx, 1)
                elif (state == 0) and (num == 3):
                    self.setCellState(idx, 1)
                else:
                    self.setCellState(idx, 0)

    def randomizeCells(self, alive_weight=0.5):
        for rowx in range(1, self.nrows - 1):
            for colx in range(1, self.ncols - 1):
                idx = self.rc2i(rowx, colx)
                rand = random.randint(1, 100)
                if rand < (1.0 - alive_weight)*100:
                    state = 0
                else:
                    state = 1
                self.setCellState(idx, state)

    def refresh(self):
        self.updateCells()
        top.after(self.refresh_interval, self.refresh)
        



if __name__ == '__main__':
    top = tk.Tk()
    height, width = 600, 600
    size = 6
    top.geometry('{w}x{h}'.format(w=width, h=height))
    gol = GameOfLife(top, width=width, height=height, size=size)
    gol.randomizeCells(alive_weight=0.2)
    top.mainloop()
