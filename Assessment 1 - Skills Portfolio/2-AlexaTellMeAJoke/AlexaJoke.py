import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps
import random

root = tk.Tk()
root.title("Alexa, Tell Me a Joke!")
root.geometry("1100x700")
root.resizable(False, False)

#Colours
BG_TOP = (10, 14, 40)
BG_BOTTOM = (45, 20, 90)
PANEL = "#12203A"
CYAN = "#3FE0F5"
PINK = "#FF5FA2"
YELLOW = "#FFD166"
WHITE = "#F4F8FF"
SOFT = "#9FB3D9"
DARK = "#0A0E28"
RED = "#E05260"

#Fonts
HEADING_FONT = ("Georgia", 34, "bold")
SUB_FONT = ("Trebuchet MS", 15, "bold")
SECTION_FONT = ("Georgia", 17, "bold")
JOKE_FONT = ("Georgia", 19, "bold")
PUNCHLINE_FONT = ("Georgia", 16, "bold")
BUTTON_FONT = ("Trebuchet MS", 11, "bold")

#Canvas
canvas = tk.Canvas(root, width=1100, height=700, highlightthickness=0)
canvas.pack(fill="both", expand=True)


#Background Design
def draw_gradient():
    """Draw a simple navy-to-purple background if the image is unavailable."""
    for y in range(700):
        t = y / 700
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
        canvas.create_line(0, y, 1100, y, fill=f"#{r:02x}{g:02x}{b:02x}")


def draw_circuits():
    """Add circuit-style lines to the corners of the fallback background."""
    lines = [
        (0, 600, 120, 600, 120, 660, 260, 660),
        (0, 640, 60, 640, 60, 700),
        (1100, 80, 980, 80, 980, 30, 860, 30),
        (1100, 120, 1040, 120, 1040, 0),
        (1100, 640, 1000, 640, 1000, 690),
    ]

    for points in lines:
        canvas.create_line(*points, fill="#2A4A7A", width=2)
        end_x = points[-2]
        end_y = points[-1]
        canvas.create_oval(
            end_x - 5, end_y - 5, end_x + 5, end_y + 5,
            fill=CYAN, outline=""
        )


def draw_stars():
    """Draw small stars without changing the random joke selection."""
    star_random = random.Random(7)

    for _ in range(60):
        x = star_random.randint(0, 1100)
        y = star_random.randint(0, 700)
        size = star_random.choice([1, 1, 2])
        canvas.create_oval(
            x, y, x + size, y + size,
            fill="#7F93C8", outline=""
        )


#Background Image
# Keep AlexaJoke.png in the same folder as this Python file.
BACKGROUND_FILE = "AlexaJoke.png"
background_photo = None

try:
    original_image = Image.open(BACKGROUND_FILE).convert("RGB")

    # Resize the picture to fit the window while keeping its proportions.
    resized_image = ImageOps.fit(
        original_image,
        (1100, 700),
        method=Image.Resampling.LANCZOS
    )

    background_photo = ImageTk.PhotoImage(resized_image)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")

except (FileNotFoundError, OSError):
    # Use the drawn background if the image cannot be loaded.
    draw_gradient()
    draw_stars()
    draw_circuits()


