from tkinter import *
from gtts import gTTS
import os
import pandas
import random
from playsound3 import playsound

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    origin_data = pandas.read_csv("./data/japanese_words.csv")
    to_learn = origin_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
# ---------------------- Create New Flash Card ------------------------ #
def next_card():
    LANG = 'ja'
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Japanese", fill="black")
    canvas.itemconfig(card_word, text=current_card["japanese"], fill="black")
    window.after(100)
    audio_output = gTTS(text=current_card["japanese"], lang=LANG)
    audio_output.save("japan_word.mp3")
    playsound("japan_word.mp3", True)
    os.remove("japan_word.mp3")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="Chinese", fill="white")
    canvas.itemconfig(card_word, text=current_card["chinese"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash Card")
window.config(padx=100, pady=50, bg=BACKGROUND_COLOR)

flip_timer= window.after(300, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=(FONT_NAME, 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

#Button
w_img = PhotoImage(file="./images/wrong.png")
w_button = Button(image=w_img, highlightthickness=0, command=next_card)
w_button.grid(column=0, row=1)

r_img = PhotoImage(file="./images/right.png")
r_button = Button(image=r_img, highlightthickness=0, command=is_known)
r_button.grid(column=1, row=1)

next_card()

window.mainloop()