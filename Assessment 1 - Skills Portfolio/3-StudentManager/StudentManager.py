import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pathlib import Path

#File location 
PROGRAM_FOLDER = Path(__file__).resolve().parent
FILE_NAME = PROGRAM_FOLDER / "studentMarks.txt"

#Window
root = tk.Tk()
root.title("Student Manager | Academic Dashboard")
root.geometry("1100x720")
root.resizable(False, False)


#Colours
BG = "#F3F4FA"
HEADER = "#2E2A72"
BUTTON = "#4F46E5"
BUTTON_LIGHT = "#6D66F0"
BUTTON_DARK = "#1E1B5A"
ACCENT = "#FFC857"
GREEN = "#10B981"
INK = "#1B1F3B"
GREY = "#6B7194"
CARD = "#FFFFFF"
TRACK = "#E3E5F3"
BORDER = "#E0E3F2"
WHITE = "#FFFFFF"
RED = "#EF4444"

GRADE_COLOURS = {
    "A": "#10B981",
    "B": "#3B82F6",
    "C": "#F5A524",
    "D": "#F97316",
    "F": "#EF4444"
}


#Fonts
FONT = "Candara"
TITLE_FONT_NAME = "Georgia"

HEADING_FONT = (TITLE_FONT_NAME, 26, "bold")
VALUE_FONT = (TITLE_FONT_NAME, 24, "bold")
NAME_FONT = (FONT, 14, "bold")
BODY_FONT = (FONT, 11)
SMALL_FONT = (FONT, 10)
BUTTON_FONT = (FONT, 10, "bold")


#Student data

students = []

#Dialog functions
#These functions open input boxes in front of the main window.
def askString(title, prompt, **options):
    root.lift()
    root.focus_force()

    return simpledialog.askstring(
        title,
        prompt,
        parent=root,
        **options
    )


def askInteger(title, prompt, **options):
    root.lift()
    root.focus_force()

    return simpledialog.askinteger(
        title,
        prompt,
        parent=root,
        **options
    )

#Main background
backgroundCanvas = tk.Canvas(
    root,
    width=1100,
    height=720,
    highlightthickness=0,
    bd=0,
    bg=BG
)
backgroundCanvas.place(x=0, y=0)

#File handling
def loadStudents():
    """Load student records from the text file."""

    students.clear()

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            lines = file.readlines()

        if len(lines) == 0:
            messagebox.showerror("File Error", "studentMarks.txt is empty.")
            return

        expectedCount = int(lines[0].strip())

        if expectedCount < 0:
            raise ValueError

        for line in lines[1:]:
            row = line.strip().split(",")

            if len(row) != 6:
                continue

            try:
                studentCode = int(row[0].strip())
                studentName = row[1].strip()
                mark1 = int(row[2].strip())
                mark2 = int(row[3].strip())
                mark3 = int(row[4].strip())
                exam = int(row[5].strip())

                # Check that the information is within the allowed limits.
                if not (1000 <= studentCode <= 9999):
                    continue

                if studentName == "" or "," in studentName:
                    continue

                if not (
                    0 <= mark1 <= 20 and
                    0 <= mark2 <= 20 and
                    0 <= mark3 <= 20 and
                    0 <= exam <= 100
                ):
                    continue

                # Do not load the same student number more than once.
                if findStudent(str(studentCode)) is not None:
                    continue

                student = {
                    "id": str(studentCode),
                    "name": studentName,
                    "mark1": mark1,
                    "mark2": mark2,
                    "mark3": mark3,
                    "exam": exam
                }

                students.append(student)

            except ValueError:
                # Skip a record if one of its marks is not a whole number.
                continue

        if len(students) != expectedCount:
            messagebox.showwarning(
                "File Warning",
                "The file says there should be " + str(expectedCount) +
                " students, but " + str(len(students)) +
                " valid records were loaded."
            )

    except FileNotFoundError:
        messagebox.showerror(
            "File Error",
            "studentMarks.txt was not found.\n\n"
            "Please put it in the StudentManager folder."
        )

    except ValueError:
        messagebox.showerror(
            "File Error",
            "The first line must contain a valid student count."
        )

    except OSError as error:
        messagebox.showerror("File Error", str(error))


def saveStudents():
    """Save the current student records to the text file."""

    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            file.write(str(len(students)) + "\n")

            for student in students:
                file.write(
                    student["id"] + "," +
                    student["name"] + "," +
                    str(student["mark1"]) + "," +
                    str(student["mark2"]) + "," +
                    str(student["mark3"]) + "," +
                    str(student["exam"]) + "\n"
                )

        return True

    except OSError as error:
        messagebox.showerror(
            "Save Error",
            "Could not save the student records.\n\n" + str(error)
        )
        return False

