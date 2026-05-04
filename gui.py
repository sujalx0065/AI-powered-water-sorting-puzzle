import tkinter as tk
import copy
from logic import *
from levels import LEVELS

BG_COLOR = "#1e1e2f"

COLORS = {
    "R":"#ff3b3b",
    "B":"#2f5cff",
    "G":"#19c84f",
    "Y":"#ffd93b",
    "P":"#b84dff",
    "C":"#31d7ff",
    "O":"#ff9f1a"
}

BOTTLE_W = 70
BOTTLE_H = 220
BLOCK_H = 50


class WaterSortGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Water Sort Puzzle AI")
        self.root.configure(bg=BG_COLOR)

        self.level_var = tk.IntVar(value=1)

        top = tk.Frame(root, bg=BG_COLOR)
        top.pack(pady=10)

        tk.Label(top,text="LEVEL",fg="white",bg=BG_COLOR,font=("Arial",14,"bold")).pack(side=tk.LEFT,padx=5)

        tk.OptionMenu(
            top,
            self.level_var,
            *LEVELS.keys(),
            command=self.load_level
        ).pack(side=tk.LEFT,padx=10)

        tk.Button(top,text="AI Solve",command=self.ai_solve,bg="#7a5cff",fg="white").pack(side=tk.LEFT,padx=6)
        tk.Button(top,text="Reset",command=self.reset,bg="#7a5cff",fg="white").pack(side=tk.LEFT,padx=6)

        self.canvas = tk.Canvas(
            root,
            width=900,
            height=450,
            bg=BG_COLOR,
            highlightthickness=0
        )
        self.canvas.pack()

        self.selected = None
        self.state = copy.deepcopy(LEVELS[1])

        self.canvas.bind("<Button-1>", self.click)

        self.draw()

    # --------------------
    def load_level(self,*args):
        lvl = self.level_var.get()
        self.state = copy.deepcopy(LEVELS[lvl])
        self.selected = None
        self.draw()

    # --------------------
    def draw(self):

        self.canvas.delete("all")

        for i,bottle in enumerate(self.state):

            x1 = 40+i*100
            y1 = 100
            x2 = x1+BOTTLE_W
            y2 = y1+BOTTLE_H

            if self.selected == i:
                self.canvas.create_rectangle(
                    x1-6,y1-6,x2+6,y2+6,
                    outline="#ffd93b",
                    width=4
                )

            self.canvas.create_rectangle(
                x1,y1,x2,y2,
                outline="white",
                width=3
            )

            for j,color in enumerate(bottle):

                cy1 = y2-(j+1)*BLOCK_H
                cy2 = y2-j*BLOCK_H

                self.canvas.create_rectangle(
                    x1+5,cy1+5,
                    x2-5,cy2-5,
                    fill=COLORS[color],
                    outline=""
                )

        if is_goal(self.state):
            self.canvas.create_text(
                450,40,
                text="PUZZLE SOLVED!",
                fill="#19c84f",
                font=("Arial",22,"bold")
            )

    # --------------------
    def click(self,event):

        index = (event.x-40)//100

        if index < 0 or index >= len(self.state):
            return

        if self.selected is None:
            self.selected = index
        else:

            src = self.selected
            dest = index

            if is_valid_move(self.state,src,dest):
                self.state = pour(self.state,src,dest)

            self.selected = None

        self.draw()

    # --------------------
    def ai_solve(self):

        solution = solve_bfs(self.state)

        if solution:
            self.animate_solution(solution)

    def animate_solution(self,sol,step=0):

        if step >= len(sol):
            return

        s,d = sol[step]

        self.state = pour(self.state,s,d)
        self.draw()

        self.root.after(300,lambda:self.animate_solution(sol,step+1))

    # --------------------
    def reset(self):
        lvl = self.level_var.get()
        self.state = copy.deepcopy(LEVELS[lvl])
        self.selected = None
        self.draw()
