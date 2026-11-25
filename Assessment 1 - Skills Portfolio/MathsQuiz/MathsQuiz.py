import tkinter as tk
import random
from PIL import Image, ImageDraw, ImageTk

root = tk.Tk()
root.title("Maths Quiz")
root.geometry("1000x650")
root.resizable(False, False)

WIDTH = 1000
HEIGHT = 650
CENTRE = 500

# Colours
BG = "#080D2B"
PANEL = "#101936"
CYAN = "#00D9FF"
PURPLE = "#9146E8"
GOLD = "#FFC857"
GREEN = "#00C995"
WHITE = "#FFFFFF"
RED = "#FF5577"
GREY = "#8FA3C8"

TOTAL_QUESTIONS = 10


# FONTS
# These are the fonts installed.
titleFont = "Press Start 2P"
textFont = "Pixelify Sans"
TITLE_FONT = (titleFont, 24, "normal")
HEADING_FONT = (titleFont, 14, "normal")
QUESTION_FONT = (titleFont, 20, "normal")
SCORE_FONT = (titleFont, 32, "normal")
FEEDBACK_FONT = (titleFont, 12, "normal")
TEXT_FONT = (textFont, 16, "bold")
SMALL_FONT = (textFont, 14, "bold")
BUTTON_FONT = (textFont, 16, "bold")
ENTRY_FONT = (textFont, 22, "bold")

#BACKGROUND IMAGES
imageFiles = {
    "start": "start_bg.jpg",
    "level": "level_bg.jpg",
    "quiz": "quiz_bg.jpg",
    "score": "score_bg.jpg"
}

# Each screen has its own background and panel position.
panelBoxes = {
    "start": (270, 140, 730, 480),
    "level": (145, 50, 855, 600),
    "quiz": None,
    "score": (145, 50, 855, 600)
}

images = {}
canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    highlightthickness=0,
    bd=0,
    bg=BG
)
canvas.place(x=0, y=0)

def createBackground(screen):

    # Load the background image. If it is missing, use a plain background.
    try:
        background = Image.open(imageFiles[screen])
        background = background.resize((WIDTH, HEIGHT))
        background = background.convert("RGBA")

    except Exception:
        background = Image.new("RGBA", (WIDTH, HEIGHT), BG)

    box = panelBoxes[screen]

    # Add a dark overlay to make the quiz text easier to read.
    if screen == "quiz":
        shade = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 110))
        background = Image.alpha_composite(background, shade)

    # Draw a rounded panel on screens that need one.
    if box is not None:

        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        draw.rounded_rectangle(
            box,
            radius=30,
            fill=(8, 13, 43, 225),
            outline=(0, 217, 255, 255),
            width=3
        )

        background = Image.alpha_composite(background, overlay)

    return ImageTk.PhotoImage(background)

#QUIZ VARIABLES
score = 0
questionNumber = 0
attempts = 0
correctAnswer = 0
difficulty = ""

questionText = None
progressText = None
scoreText = None
progressFill = None
feedbackText = None
answerEntry = None
submitButton = None

#BACKGROUND ANIMATION
particles = []
def createParticles():

    particles.clear()

    # Create small moving particles for the background.
    for i in range(25):

        x = random.randint(60, 940)
        y = random.randint(60, 590)
        size = random.randint(2, 4)
        speed = random.randint(1, 3)

        dot = canvas.create_rectangle(
            x, y, x + size, y + size,
            fill="#0A8FA8",
            outline=""
        )

        particles.append((dot, speed))


def moveParticles():

    for dot, speed in particles:

        canvas.move(dot, 0, -speed)

        x1, y1, x2, y2 = canvas.coords(dot)

        # Move particles back to the bottom when they reach the top.
        if y2 < 50:
            canvas.move(dot, 0, 550)

    root.after(40, moveParticles)

#COMMON FUNCTIONS
def clearWindow(screen):

    # Clear the previous screen and display the new background.
    for widget in canvas.winfo_children():
        widget.destroy()

    if screen not in images:
        images[screen] = createBackground(screen)

    canvas.delete("all")
    canvas.create_image(0, 0, image=images[screen], anchor="nw")

    createParticles()


def addText(text, font, colour, x, y, anchor="center"):

    return canvas.create_text(
        x, y,
        text=text,
        font=font,
        fill=colour,
        anchor=anchor
    )


def addLine(y, left=230, right=770):

    canvas.create_line(
        left, y, right, y,
        fill=CYAN,
        width=1
    )


