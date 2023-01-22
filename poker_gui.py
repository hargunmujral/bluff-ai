import tkinter as tk
from tkinter import messagebox
import card_eval as ce

class BluffGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Bluff Game")
        self.geometry("300x200")
        self.bluff = ce.Bluff(1)
        self.create_widgets()
        self.bluff.deck.shuffle()
        self.bluff.hands[0] = self.bluff.deck.deal(5)
    def create_widgets(self):
        self.hands_label = tk.Label(self, text="Your Hand:")
        self.hands_label.pack()
        self.hands_display = tk.Text(self, height=5, width=30)
        self.hands_display.pack()
        self.play_button = tk.Button(self, text="Play", command=self.play)
        self.play_button.pack()

    def play(self):
        self.hands_display.delete("1.0", tk.END)
        for card in self.bluff.hands[0]:
            self.hands_display.insert(tk.END, str(card) + " ")
        self.bluff.startGame(self.bluff.hands[0])
        messagebox.showinfo("Result", self.bluff.tlist)

if __name__ == "__main__":
    app = BluffGUI()
    app.mainloop()