#Calculations
def getCoursework(student):
    """Add the three coursework marks."""

    return (
        student["mark1"] +
        student["mark2"] +
        student["mark3"]
    )


def getTotal(student):
    """Calculate the total mark out of 160."""

    return getCoursework(student) + student["exam"]


def getPercentage(student):
    """Calculate the overall percentage."""

    return getTotal(student) / 160 * 100


def getGrade(percentage):
    """Return a grade based on the student's percentage."""

    if percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"

#Find student

def findStudent(query):
    """Find a student using their number or full name."""

    query = query.strip().lower()

    for student in students:
        if (
            student["id"] == query or
            student["name"].lower() == query
        ):
            return student

    return None


def askForStudent(title):
    query = askString(
        title,
        "Enter the student number or full name:"
    )

    if query is None:
        return None

    student = findStudent(query)

    if student is None:
        messagebox.showwarning(
            "Student Not Found",
            "No student matches that number or name."
        )

    return student

#Status message
def setStatus(message, colour=ACCENT):
    if colour == RED:
        colour = "#FFB3BC"

    backgroundCanvas.itemconfig(
        statusText,
        text=message,
        fill=colour
    )

#Display student records
def showRecords(records):
    """Display the selected student records as cards."""

    for card in cardFrame.winfo_children():
        card.destroy()

    position = 0

    for student in records:
        percentage = getPercentage(student)
        grade = getGrade(percentage)
        colour = GRADE_COLOURS[grade]

        # Each student is shown in a separate card.
        card = tk.Frame(
            cardFrame,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.grid(
            row=position // 2,
            column=position % 2,
            sticky="ew",
            padx=6,
            pady=6
        )
        card.columnconfigure(1, weight=1)
        position += 1

        tk.Frame(card, bg=colour, width=8).grid(
            row=0, column=0, sticky="ns"
        )

        info = tk.Frame(card, bg=CARD)
        info.grid(row=0, column=1, sticky="ew", padx=14, pady=12)

        tk.Label(
            info,
            text=student["name"],
            font=NAME_FONT,
            bg=CARD,
            fg=INK
        ).pack(anchor="w")

        tk.Label(
            info,
            text="Student number: " + student["id"],
            font=SMALL_FONT,
            bg=CARD,
            fg=GREY
        ).pack(anchor="w")

        # The bar gives a quick view of the student's percentage.
        barRow = tk.Frame(info, bg=CARD)
        barRow.pack(anchor="w", pady=(8, 4))

        bar = tk.Canvas(
            barRow,
            width=190,
            height=10,
            bg=TRACK,
            highlightthickness=0,
            bd=0
        )
        bar.pack(side="left")

        bar.create_rectangle(
            0, 0,
            190 * min(percentage, 100) / 100, 10,
            fill=colour,
            outline=""
        )

        tk.Label(
            barRow,
            text=str(round(percentage, 1)) + "%",
            font=(FONT, 12, "bold"),
            bg=CARD,
            fg=colour
        ).pack(side="left", padx=10)

        marks = (
            "Coursework: " + str(getCoursework(student)) + "/60"
            + "     Exam: " + str(student["exam"]) + "/100"
            + "     Total: " + str(getTotal(student)) + "/160"
        )

        tk.Label(
            info,
            text=marks,
            font=SMALL_FONT,
            bg=CARD,
            fg=GREY
        ).pack(anchor="w")

        tk.Label(
            card,
            text=grade,
            font=VALUE_FONT,
            bg=colour,
            fg=WHITE,
            width=3
        ).grid(row=0, column=2, sticky="ns")

    if len(records) == 0:
        tk.Label(
            cardFrame,
            text="No student records to show.",
            font=BODY_FONT,
            bg=BG,
            fg=GREY
        ).grid(row=0, column=0, columnspan=2, pady=40)

    cardCanvas.yview_moveto(0)

    # The dashboard tiles always show statistics for the whole class.
    count = len(students)
    studentsValue.config(text=str(count))

    if count > 0:
        totalPercentage = 0
        best = students[0]

        for student in students:
            percentage = getPercentage(student)
            totalPercentage += percentage

            if percentage > getPercentage(best):
                best = student

        averageValue.config(
            text=str(round(totalPercentage / count, 1)) + "%"
        )
        topValue.config(
            text=str(round(getPercentage(best), 1)) + "%"
        )
        topCaption.config(text="TOP SCORE • " + best["name"])

    else:
        averageValue.config(text="0%")
        topValue.config(text="0%")
        topCaption.config(text="TOP SCORE")

#View all students    
def viewAllStudents():
    showRecords(students)
    setStatus("Showing all student records.")

#View individual student
def viewIndividualStudent():
    student = askForStudent("View Student")

    if student is not None:
        showRecords([student])
        setStatus("Showing record for " + student["name"] + ".")

#Highest mark
def highestMark():
    if len(students) == 0:
        messagebox.showinfo("No Records", "There are no student records.")
        return

    best = students[0]

    for student in students:
        if getTotal(student) > getTotal(best):
            best = student

    showRecords([best])
    setStatus("Highest overall mark: " + best["name"])

#Lowest mark
def lowestMark():
    if len(students) == 0:
        messagebox.showinfo("No Records", "There are no student records.")
        return

    worst = students[0]

    for student in students:
        if getTotal(student) < getTotal(worst):
            worst = student

    showRecords([worst])
    setStatus("Lowest overall mark: " + worst["name"])

#Sort records
def sortStudents():
    if len(students) == 0:
        messagebox.showinfo(
            "No Records",
            "There are no student records to sort."
        )
        return

    highFirst = messagebox.askyesno(
        "Sort Records",
        "Sort from highest to lowest?\n"
        "(Choose No for lowest to highest)"
    )

    students.sort(key=getTotal, reverse=highFirst)
    showRecords(students)

    if highFirst:
        setStatus("Sorted from highest to lowest.")
    else:
        setStatus("Sorted from lowest to highest.")

#Enter marks
def askMark(label, maximum, current=None):
    return askInteger(
        "Enter Mark",
        label + " (0-" + str(maximum) + "):",
        minvalue=0,
        maxvalue=maximum,
        initialvalue=current
    )

#Add student
def addStudent():
    code = askInteger(
        "Add Student",
        "Enter student number (1000-9999):",
        minvalue=1000,
        maxvalue=9999
    )

    if code is None:
        return

    if findStudent(str(code)) is not None:
        messagebox.showwarning(
            "Duplicate ID",
            "This student number already exists."
        )
        return

    name = askString("Add Student", "Enter student name:")

    if name is None:
        return

    name = name.strip()

    if name == "" or "," in name:
        messagebox.showwarning(
            "Invalid Name",
            "Name cannot be empty or contain commas."
        )
        return

    mark1 = askMark("Course mark 1", 20)
    if mark1 is None:
        return

    mark2 = askMark("Course mark 2", 20)
    if mark2 is None:
        return

    mark3 = askMark("Course mark 3", 20)
    if mark3 is None:
        return

    exam = askMark("Exam mark", 100)
    if exam is None:
        return

    newStudent = {
        "id": str(code),
        "name": name,
        "mark1": mark1,
        "mark2": mark2,
        "mark3": mark3,
        "exam": exam
    }

    students.append(newStudent)

    if saveStudents():
        showRecords(students)
        setStatus(name + " added successfully!")
    else:
        students.pop()

#Delete student
def deleteStudent():
    student = askForStudent("Delete Student")

    if student is None:
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete " + student["name"] + "?"
    )

    if confirm:
        originalPosition = students.index(student)
        students.remove(student)

        if saveStudents():
            showRecords(students)
            setStatus("Student deleted successfully.", RED)
        else:
            # Put the student back if the file could not be saved.
            students.insert(originalPosition, student)