def addButton(text, command, colour, x, y, width, height):

    button = tk.Button(
        canvas,
        text=text,
        command=command,
        font=BUTTON_FONT,
        bg=colour,
        fg=WHITE,
        activebackground=CYAN,
        activeforeground=BG,
        relief="flat",
        bd=0,
        cursor="hand2"
    )

    button.place(
        x=x,
        y=y,
        width=width,
        height=height,
        anchor="center"
    )

    # Change the button colour when the mouse moves over it.
    button.bind("<Enter>", lambda event: button.config(bg=CYAN, fg=BG))
    button.bind("<Leave>", lambda event: button.config(bg=colour, fg=WHITE))

    return button

#START SCREEN
def displayStartScreen():

    clearWindow("start")

    addText("MATHS QUIZ", TITLE_FONT, CYAN, CENTRE, 195)
    addText("Test your maths skills", TEXT_FONT, GREY, CENTRE, 245)
    addLine(280, 340, 660)

    addButton("START", displayMenu, PURPLE, CENTRE, 340, 240, 50)
    addButton("QUIT", root.destroy, PANEL, CENTRE, 410, 240, 50)

#DIFFICULTY MENU
def displayMenu():

    clearWindow("level")

    addText("CHOOSE LEVEL", TITLE_FONT, CYAN, CENTRE, 105)
    addLine(150)

    # The difficulty levels determine the number of digits in each question.
    levels = [
        ("EASY", "Single digit numbers", "Easy"),
        ("MODERATE", "Double digit numbers", "Moderate"),
        ("ADVANCED", "Four digit numbers", "Advanced")
    ]

    rowY = 215

    for title, description, selectedLevel in levels:

        canvas.create_rectangle(
            200, rowY - 40, 800, rowY + 40,
            fill=PANEL,
            outline=CYAN,
            width=1
        )

        addText(title, HEADING_FONT, WHITE, 230, rowY - 14, "w")
        addText(description, SMALL_FONT, GREY, 230, rowY + 18, "w")

        # Pass the selected difficulty to the startQuiz function.
        addButton(
            "SELECT",
            lambda level=selectedLevel: startQuiz(level),
            PURPLE,
            695, rowY,
            150, 40
        )

        rowY += 100

    addButton("BACK", displayStartScreen, PANEL, CENTRE, 540, 160, 40)

#RANDOM NUMBER FUNCTION
def randomInt(level):

    # Generate numbers according to the selected difficulty.
    if level == "Easy":
        return random.randint(0, 9)

    elif level == "Moderate":
        return random.randint(10, 99)

    else:
        return random.randint(1000, 9999)

#OPERATION FUNCTION
def decideOperation():

    # Randomly choose addition or subtraction.
    return random.choice(["+", "-"])


#START QUIZ
def startQuiz(selectedDifficulty):

    global difficulty, score, questionNumber, attempts

    difficulty = selectedDifficulty

    # Reset the quiz values whenever a new game starts.
    score = 0
    questionNumber = 0
    attempts = 0

    displayQuiz()
    displayProblem()


#QUIZ SCREEN
def displayQuiz():

    global questionText, progressText, scoreText, progressFill
    global feedbackText, answerEntry, submitButton

    clearWindow("quiz")

    # Display the quiz title and selected difficulty.
    addText("MATHS", TITLE_FONT, CYAN, 492, 115, "e")
    addText("QUIZ", TITLE_FONT, CYAN, 508, 115, "w")
    addText("LEVEL: " + difficulty.upper(), HEADING_FONT, GOLD, CENTRE, 160)

    # Progress bar showing the user's progress through the quiz.
    canvas.create_rectangle(
        300, 194, 700, 206,
        fill=PANEL,
        outline=CYAN,
        width=1
    )

    progressFill = canvas.create_rectangle(
        300, 194, 300, 206,
        fill=CYAN,
        outline=""
    )

    # Boxes for the question number and current score.
    canvas.create_rectangle(
        250, 222, 470, 262,
        fill=PANEL,
        outline=CYAN,
        width=1
    )

    canvas.create_rectangle(
        530, 222, 750, 262,
        fill=PANEL,
        outline=GREEN,
        width=1
    )

    progressText = addText("", SMALL_FONT, WHITE, 360, 242)
    scoreText = addText("", SMALL_FONT, GREEN, 640, 242)

    # Question display area.
    canvas.create_rectangle(
        250, 285, 750, 385,
        fill=PANEL,
        outline=CYAN,
        width=2
    )

    questionText = addText("", QUESTION_FONT, WHITE, CENTRE, 335)

    feedbackText = addText("", FEEDBACK_FONT, WHITE, CENTRE, 406)

    addText("ENTER YOUR ANSWER", TEXT_FONT, CYAN, CENTRE, 437)

    answerEntry = tk.Entry(
        canvas,
        font=ENTRY_FONT,
        bg=WHITE,
        fg=BG,
        justify="center",
        relief="flat",
        disabledbackground="#DDDDDD",
        disabledforeground=BG
    )

    answerEntry.place(
        x=CENTRE,
        y=477,
        width=240,
        height=42,
        anchor="center"
    )

    submitButton = addButton(
        "SUBMIT", submitAnswer, PURPLE, CENTRE, 533, 240, 42
    )

    # Allow the user to submit an answer using the Enter key.
    answerEntry.bind("<Return>", lambda event: submitAnswer())

