from tkinter import *
from tkinter import messagebox
from time import strftime
#from voiceRec import *
from confirmationGUI import *

from evaGUI import *
from postScanDisplay import *
from reportsGui import *
from drugInfoGui import *

root = Tk()
root.geometry("1280x730")

def options():
    print("options")

def my_time():
    time_string = strftime('%I:%M %p \n %A \n %B %d, %Y')
    #return time_string
    my_text.config(text=time_string)
    my_text.after(1000, my_time)  # time delay of 1000 milliseconds

def scanSelect():
    loadingRamGui()
    displayFunct()

def confirmSelect():
    loadingGui("/home/pi/Desktop/EVA/expoEva-main/image1.png")

def reportSelect():
    loadingReportGui()

def drugInfoSelect():
    loadingDrugGui()

def openNewWindow():
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(root)

    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")

    # sets the geometry of toplevel
    newWindow.geometry("1280x730")

    # A Label widget to show in toplevel
    Label(newWindow,
          text="This is a new window").pack()

def showHomeScreen():

    bg = PhotoImage(file="view.png")
    evaFace = PhotoImage(file="evaFace4Home.png")

    my_canvas = Canvas(root, width=1280, height=800)
    my_canvas.pack(fill="both", expand=True)

    my_canvas.create_image(0, 0, image=bg, anchor="nw")
    my_canvas.create_image(0, 0, image=evaFace, anchor="nw")
    global my_text
    my_text = Label(root, text="", font=("Roboto", 50), fg="black")

    myText_window = my_canvas.create_window(70, 430, anchor='nw', window=my_text)


    evaText = "Hi I'm Eva.\nHow can I help you?"
    my_canvas.create_text(410, 80, text=evaText, font=("Roboto", 40), fill="white")

    Button(root, text='Scan Bottle', bg='#E1912A', font=('arial', 50, 'normal'), command=scanSelect).place(x=604, y=175)
    Button(root, text='Drug Info', bg='#A1E12A', font=('arial', 50, 'normal'), command=drugInfoSelect).place(x=604,
                                                                                                              y=320)

    Button(root, text='Confirmation Demo', bg='#1AA8AC', font=('arial', 50, 'normal'), command=confirmSelect).place(x=604,
                                                                                                              y=470)

    Button(root, text='Reports', bg='#6F31CF', font=('arial', 55, 'normal'), command=reportSelect).place(x=604,
                                                                                                              y=620)

    print("expoFunct")
    while True:
        my_time()
        #command2()
        root.update_idletasks()
        root.update()
    #root.mainloop()


#home screen may need to be image absed then guia based. I just need to find a good way to update and close the image.

showHomeScreen()