#Update student
def updateStudent():
    student = askForStudent("Update Student")

    if student is None:
        return

    # Keep a copy so the old record can be restored if saving fails.
    oldStudent = student.copy()

    newCode = askInteger(
        "Update Student",
        "Enter new student number (1000-9999):",
        minvalue=1000,
        maxvalue=9999,
        initialvalue=int(student["id"])
    )

    if newCode is None:
        return

    existingStudent = findStudent(str(newCode))

    if existingStudent is not None and existingStudent is not student:
        messagebox.showwarning(
            "Duplicate ID",
            "Another student already uses this number."
        )
        return

    newName = askString(
        "Update Student",
        "Enter student name:",
        initialvalue=student["name"]
    )

    if newName is None:
        return

    newName = newName.strip()

    if newName == "" or "," in newName:
        messagebox.showwarning(
            "Invalid Name",
            "Name cannot be empty or contain commas."
        )
        return

    mark1 = askMark("Course mark 1", 20, student["mark1"])
    if mark1 is None:
        return

    mark2 = askMark("Course mark 2", 20, student["mark2"])
    if mark2 is None:
        return

    mark3 = askMark("Course mark 3", 20, student["mark3"])
    if mark3 is None:
        return

    exam = askMark("Exam mark", 100, student["exam"])
    if exam is None:
        return

    student["id"] = str(newCode)
    student["name"] = newName
    student["mark1"] = mark1
    student["mark2"] = mark2
    student["mark3"] = mark3
    student["exam"] = exam

    if saveStudents():
        showRecords(students)
        setStatus(newName + " updated successfully.")
    else:
        student.update(oldStudent)

