import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
import actions
import random
from PIL import *
import PIL.Image as Image
import PIL.ImageTk as ImageTk
cards = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
cols = ["-","2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
WIDTH = 500
HEIGHT = 450


def create_card(exemption):
    return actions.pocketcard(exemption)


def resize(img):
    img = img.resize((250, 382))
    return ImageTk.PhotoImage(img)


def name_pocket(card1, card2):
    
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
    base = ttk.Treeview

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.winfo_toplevel().title("Pocket Trainer")

        try:
            self.sets = actions.read("custom_hand_rules.csv")
        except:
            self.sets = actions.read("poker_2.csv")
        self.seatName = self.seats[random.choice(range(0, 3))]
        self.column = StringVar()
        self.column.set("Column: ")
        self.row = StringVar()
        self.selected = ""
        self.row.set("Row: ")
        self.fold_btn = tk.Button(self, text="Fold", fg="red", padx=10, pady=10)
        self.fold_btn["command"] = self.fold_it
        self.raise_btn = tk.Button(self, text="Raise", fg="green", padx=10, pady=10)
        self.raise_btn["command"] = self.raise_it
        self.expand_text = tk.StringVar()
        self.expand_text.set("<")
        sImg = Image.open("SaveIco.png")
        saveImage=ImageTk.PhotoImage(sImg.resize((35,35)))
        self.save = tk.Button(self, image=saveImage)
        self.save["command"] = lambda: actions.save("custom_hand_rules.csv", self.sets)
        self.tableFrame = tk.Frame(bg="light grey")
        self.infoFrame = tk.Frame(self.tableFrame, bg="light grey")
        self.list = tk.Listbox(self.infoFrame, width=23)
        self.instruct = tk.Label(self.infoFrame, wraplength=140, text="Saving creates a new file called 'custom_hand_rules.csv'. In order to revert to the default rule set, either delete the new file or rename it. Saving again always overwrites said file.")
        self.list.insert(END, "E - Early", "M - Middle", "L - Late", "N - Never", "UNALTERABLE", "s - Same suit", "o - Off suit")
        self.entry_field = tk.Text(self, height=1, width=10 ,bd=1, font=("Helvetica", 28))
        self.entry_field.bind("<Return>", self.write)
        self.expand_btn = tk.Button(self, textvariable=self.expand_text, padx=10, pady=10)
        self.expand_btn["command"] = self.expand
        self.col_label = tk.Label(self, textvariable=self.column, padx=55, pady=1)
        self.row_label = tk.Label(self, textvariable=self.row, padx=55, pady=1)
        self.table = ttk.Treeview(self.tableFrame, columns=cols, show="headings")
        for column in cols:
            self.table.heading(column, text=column)
            self.table.column(column, minwidth=0, width=30)
        self.buildTable()
        self.table.bind('<ButtonRelease-1>', self.selectItem)
        self.seat = tk.Label(self, text=self.seatName, padx=10, pady=13, bg="yellow")
        img1 = resize(Image.open("./cards/red_back.png"))
        self.card1 = tk.Label(image=img1)
        img2 = resize(Image.open("./cards/red_back.png"))
        self.card2 = tk.Label(image=img2)
        self.result = tk.Label(self, text="waiting", padx=40, pady=10, bg="grey")
        self.score = tk.Label(self, text=self.score_num, padx=90, pady=10)
        self.instruct.pack(side="top", padx=(0,0),expand="YES",fill="both")
        self.list.pack(side="top", padx=(0,0), expand="NO")
        self.table.pack(side="left",expand="YES", fill="both", padx=(0,0))
        self.infoFrame.pack(side="left",expand="YES", fill="both", padx=(0,0))
        self.create_widgets()

    def create_widgets(self):
        self.expand_btn.pack(side="left")
        self.seat.pack(side="right")
        self.raise_btn.pack(side="right")
        self.fold_btn.pack(side="right")
        self.result.pack(side="right")
        self.score.pack(side="right")
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

    def expand(self):
        if self.table.winfo_ismapped():
            self.entry_field.forget()
            self.tableFrame.forget()
            self.col_label.forget()
            self.row_label.forget()
            self.save.forget()
            self.expand_text.set("<")
        else:
            self.col_label.pack(side="right")
            self.row_label.pack(side="right")
            self.save.pack(side="left")
            self.entry_field.pack(side="right", expand="YES", fill="x", padx=(0,0))
            self.tableFrame.pack(expand="YES", fill="both", padx=(0,0))
            self.expand_text.set(">")

    def selectItem(self, event):
        curItem = self.table.item(self.table.focus())
        col = self.table.identify_column(event.x)
        self.row.set("Row: " + str(curItem["values"][0]))
        self.column.set("Column: " + cols[int(col[1:])-1])
        self.selected=curItem["values"][int(col[1:])-1]
        self.entry_field.delete('1.0', 'end')
        self.entry_field.insert('1.0',curItem["values"][int(col[1:])-1][0:1])
        root.update_idletasks()

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
        
    def write(self, e):
        input = self.entry_field.get('1.0', 'end-1c')
        if input in self.seats:
            if "s" in self.selected:
                self.sets[self.column.get()[8:] + self.row.get()[5:]+'s'] = self.entry_field.get('1.0', 'end-1c')
            elif  "o" in self.selected:
                self.sets[self.row.get()[5:] + self.column.get()[8:] + 'o'] = self.entry_field.get('1.0', 'end-1c')
            else:
                self.sets[self.row.get()[5:] + self.column.get()[8:]] = self.entry_field.get('1.0', 'end-1c')
        self.entry_field.delete('1.0','end')
        self.buildTable()
    
    def buildTable(self):
        for i in self.table.get_children():
            self.table.delete()
        for pair in self.sets:  
            if len(pair)==3 and pair[2] == 's':
                if not self.table.exists(pair[1]+"r"):
                    self.table.insert("", 0, pair[1]+'r' , values=pair[1])
                self.table.set(pair[1]+"r", pair[0], self.sets[pair]+pair[2])
            elif len(pair)==3 and pair[2] == 'o':
                if not self.table.exists(pair[0]+"r"):
                    self.table.insert("", 0, pair[0]+'r', values=pair[1])
                self.table.set(pair[0]+"r", pair[1], self.sets[pair]+pair[2])
            else:
                if not self.table.exists(pair[0]+"r"):
                    self.table.insert("", 0, pair[0]+'r', values=pair[1])
                self.table.set(pair[0]+"r", pair[1], self.sets[pair])


root = tk.Tk()
app = Application(master=root)
app.mainloop()
