import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image

# this is the function called when the button is clicked


confir = 4

def btnClickFunction():
	root.destroy()

def noFunct():
	global confirA
	confir = 1
	print(confir)


def yesFunct():
	global confir
	confir = 2
	print(confir)

def idkFunct():
	# global confir
	# confir = 3
	print("idk")



# creating tkinter window

def loadingGui(imPath):
	global root
	root = Toplevel()

	root.geometry('1280x800')
	root.configure(background='#F0F8FF')
	root.title('hi')

	# Adding widgets to the root window

	# This is the section of code which creates the a label
	Label(root, text='Have you taken your medicine yet?', bg='#F0F8FF', font=('arial', 40, 'normal')).place(x=38, y=37)

	# Creating a photoimage object to use image
	print(imPath)
	photo = PhotoImage(file=r'%s' % imPath)

	# photo1 = Image.open("C:\EVA\pillbottles\pillbottle1\Image1.png")
	#
	# photo1 = photo1._PhotoImage__photo.zoom(2)
	#
	#
	# photo = PhotoImage(photo1)
	# here, image option is used to
	# set image on button
	Button(root, text='Click Me !', image=photo).place(x=500, y=125)

	Button(root, text='No', bg='#FF4040', font=('arial', 70, 'normal'), command=btnClickFunction).place(x=24, y=150) # all set to same destroy function for demo

	# This is the section of code which creates a button
	Button(root, text='Yes', bg='#76EE00', font=('arial', 70, 'normal'), command=btnClickFunction).place(x=24, y=375)

	Button(root, text='IDK', bg='#FFB90F', font=('arial', 70, 'normal'), command=btnClickFunction).place(x=24, y=600)

	#Button(root, text='Exit', bg='#9A32CD', font=('arial', 12, 'normal'), command=btnClickFunction).place(x=1100, y=740)

	if confir != 4:
		return confir
	print(confir)
	print("imhere")

	root.mainloop()


# path = "C:\EVA\pillbottles\pillbottle1\image1.png"
# loadingGui(path)