#Interface
# Header and status message.
backgroundCanvas.create_rectangle(
    0, 0, 1100, 105,
    fill=HEADER,
    outline=""
)

backgroundCanvas.create_rectangle(
    0, 105, 1100, 109,
    fill=ACCENT,
    outline=""
)

backgroundCanvas.create_text(
    40, 42,
    text="STUDENT MANAGER",
    font=HEADING_FONT,
    fill=WHITE,
    anchor="w"
)

statusText = backgroundCanvas.create_text(
    40, 80,
    text="",
    font=(FONT, 11, "italic"),
    fill=ACCENT,
    anchor="w"
)


def createButton(text, command, x, y, width, colour=BUTTON,
                 hoverColour=BUTTON_LIGHT, textColour=WHITE):

    button = tk.Button(
        root,
        text=text,
        command=command,
        font=BUTTON_FONT,
        bg=colour,
        fg=textColour,
        activebackground=hoverColour,
        activeforeground=textColour,
        relief="flat",
        bd=0,
        cursor="hand2"
    )

    button.bind("<Enter>", lambda event: button.config(bg=hoverColour))
    button.bind("<Leave>", lambda event: button.config(bg=colour))
    button.place(x=x, y=y, width=width, height=40)

    return button


# Exit button in the top-right corner.
createButton(
    "EXIT",
    root.destroy,
    960, 32, 100,
    BUTTON_DARK,
    BUTTON
)

#Dashboard tiles
def makeTile(x, caption):
    tile = tk.Frame(
        root,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    tile.place(x=x, y=128, width=320, height=82)

    tk.Frame(tile, bg=ACCENT, height=4).pack(fill="x")

    value = tk.Label(
        tile,
        text="0",
        font=VALUE_FONT,
        bg=CARD,
        fg=INK
    )
    value.pack(pady=(2, 0))

    captionLabel = tk.Label(
        tile,
        text=caption,
        font=(FONT, 10, "bold"),
        bg=CARD,
        fg=GREY
    )
    captionLabel.pack()

    return value, captionLabel


studentsValue, studentsCaption = makeTile(40, "STUDENTS")
averageValue, averageCaption = makeTile(390, "CLASS AVERAGE")
topValue, topCaption = makeTile(740, "TOP SCORE")

#Toolbar buttons
createButton("VIEW ALL", viewAllStudents, 43, 232, 118)
createButton("FIND STUDENT", viewIndividualStudent, 171, 232, 118)
createButton("HIGHEST", highestMark, 299, 232, 118)
createButton("LOWEST", lowestMark, 427, 232, 118)
createButton("SORT", sortStudents, 555, 232, 118)
createButton("ADD", addStudent, 683, 232, 118, GREEN, "#34D399")
createButton("DELETE", deleteStudent, 811, 232, 118, RED, "#F87171")
createButton("UPDATE", updateStudent, 939, 232, 118)

#Scrollable student list
cardArea = tk.Frame(root, bg=BG)
cardArea.place(x=40, y=290, width=1020, height=410)

cardCanvas = tk.Canvas(
    cardArea,
    bg=BG,
    highlightthickness=0,
    bd=0
)

cardScroll = ttk.Scrollbar(
    cardArea,
    orient="vertical",
    command=cardCanvas.yview
)

cardCanvas.configure(yscrollcommand=cardScroll.set)

cardScroll.pack(side="right", fill="y")
cardCanvas.pack(side="left", fill="both", expand=True)

cardFrame = tk.Frame(cardCanvas, bg=BG)
cardFrame.columnconfigure(0, weight=1, uniform="cards")
cardFrame.columnconfigure(1, weight=1, uniform="cards")

cardWindow = cardCanvas.create_window(
    (0, 0),
    window=cardFrame,
    anchor="nw"
)


def resizeCardFrame(event):
    cardCanvas.itemconfig(cardWindow, width=event.width)


def updateScrollArea(event):
    cardCanvas.configure(scrollregion=cardCanvas.bbox("all"))


def mouseScroll(event):
    cardCanvas.yview_scroll(int(-event.delta / 120), "units")


cardCanvas.bind("<Configure>", resizeCardFrame)
cardFrame.bind("<Configure>", updateScrollArea)
root.bind_all("<MouseWheel>", mouseScroll)

loadStudents()
showRecords(students)
setStatus("Showing all student records.")

root.mainloop()