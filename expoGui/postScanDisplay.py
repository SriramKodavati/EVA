import psycopg2
import tkinter as tk
from tkinter import *
from bottleFixerKeyboard import *
from franklinKeyboard import *

c = 1
my_connect = psycopg2.connect(
    host="localhost",
    database="pi",
    user="pi",
    password="postgres"
)
my_conn = my_connect.cursor()


def funct2(): #grabs latest scanned pills bottles info and corrected values so far

    my_conn.execute("SELECT * FROM medicine1 order by id")

    allDBEntries = my_conn.fetchall()

    latestScanVals = allDBEntries[-1]
    global idVal
    idVal = str(latestScanVals[0])

    print("this id value is: " + idVal)
    medNameVal = latestScanVals[1]
    dateFilledVal = latestScanVals[2]
    quantityVal = latestScanVals[3]
    refillsLeftVal = latestScanVals[4]
    timePerDay = latestScanVals[7]
    photopath = latestScanVals[6]
    print(latestScanVals)
    i = 0
    processedList = []

    while i < 7:
        if i == 0:
            processedList.append(tuple(["Medicine Name", medNameVal]))
        if i == 1:
            processedList.append(tuple(["Date Filled", dateFilledVal]))
        if i == 2:
            processedList.append(tuple(["Quantity", quantityVal]))
        if i == 3:
            processedList.append(tuple(["Refills Left", refillsLeftVal]))
        if i == 4:
            processedList.append(tuple(["Times Per Day", timePerDay]))
        if i == 5:
            processedList.append(tuple(["ID", idVal]))
        if i == 6:
            processedList.append(tuple(["Photo Path", photopath]))
        i += 1
    print(processedList)
    return processedList

def dunzo():
    root.quit()
    root.destroy()


    # i = 0
    # global c
    # while i < c:
    #
    #     root.quit()
    #     c +=1

def correctValue(columnVal, idValue):
    if columnVal == 0:
        theVal = onscreenkeyboardReturn()
        #theVal = fixVal()
        mystr = "update medicine1 set medname = '" + theVal + "' where id = " + idValue
        my_conn.execute(mystr)
        my_connect.commit()
    elif columnVal == 1:
        #theVal = fixVal()
        theVal = onscreenkeyboardReturn()
        mystr = "update medicine1 set datefilled = '" + theVal + "' where id = " + str(idValue)
        my_conn.execute(mystr)
        my_connect.commit()
    elif columnVal == 2:
        theVal = onscreenkeyboardReturn()
        mystr = "update medicine1 set quantity = '" + theVal + "' where id = " + str(idValue)
        my_conn.execute(mystr)
        my_connect.commit()
    elif columnVal == 3:
        theVal = onscreenkeyboardReturn()
        mystr = "update medicine1 set refillsleft = '" + theVal + "' where id = " + str(idValue)
        my_conn.execute(mystr)
        my_connect.commit()
    elif columnVal == 4:
        theVal = onscreenkeyboardReturn()
        print(theVal)
        mystr = "update medicine1 set timesperday = '" + theVal + "' where id = " + str(idValue)
        my_conn.execute(mystr)
        my_connect.commit()
    global c
    c +=1
    print(c)
    root.destroy()
    displayFunct()

def displayFunct():
    global root
    #root = Tk()
    root = Toplevel()

    processedList = funct2()
    myIDVal = processedList[5][1]
    root.geometry('1280x730')

    tk.Label(root, text=processedList[0][0], width=15, fg='Black', font=('Roboto', 14, 'bold')).grid(row=2, column=0)
    tk.Label(root, text=processedList[1][0], width=15, fg='Black', font=('Roboto', 14, 'bold')).grid(row=2, column=1)
    tk.Label(root, text=processedList[2][0], width=15, fg='Black', font=('Roboto', 14, 'bold')).grid(row=2, column=2)
    tk.Label(root, text=processedList[3][0], width=15, fg='Black', font=('Roboto', 14, 'bold')).grid(row=2, column=3)
    tk.Label(root, text=processedList[4][0], width=15, fg='Black', font=('Roboto', 14, 'bold')).grid(row=2, column=4)

    button1 = Button(root, text=processedList[0][1], width=15, fg='Black', font=('Roboto', 16, 'bold'),
                     command=lambda: correctValue(0, idVal))  # need to add command for actual button press
    button1.grid(row=3, column=0)

    button2 = Button(root, text=processedList[1][1], width=15, fg='Black', font=('Roboto', 16, 'bold'),
                     command=lambda: correctValue(1, idVal))
    button2.grid(row=3, column=1)

    button3 = Button(root, text=processedList[2][1], width=15, fg='Black', font=('Roboto', 16, 'bold'),
                     command=lambda: correctValue(2, idVal))
    button3.grid(row=3, column=2)

    button4 = Button(root, text=processedList[3][1], width=15, fg='Black', font=('Roboto', 16, 'bold'),
                     command=lambda: correctValue(3, idVal))
    button4.grid(row=3, column=3)

    button5 = Button(root, text=processedList[4][1], width=15, fg='Black', font=('Roboto', 16, 'bold'),
                     command=lambda: correctValue(4, idVal))
    button5.grid(row=3, column=4)

    button6 = Button(root, text="Done", width=15, fg='Black', font=('Roboto', 16, 'bold'),
                     command=dunzo)
    button6.grid(row=10, column=4)

    button7 = Button(root, text="Update", width=15, fg='Black', font=('Roboto', 16, 'bold'),
                     command=dunzo)
    button7.grid(row=10, column=3)

    imPath = processedList[6][1]

    imPath = imPath.replace("/","\\")

    imPath = imPath + "\Image1.png"

    # if imPath == "FolderPathNone":
    #     imPath = "C:\EVA\pillbottles\pillbottle1\image1.png"
    # print("impath "+imPath)

    photo = PhotoImage(file=r'%s' % imPath)

    Button(root, text='Click Me !', image=photo).place(x=500, y=200)

    root.mainloop()

    print("hereafter")
    root.quit()
