# file stuff from https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/
# other gui adapted from https://likegeeks.com/python-gui-examples-tkinter-tutorial/

from tkinter import *
from tkinter import filedialog as fd
from balance import *
from log import *
import os
from os.path import join

window = Tk()
global filename

def login():
    global name, lbl3
    name = txt.get()
    txt.delete(0, END)
    lbl3['text'] = "Logged in: " + name
    logLogIn(name)

def comment():
    cmnt = commentBox.get('1.0', 'end-1c')
    commentBox.delete('1.0', END)
    logComment(cmnt)


def openBalanceMenu(filename): # also used https://www.geeksforgeeks.org/open-a-new-window-with-a-button-in-python-tkinter/
    global commentBox, solNode, lblp, lblt, startGrid
    global name, lbl4, moves, nextBtn, newWindow, move

    moveNumber = 1
    newWindow = Toplevel(window) 
    newWindow.title("New Window")
    newWindow.geometry("900x900")
    if not filename:
        newWindow.close()
    commentBox = Text(newWindow)
    commentBox.grid(column=1, row=0)
    commentBtn = Button(newWindow, text="Submit", command=comment)
    commentBtn.grid(column=3, row=0)
    move = "Started Balancing"
    nextBtn = Button(newWindow, text='Start',command=doNextMove)
    nextBtn.grid(column=2, row=12)
    lbl2 = Label(newWindow, text="Type comment in box and hit submit to leave comment in log\nTo Log in new user, use secondary window text box and hit \'Log In\'")
    lbl2.grid(column=1, row=4)
    # A Label widget to show in toplevel
    lbl = Label(newWindow, text="Working on " + os.path.basename(filename))
    lbl.grid(column=1, row=9)
    lbl4 = Label(newWindow, text="Hit Start to Begin")
    lbl4.grid(row=12, column=0)
    solNode = search()
    solNode.appendSolStep(solNode.getmatrix())
    solNode.appendSolStep(solNode.getmatrix())
    startGrid = solNode.getPrevMoves().pop(0)
    print('--------------------------------- INITAL PROBLEM --------------------------------')
    s = ''
    for y in range(8)[::-1]:
        for x in range(12):
            s += (str(startGrid[x][y].getName().center(16, ' ')))
        s += '\n'
    n = "AFTER MOVE:\n"
    lblt = Label(newWindow, text=n+s)
    lblt.grid(row=24, column=1)
    a = "CURRENT STATE:\n"
    lblp = Label(newWindow, text=a+s)
    lblp.grid(row=36, column=1)
    moves = solNode.getMoves()
    moves.append('COMPLETED!')

def doNextMove():
    global lbl4, moves, nextBtn, move, lblp, lblt, startGrid
    logComment(move)
    s = ''
    for y in range(8)[::-1]:
        for x in range(12):
            s += (str(startGrid[x][y].getName().center(16, ' ')))
        s += '\n'
    lblp['text'] = "CURRENT STATE\n" + s
    startGrid = solNode.getPrevMoves().pop(0)
    s = ''
    for y in range(8)[::-1]:
        for x in range(12):
            s += (str(startGrid[x][y].getName().center(16, ' ')))
        s += '\n'
    lblt['text'] = "AFTER MOVE:\n" + s
    move = moves.pop(0)
    if not moves:
        nextBtn['text'] = 'FINISH'
        nextBtn['command'] = exit
    else:
        nextBtn['text'] = 'Next Step'
    lbl4['text'] = move

def exit():
    createManifest()
    newWindow.destroy()

def closePop():
    top.destroy()

def createManifest(): # https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
    global top
    fname = os.path.basename(filename)
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') # https://stackoverflow.com/questions/34275782/how-to-get-desktop-location
    fname = fname.strip('.txt') + 'OUTBOUND.txt'
    f = open(join(desktop, fname), 'w') #https://stackoverflow.com/questions/35415647/how-to-write-a-file-to-the-desktop-in-python
    m = solNode.getmatrix()
    #[01,01], {00000}, NAN
    for y in range(8):
        for x in range(12):
            if m[x][y].getWeight() == -1:
                s = '[' + str("{:02d}".format(y + 1)) + ',' + str("{:02d}".format(x + 1)) + '],' + ' {' + str("{:05d}".format(0)) + '}, ' + m[x][y].getName() + '\n'
            else:
                s = '[' + str("{:02d}".format(y + 1)) + ',' + str("{:02d}".format(x + 1)) + '],' + ' {' + str("{:05d}".format(m[x][y].getWeight())) + '}, ' + m[x][y].getName() + '\n'
            f.write(s)
    # AFTER MANIFEST CREATED, PUT POPUP TO USER
    top= Toplevel(window)
    top.geometry("400x200")
    top.title("Reminder")
    l = Label(top, text= "Outbound manifest written to desktop, make sure to email!")
    l.grid(column=10, row=10)
    b = Button(top, text='OK',command=closePop)
    b.grid(column=10, row=20)

def openFile():
    global filename
    filename = fd.askopenfilename()
    
    readManifest(filename)
    return openBalanceMenu(filename)

def mainMenu():
    global txt, name, lbl3, window
    initLog()
    name = 'No User'
    window.title("Balance Ship")

    window.geometry('350x200')

    lbl = Label(window, text="Welcome to the CS179M Balancer")

    lbl.grid(column=0, row=0)

    lbl3 = Label(window, text="Logged in: " + name)
    lbl3.grid(column=0, row=5)

    txt = Entry(window,width=10)
    txt.grid(column=1, row=0)
    logBtn = Button(window, text="Log In", command=login)
    balBtn = Button(window, text="Balance Ship", command=openFile)
    logBtn.grid(column=2, row=0)
    balBtn.grid(column=1, row=2)

mainMenu()

window.mainloop()
