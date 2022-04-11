import PySimpleGUI as sg
import time
import cv2
import saveImages
import textExtraction
import saveToDb


def time_as_int():
    return int(round(time.time() * 100))

# ----------------  Create Form  ----------------
def loadingRamGui():
    # ----------------  Create Form  ----------------
    sg.theme('Blue')
    button_graph = {'size': (12, 3), 'button_color': ("white", "#F4564F"), 'font': ('Calibri', 36), 'pad': (20, 20)}
    # Camera Settings
    camera_Width = 500  # 480 # 640 # 1024 # 1280
    camera_Heigth = 300  # 320 # 480 # 780  # 960
    frameSize = (camera_Width, camera_Heigth)
    startReadingFrames = False
    startVideo = False
    imgDirPath = ""
    images = []  # stores the images of each pill bottle and sends them to saveImages file.
    imageCount = 0

    startPage = [[sg.Text('EVA', justification='center', font=('Helvetica', 48))],
                 [sg.Text('Never miss medications again..!', justification="center", font=('Calibri', 36))],
                 [sg.Button('Get Started->', key='getStarted')]
                 ]

    mainPage = [
        [sg.Button('Add Medicine', key="addMedicine", **button_graph),
         sg.Button('exit', key="exit", **button_graph)]
    ]

    instructionPage = [
        [sg.Text('Instructions:', justification="center", font=('Calibri', 45))],
        [sg.Text('Capture images covering entire label of pill bottle', justification="center", font=('Calibri', 36))],
        [sg.Text('Hold the bottle closer to camera', justification="center", font=('Calibri', 36))],
        [sg.Text('Make sure there is proper lighting', justification="center", font=('Calibri', 36))],
        [sg.Button('Next', key='goToCameraPage',font=('Calibri', 45))]
    ]

    cameraPage = [
        [sg.Image(filename="", key="cam")],
        [sg.Button('Done', key="doneCapturing", **button_graph),
         sg.Button('Capture Images', key='captureImage', **button_graph)]
    ]

    layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
              [sg.Text('', pad=(0, 0), key='-EXPAND2-'),  # the thing that expands from left
               sg.Column(startPage, key='startPage'),
               sg.Column(mainPage, visible=False, key='mainPage'),
               sg.Column(instructionPage, visible=False, key="instructionPage"),
               sg.Column(cameraPage, visible=False, key='cameraPage')
               ]]

    print(sg.Window.get_screen_size())
    w, h = sg.Window.get_screen_size()
    window = sg.Window('EVA', layout,
                       no_titlebar=False,
                       auto_size_buttons=False,
                       size=(w, h),
                       keep_on_top=True,
                       element_padding=(0, 0),
                       finalize=True,
                       element_justification='c',
                       right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_EXIT)
    # window.Size(w,h)
    window['startPage'].expand(True, True, True)
    # window['mainPage'].expand(True,True,True)
    window['-EXPAND-'].expand(True, True, True)
    window['-EXPAND2-'].expand(True, False, True)
    # window.Maximize()

    current_time, paused_time, paused = 0, 0, False
    start_time = time_as_int()

    while True:
        event, values = window.read(timeout=1)
        print(event, values)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'getStarted':
            window['startPage'].update(visible=False)
            window['mainPage'].update(visible=True)
        elif event == 'addMedicine':
            window['mainPage'].update(visible=False)
            window['instructionPage'].update(visible=True)
            # time.sleep(15)
        elif event == "goToCameraPage":
            window['instructionPage'].update(visible=False)
            window['cameraPage'].update(visible=True)
            startVideo = True
            startReadingFrames = True
        elif event == "captureImage":
            imageCount += 1
            window['captureImage'].update(text=f"Capture Images({imageCount})")
            frame = cv2.cvtColor(frameOrig, cv2.COLOR_BGR2RGB)
            images.append(frame)
        elif event == "doneCapturing":
            if imageCount > 0:
                imageCount = 0
                imgDirPath = saveImages.saveImages(images)
                images = []
                pillInfo = textExtraction.beginOCR(imgDirPath)
                saveToDb.saveToDb(pillInfo)
            video_capture.release()
            cv2.destroyAllWindows()
            window['captureImage'].update(text=f"Capture Images({imageCount})")
            startReadingFrames = False
            window['cameraPage'].update(visible=False)
            window['mainPage'].update(visible=True)
        elif event == "exit":
            window.close()
        if startVideo:
            video_capture = cv2.VideoCapture(0)
            startVideo = False
        if startReadingFrames:
            ret, frameOrig = video_capture.read()  # get camera frame
            frame = cv2.resize(frameOrig, frameSize)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            window["cam"].update(data=imgbytes)

    window.close()




