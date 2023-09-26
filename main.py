from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"


# ------------------------ CREATING NEW FLASHCARDS --------------------------- #

try:
    data_frame = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data_frame = pandas.read_csv("data/spanish_words.csv")
    dict = original_data_frame.to_dict(orient="records")
else:
    dict = data_frame.to_dict(orient="records")

current_card = {}

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(dict)
    canvas.itemconfig(canvas_image, image=front_img)
    canvas.itemconfig(card_title, text="Spanish", fill="black")
    canvas.itemconfig(card_word, text=current_card["SPANISH"], fill="black")
    flip_timer = window.after(3000, func=flip_card)
    

# ------------------------- FLIPPING THE CARDS ---------------------------- #

def flip_card():
    canvas.itemconfig(canvas_image, image=back_img)
    canvas.itemconfig(card_title, text="Turkish", fill="white")
    canvas.itemconfig(card_word, text=current_card["TURKISH"], fill="white")
    

# -------------------- SAVING THE WORDS USER HAVE KNOWN ----------------------- #

def is_known():
    dict.remove(current_card)
    print(len(dict))
    next_card()
    data = pandas.DataFrame(dict)
    data.to_csv("data/words_to_learn.csv", index=False)

# words_to_learn = {word for word in dict if word not in is_known}


# ------------------------------- UI SETUP ---------------------------------- #
window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=500, highlightthickness=0)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 250, image= front_img)
canvas.grid(column=1, row=1, columnspan=2)
card_title = canvas.create_text(400, 150, text="Spanish", font=("Ariel", 40,"italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))

wrong_photo = PhotoImage(file="images/wrong.png")
right_photo = PhotoImage(file="images/right.png")

wrong_button = Button(image=wrong_photo, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=2)
right_button = Button(image=right_photo, highlightthickness=0, command=is_known)
right_button.grid(column=2, row=2)

next_card()

window.mainloop()
