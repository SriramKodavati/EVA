# from PIL import Image, ImageFont, ImageDraw
#
# import textwrap
#
# def putText(result: object):
#     text = result
#     text = textwrap.fill(text=text, width=35)
#     strip_width, strip_height = 1280, 800
#
#
#     #my_image = Image.open("mountain1.jpg")
#     #my_image = Image.open("water1.jpg")
#     #my_image = Image.open("lake.jpg")
#     my_image = Image.open("view.jpg")
#     #my_image = Image.open("water1.jpg")
#
#
#
#     title_font = ImageFont.truetype('Yagora.ttf', 60)
#
#     draw = ImageDraw.Draw(my_image)
#
#     text_width, text_height = draw.textsize(text, title_font)
#     position = ((strip_width - text_width) / 2, (strip_height - text_height) / 2)
#
#     draw.text(position, text=text, fill=(250, 250, 250), font=title_font)
#
#     my_image.format = "PNG"
#
#     my_image.show()
#
#     my_image.close()
#
#



from tkinter import *
from tkinter import messagebox
from time import strftime
import time
#import speech

text = "Sample text for an on screen display"

def speechy(mystr):
    speech.speak(mystr)
    root.destroy()




def putText(textInput):
    global root
    root = Tk()
    root.geometry("1280x800")

    bg = PhotoImage(master = root, file="view.png")
    my_canvas = Canvas(root, width=1280, height=800)
    my_canvas.pack(fill="both", expand=True)

    # my_text = Label(root, text = "hi", font=("Helvetica", 50), fg = "black")
    # my_text.place(x=100, y=500)
    # my_text.pack()

    my_canvas.create_image( 0, 0, image=bg, anchor="nw")

    # my_text = Label(root, text=textInput, font=("Helvetica", 50), fg="black")

    # myText_window = my_canvas.create_window(70, 530, anchor='nw', window=my_text)

    my_canvas.create_text(600,400,text=textInput, font=("Roboto", 40), fill="white", width=1080)

    #speechy(textInput)
    #root.after_idle(speechy())
    # root.mainloop()
    root.update_idletasks()
    root.update()
    speechy(textInput)


def putText2(textInput):
    global root
    root = Tk()
    root.geometry("1280x800")

    bg = PhotoImage(master = root, file="view.png")
    my_canvas = Canvas(root, width=1280, height=800)
    my_canvas.pack(fill="both", expand=True)

    # my_text = Label(root, text = "hi", font=("Helvetica", 50), fg = "black")
    # my_text.place(x=100, y=500)
    # my_text.pack()

    my_canvas.create_image( 0, 0, image=bg, anchor="nw")

    # my_text = Label(root, text=textInput, font=("Helvetica", 50), fg="black")

    # myText_window = my_canvas.create_window(70, 530, anchor='nw', window=my_text)

    hello = my_canvas.create_text(600,400,text=textInput, font=("Roboto", 50), fill="black", width=1080)
    r = my_canvas.create_rectangle(my_canvas.bbox(hello), fill="white")
    my_canvas.tag_lower(r, hello)
    #speechy(textInput)
    #root.after_idle(speechy())
    # root.mainloop()
    root.update_idletasks()
    root.update()
    speechy(textInput)


