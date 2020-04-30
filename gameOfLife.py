import tkinter as tk
import numpy as np

L1 = [10, 9, 9, 10, 11]
L2 = [9, 10, 11, 10, 10]


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.width = 1500
        self.height = 1000
        self.delay = 200
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.canvas.bind("<Button-1>", self.click)
        self.cellwidth = 10
        self.cellheight = 10
        self.state = np.array([[0 for i in range(int(self.width/self.cellwidth))] for j in range(int(self.height/self.cellheight))])
        for i in range(len(L1)):
            self.state[L1[i]][L2[i]] = 1
        self.iteration = 0
        self.rect = {}
        self.oval = {}
        for column in range(int(self.width/self.cellwidth)):
            for row in range(int(self.height/self.cellheight)):
                x1 = column * self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags="rect")
                # self.oval[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="blue", tags="oval")
        self.redraw()

    def click(self, event):
        if self.delay < 1000:
            self.delay = 60000
        else:
            self.delay = 0
            self.redraw()

    def change(self):
        state = self.state.copy()
        for i in range(int(self.height/self.cellheight)):
            for j in range(int(self.width/self.cellwidth)):
                N = 0
                if (i - 1 >= 0 and j - 1 >= 0 and state[i - 1][j - 1]):
                    N += 1
                if (i - 1 >= 0 and state[i - 1][j]):
                    N += 1
                if (i - 1 >= 0 and j + 1 < self.width/self.cellwidth and state[i - 1][j + 1]):
                    N += 1
                if (i + 1 < self.height/self.cellheight and j - 1 >= 0 and state[i + 1][j - 1]):
                    N += 1
                if (i + 1 < self.height/self.cellheight and state[i + 1][j]):
                    N += 1
                if (i + 1 < self.height/self.cellheight and j + 1 < self.width/self.cellwidth and state[i + 1][j + 1]):
                    N += 1
                if (j - 1 >= 0 and state[i][j - 1]):
                    N += 1
                if (j + 1 < self.width/self.cellwidth and state[i][j + 1]):
                    N += 1
                if (state[i][j]):
                    if (N < 2 or N > 3):
                        self.state[i][j] = 0
                if (not state[i][j] and N == 3):
                    self.state[i][j] = 1

    def redraw(self):
        self.canvas.itemconfig("rect", fill="white")
        # self.canvas.itemconfig("oval", fill="blue")

        if self.iteration != 0:
            self.change()
        self.iteration += 1
        for i in range(int(self.height/self.cellheight)):
            for j in range(int(self.width/self.cellwidth)):
                item_id = self.rect[i, j]
                if self.state[i][j]:
                    self.canvas.itemconfig(item_id, fill="black")
                else:
                    self.canvas.itemconfig(item_id, fill="white")
        self.after(self.delay, lambda: self.redraw())


if __name__ == "__main__":
    app = App()
    app.mainloop()