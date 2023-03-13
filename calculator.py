from tkinter import *
 
equation = ""

def buttonPress(num):
    global equation
    equation = equation + str(num)
    display.set(equation)
 
def equate():
    try:
        global equation
        display.set(str(eval(equation)))
        equation = ""
    except:
        display.set(" error ")
        equation = ""

def fullClear():
    global equation
    equation = ""
    display.set("")

def delete():
    global equation
    if len(equation) != 0:
        equation = equation[:-1]
        display.set(equation)

if __name__ == "__main__":
    C1 = 'black'
    C2 = 'red'
    HEIGHT = 1
    WIDTH = 7
    CHARS = [7, 8, 9, 4, 5, 6, 1, 2, 3, 0, '+', '-', '*', '/', '.']
    WINDOW_WIDTH = 540
    WINDOW_HEIGHT = 300
    buttons = []

    gui = Tk()
    gui.configure(background="light blue")
    gui.title("Calculator")
    gui.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))

    display = StringVar()
 
    equation_field = Entry(gui, textvariable=display)
 
    equation_field.grid(columnspan=5, ipadx=20)

    buttons.append(Button(gui, text = str(CHARS[0]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[0]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = str(CHARS[1]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[1]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = str(CHARS[2]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[2]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = str(CHARS[3]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[3]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = str(CHARS[4]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[4]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = str(CHARS[5]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[5]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = str(CHARS[6]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[6]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = str(CHARS[7]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[7]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = str(CHARS[8]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[8]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = str(CHARS[9]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[9]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text =str(CHARS[10]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[10]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = str(CHARS[11]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[11]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = str(CHARS[12]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[12]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = str(CHARS[13]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[13]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = str(CHARS[14]), fg=C1, bg=C2, command=lambda: buttonPress(CHARS[14]), height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = '=', fg=C1, bg=C2, command=equate, height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = 'Clear', fg=C1, bg=C2, command=fullClear, height = HEIGHT, width = WIDTH))
    buttons.append(Button(gui, text = 'Delete', fg=C1, bg=C2, command=delete, height = HEIGHT, width = WIDTH))


    buttons[0].grid(row=2, column=1)
    buttons[1].grid(row=2, column=2)
    buttons[2].grid(row=2, column=3)
    buttons[3].grid(row=3, column=1)
    buttons[4].grid(row=3, column=2)
    buttons[5].grid(row=3, column=3)
    buttons[6].grid(row=4, column=1)
    buttons[7].grid(row=4, column=2)
    buttons[8].grid(row=4, column=3)
    buttons[9].grid(row=5, column=1)
    buttons[10].grid(row=2, column=4)
    buttons[11].grid(row=3, column=4)
    buttons[12].grid(row=4, column=4)
    buttons[13].grid(row=5, column=4)
    buttons[14].grid(row=5, column=2)
    buttons[15].grid(row=5, column=3)
    buttons[16].grid(row=6, column=2)
    buttons[17].grid(row=6, column=3)
    curr = Button(gui)
    curr.grid(row=0, column=0)

    gui.mainloop()