#Load Jokes from Text File
jokes = []
try:
    with open("randomJokes.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # Each joke must have a setup and punchline separated by '?'.
            if "?" in line:
                parts = line.split("?", 1)
                setup = parts[0].strip() + "?"
                punchline = parts[1].strip()

                if setup != "?" and punchline:
                    jokes.append([setup, punchline])

except FileNotFoundError:
    messagebox.showerror(
        "File Missing",
        "randomJokes.txt could not be found!"
    )

except OSError as error:
    messagebox.showerror("File Error", str(error))

current_joke = None

#Heading
# The two heading layers create a simple neon effect.
canvas.create_text(
    653, 88, text="ALEXA'S JOKE",
    font=HEADING_FONT, fill=PINK
)
canvas.create_text(
    650, 85, text="ALEXA'S JOKE",
    font=HEADING_FONT, fill=CYAN
)
canvas.create_text(
    650, 135, text="Alexa, tell me a joke!",
    font=SUB_FONT, fill=SOFT
)

#Robot Reaction Text
# The robot picture is part of the background image.
laugh_text = canvas.create_text(
    130, 245, text="",
    font=("Comic Sans MS", 20, "bold"),
    fill=YELLOW
)

#Joke Display Panel
canvas.create_rectangle(
    383, 188, 923, 468,
    fill="#0A1224", outline=""
)
canvas.create_rectangle(
    380, 185, 920, 465,
    fill=PANEL, outline=CYAN, width=3
)
canvas.create_text(
    650, 213, text="- YOUR JOKE -",
    font=SECTION_FONT, fill=PINK
)

joke_label = tk.Label(
    root,
    text="Press 'Alexa tell me a joke' to begin!",
    font=JOKE_FONT,
    bg=PANEL,
    fg=WHITE,
    wraplength=490,
    justify="center"
)
canvas.create_window(
    650, 295, window=joke_label,
    width=500, height=90
)

punchline_label = tk.Label(
    root,
    text="",
    font=PUNCHLINE_FONT,
    bg=PANEL,
    fg=YELLOW,
    wraplength=490,
    justify="center"
)
canvas.create_window(
    650, 398, window=punchline_label,
    width=500, height=70
)

#Robot Reactions
def robot_happy():
    """Show a happy message when the punchline appears."""
    canvas.itemconfig(laugh_text, text="HA HA HA!")


def robot_normal():
    """Clear the robot's reaction message."""
    canvas.itemconfig(laugh_text, text="")

#Joke Functions
def next_joke():
    """Choose a random joke and display its setup."""
    global current_joke

    if not jokes:
        messagebox.showerror(
            "No Jokes",
            "Please check your randomJokes.txt file."
        )
        return

    # Avoid showing the same joke twice in a row when possible.
    available_jokes = []

    for joke in jokes:
        if joke != current_joke:
            available_jokes.append(joke)

    if not available_jokes:
        available_jokes = jokes

    current_joke = random.choice(available_jokes)

    joke_label.config(text=current_joke[0])
    punchline_label.config(text="")
    robot_normal()


def show_punchline():
    """Display the answer for the current joke."""
    if current_joke is None:
        messagebox.showinfo(
            "Alexa",
            "Please ask for a joke first!"
        )
        return

    punchline_label.config(text=current_joke[1])
    robot_happy()


def quit_program():
    """Close the joke application."""
    root.destroy()

#Button Design
def create_button(text, command, bg, fg, hover, x, y, width):
    """Create a button with a simple colour change when hovered over."""
    button = tk.Button(
        root,
        text=text,
        command=command,
        font=BUTTON_FONT,
        bg=bg,
        fg=fg,
        activebackground=hover,
        activeforeground=fg,
        relief="flat",
        bd=0,
        cursor="hand2"
    )

    # Change the button colour while the pointer is over it.
    button.bind("<Enter>", lambda event: button.config(bg=hover))
    button.bind("<Leave>", lambda event: button.config(bg=bg))

    canvas.create_window(
        x, y, window=button,
        width=width, height=46
    )
    return button


#Application Buttons
alexa_button = create_button(
    "ALEXA, TELL ME A JOKE", next_joke,
    CYAN, DARK, "#8FF0FF", 650, 507, 540
)

punchline_button = create_button(
    "SHOW PUNCHLINE", show_punchline,
    PINK, WHITE, "#FF8DBD", 465, 574, 170
)

next_button = create_button(
    "NEXT JOKE", next_joke,
    YELLOW, DARK, "#FFE29A", 650, 574, 170
)

quit_button = create_button(
    "QUIT", quit_program,
    RED, WHITE, "#F07A85", 835, 574, 170
)

root.mainloop()