#DISPLAY QUESTION
def displayProblem():

    global correctAnswer, attempts

    attempts = 0

    number1 = randomInt(difficulty)
    number2 = randomInt(difficulty)

    operation = decideOperation()

    if operation == "+":
        correctAnswer = number1 + number2

    else:
        correctAnswer = number1 - number2

    # Display the randomly generated arithmetic question.
    canvas.itemconfig(
        questionText,
        text=str(number1) + " " + operation + " " + str(number2) + " = ?"
    )

    canvas.itemconfig(
        progressText,
        text="QUESTION " + str(questionNumber + 1) + " / " + str(TOTAL_QUESTIONS)
    )

    canvas.itemconfig(
        scoreText,
        text="SCORE: " + str(score)
    )

    # Update the progress bar according to the current question.
    barEnd = 300 + 400 * (questionNumber + 1) / TOTAL_QUESTIONS
    canvas.coords(progressFill, 300, 194, barEnd, 206)

    canvas.itemconfig(feedbackText, text="", fill=WHITE)

    answerEntry.config(state="normal")
    answerEntry.delete(0, tk.END)
    answerEntry.focus()

    submitButton.config(state="normal")

#CHECK ANSWER
def isCorrect(userAnswer):

    # Compare the user's answer with the correct answer.
    return userAnswer == correctAnswer

#SUBMIT ANSWER
def submitAnswer():

    global attempts, score

    # Prevent additional submissions while moving to the next question.
    if submitButton["state"] == "disabled":
        return

    userInput = answerEntry.get().strip()

    if userInput == "":
        canvas.itemconfig(
            feedbackText,
            text="Please enter an answer.",
            fill=GOLD
        )
        return

    try:
        userAnswer = int(userInput)

    except ValueError:
        canvas.itemconfig(
            feedbackText,
            text="Enter a valid number.",
            fill=RED
        )
        return

    attempts += 1

    if isCorrect(userAnswer):

        # Award 10 points for the first attempt and 5 for the second.
        if attempts == 1:
            score += 10
        else:
            score += 5

        canvas.itemconfig(scoreText, text="SCORE: " + str(score))
        canvas.itemconfig(feedbackText, text="CORRECT!", fill=GREEN)

        finishQuestion()

    elif attempts == 1:

        # Give the user one more chance if the first answer is incorrect.
        canvas.itemconfig(feedbackText, text="TRY AGAIN!", fill=GOLD)

        answerEntry.delete(0, tk.END)
        answerEntry.focus()

    else:

        canvas.itemconfig(
            feedbackText,
            text="ANSWER: " + str(correctAnswer),
            fill=RED
        )

        finishQuestion()

#NEXT QUESTION
def finishQuestion():

    answerEntry.config(state="disabled")
    submitButton.config(state="disabled")

    # Wait briefly before showing the next question.
    root.after(1000, moveToNextQuestion)


def moveToNextQuestion():

    global questionNumber

    questionNumber += 1

    if questionNumber >= TOTAL_QUESTIONS:
        displayResults()

    else:
        displayProblem()

#RESULTS SCREEN
def displayResults():

    clearWindow("score")

    addText("YOUR SCORE", TITLE_FONT, CYAN, CENTRE, 130)
    addLine(175)

    addText(str(score) + " / 100", SCORE_FONT, GOLD, CENTRE, 255)

    # Assign a grade based on the final score.
    if score > 90:
        grade = "A+"

    elif score >= 80:
        grade = "A"

    elif score >= 70:
        grade = "B"

    elif score >= 60:
        grade = "C"

    elif score >= 50:
        grade = "D"

    else:
        grade = "F"

    addText("GRADE: " + grade, HEADING_FONT, GREEN, CENTRE, 335)

    addButton("PLAY AGAIN", displayStartScreen, PURPLE, CENTRE, 420, 240, 50)
    addButton("QUIT", root.destroy, PANEL, CENTRE, 490, 240, 50)

displayStartScreen()
moveParticles()
root.mainloop()
