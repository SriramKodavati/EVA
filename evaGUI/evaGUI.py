import PySimpleGUI as sg
import time
import cv2

def time_as_int():
    return int(round(time.time() * 100))

# ----------------  Create Form  ----------------
sg.theme('Black')
button_graph = {'size':(12,3),'button_color':("white","#F4564F"),'font':('Calibri',36),'pad':(20,20)}
# Camera Settings
camera_Width  = 320 # 480 # 640 # 1024 # 1280
camera_Heigth = 240 # 320 # 480 # 780  # 960
frameSize = (camera_Width, camera_Heigth)
startReadingFrames = False
startVideo = False

startPage = [[sg.Text('EVA',justification='center',font=('Helvetica',48))],
          [sg.Text('Never miss medications again..!',justification="center",font=('Helvetica',36))],
          [sg.Button('Get Started->',key='getStarted')]
          ]

mainPage = [
    [sg.Button('View Medications',**button_graph),sg.Button('Add Medicine',key="addMedicine",**button_graph)]
]

instructionPage = [
    [sg.Text('Capture images covering entire label of pill bottle',justification="center",font=('Helvetica',36))],
    [sg.Text('Hold the bottle closer to camera',justification="center",font=('Helvetica',36))],
    [sg.Text('Make sure there is proper lighting',justification="center",font=('Helvetica',36))]
]

cameraPage = [
[sg.Image(filename="",key="cam")],
[sg.Button('Done',key="doneCapturing",**button_graph),sg.Button('Capture Image',key='captureImage',**button_graph)]
]

layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
              [sg.Text('', pad=(0,0),key='-EXPAND2-'),              # the thing that expands from left
          sg.Column(startPage, key='startPage'),
          sg.Column(mainPage,visible=False,key='mainPage'),
          sg.Column(instructionPage,visible=False,key="instructionPage"),
          sg.Column(cameraPage,visible=False,key='cameraPage')
          ]]

window = sg.Window('EVA', layout,
                   no_titlebar=False,
                   auto_size_buttons=False,
                   keep_on_top=True,
                   grab_anywhere=True,
                   element_padding=(0, 0),
                   finalize=True,
                   element_justification='c',
                   right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_EXIT)
window['startPage'].expand(True, True, True)
#window['mainPage'].expand(True,True,True)
window['-EXPAND-'].expand(True, True, True)
window['-EXPAND2-'].expand(True, False, True)
window.Maximize()

current_time, paused_time, paused = 0, 0, False
start_time = time_as_int()

while True:
    event, values = window.read(timeout=3)
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'getStarted':
        window['startPage'].update(visible=False)
        window['mainPage'].update(visible=True)
    elif event == 'addMedicine':
        window['mainPage'].update(visible=False)
        window['instructionPage'].update(visible=True)
        time.sleep(15)
        window['instructionPage'].update(visible=False)
        window['cameraPage'].update(visible=True)
        video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        startVideo = True
        startReadingFrames = True
    if startVideo:
        video_capture = cv2.VideoCapture(0)
        startVideo = False
    if startReadingFrames:
        ret, frameOrig = video_capture.read()        # get camera frame
        frame = cv2.resize(frameOrig, frameSize)
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["cam"].update(data=imgbytes)

cv2.destroyAllWindows()
window.close()