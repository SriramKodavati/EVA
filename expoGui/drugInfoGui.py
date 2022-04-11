#specificDruginfo

import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image

from drugsCom import *


# this is the function called when the button is clicked


confir = 4

def btnClickFunction():

	root.destroy()


# creating tkinter window

def loadingDrugGui():
	global root
	root = Toplevel()

	bg = PhotoImage(file="view.png")

	root.geometry('1280x800')

	# Adding widgets to the root window

	# This is the section of code which creates the a label
	Label(root, text='Click Me !', image=bg).place(x=0, y=0)


	# Creating a photoimage object to use image
	imPath = "/home/pi/Desktop/EVA/expoEva-main/timesAsked.PNG"
	photo = PhotoImage(file=imPath)

	print("oeo")

	Button(root, text='Rosuvastatin', bg='#FFB90F', font=('Roboto', 40, 'normal'), command=rosuvastatin).place(x=200, y=200)

	Button(root, text='Tamsulosin', bg='#E1912A', font=('Roboto', 40, 'normal'), command=tamsulosin).place(x=700, y=200)

	Button(root, text='Exit', bg='#9A32CD', font=('Roboto', 40, 'normal'), command=btnClickFunction).place(x=1100, y=640)


	if confir != 4:
		return confir
	print(confir)
	print("imhere")

	root.mainloop()


# path = "C:\EVA\pillbottles\pillbottle1\image1.png"
# loadingGui(path)
