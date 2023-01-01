import tkinter as tk
import actions
import random
from PIL import *
import PIL.Image as Image
import PIL.ImageTk as ImageTk

def create_card(exemption):
    return actions.pocketcard(exemption)


def resize(img):
    img = img.resize((250, 382))
    return ImageTk.PhotoImage(img)


def name_pocket(card1, card2):
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    if cards.index(card1) > cards.index(card2):
        return card1 + card2
    else:
        return card2 + card1


class Application(tk.Frame):
    name = ""
    seatName = ""
    sets = {}
    seats = "EMLN"
    pos = 0
    score_num = 0

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.sets = actions.read("poker_2.csv")
        self.seatName = self.seats[random.choice(range(0, 3))]

        self.fold_btn = tk.Button(self, text="Fold", fg="red")
        self.fold_btn["command"] = self.fold_it
        self.raise_btn = tk.Button(self, text="Raise", fg="green")
        self.raise_btn["command"] = self.raise_it
        self.seat = tk.Label(self, text=self.seatName, padx=10, pady=10, bg="yellow")
        img1 = resize(Image.open("./cards/red_back.png"))
        self.card1 = tk.Label(image=img1)
        img2 = resize(Image.open("./cards/red_back.png"))
        self.card2 = tk.Label(image=img2)
        self.result = tk.Label(self, text="waiting", padx=40, pady=10, bg="grey")
        self.score = tk.Label(self, text=self.score_num, padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        self.raise_btn.pack(side="right")
        self.fold_btn.pack(side="right")
        self.result.pack(side="right")
        self.score.pack(side="right")
        self.seat.pack(side="right")
        self.card1.pack(side="right")
        self.card2.pack(side="right")
        card1 = create_card("")
        img1 = resize(Image.open("./cards/" + card1 + ".png"))
        self.card1.config(image=img1)
        card2 = create_card(card1)
        if card1[0] == card2[0]:
            name = card1[0] + card1[0]
        else:
            if card1[1] == card2[1]:
                name = name_pocket(card1[0], card2[0]) + "s"
            else:
                name = name_pocket(card1[0], card2[0]) + "o"
        self.pos = self.seats.find(self.sets[name])
        img2 = resize(Image.open("./cards/" + card2 + ".png"))
        self.card2.config(image=img2)
        tk.mainloop()

    def draw(self):
        self.seatName = self.seats[random.choice(range(0, 3))]
        self.seat.config(text=self.seatName)
        self.after(1, self.create_widgets())

    def fold_it(self):
        if self.check_seat():
            self.result.config(text="Fail", bg="red")
            self.score_num = self.score_num - 2
            self.score.config(text=self.score_num)
        else:
            self.result.config(text="Pass", bg="green")
            self.score_num = self.score_num + 1
            self.score.config(text=self.score_num)
        self.draw()

    def raise_it(self):
        if self.check_seat():
            self.result.config(text="Pass", bg="green")
            self.score_num = self.score_num + 1
            self.score.config(text=self.score_num)
        else:
            self.result.config(text="Fail", bg="red")
            self.score_num = self.score_num - 2
            self.score.config(text=self.score_num)
        self.draw()

    def check_seat(self):
        if self.pos <= self.seats.find(self.seatName):
            return True
        else:
            return False


root = tk.Tk()
app = Application(master=root)
app.mainloop()
