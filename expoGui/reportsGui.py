import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image

from report2 import *

# this is the function called when the button is clicked


confir = 4

def report2command():
	root.destroy()
	loadingReportGui2()

def btnClickFunction():
	root.destroy()


# creating tkinter window

def loadingReportGui():
	global root
	root = Toplevel()

	root.geometry('1280x800')
	root.configure(background='#F0F8FF')
	root.title('hi')

	#mat = PhotoImage(file="matplotlib.png")


	# Adding widgets to the root window

	# This is the section of code which creates the a label
	Label(root, text='', bg='#F0F8FF', font=('arial', 40, 'normal')).place(x=38, y=37)

	# Creating a photoimage object to use image
	imPath = "/home/pi/Desktop/EVA/expoEva-main/report1.PNG"
	photo = PhotoImage(file=imPath)

	print("oeo")

	Button(root, text='Click Me !', image=photo).place(x=100, y=125)

	#Label(root, text='Click Me !', image=mat, height=100, width=100).place(x=0, y=0)



	# This is the section of code which creates a button
	Button(root, text='Cognitive report', bg='#76EE00', font=('arial', 40, 'normal'), command=report2command).place(x=24, y=675)


	Button(root, text='Exit', bg='#9A32CD', font=('arial', 40, 'normal'), command=btnClickFunction).place(x=1100, y=640)

	if confir != 4:
		return confir
	print(confir)
	print("imhere")

	root.mainloop()


# path = "C:\EVA\pillbottles\pillbottle1\image1.png"
# loadingGui(path)
